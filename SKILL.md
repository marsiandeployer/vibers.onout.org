# Vibers Code Review — How It Works

## Overview

This project uses **Vibers** — a human code review service. A reviewer (`marsiandeployer`) checks your commits against the project spec, fixes issues, and submits pull requests.

Vibers is NOT an automated linter. It's a human who reads your spec and verifies that the code does what was requested.

## Workflow

### Your side (developer/vibecoder):
1. Write code and push commits as usual
2. GitHub Action automatically notifies Vibers about new changes
3. Wait for a PR from `marsiandeployer` with fixes (usually within 24h)
4. Review the PR, merge if good, comment if you disagree

### Vibers side (marsiandeployer):
1. Receives notification about new commits
2. Reads the spec document (Google Doc / Notion / README)
3. Reviews changed files against the spec
4. Fixes found issues directly in code
5. Submits a PR with all fixes + a structured review summary

## What Gets Checked

| Category | Examples |
|----------|----------|
| **Spec compliance** | Feature matches requirements, correct behavior, nothing missing |
| **Security** | Hardcoded secrets, SQL injection, XSS, missing auth, OWASP top 10 |
| **AI hallucinations** | Non-existent APIs, deprecated methods, fabricated imports |
| **Logic bugs** | Edge cases, off-by-one, race conditions, null handling |
| **Visual/UI** | Broken layouts, wrong colors, mobile responsiveness, accessibility |
| **Architecture** | Inconsistent patterns, copy-paste code, missing error handling |

## What Does NOT Get Checked

- Code style / formatting (use Prettier/ESLint for that)
- Performance benchmarks (use profiling tools)
- Full QA / end-to-end testing (use Playwright/Cypress)

## How to Help the Reviewer

To get the best review, follow these practices:

### 1. Keep your spec up to date
The reviewer checks code against your spec. If the spec is outdated, the review will miss things.

### 2. Write clear commit messages
Bad: `fix stuff`
Good: `Add user registration form (spec section 3.2)`

### 3. One feature per PR
Don't mix 5 features in one commit. The reviewer can't verify spec compliance if changes are tangled.

### 4. Flag what you're unsure about
Add a comment in the PR description: "Not sure about the auth flow in signup.ts — please check carefully."

## Configuration

### GitHub Action (`.github/workflows/vibers.yml`)

```yaml
name: Vibers Code Review
on:
  push:
    branches: [main]
  pull_request:

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

### Inputs

| Input | Description |
|-------|-------------|
| `spec_url` | Link to your spec document |
| `review_scope` | `full` (default), `security`, or `spec-compliance` |
| `telegram_contact` | Your Telegram for status updates |

## Pricing

| Plan | Rate | What's included |
|------|------|-----------------|
| **Promo** | $1/hour | Full review + PRs with fixes. In exchange for honest feedback. |
| **Standard** | $15/hour | Full review + PRs + security audit + priority turnaround. |

Pay as you go. No subscriptions. No contracts.

## Contact

- Telegram: [@onoutnoxon](https://t.me/onoutnoxon)
- Landing: [vibers.onout.org](https://vibers.onout.org)
- GitHub: [marsiandeployer](https://github.com/marsiandeployer)

## FAQ

**Q: Do I need an API key?**
A: Not for the promo plan. Just add `marsiandeployer` as collaborator and set up the action.

**Q: What languages do you support?**
A: JS/TS, Python, React, Node.js, Django, Flask, Next.js, and more. If it's on GitHub, we can review it.

**Q: How fast is the review?**
A: Usually within 24 hours. Standard plan gets priority.

**Q: What if I disagree with a fix?**
A: Comment on the PR. We'll discuss and adjust. No ego, no unnecessary questions.

**Q: Can I use this without GitHub?**
A: Yes — write to Telegram, send your code and spec. We'll review manually.
