---
name: vibers-code-review
description: |
  Human-in-the-loop code review for AI-generated projects. Installs automatically: adds "How to test" commit rules so the agent writes test cases in every commit, then sets up the Vibers GitHub App that triggers a real human to spin up the app, test it live, and submit a PR with fixes.

  Use when: user says "set up review", "review my code", "send for review", "human review", "set up vibers", or when the user installs this skill for the first time.

  After install: on every commit, if "How to test" is missing from the commit body — remind the user to add it or add it yourself based on the changes made.
---

# Vibers — Human-in-the-loop Code Review

**What the skill does:** teaches your agent to automatically write "How to test" sections in every commit. Those test cases tell a real human reviewer exactly what to click and what to expect — triggering a live review of your running app with a PR of fixes.

You push code → reviewer spins it up in an isolated container → tests the flows you described → submits a PR with fixes.

## What to Do When This Skill Is Invoked

### Step 1 — Add "How to test" commit rules (do this automatically)

Add the following block to `CLAUDE.md`, `.cursorrules`, or `AGENTS.md` in the project root:

```markdown
## Commit messages

Every commit must include a "How to test" section in the body:
- Live URL to open and verify the change (staging/preview URL preferred)
- Step-by-step what to click/check
- Expected result for each step

Example:
  feat: Add user registration form

  How to test:
  - Open https://myapp.vercel.app/register
  - Fill in email/password, submit
  - Check that confirmation email arrives
  - Try submitting with invalid email — should show error
```

> **Without "How to test" in the commit body — the push is silently skipped by Vibers.** Always include it.

> Checkpoint: commit rule block added to `CLAUDE.md` or equivalent.

### Step 2 — Install the Vibers GitHub App

Direct the user to install:
**https://github.com/apps/vibers-review/installations/new**

Click **Install** → choose the repo → confirm. No YAML files, no collaborator invites, no CI config.

After installation: every push to `main` with "How to test" in the commit body triggers a review. PR with fixes arrives within 24 hours.

> Checkpoint: user confirmed GitHub App is installed on their repo.

### Step 3 — Ensure the repo is runnable

The reviewer clones the repo and tries to run it from scratch. Make sure:

- **`.env.example`** exists with all required env vars as placeholder values (never real secrets)
- **`README.md`** has a "How to run locally" section with exact commands

> Checkpoint: `.env.example` and `README.md` "How to run" section exist.

## Setup Complete — Verify

- [ ] `CLAUDE.md` (or `.cursorrules` / `AGENTS.md`) contains "How to test" commit rule
- [ ] Vibers GitHub App installed on the repo
- [ ] `.env.example` exists with placeholder values
- [ ] `README.md` has a "How to run" section
- [ ] Next push to `main` with "How to test" in commit body will trigger review

Tell the user: setup is complete. The agent will now write test cases automatically in every commit. First review PR arrives within 24 hours of the next push.

> **Worried about write access?** Add branch protection on `main`:
> Repo → Settings → Branches → Add rule → Branch name: `main` → ✅ Require a pull request before merging.
> This ensures all Vibers fixes come as PRs you approve — nothing is pushed directly.

## Ongoing — After Every Commit

When the agent writes a commit, check that "How to test" is in the body. If it's missing — add it based on what changed:

```
How to test:
- Open [relevant URL or describe where to navigate]
- [Action to take]
- Expected: [what should happen]
```

If there's no live URL yet, describe the flow locally or note "not yet deployed — test locally with `npm run dev`".

## One-off Review (no App setup)

To send a single review without installing the App:

```bash
curl -X POST https://vibers.onout.org/feedback \
  -H 'Content-Type: application/json' \
  -d '{
    "message": "Please review the payment flow.\n\nHow to test:\n- Open https://myapp.vercel.app/checkout\n- Add item to cart, proceed\n- Enter card 4242 4242 4242 4242 exp 12/26 cvc 123\n- Expected: order confirmation page",
    "repo": "https://github.com/owner/repo"
  }'
```

Both `message` (with "How to test") and `repo` are required. Response: `{"status": "accepted"}`.

## What We Check (and Don't)

We spin up the app and check it hands-on:
- Spec compliance — does it match what you described?
- AI hallucinations — fake APIs, non-existent imports, broken dependencies
- Obvious logic bugs — edge cases, broken flows, null handling
- UI issues — broken layouts, wrong behavior on the live app
- Degradation — things that worked before and quietly stopped

We don't check: code style (use ESLint/Prettier), performance benchmarks, security pentests, full regression suites (use Playwright/Cypress).

## Free First Review

⭐ **Star [marsiandeployer/human-in-the-loop-review](https://github.com/marsiandeployer/human-in-the-loop-review) on GitHub** to get your first review for free. After starring — message [@onoutnoxon](https://t.me/onoutnoxon).

## Support

Telegram [@onoutnoxon](https://t.me/onoutnoxon) · GitHub App: [github.com/apps/vibers-review](https://github.com/apps/vibers-review) · Site: [vibers.onout.org](https://vibers.onout.org)

**FAQ**

- **API key?** No. Install the GitHub App — that's it.
- **Real secrets needed?** No. `.env.example` with placeholders is enough.
- **Languages?** JS/TS, Python, React, Next.js, Django, Flask, and more.
- **Disagree with a fix?** Comment on the PR — we discuss and adjust.
- **No GitHub?** Send code and description directly to Telegram.
