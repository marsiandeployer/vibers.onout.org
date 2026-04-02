# Human-in-the-loop Review — Code Review for Vibe Coders

[![Star on GitHub](https://img.shields.io/github/stars/marsiandeployer/human-in-the-loop-review?style=social)](https://github.com/marsiandeployer/human-in-the-loop-review)

**AI writes the code. We check if it actually works.**

You vibe code fast with Cursor, Copilot, or Claude. Then spend 3x longer debugging things you didn't write. Sound familiar?

It puts a human in the loop. We look at your code, catch the obvious stuff AI misses, fix it, and send you a PR. You merge and keep shipping.

> **Honest about what this is:** We're not a security firm. No OWASP pentests, no architecture deep-dives. We're regular people who review your code with fresh eyes — catch obvious bugs, check that main flows work, write the fix. Think alpha tester who sends a PR instead of filing a ticket.

---

## Try It Now

**Got an AI agent? Just say:**

```
Install skill from https://vibers.onout.org/SKILL.md
```

Claude Code, Cursor, and Codex will set everything up automatically.

**No agent? Do it manually:**

1. Add [`marsiandeployer`](https://github.com/marsiandeployer) as collaborator to your repo
2. Push some code
3. Get a PR with fixes within 24 hours

---

## What We Catch

| | What we look for |
|---|---|
| **Spec compliance** | Does the code actually do what you described? |
| **AI hallucinations** | Fake APIs, non-existent imports, fabricated methods |
| **Logic bugs** | Edge cases, broken flows, null handling, off-by-one |
| **UI issues** | Broken layouts, missing states, wrong behavior |
| **Obvious security gaps** | Hardcoded secrets, open CORS, missing auth checks |

---

## How It Works

```
You push → GitHub Action notifies us → Human reviews vs your spec → PR with fixes → You merge
```

Setup takes 30 seconds. Spec is optional — we read the code.

---

## Pricing

| Plan | Price | What happens |
|------|-------|-------------|
| **Promo** | Free | Share how to test your product. We look, fix what we find, send a PR. GitHub ⭐ + feedback in return. |
| **Standard** | $15/hour | Full review against spec, PRs with fixes, priority turnaround. Pay only for hours spent. |

No subscriptions. No contracts. No minimums.

---

## Who It's For

- **Solo founders** who vibecoded an MVP and want a sanity check before launch
- **Non-technical founders** who have a spec but can't read the code
- **AI-first teams** where most code is generated and nobody's reviewing it
- **Startup founders** who hired cheap devs and need a quality gate

---

## GitHub Action Setup

```yaml
- uses: marsiandeployer/vibers-action@v1.1
  with:
    spec_url: 'https://docs.google.com/document/d/YOUR_SPEC/edit'
    telegram_contact: '@your_telegram'
```

Full setup guide in [SKILL.md](https://vibers.onout.org/SKILL.md).

---

## FAQ

**Do I need to share my spec?**
Nope — it's optional. We read the code and figure out context. But a spec means faster, more targeted reviews.

**What languages?**
JS/TS, Python, React, Next.js, Node.js, Django, Flask. If it's on GitHub, we can review it.

**How fast?**
Within 24 hours. Standard plan gets priority.

**What if I disagree with a fix?**
Comment on the PR. We discuss, adjust, or explain.

**No GitHub?**
[Write us on Telegram](https://t.me/onoutnoxon) and send your code + spec directly.

---

If this sounds useful — a ⭐ helps others find the project!

[![Star on GitHub](https://img.shields.io/github/stars/marsiandeployer/human-in-the-loop-review?style=social)](https://github.com/marsiandeployer/human-in-the-loop-review)

[Landing page](https://vibers.onout.org) · [Skill file](https://vibers.onout.org/SKILL.md) · [GitHub Action](https://github.com/marsiandeployer/vibers-action) · [Telegram](https://t.me/onoutnoxon)
