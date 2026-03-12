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

    def do_POST(self):
        if self.path != "/feedback":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error": "not found"}')
            return

        # Rate limiting
        client_ip = self.headers.get("X-Real-IP", self.client_address[0])
        if not check_rate_limit(client_ip):
            self.send_response(429)
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"error": "too many requests, try again later"}')
            return

        try:
            content_length = int(self.headers.get("Content-Length", 0))
        except (ValueError, TypeError):
            self.send_response(400)
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"error": "invalid content-length"}')
            return

        if content_length > 10000:
            self.send_response(413)
            self.end_headers()
            self.wfile.write(b'{"error": "too large"}')
            return

        body = self.rfile.read(content_length)
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"error": "invalid json"}')
            return

        # Type-safe field extraction
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

        message = message.strip()[:2000]  # cap message length
        repo = repo.strip()[:500]

        tg_text = (
            f"**Vibers Feedback**\n\n"
            f"Repo: {repo}\n"
            f"Message: {message}"
        )

        sent = send_telegram(tg_text)

        if sent:
            self.send_response(200)
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"status": "feedback accepted"}')
        else:
            self.send_response(502)
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"error": "failed to deliver feedback, please contact us on Telegram @onoutnoxon"}')

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
