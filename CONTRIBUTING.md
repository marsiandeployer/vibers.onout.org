# Contributing to Vibers

Thanks for your interest in contributing! Here's how you can help.

## Ways to Contribute

- **Report bugs** — [Open an issue](https://github.com/marsiandeployer/human-in-the-loop-review/issues/new?template=bug_report.md) with steps to reproduce
- **Suggest features** — [Open an issue](https://github.com/marsiandeployer/human-in-the-loop-review/issues/new?template=feature_request.md) describing your idea
- **Write blog posts** — Share your experience with AI code review on our [blog](https://onout.org/vibers/blog/)
- **Improve docs** — Fix typos, clarify instructions, add examples
- **Share the project** — Star the repo, tell friends, post on social media

## Development Setup

```bash
git clone https://github.com/marsiandeployer/human-in-the-loop-review.git
cd human-in-the-loop-review
```

### Running Tests

```bash
python3 tests/test_server.py
```

### Project Structure

```
index.html          — Landing page
setup.html          — GitHub App setup form
scripts/            — Backend (feedback server, webhook handler)
vibers-action/      — GitHub Action source
blog/               — SEO blog articles
tests/              — Test suite
```

## Pull Request Process

1. Fork the repo and create your branch from `main`
2. Make your changes
3. Include "How to test" in your commit message (our webhook checks for this)
4. Open a PR with a clear description

## Code Style

- Python: follow PEP 8
- JavaScript: no framework required, vanilla is fine
- HTML: semantic markup, accessible

## Questions?

- [Telegram](https://t.me/onoutnoxon)
- [Open a discussion](https://github.com/marsiandeployer/human-in-the-loop-review/issues)
