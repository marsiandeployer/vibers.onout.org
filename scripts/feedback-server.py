#!/usr/bin/env python3
"""
Vibers Feedback API — accepts user feedback and sends to Telegram.

POST /feedback
Body: {"message": "...", "repo": "https://github.com/user/repo"}

Run via PM2.
"""

import json
import os
import subprocess
import sys
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
# Single-threaded: pyrogram requires main thread event loop

TELEGRAM_API_ID = int(os.environ.get("TELEGRAM_API_ID", "20663119"))
TELEGRAM_API_HASH = os.environ.get("TELEGRAM_API_HASH", "")
TELEGRAM_SESSION = os.environ.get("TELEGRAM_SESSION_STRING", "")
TELEGRAM_CHAT_ID = int(os.environ.get("TELEGRAM_CHAT_ID", "-5058393445"))
TELEGRAM_REVIEW_CHAT_ID = int(os.environ.get("TELEGRAM_REVIEW_CHAT_ID", TELEGRAM_CHAT_ID))
PORT = int(os.environ.get("FEEDBACK_PORT", "3847"))

# Rate limiting: max 5 requests per minute per IP
RATE_LIMIT = {}
RATE_WINDOW = 60
RATE_MAX = 5


def send_telegram(text, chat_id=None):
    if chat_id is None:
        chat_id = TELEGRAM_CHAT_ID
    if not TELEGRAM_SESSION:
        print(f"No TELEGRAM_SESSION_STRING, printing instead:\n{text}")
        return False
    if not TELEGRAM_API_HASH:
        print("No TELEGRAM_API_HASH set, skipping telegram", file=sys.stderr)
        return False

    try:
        from pyrogram import Client

        app = Client(
            "vibers_feedback",
            api_id=TELEGRAM_API_ID,
            api_hash=TELEGRAM_API_HASH,
            session_string=TELEGRAM_SESSION,
            in_memory=True
        )
        with app:
            for _ in app.get_dialogs():
                pass
            app.send_message(chat_id, text)
        print(f"Telegram sent to {chat_id}")
        return True
    except Exception as e:
        print(f"Telegram send failed: {e}", file=sys.stderr)
        return False


GH_BOT = "marsiandeployer"
GH_TIMEOUT = 10  # seconds per gh api call


def check_access_status(repo_full_name):
    """Check if GH_BOT is collaborator or has pending invite. Returns status string."""
    if "/" not in repo_full_name or repo_full_name.startswith("http"):
        return "⚠️ не удалось проверить (нет owner/repo)"

    # Check collaborator
    try:
        r = subprocess.run(
            ["gh", "api", f"/repos/{repo_full_name}/collaborators/{GH_BOT}",
             "-i", "--silent"],
            capture_output=True, text=True, timeout=GH_TIMEOUT
        )
        if r.returncode == 0 and "204" in r.stdout.split("\n")[0]:
            return "✅ коллаборатор"
    except Exception:
        pass

    # Check pending invite
    try:
        r = subprocess.run(
            ["gh", "api", f"/repos/{repo_full_name}/invitations"],
            capture_output=True, text=True, timeout=GH_TIMEOUT
        )
        if r.returncode == 0:
            invites = json.loads(r.stdout)
            if isinstance(invites, list):
                for inv in invites:
                    if isinstance(inv, dict):
                        invitee = inv.get("invitee") or {}
                        if isinstance(invitee, dict) and invitee.get("login") == GH_BOT:
                            return "⏳ инвайт отправлен, ещё не принят"
    except Exception:
        pass

    return "❌ не добавлен"


_last_cleanup = 0
_server_start = time.time()

def check_rate_limit(ip):
    global _last_cleanup
    now = time.time()

    # Evict stale IPs every 5 minutes
    if now - _last_cleanup > 300:
        stale = [k for k, v in RATE_LIMIT.items() if not v or now - v[-1] > RATE_WINDOW]
        for k in stale:
            del RATE_LIMIT[k]
        _last_cleanup = now

    if ip in RATE_LIMIT:
        timestamps = [t for t in RATE_LIMIT[ip] if now - t < RATE_WINDOW]
        RATE_LIMIT[ip] = timestamps
        if len(timestamps) >= RATE_MAX:
            return False
    else:
        RATE_LIMIT[ip] = []
    RATE_LIMIT[ip].append(now)
    return True


class FeedbackHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self._cors_headers()
        self.end_headers()

    def _read_json_body(self, max_size=10000):
        """Read and parse JSON body. Returns (data, error_sent) tuple."""
        # Rate limiting
        client_ip = self.headers.get("X-Real-IP", self.client_address[0])
        if not check_rate_limit(client_ip):
            self.send_response(429)
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"error": "too many requests, try again later"}')
            return None, True

        try:
            content_length = int(self.headers.get("Content-Length", 0))
        except (ValueError, TypeError):
            self.send_response(400)
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"error": "invalid content-length"}')
            return None, True

        if content_length < 0 or content_length > max_size:
            self.send_response(413)
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"error": "invalid or too large body"}')
            return None, True

        body = self.rfile.read(content_length)
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"error": "invalid json"}')
            return None, True

        if not isinstance(data, dict):
            self.send_response(400)
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"error": "expected json object"}')
            return None, True

        return data, False

    def _send_and_respond(self, tg_text, chat_id=None):
        """Send to Telegram and write HTTP response."""
        sent = send_telegram(tg_text, chat_id)
        if sent:
            self.send_response(200)
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"status": "accepted"}')
        else:
            self.send_response(502)
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"error": "failed to deliver, contact @onoutnoxon on Telegram"}')

    def do_GET(self):
        if self.path == "/health":
            import subprocess
            uptime = time.time() - _server_start
            tg_configured = bool(TELEGRAM_SESSION and TELEGRAM_API_HASH)

            # Check invite-checker PM2 status
            try:
                result = subprocess.run(
                    ["pm2", "jlist"], capture_output=True, text=True, timeout=5
                )
                pm2_list = json.loads(result.stdout) if result.returncode == 0 else []
                invite_proc = next((p for p in pm2_list if p.get("name") == "vibers-invite-checker"), None)
                invite_status = invite_proc["pm2_env"]["status"] if invite_proc else "not found"
            except Exception:
                invite_status = "unknown"

            health = {
                "status": "ok" if tg_configured else "degraded",
                "uptime_seconds": int(uptime),
                "telegram_configured": tg_configured,
                "invite_checker": invite_status,
                "rate_limit_ips": len(RATE_LIMIT),
            }
            self.send_response(200)
            self._cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(health).encode())
        else:
            self.send_response(404)
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"error": "not found"}')

    def do_POST(self):
        if self.path == "/feedback":
            self._handle_feedback()
        elif self.path == "/review":
            self._handle_review()
        else:
            self.send_response(404)
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"error": "not found"}')

    def _handle_feedback(self):
        data, err = self._read_json_body()
        if err:
            return

        message = data.get("message") if isinstance(data.get("message"), str) else None
        repo = data.get("repo") if isinstance(data.get("repo"), str) else None

        if not message or not message.strip():
            self.send_response(400)
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"error": "message is required (string)"}')
            return

        if not repo or not repo.strip():
            self.send_response(400)
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"error": "repo is required (string)"}')
            return

        message = message.strip()[:2000]
        repo = repo.strip()[:500]

        tg_text = (
            f"**Vibers Feedback**\n\n"
            f"Repo: {repo}\n"
            f"Message: {message}"
        )
        self._send_and_respond(tg_text, TELEGRAM_REVIEW_CHAT_ID)

    def _str_field(self, data, key, max_len=500, default=""):
        """Extract string field from data safely."""
        val = data.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()[:max_len]
        return default

    def _handle_review(self):
        data, err = self._read_json_body(max_size=50000)
        if err:
            return

        repo = self._str_field(data, "repo")
        if not repo:
            self.send_response(400)
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"error": "repo is required"}')
            return

        branch = self._str_field(data, "branch", 100, "unknown")
        sha = self._str_field(data, "sha", 40)
        author = self._str_field(data, "author", 100, "unknown")
        spec_url = self._str_field(data, "spec_url", 500)
        contact = self._str_field(data, "contact", 100)
        commit_msg = self._str_field(data, "commit_msg", 200)
        commit_body = self._str_field(data, "commit_body", 2000)
        diff_stat = self._str_field(data, "diff_stat", 200)
        deploy_url = self._str_field(data, "deploy_url", 500)
        stack = self._str_field(data, "stack", 200)
        creds = self._str_field(data, "creds", 1000)
        files = self._str_field(data, "changed_files", 3000)
        file_count = len([f for f in files.split("\n") if f.strip()]) if files else 0

        repo_url = f"https://github.com/{repo}" if "/" in repo and not repo.startswith("http") else repo
        commit_url = f"{repo_url}/commit/{sha}" if sha else ""

        # Check if marsiandeployer has access
        repo_full_name = repo if "/" in repo and not repo.startswith("http") else ""
        access_status = check_access_status(repo_full_name) if repo_full_name else "⚠️ не удалось проверить"

        # Build Telegram message — compact, useful
        tg_text = f"**Vibers: Review Request**\n\n"
        tg_text += f"[{repo}]({repo_url}) | [{sha[:8]}]({commit_url})\n"
        tg_text += f"Author: {author} | Branch: `{branch}`\n"
        tg_text += f"Access: {access_status}\n"

        if commit_msg:
            tg_text += f"\n**{commit_msg}**\n"

        if commit_body:
            tg_text += f"\n{commit_body}\n"

        if diff_stat:
            tg_text += f"\n`{diff_stat}`\n"

        if stack:
            tg_text += f"Stack: {stack}\n"

        if spec_url:
            tg_text += f"Spec: {spec_url}\n"
        if contact:
            tg_text += f"Contact: {contact}\n"
        if deploy_url:
            tg_text += f"Deploy: {deploy_url}\n"

        if creds:
            tg_text += f"\n**Credentials:**\n```\n{creds[:500]}\n```\n"

        if files:
            tg_text += f"\n**Files ({file_count}):**\n```\n{files[:800]}\n```"

        self._send_and_respond(tg_text)

    def _cors_headers(self):
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def log_message(self, format, *args):
        print(f"[feedback-server] {args[0]}")


class TimeoutHTTPServer(HTTPServer):
    """HTTPServer that sets a socket timeout on accepted connections."""
    request_timeout = 30

    def get_request(self):
        conn, addr = super().get_request()
        conn.settimeout(self.request_timeout)
        return conn, addr


if __name__ == "__main__":
    server = TimeoutHTTPServer(("127.0.0.1", PORT), FeedbackHandler)
    print(f"Feedback server listening on 127.0.0.1:{PORT}")
    server.serve_forever()
