# Vibers — Human-in-the-Loop Code Review

Landing page and integration tools for [vibers.onout.org](https://vibers.onout.org).

## What is Vibers?

Human code review service for vibecoded projects. We review commits, fix issues, and send pull requests.

- **Plug & play** — tell your AI agent: `Install skill from https://vibers.onout.org/SKILL.md`
- **Or just add** `marsiandeployer` as collaborator to your GitHub repo
- **Spec optional** — we figure out context from the code
- **We fix, not just report** — every review = PR with working code

## Pricing

| Plan | Rate | Includes |
|------|------|----------|
| **Promo** | $1/hour | Full review + PRs with fixes. In exchange for feedback. |
| **Standard** | $15/hour | Full review + PRs + security & architecture audit. Priority. |

Pay as you go. No subscriptions. No contracts.

## Files

| File | Purpose |
|------|---------|
| `index.html` | Landing page (glassmorphism, i18n EN/RU) |
| `SKILL.md` | AI agent skill — describes workflow, what gets checked, how to help the reviewer |
| `scripts/check-invites.py` | PM2 cron: monitors GitHub invitations, auto-accepts, notifies Telegram |
| `scripts/check-prices.sh` | Pre-commit hook: validates prices match across SKILL.md and index.html |
| `scripts/ecosystem.config.js` | PM2 config for invite checker |

## Deployment

- **Server:** REDACTED_IP (VM104)
- **Path:** `/root/vibers.onout.org/`
- **Nginx:** `vibers.onout.org` → root `/root/vibers.onout.org/`
- **DNS:** Cloudflare A record → REDACTED_IP (proxied)

Deploy = `git push` (manual pull on server for now).

## Important: Keep Content in Sync!

Three files must have consistent descriptions and pricing:

1. **`index.html`** — landing page (both EN and RU translations in JS)
2. **`SKILL.md`** — AI agent skill file
3. **`README.md`** — this file

The pre-commit hook checks price consistency between `index.html` and `SKILL.md`.
Text descriptions should be manually kept in sync.

## PM2 Processes

| Process | Schedule | Purpose |
|---------|----------|---------|
| `vibers-invite-checker` | every 1 min | Check GitHub invitations, auto-accept, notify Telegram |

## Support the Project

If Vibers helps you ship better code — give us a star! It helps others find the project and keeps us going.

[![GitHub stars](https://img.shields.io/github/stars/marsiandeployer/human-in-the-loop-review?style=social)](https://github.com/marsiandeployer/human-in-the-loop-review)

## Links

- Landing: https://vibers.onout.org
- Skill: https://vibers.onout.org/SKILL.md
- GitHub Action: https://github.com/marsiandeployer/vibers-action
- Telegram: https://t.me/onoutnoxon
- Product on habab.ru: https://habab.ru/products/vibecoder_review
- SEO article: https://habab.ru/vibecoder-review
