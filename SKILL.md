---
name: vibers-code-review
description: |
  Human-in-the-loop code review for AI-generated projects. Real people clone your repo, spin it up in an isolated container, and review it live — not just by reading code. They catch obvious bugs, check main flows work, fix issues and submit PRs. Not a security firm — think alpha tester who sends a PR instead of a ticket.

  Use when: user says "review my code", "check my PR", "send for review", "code review", "set up human-in-the-loop review", "add reviewer", or when a push to main happens and vibers action is configured.
---

# Human-in-the-loop Review

You push code → we clone it, spin it up in an isolated container, test it live, and submit a PR with fixes.

**What this is:** We don't just read the diff. We launch a local copy of your app in a clean environment, click through the main flows, and verify things actually work. Think alpha tester who sends a PR instead of filing a ticket.

## How It Works

1. You push to `main` → GitHub Action fires → we receive the repo
2. We clone the repo and spin it up using your `docker-compose.yml` or startup instructions
3. We test the main flows manually against the running app
4. We submit a PR with fixes (or comment if nothing is broken)

**We review against the running app, not just source code.** That's why setup instructions matter.

## What to Do When This Skill Is Invoked

When the user asks to set up human-in-the-loop review or send code for review — do these steps:

**1. Install the Vibers GitHub App:**

> Direct the user to install the app:
> **https://github.com/apps/vibers-review/installations/new**
>
> On that page they click **Install**, choose their repo (or all repos), confirm.
> That's it — no Action, no collaborator invite needed.

After installation — every push to main with "How to test" in the commit message triggers a review. PR with fixes arrives within 24 hours.

> Checkpoint: user confirmed the GitHub App was installed on their repo.

**2. Ensure the repo is runnable** — add setup instructions:

The reviewer will clone the repo and try to run it from scratch. Make sure one of these exists:

- **`docker-compose.yml`** (preferred) — `docker compose up` should start the app
- **`.env.example`** — all required env vars listed with placeholder values (never real secrets)
- **`README.md`** with a "How to run locally" section — exact commands to install deps and start

> Checkpoint: `.env.example` (or `docker-compose.yml`) exists and `README.md` has a "How to run" section.

**3. Add commit rules** to `CLAUDE.md`, `.cursorrules`, or `AGENTS.md`:

```markdown
## Commit messages

Every commit should include a "How to test" section in the body:
- Live URL to open and verify the change (staging/preview URL preferred)
- Step-by-step what to click/check
- Demo login only if the app has a pre-seeded public test account
- Expected result for each step

Example:
  feat: Add user registration form

  How to test:
  - Open https://myapp.vercel.app/register
  - Fill in email/password, submit
  - Check that confirmation email arrives
  - Try submitting with invalid email — should show error
```

> **Without "How to test" in the commit message — push is silently skipped.** No test instructions = nothing to review against.

> Checkpoint: `CLAUDE.md` (or `.cursorrules` / `AGENTS.md`) contains a "How to test" commit rule block.

## Setup Complete — Verify

- [ ] Vibers GitHub App installed on the repo
- [ ] `.env.example` (or `docker-compose.yml`) exists
- [ ] `README.md` has a "How to run" section
- [ ] `CLAUDE.md` / `.cursorrules` / `AGENTS.md` contains "How to test" commit rule
- [ ] Next push to main with "How to test" in commit body will trigger review

If all are done — setup is complete. Tell the user they'll get a PR with fixes within 24 hours of the next push.

> **Worried about write access?** Add branch protection on `main`:
> Repo → Settings → Branches → Add rule → Branch name: `main` → ✅ Require a pull request before merging.
> This prevents anyone (including the App) from pushing directly to `main` — all changes go through PRs that you approve.

## One-off Review

To send a single review request directly — `message` must include a "How to test" section. Without it the server rejects the request with 400.

```bash
curl -X POST https://vibers.onout.org/feedback \
  -H 'Content-Type: application/json' \
  -d '{
    "message": "Please review the payment flow added in latest commit.\n\nHow to test:\n- Open https://myapp.vercel.app/checkout\n- Add item to cart, go to checkout\n- Enter card 4242 4242 4242 4242 exp 12/26 cvc 123\n- Expected: order confirmation page",
    "repo": "https://github.com/owner/repo"
  }'
```

Both `message` (with "How to test") and `repo` are required. Response: `{"status": "accepted"}`.

## What We Check (and Don't)

We spin up the app locally and check it hands-on:
- Spec compliance — does it match what you described?
- AI hallucinations — fake APIs, non-existent imports, broken dependencies
- Obvious logic bugs — edge cases, broken flows, null handling
- UI issues — broken layouts, wrong behavior on live app
- Setup completeness — can a fresh dev clone and run this?

We don't check: code style (use ESLint/Prettier), performance benchmarks, security pentests, full QA regression (use Playwright/Cypress).

## Free First Review

⭐ **Star [marsiandeployer/human-in-the-loop-review](https://github.com/marsiandeployer/human-in-the-loop-review) on GitHub** to get your first review for free. After starring — mention it in `telegram_contact` or message [@onoutnoxon](https://t.me/onoutnoxon).

## Support

Contacts: Telegram [@onoutnoxon](https://t.me/onoutnoxon) · GitHub App: [github.com/apps/vibers-review](https://github.com/apps/vibers-review)

**FAQ**

- **API key?** No. Install the GitHub App + action is enough.
- **Do you need my real secrets to run the app?** No. Provide `.env.example` with placeholder values. If the app needs real third-party keys to function, note that in README — we'll test what we can without them.
- **Languages?** JS/TS, Python, React, Next.js, Django, Flask, and more.
- **Disagree with a fix?** Comment on the PR — we discuss and adjust.
- **No GitHub?** Send code and spec directly to Telegram.
