#!/usr/bin/env python3
"""
Check GitHub repository invitations for marsiandeployer.
Accept them and send Telegram notification.

Runs once per invocation. Scheduled via PM2 cron (*/1 * * * *).
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# --- Config ---
STATE_FILE = Path(__file__).parent / ".invite-state.json"
TELEGRAM_API_ID = int(os.environ.get("TELEGRAM_API_ID", "20663119"))
TELEGRAM_API_HASH = os.environ.get("TELEGRAM_API_HASH", "")
TELEGRAM_SESSION = os.environ.get("TELEGRAM_SESSION_STRING", "")
TELEGRAM_CHAT_ID = int(os.environ.get("TELEGRAM_CHAT_ID", "-5058393445"))
GH_TIMEOUT = 30  # seconds


def load_state():
    try:
        if STATE_FILE.exists():
            data = json.loads(STATE_FILE.read_text())
            if isinstance(data.get("processed"), list):
                if "pending_notifications" not in data:
                    data["pending_notifications"] = []
                return data
    except (json.JSONDecodeError, OSError) as e:
        print(f"Warning: corrupted state file, resetting: {e}", file=sys.stderr)
    return {"processed": [], "pending_notifications": []}


def save_state(state):
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2))
    os.replace(tmp, STATE_FILE)


def get_invitations():
    """Get pending repo invitations via gh CLI."""
    try:
        result = subprocess.run(
            ["gh", "api", "/user/repository_invitations"],
            capture_output=True, text=True, timeout=GH_TIMEOUT
        )
    except subprocess.TimeoutExpired:
        print("Error: gh api timed out", file=sys.stderr)
        return []
    if result.returncode != 0:
        print(f"Error fetching invitations: {result.stderr}", file=sys.stderr)
        return []
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"Error: invalid JSON from gh api", file=sys.stderr)
        return []


def accept_invitation(invite_id):
    """Accept a repository invitation."""
    try:
        result = subprocess.run(
            ["gh", "api", "-X", "PATCH", f"/user/repository_invitations/{invite_id}"],
            capture_output=True, text=True, timeout=GH_TIMEOUT
        )
    except subprocess.TimeoutExpired:
        print(f"Error: gh api PATCH timed out for invite {invite_id}", file=sys.stderr)
        return False
    if result.returncode != 0:
        print(f"Error accepting invite {invite_id}: {result.stderr.strip()}", file=sys.stderr)
    return result.returncode == 0


def send_telegram(text):
    """Send message via Pyrogram (userbot session). Returns True if sent."""
    if not TELEGRAM_SESSION:
        print(f"No TELEGRAM_SESSION_STRING, printing instead:\n{text}")
        return True  # no session = print-only mode, consider "delivered"
    if not TELEGRAM_API_HASH:
        print("No TELEGRAM_API_HASH set, skipping telegram", file=sys.stderr)
        return False

    try:
        from pyrogram import Client

        app = Client(
            "vibers_notifier",
            api_id=TELEGRAM_API_ID,
            api_hash=TELEGRAM_API_HASH,
            session_string=TELEGRAM_SESSION,
            in_memory=True
        )
        with app:
            # Load dialogs to cache peer for group chats
            for _ in app.get_dialogs():
                pass
            app.send_message(TELEGRAM_CHAT_ID, text)
        print(f"Telegram sent to {TELEGRAM_CHAT_ID}")
        return True
    except Exception as e:
        print(f"Telegram send failed: {e}", file=sys.stderr)
        return False


def main():
    state = load_state()
    processed_list = state["processed"]
    processed = set(processed_list)
    pending = state.get("pending_notifications", [])

    # Retry pending notifications from previous runs
    still_pending = []
    for item in pending:
        if send_telegram(item["msg"]):
            processed.add(item["inv_id"])
            print(f"[{datetime.now().isoformat()}] Retried notification for {item.get('repo', '?')} — sent")
        else:
            still_pending.append(item)

    # Process new invitations
    invitations = get_invitations()
    if not isinstance(invitations, list):
        print(f"Warning: expected list from API, got {type(invitations).__name__}", file=sys.stderr)
        invitations = []
    for inv in invitations:
        if not isinstance(inv, dict) or "id" not in inv:
            print(f"Warning: skipping malformed invitation: {str(inv)[:100]}", file=sys.stderr)
            continue
        inv_id = inv["id"]
        if inv_id in processed:
            continue

        repo = inv.get("repository") or {}
        repo_name = repo.get("full_name", "unknown") if isinstance(repo, dict) else "unknown"
        repo_url = repo.get("html_url", "") if isinstance(repo, dict) else ""
        inviter_obj = inv.get("inviter") or {}
        inviter = inviter_obj.get("login", "unknown") if isinstance(inviter_obj, dict) else "unknown"
        permissions = inv.get("permissions", "unknown")
        created = inv.get("created_at", "")

        accepted = accept_invitation(inv_id)
        if not accepted:
            print(f"[{datetime.now().isoformat()}] FAILED to accept invite {inv_id} from {inviter} for {repo_name} — will retry next run")
            continue

        msg = (
            f"**Vibers: New repo invitation!**\n\n"
            f"Repo: [{repo_name}]({repo_url})\n"
            f"Invited by: @{inviter}\n"
            f"Permissions: {permissions}\n"
            f"Date: {created}\n"
            f"Status: accepted\n\n"
            f"Next: check repo for spec/docs and start review."
        )

        print(f"[{datetime.now().isoformat()}] Invitation from {inviter} for {repo_name} — accepted")
        if send_telegram(msg):
            processed.add(inv_id)
        else:
            # Save for retry — invite will be gone from API next run
            still_pending.append({"inv_id": inv_id, "repo": repo_name, "msg": msg})
            print(f"[{datetime.now().isoformat()}] Telegram failed for {repo_name} — saved for retry")

    # Preserve order: append new IDs in the order they were added
    processed_list_set = set(processed_list)
    new_ids = sorted(i for i in processed if i not in processed_list_set)
    processed_list.extend(new_ids)
    state["processed"] = processed_list[-100:]
    state["pending_notifications"] = still_pending[-20:]  # keep last 20
    save_state(state)


if __name__ == "__main__":
    # PM2 cron (*/1 * * * *) handles scheduling — run once and exit
    try:
        main()
    except Exception as e:
        print(f"Unexpected error in main: {e}", file=sys.stderr)
        sys.exit(1)
