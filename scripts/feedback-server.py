#!/usr/bin/env python3
"""
Vibers Feedback API — accepts user feedback and sends to Telegram.

POST /feedback
Body: {"message": "...", "repo": "https://github.com/user/repo"}

Run via PM2.
"""

import json
import os
import sys
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
# Single-threaded: pyrogram requires main thread event loop

TELEGRAM_API_ID = int(os.environ.get("TELEGRAM_API_ID", "20663119"))
TELEGRAM_API_HASH = os.environ.get("TELEGRAM_API_HASH", "")
TELEGRAM_SESSION = os.environ.get("TELEGRAM_SESSION_STRING", "")
TELEGRAM_CHAT_ID = int(os.environ.get("TELEGRAM_CHAT_ID", "-5058393445"))
PORT = int(os.environ.get("FEEDBACK_PORT", "3847"))

# Rate limiting: max 5 requests per minute per IP
RATE_LIMIT = {}
RATE_WINDOW = 60
RATE_MAX = 5


def send_telegram(text):
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
            app.send_message(TELEGRAM_CHAT_ID, text)
        print(f"Telegram sent to {TELEGRAM_CHAT_ID}")
        return True
    except Exception as e:
        print(f"Telegram send failed: {e}", file=sys.stderr)
        return False


def check_rate_limit(ip):
    now = time.time()
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

    def _send_and_respond(self, tg_text):
        """Send to Telegram and write HTTP response."""
        sent = send_telegram(tg_text)
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
        self._send_and_respond(tg_text)

    def _handle_review(self):
        data, err = self._read_json_body(max_size=50000)
        if err:
            return

        repo = data.get("repo") if isinstance(data.get("repo"), str) else None
        if not repo or not repo.strip():
            self.send_response(400)
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"error": "repo is required"}')
            return

        repo = repo.strip()[:500]
        branch = (data.get("branch") or "unknown")[:100] if isinstance(data.get("branch"), str) else "unknown"
        sha = (data.get("sha") or "")[:40] if isinstance(data.get("sha"), str) else ""
        author = (data.get("author") or "unknown")[:100] if isinstance(data.get("author"), str) else "unknown"
        scope = (data.get("scope") or "full")[:50] if isinstance(data.get("scope"), str) else "full"
        spec_url = (data.get("spec_url") or "")[:500] if isinstance(data.get("spec_url"), str) else ""
        contact = (data.get("contact") or "")[:100] if isinstance(data.get("contact"), str) else ""
        files = (data.get("changed_files") or "")[:3000] if isinstance(data.get("changed_files"), str) else ""
        file_count = len([f for f in files.split("\n") if f.strip()]) if files else 0

        repo_url = f"https://github.com/{repo}" if "/" in repo and not repo.startswith("http") else repo

        tg_text = (
            f"**Vibers: Review Request**\n\n"
            f"Repo: [{repo}]({repo_url})\n"
            f"Branch: `{branch}`\n"
            f"Commit: `{sha[:8]}`\n"
            f"Author: {author}\n"
            f"Scope: {scope}\n"
        )
        if spec_url:
            tg_text += f"Spec: {spec_url}\n"
        if contact:
            tg_text += f"Contact: {contact}\n"
        tg_text += f"\nChanged files ({file_count}):\n```\n{files[:1000]}\n```"

        self._send_and_respond(tg_text)

    def _cors_headers(self):
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def log_message(self, format, *args):
        print(f"[feedback-server] {args[0]}")


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", PORT), FeedbackHandler)
    print(f"Feedback server listening on 127.0.0.1:{PORT}")
    server.serve_forever()
