# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in Vibers, please report it responsibly.

**Do NOT open a public GitHub issue for security vulnerabilities.**

Instead, contact us directly:

- **Telegram:** [@onoutnoxon](https://t.me/onoutnoxon)
- **Email:** support@onout.org

We will acknowledge receipt within 48 hours and provide an estimated timeline for a fix.

## Scope

This policy covers:

- The Vibers webhook server (`scripts/feedback-server.py`)
- The GitHub Action (`vibers-action/`)
- The landing page and setup form

## What We Consider Vulnerabilities

- Authentication bypasses
- Webhook signature verification issues
- Data exposure (installation data, setup data)
- XSS or injection in admin interface
- Rate limiting bypasses

## Supported Versions

| Version | Supported |
|---------|-----------|
| Latest (main branch) | Yes |
| Older versions | No |
