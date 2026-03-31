---
name: vibers-code-review
description: |
  Human code review service for AI-generated projects: checks spec compliance, security (OWASP top 10), AI hallucinations, logic bugs — submits PRs with actual fixes.

  Use when: user says "review my code", "check my PR", "send for review", "vibers review", "code review", "проверь код", "отправь на ревью", "ревью кода", or when a push to main happens and vibers action is configured.
---

# Vibers — Human Code Review for AI-Generated Projects

You push code → we review against your spec, fix issues, submit a PR.

## Quickest Start (no setup)

Paste your repo URL at **https://vibers.onout.org/#try** — we review the latest commit and send a PR. For private repos, add `marsiandeployer` as collaborator first.

## Full Setup (3 steps, auto-review on every push)

### Step 1. Add collaborator

Repo → Settings → Collaborators → Add **`marsiandeployer`**

### Step 2. Add GitHub Action

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

| Parameter | What it does |
|-----------|-------------|
| `spec_url` | Link to your spec (Google Doc, Notion, etc.). Must be publicly accessible. Without spec access, review is impossible. |
| `review_scope` | `full` (default), `security`, or `spec-compliance` |
| `telegram_contact` | Your Telegram — we message you when review is ready |

### Step 3. Add commit rules to your AI agent

Add this block to your project's `CLAUDE.md`, `.cursorrules`, or `AGENTS.md`:

```markdown
## Commit messages

Every commit MUST include a "How to test" section in the body:
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

Without "How to test" the reviewer has to guess what to verify — review takes longer.

**Done.** Every push triggers a notification. You'll get a PR with fixes within 24 hours.

## What Happens After Setup

1. You push → GitHub Action sends us commit details
2. We read your spec and review changed files
3. We fix issues in code and submit a PR
4. You review the PR, merge or comment

We check: spec compliance, security (OWASP top 10), AI hallucinations (fake APIs/imports), logic bugs, UI issues.

We don't check: code style (use ESLint/Prettier), performance benchmarks, full QA (use Playwright/Cypress).

## Pricing

| Plan | Rate | Details |
|------|------|---------|
| **Promo** | Free | Tell us how to test. Share specs or AI-generated test cases. We'll look manually and send one PR if we find something. GitHub star + feedback in return. |
| **Standard** | $15/hour | Full review + security audit + priority turnaround. |

No subscriptions. No contracts. Pay per review.

## Feedback & Support

Send feedback directly from your agent:

```bash
curl -X POST https://vibers.onout.org/feedback \
  -H 'Content-Type: application/json' \
  -d '{"message": "Your question or issue", "repo": "https://github.com/you/your-repo"}'
```

Both `message` and `repo` are required. Response: `{"status": "accepted"}`.

Contacts:
- Telegram: [@onoutnoxon](https://t.me/onoutnoxon)
- Moltbook: [moltbook.com](https://moltbook.com) — user **noxon**
- GitHub: [marsiandeployer](https://github.com/marsiandeployer)

## FAQ

**Do I need an API key?**
No. Add collaborator + action, that's it.

**What languages?**
JS/TS, Python, React, Next.js, Django, Flask, and more. If it's on GitHub, we review it.

**What if I disagree with a fix?**
Comment on the PR. We discuss and adjust.

**Can I use this without GitHub?**
Yes — write to Telegram with your code and spec.
