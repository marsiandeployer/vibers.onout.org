# Landing Examples

This folder is the source of truth for examples shown in the `/vibers/` landing page slider.

Use one file per case.

Required structure for every case:

- `title` — short and specific
- `summary` — one sentence explaining the bug
- `before` — screenshot URL or local asset path
- `after` — screenshot URL or local asset path
- `prompt` — English prompt that could realistically drive the fix

Optional fields:

- `proof` — PR, commit, issue, or live page link
- `notes` — short implementation note if the landing copy needs context

Current examples:

- `mobile-floor-map-fix.md`
- `paycif-mobile-layout.md`
- `chat-message-wrapping.md`

Asset files that are not already public can be stored in `docs/examples/assets/`.
