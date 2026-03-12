#!/usr/bin/env python3
"""
Check GitHub repository invitations for marsiandeployer.
Accept them and send Telegram notification.

Run via PM2 cron every 60 seconds.
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
                return data
    except (json.JSONDecodeError, OSError) as e:
        print(f"Warning: corrupted state file, resetting: {e}", file=sys.stderr)
    return {"processed": []}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))


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
    return result.returncode == 0


def send_telegram(text):
    """Send message via Pyrogram (userbot session)."""
    if not TELEGRAM_SESSION:
        print(f"No TELEGRAM_SESSION_STRING, printing instead:\n{text}")
        return
    if not TELEGRAM_API_HASH:
        print("No TELEGRAM_API_HASH set, skipping telegram", file=sys.stderr)
        return

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
    except Exception as e:
        print(f"Telegram send failed: {e}", file=sys.stderr)


def main():
    invitations = get_invitations()
    if not invitations:
        return

    state = load_state()
    processed = set(state["processed"])

    for inv in invitations:
        inv_id = inv["id"]
        if inv_id in processed:
            continue

        repo = inv.get("repository", {})
        repo_name = repo.get("full_name", "unknown")
        repo_url = repo.get("html_url", "")
        inviter = inv.get("inviter", {}).get("login", "unknown")
        permissions = inv.get("permissions", "unknown")
        created = inv.get("created_at", "")

        # Accept the invitation
        accepted = accept_invitation(inv_id)
        status = "accepted" if accepted else "FAILED to accept"

        # Only mark as processed if accepted successfully
        if not accepted:
            print(f"[{datetime.now().isoformat()}] FAILED to accept invite {inv_id} from {inviter} for {repo_name} — will retry next run")
            continue

        # Build message
        msg = (
            f"**Vibers: New repo invitation!**\n\n"
            f"Repo: [{repo_name}]({repo_url})\n"
            f"Invited by: @{inviter}\n"
            f"Permissions: {permissions}\n"
            f"Date: {created}\n"
            f"Status: {status}\n\n"
            f"Next: check repo for spec/docs and start review."
        )

        print(f"[{datetime.now().isoformat()}] Invitation from {inviter} for {repo_name} — {status}")
        send_telegram(msg)

        processed.add(inv_id)

    state["processed"] = list(processed)[-100:]  # keep last 100
    save_state(state)


if __name__ == "__main__":
    import time
    POLL_INTERVAL = 60  # seconds
    print(f"Invite checker started, polling every {POLL_INTERVAL}s")
    while True:
        try:
            main()
        except Exception as e:
            print(f"Unexpected error in main loop: {e}", file=sys.stderr)
        time.sleep(POLL_INTERVAL)
