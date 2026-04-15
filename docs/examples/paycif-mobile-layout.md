# Paycif Mobile Pricing Cards

- title: Paycif Mobile Pricing Cards
- summary: The pricing cards stayed in columns on mobile because the new grid shipped without a small-screen breakpoint.
- before: https://i.wpmix.net/image/photo/photo_1774439739463.jpg
- after: docs/examples/assets/paycif-mobile-after.png
- prompt: Fix the fee-card section on mobile. The pricing cards still render in columns at small widths and the section feels cramped. Add a mobile breakpoint that collapses the grid to one column, remove decorative transforms that break spacing on small screens, and keep the desktop layout unchanged.
- proof: https://github.com/MethasMP/Paycif/pull/3
- notes: The local after asset was captured from the public page with the PR's responsive rules applied in-browser so the landing page shows the intended mobile result even if the live deploy drifts later.
