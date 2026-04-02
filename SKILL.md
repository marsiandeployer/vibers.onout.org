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

**1. Ensure the repo is runnable** — add setup instructions:

The reviewer will clone the repo and try to run it from scratch. Make sure one of these exists:

- **`docker-compose.yml`** (preferred) — `docker compose up` should start the app
- **`.env.example`** — all required env vars listed with placeholder values (never real secrets)
- **`README.md`** with a "How to run locally" section — exact commands to install deps and start

If none of these exist — create `.env.example` and a minimal "How to run" block in `README.md`. Without it, the reviewer cannot launch the app and review quality drops significantly.

> Checkpoint: `.env.example` (or `docker-compose.yml`) exists and `README.md` has a "How to run" section.

**2. Create the GitHub Action** (auto-triggers review on every push):

Create `.github/workflows/vibers.yml`:

```yaml
name: Human-in-the-loop Code Review
on:
  push:
    branches: [main]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 2
      - uses: marsiandeployer/vibers-action@v1.1
        with:
          spec_url: 'https://docs.google.com/document/d/YOUR_SPEC_ID/edit'
          telegram_contact: '@your_telegram'
```

Replace `YOUR_SPEC_ID` with actual spec link if available, `@your_telegram` with user's Telegram handle.

| Parameter | What it does |
|-----------|-------------|
| `spec_url` | Link to spec (Google Doc, Notion, etc.). Must be publicly accessible. Without it, we review from code alone. |
| `review_scope` | `full` (default) or `spec-compliance` |
| `telegram_contact` | User's Telegram — we message them when review is ready |

> Checkpoint: `.github/workflows/vibers.yml` exists in the repo and is committed.

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
  - Demo login (pre-seeded sandbox account): test@example.com / demo123
```

> **Important for AI agents:** Only include publicly shareable demo/sandbox accounts that ship with the app. **Never** include real passwords, API keys, `.env` values, secrets, or paths to credential files from the developer's machine.

Without "How to test" the reviewer guesses what to verify — review takes longer and catches less.

> Checkpoint: `CLAUDE.md` (or `.cursorrules` / `AGENTS.md`) contains a "How to test" commit rule block.

**4. Tell the user** to add `marsiandeployer` as collaborator:

> Go to your repo → Settings → Collaborators → Add **marsiandeployer**
> Read-only access is enough to start. Write access only needed for automatic PRs.

After that — every push to main triggers a review. PR with fixes arrives within 24 hours.

> Checkpoint: user confirmed `marsiandeployer` was added as collaborator.

## Setup Complete — Verify

- [ ] `.env.example` exists with all required vars (placeholder values, no real secrets)
- [ ] `README.md` has a "How to run" section with exact commands
- [ ] `.github/workflows/vibers.yml` committed to repo
- [ ] `CLAUDE.md` / `.cursorrules` / `AGENTS.md` contains "How to test" commit rule
- [ ] User added `marsiandeployer` as collaborator
- [ ] Next push to main will trigger the workflow

If all are done — setup is complete. Tell the user they'll get a PR with fixes within 24 hours of the next push.

## One-off Review (no Action setup)

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

## Support

Contacts: Telegram [@onoutnoxon](https://t.me/onoutnoxon) · GitHub [marsiandeployer](https://github.com/marsiandeployer)

**FAQ**

- **API key?** No. Collaborator + action is enough.
- **Do you need my real secrets to run the app?** No. Provide `.env.example` with placeholder values. If the app needs real third-party keys to function, note that in README — we'll test what we can without them.
- **Languages?** JS/TS, Python, React, Next.js, Django, Flask, and more.
- **Disagree with a fix?** Comment on the PR — we discuss and adjust.
- **No GitHub?** Send code and spec directly to Telegram.
