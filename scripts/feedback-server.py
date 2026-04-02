#!/usr/bin/env python3
"""
Human-in-the-loop Review Feedback API — accepts user feedback and sends to Telegram.

POST /feedback
Body: {"message": "...", "repo": "https://github.com/user/repo"}

Run via PM2.
"""

import hashlib
import hmac
import json
import os
import subprocess
import sys
import time
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
# Single-threaded: pyrogram requires main thread event loop

TELEGRAM_API_ID = int(os.environ.get("TELEGRAM_API_ID", "20663119"))
TELEGRAM_API_HASH = os.environ.get("TELEGRAM_API_HASH", "")
TELEGRAM_SESSION = os.environ.get("TELEGRAM_SESSION_STRING", "")
TELEGRAM_CHAT_ID = int(os.environ.get("TELEGRAM_CHAT_ID", "-5058393445"))
TELEGRAM_REVIEW_CHAT_ID = int(os.environ.get("TELEGRAM_REVIEW_CHAT_ID", TELEGRAM_CHAT_ID))
PORT = int(os.environ.get("FEEDBACK_PORT", "3847"))

# GitHub App credentials
GH_APP_ID = os.environ.get("GH_APP_ID", "")
GH_WEBHOOK_SECRET = os.environ.get("GH_WEBHOOK_SECRET", "")
GH_APP_SLUG = os.environ.get("GH_APP_SLUG", "vibers-review")

_pem_path = os.environ.get("GH_APP_PRIVATE_KEY_PATH", "")
if _pem_path and os.path.exists(_pem_path):
    with open(_pem_path) as _f:
        GH_APP_PRIVATE_KEY = _f.read()
else:
    GH_APP_PRIVATE_KEY = os.environ.get("GH_APP_PRIVATE_KEY", "")

# In-memory: installation_id -> {"account": str, "repos": list}
_app_installations: dict[int, dict] = {}

# Setup data storage
_SETUP_FILE = os.path.join(os.path.dirname(__file__), "setup-data.json")

def _load_setup_data() -> dict:
    try:
        with open(_SETUP_FILE) as f:
            return json.load(f)
    except Exception:
        return {}

def _save_setup_data(data: dict):
    try:
        with open(_SETUP_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Failed to save setup data: {e}", file=sys.stderr)

_setup_data: dict = _load_setup_data()

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


# ─── GitHub App helpers ────────────────────────────────────────────────────────

def verify_github_signature(payload: bytes, sig_header: str) -> bool:
    """Verify X-Hub-Signature-256 from GitHub webhook."""
    if not GH_WEBHOOK_SECRET:
        return True  # not configured — skip verification
    if not sig_header or not sig_header.startswith("sha256="):
        return False
    expected = "sha256=" + hmac.new(
        GH_WEBHOOK_SECRET.encode(), payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, sig_header)


def make_github_app_jwt() -> str:
    """Generate JWT for GitHub App authentication (valid 10 min)."""
    if not GH_APP_ID or not GH_APP_PRIVATE_KEY:
        raise RuntimeError("GH_APP_ID or GH_APP_PRIVATE_KEY not configured")
    import jwt as pyjwt
    now = int(time.time())
    payload = {"iat": now - 60, "exp": now + 600, "iss": GH_APP_ID}
    return pyjwt.encode(payload, GH_APP_PRIVATE_KEY, algorithm="RS256")


def get_installation_token(installation_id: int) -> str:
    """Exchange app JWT for short-lived installation access token."""
    jwt_token = make_github_app_jwt()
    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    req = urllib.request.Request(
        url, method="POST",
        headers={
            "Authorization": f"Bearer {jwt_token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": f"vibers-review-app/{GH_APP_SLUG}",
        }
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())["token"]


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

# Daily queue counter: {date_str: count}
_daily_queue: dict[str, int] = {}


def get_queue_position() -> int:
    """Increment today's counter and return the position (1-based)."""
    today = time.strftime("%Y-%m-%d")
    _daily_queue[today] = _daily_queue.get(today, 0) + 1
    # Evict old dates (keep only today)
    for key in list(_daily_queue.keys()):
        if key != today:
            del _daily_queue[key]
    return _daily_queue[today]

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

    def _send_and_respond(self, tg_text, chat_id=None, queue_position=None):
        """Send to Telegram and write HTTP response."""
        sent = send_telegram(tg_text, chat_id)
        if sent:
            self.send_response(200)
            self._cors_headers()
            self.end_headers()
            resp = {"status": "accepted"}
            if queue_position is not None:
                resp["queue_position"] = queue_position
            self.wfile.write(json.dumps(resp).encode())
        else:
            self.send_response(502)
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"error": "failed to deliver, contact @onoutnoxon on Telegram"}')

    def do_GET(self):
        if self.path == "/admin/installs":
            self._handle_admin_installs()
        elif self.path == "/health":
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
        elif self.path == "/github/webhook":
            self._handle_github_webhook()
        elif self.path == "/github/setup":
            self._handle_github_setup()
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

        # Require "How to test" in message
        import re as _re
        if not _re.search(r'(?i)how to test', message):
            self.send_response(400)
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"error": "missing \\"How to test\\" section. Add test instructions: live URL, steps to verify, expected result. Without it reviewer cannot check what was changed."}')
            return

        # Fetch last 5 commits from GitHub API
        recent_commits = ""
        repo_path = repo.rstrip("/").replace("https://github.com/", "")
        if "/" in repo_path and not repo_path.startswith("http"):
            try:
                import urllib.request
                api_url = f"https://api.github.com/repos/{repo_path}/commits?per_page=5"
                req = urllib.request.Request(api_url, headers={"User-Agent": "vibers-review-bot"})
                with urllib.request.urlopen(req, timeout=5) as resp:
                    import json as _json
                    commits = _json.loads(resp.read())
                    if isinstance(commits, list):
                        lines = [f"- `{c['sha'][:7]}` {c['commit']['message'].splitlines()[0][:80]}" for c in commits]
                        recent_commits = "\n".join(lines)
            except Exception:
                pass

        tg_text = (
            f"**Feedback**\n\n"
            f"Repo: {repo}\n"
            f"Message: {message}"
        )
        if recent_commits:
            tg_text += f"\n\n📋 Last commits:\n{recent_commits}"
        self._send_and_respond(tg_text)

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
        tg_text = f"**Review Request**\n\n"
        tg_text += f"[{repo}]({repo_url}) | [{sha[:8]}]({commit_url})\n"
        tg_text += f"Author: {author} | Branch: `{branch}`\n"
        tg_text += f"Access: {access_status}\n"

        if commit_msg:
            tg_text += f"\n**{commit_msg}**\n"

        # Parse "How to test" from commit body
        how_to_test = ""
        other_body = commit_body or ""
        if commit_body:
            import re
            m = re.search(r'(?i)(how to test[:\s]*\n)(.*?)(?=\n\n|\Z)', commit_body, re.DOTALL)
            if m:
                how_to_test = m.group(0).strip()
                other_body = commit_body[:m.start()].strip()

        if other_body:
            tg_text += f"\n{other_body}\n"

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

        # How to test block — always last, most important for reviewer
        if how_to_test:
            tg_text += f"\n\n✅ **How to test:**\n```\n{how_to_test}\n```"
        else:
            missing = []
            if not deploy_url:
                missing.append("no deploy URL")
            if not spec_url:
                missing.append("no spec")
            hint = f" ({', '.join(missing)})" if missing else ""
            tg_text += f"\n\n⚠️ **No test instructions in commit{hint}** — ask client via {contact or 'Telegram'}"

        queue_pos = get_queue_position()

        tg_text += f"\n\n🔢 **Queue today: #{queue_pos}**"

        self._send_and_respond(tg_text, TELEGRAM_REVIEW_CHAT_ID, queue_position=queue_pos)

    def _handle_admin_installs(self):
        rows = ""
        all_ids = set(str(k) for k in _app_installations) | set(_setup_data.keys())
        for iid in sorted(all_ids, key=lambda x: int(x) if x.isdigit() else 0, reverse=True):
            inst = _app_installations.get(int(iid) if iid.isdigit() else iid, {})
            setup = _setup_data.get(str(iid), {})
            account = inst.get("account") or setup.get("account", "—")
            repos = ", ".join(inst.get("repos", [])) or "—"
            spec = setup.get("spec_url", "")
            figma = setup.get("figma_url", "")
            tg = setup.get("telegram", "")
            saved = setup.get("saved_at", "")
            spec_html = f'<a href="{spec}" target="_blank">link</a>' if spec else "—"
            figma_html = f'<a href="{figma}" target="_blank">link</a>' if figma else "—"
            rows += f"""<tr>
              <td><a href="https://github.com/{account}" target="_blank">@{account}</a></td>
              <td style="font-size:12px">{repos}</td>
              <td>{spec_html}</td>
              <td>{figma_html}</td>
              <td>{tg or "—"}</td>
              <td style="font-size:12px;color:#999">{saved or "—"}</td>
            </tr>"""

        html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<title>Vibers — Installs</title>
<style>
  body{{font-family:-apple-system,sans-serif;padding:32px;background:#f7f7f8;color:#1a1a1a}}
  h1{{font-size:20px;margin-bottom:4px}}
  .sub{{font-size:13px;color:#999;margin-bottom:24px}}
  table{{width:100%;border-collapse:collapse;background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 1px 8px rgba(0,0,0,.07)}}
  th{{background:#5b44e8;color:#fff;text-align:left;padding:10px 14px;font-size:13px;font-weight:600}}
  td{{padding:10px 14px;border-bottom:1px solid #f0f0f0;font-size:14px;vertical-align:top}}
  tr:last-child td{{border-bottom:none}}
  tr:hover td{{background:#fafafa}}
  a{{color:#5b44e8;text-decoration:none}}
  .count{{display:inline-block;background:#5b44e8;color:#fff;font-size:12px;padding:2px 8px;border-radius:20px;margin-left:8px;vertical-align:middle}}
</style></head>
<body>
<h1>Vibers Installs <span class="count">{len(all_ids)}</span></h1>
<div class="sub">GitHub App installations · refreshed on page load</div>
<table>
  <thead><tr>
    <th>Account</th><th>Repos</th><th>Spec</th><th>Figma</th><th>Telegram</th><th>Setup at</th>
  </tr></thead>
  <tbody>{rows if rows else '<tr><td colspan="6" style="text-align:center;color:#999;padding:32px">No installations yet</td></tr>'}</tbody>
</table>
</body></html>"""

        body = html.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _handle_github_setup(self):
        data, err = self._read_json_body(max_size=5000)
        if err:
            return

        iid_raw = data.get("installation_id", "")
        try:
            iid = int(iid_raw) if iid_raw else 0
        except (ValueError, TypeError):
            iid = 0

        spec_url = str(data.get("spec_url") or "").strip()[:500]
        figma_url = str(data.get("figma_url") or "").strip()[:500]
        telegram = str(data.get("telegram") or "").strip()[:100]

        entry = {
            "installation_id": iid,
            "spec_url": spec_url,
            "figma_url": figma_url,
            "telegram": telegram,
            "saved_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        }

        # Merge with known account info
        known = _app_installations.get(iid, {})
        account = known.get("account", "unknown")
        repos = known.get("repos", [])
        entry["account"] = account

        _setup_data[str(iid)] = entry
        _save_setup_data(_setup_data)

        # Telegram notification
        parts = [f"📋 **Setup Filled**\n\nAccount: {account}"]
        if repos:
            parts.append(f"Repos: {', '.join(repos[:3])}")
        if spec_url:
            parts.append(f"Spec: {spec_url}")
        if figma_url:
            parts.append(f"Figma: {figma_url}")
        if telegram:
            parts.append(f"Telegram: {telegram}")
        if not any([spec_url, figma_url, telegram]):
            parts.append("_(skipped all fields)_")

        send_telegram("\n".join(parts))

        self.send_response(200)
        self._cors_headers()
        self.end_headers()
        self.wfile.write(b'{"ok": true}')

    def _handle_github_webhook(self):
        """Handle GitHub App webhook events."""
        # Read raw body (needed for signature verification)
        try:
            content_length = int(self.headers.get("Content-Length", 0))
        except (ValueError, TypeError):
            content_length = 0

        if content_length > 200_000:
            self.send_response(413)
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"error": "payload too large"}')
            return

        raw_body = self.rfile.read(content_length) if content_length > 0 else b""

        # Verify webhook signature
        sig = self.headers.get("X-Hub-Signature-256", "")
        if not verify_github_signature(raw_body, sig):
            self.send_response(401)
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"error": "invalid signature"}')
            return

        event = self.headers.get("X-GitHub-Event", "")

        try:
            data = json.loads(raw_body) if raw_body else {}
        except json.JSONDecodeError:
            self.send_response(400)
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"error": "invalid json"}')
            return

        # Always respond 200 quickly — Telegram send is best-effort
        self.send_response(200)
        self._cors_headers()
        self.end_headers()
        self.wfile.write(b'{"ok": true}')

        if event == "ping":
            return  # GitHub sends ping on app install — just ack

        if event == "installation":
            action = data.get("action", "")
            installation = data.get("installation", {})
            installation_id = installation.get("id")
            account = installation.get("account", {}).get("login", "unknown")
            repos = [r["full_name"] for r in data.get("repositories", [])]

            if installation_id:
                if action == "created":
                    _app_installations[installation_id] = {"account": account, "repos": repos}
                    repo_list = ", ".join(repos) if repos else "all repos"
                    msg = (
                        f"🎉 **New App Installation**\n\n"
                        f"Account: [{account}](https://github.com/{account})\n"
                        f"Repos: {repo_list}\n"
                        f"Installation ID: `{installation_id}`\n"
                        f"App: https://github.com/apps/{GH_APP_SLUG}"
                    )
                elif action == "deleted":
                    _app_installations.pop(installation_id, None)
                    msg = (
                        f"👋 **App Uninstalled**\n\n"
                        f"Account: [{account}](https://github.com/{account})"
                    )
                elif action == "added":
                    added = [r["full_name"] for r in data.get("repositories_added", [])]
                    if installation_id in _app_installations:
                        _app_installations[installation_id]["repos"].extend(added)
                    msg = (
                        f"➕ **Repos Added**\n\n"
                        f"Account: [{account}](https://github.com/{account})\n"
                        f"Added: {', '.join(added)}"
                    )
                elif action == "removed":
                    removed = [r["full_name"] for r in data.get("repositories_removed", [])]
                    msg = (
                        f"➖ **Repos Removed**\n\n"
                        f"Account: [{account}](https://github.com/{account})\n"
                        f"Removed: {', '.join(removed)}"
                    )
                else:
                    return  # ignore other sub-actions

                send_telegram(msg)
            return

        if event == "push":
            import re as _re
            repo = data.get("repository", {}).get("full_name", "")
            pusher = data.get("pusher", {}).get("name", "unknown")
            ref = data.get("ref", "")
            head_commit = data.get("head_commit") or {}
            full_message = head_commit.get("message", "")
            sha = head_commit.get("id", "")[:8]
            commit_subj = full_message.splitlines()[0][:100]
            commit_url = head_commit.get("url", "")

            if not repo or ref not in ("refs/heads/main", "refs/heads/master"):
                return  # ignore non-default branch pushes

            # Gate: require "How to test" in commit message
            if not _re.search(r'(?i)how to test', full_message):
                return  # skip silently — no test instructions

            # Collect changed files across all commits
            all_files = set()
            for c in data.get("commits", []):
                all_files.update(c.get("added", []))
                all_files.update(c.get("modified", []))
                all_files.update(c.get("removed", []))

            # Extract "How to test" block (content may start on same line or next line)
            m = _re.search(r'(?i)(how to test[:\s]*)(.+?)(?=\n\n|\Z)', full_message, _re.DOTALL)
            how_to_test = m.group(0).strip() if m else ""
            other_body = full_message[:m.start()].strip() if m else ""

            repo_url = f"https://github.com/{repo}"
            tg = f"**Review Request (App)**\n\n"
            tg += f"[{repo}]({repo_url}) | [{sha}]({commit_url})\n"
            tg += f"Pusher: {pusher}\n"
            tg += f"\n**{commit_subj}**\n"
            if other_body and other_body != commit_subj:
                tg += f"\n{other_body}\n"
            if all_files:
                files_str = "\n".join(sorted(all_files)[:30])
                tg += f"\n**Files ({len(all_files)}):**\n```\n{files_str}\n```"
            if how_to_test:
                tg += f"\n\n✅ **{how_to_test}**"

            # Attach setup data (spec, figma, telegram) if available
            install_id = data.get("installation", {}).get("id") or data.get("installation_id")
            if install_id:
                setup = _setup_data.get(str(install_id), {})
                if setup.get("spec_url"):
                    tg += f"\nSpec: {setup['spec_url']}"
                if setup.get("figma_url"):
                    tg += f"\nFigma: {setup['figma_url']}"
                if setup.get("telegram"):
                    tg += f"\nContact: {setup['telegram']}"

            queue_pos = get_queue_position()
            tg += f"\n\n🔢 **Queue today: #{queue_pos}**"

            send_telegram(tg, TELEGRAM_REVIEW_CHAT_ID)
            return

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
