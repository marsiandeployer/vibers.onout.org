# Human-in-the-loop Review — Project Instructions

## Commit messages

Every commit should include a "How to test" section in the body:
- Live URL to open and verify the change
- Step-by-step what to click/check
- Test credentials if login is required
- Expected result for each step

Example:
  feat: Add honest disclaimer block to landing

  How to test:
  - Open https://vibers.onout.org/
  - Expand "What We Do" section
  - Yellow callout block should appear with honest disclaimer text
  - Switch to RU — same block should appear in Russian
