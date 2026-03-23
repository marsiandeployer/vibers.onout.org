# Vibers Review Runbook

How to do a code review after receiving a Telegram notification.

## 1. New Invite Notification

You get: "Vibers: New repo invitation!" in Telegram.

Action:
1. Open repo link from the message
2. Check if repo has `.github/workflows/vibers.yml` — if not, the client only added collaborator but didn't set up the Action. Nothing to do until they push.
3. Check if repo has a spec (look for links in README, CLAUDE.md, or vibers.yml `spec_url`)
4. Note the repo for when commits start coming

## 2. Review Request Notification

You get: "Vibers: Review Request" in Telegram with commit details.

Action:
1. Read the commit message — especially "How to test" section
2. Clone/pull the repo:
   ```bash
   mkdir -p /root/reviews && cd /root/reviews
   REPO="owner/repo"  # from Telegram notification
   gh repo clone "$REPO" 2>/dev/null || (cd "$(basename $REPO)" && git fetch --all && git pull --ff-only)
   ```
3. Read the spec (if spec_url provided)
4. Review changed files from the notification

## 3. What to Check

Priority order:
1. **Does it build/run?** — try to compile and start, fix the most obvious blockers
2. **UI issues** — if there's a frontend, build it and open visually, check for broken layouts
3. **AI hallucinations** — non-existent APIs, deprecated methods, fake imports
4. **Logic bugs** — edge cases, off-by-one, null handling, race conditions
5. **Spec compliance** — does the code do what the spec says?

**Static code analysis (security, etc.) is a last resort, not the main focus.**

## 4. Running Code — Docker Only

⚠️ **NEVER run client code directly on the host.** Always use Docker for isolation.

```bash
REPO_DIR=/root/reviews/owner-repo   # path to cloned repo

# Go backend
docker run --rm -v "$REPO_DIR/back-end":/app -w /app golang:1.22 go build ./... 2>&1

# Node/Next.js frontend
docker run --rm -v "$REPO_DIR/frontend":/app -w /app node:20 sh -c "npm ci && npm run build" 2>&1

# Flutter web
docker run --rm -v "$REPO_DIR/frontend":/app -w /app ghcr.io/cirruslabs/flutter:stable sh -c "flutter pub get && flutter build web" 2>&1

# Full docker-compose stack (read-only network, no host ports)
cd "$REPO_DIR" && docker compose up --build 2>&1
```

Fix build errors, push fixes as a PR.

## 5. Submit the Review

1. Fork the repo (if not already forked)
2. Create a branch: `vibers/review-<date>`
3. Make fixes directly in code
4. Push and create PR:
   ```bash
   gh pr create --title "Vibers: code review fixes" --body "..."
   ```
5. Message the client on Telegram (if contact provided)

## 5. Monitoring

- Check Telegram chat periodically for missed notifications
- Health check (requires nginx proxy to be configured):
  ```bash
  curl https://vibers.onout.org/health
  # Expected: {"status": "ok"}
  ```
- PM2 status:
  ```bash
  pm2 show vibers-feedback         # should be online
  pm2 show vibers-invite-checker   # runs via cron, may show stopped between runs
  ```
- PM2 start from config (if processes missing):
  ```bash
  cd /root/vibers.onout.org/scripts && pm2 start ecosystem.config.js
  pm2 save
  ```
- If no notifications for >1 hour, SSH to server and check `pm2 logs vibers-feedback --lines 20`

## 6. Common Issues

| Problem | Fix |
|---------|-----|
| No notifications coming | Check `pm2 status vibers-feedback` — should be online |
| Telegram "send failed" | Pyrogram session may have expired. Regenerate session string |
| invite-checker errored | Normal — it's a PM2 cron, exits after each run. Check error logs if `pm2 logs vibers-invite-checker --err` shows real errors |
| Client spec is private | Message client on Telegram to make spec publicly accessible |
