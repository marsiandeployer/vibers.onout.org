---
name: vibers-code-review
description: |
  Human-in-the-loop code review for AI-generated projects. Real people look at your code, catch obvious bugs, check main flows work, fix issues and submit PRs. Not a security firm — think alpha tester who sends a PR instead of a ticket.

  Use when: user says "review my code", "check my PR", "send for review", "vibers review", "code review", "set up vibers", "add reviewer", or when a push to main happens and vibers action is configured.
---

# Vibers — Human Code Review for AI-Generated Projects

You push code → humans look at it, fix obvious issues, submit a PR.

**What this is:** Regular people reviewing with fresh eyes. We catch obvious bugs, check that main flows work, fix what's broken. Not a security audit, not OWASP penetration testing — think alpha tester who sends a PR instead of filing a ticket.

## What to Do When This Skill Is Invoked

When the user asks to set up Vibers or send code for review — do these steps:

**1. Create the GitHub Action** (auto-triggers review on every push):

Create `.github/workflows/vibers.yml`:

```yaml
name: Vibers Code Review
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
      - uses: marsiandeployer/vibers-action@v1
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

**2. Add commit rules** to `CLAUDE.md`, `.cursorrules`, or `AGENTS.md`:

```markdown
## Commit messages

Every commit should include a "How to test" section in the body:
- Live URL to open and verify the change
- Step-by-step what to click/check
- Test credentials if login is required
- Expected result for each step

Example:
  feat: Add user registration form

  How to test:
  - Open https://myapp.vercel.app/register
  - Fill in email/password, submit
  - Check that confirmation email arrives
  - Try submitting with invalid email — should show error
  - Login: test@example.com / demo123
```

Without "How to test" the reviewer guesses what to verify — review takes longer and catches less.

> Checkpoint: `CLAUDE.md` (or `.cursorrules` / `AGENTS.md`) contains a "How to test" commit rule block.

**3. Tell the user** to add `marsiandeployer` as collaborator:

> Go to your repo → Settings → Collaborators → Add **marsiandeployer**
> Read-only access is enough to start. Write access only needed for automatic PRs.

After that — every push to main triggers a review. PR with fixes arrives within 24 hours.

> Checkpoint: user confirmed `marsiandeployer` was added as collaborator.

## Setup Complete — Verify

- [ ] `.github/workflows/vibers.yml` committed to repo
- [ ] `CLAUDE.md` / `.cursorrules` / `AGENTS.md` contains "How to test" commit rule
- [ ] User added `marsiandeployer` as collaborator
- [ ] Next push to main will trigger the workflow

If all three are done — setup is complete. Tell the user they'll get a PR with fixes within 24 hours of the next push.

## One-off Review (no Action setup)

To send a single review request directly:

```bash
curl -X POST https://vibers.onout.org/feedback \
  -H 'Content-Type: application/json' \
  -d '{"message": "Please review latest commit", "repo": "https://github.com/owner/repo"}'
```

Both `message` and `repo` are required. Response: `{"status": "accepted"}`.

## What We Check (and Don't)

We check by looking at the code and trying the product manually:
- Spec compliance — does it match what you described?
- AI hallucinations — fake APIs, non-existent imports
- Obvious logic bugs — edge cases, broken flows, null handling
- UI issues — broken layouts, wrong behavior

We don't check: code style (use ESLint/Prettier), performance benchmarks, security pentests, full QA regression (use Playwright/Cypress).

## Support

Contacts: Telegram [@onoutnoxon](https://t.me/onoutnoxon) · GitHub [marsiandeployer](https://github.com/marsiandeployer)

**FAQ**

- **API key?** No. Collaborator + action is enough.
- **Languages?** JS/TS, Python, React, Next.js, Django, Flask, and more.
- **Disagree with a fix?** Comment on the PR — we discuss and adjust.
- **No GitHub?** Send code and spec directly to Telegram.
