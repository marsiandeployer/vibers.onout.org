# Chat Message Wrapping

- title: Chat Message Wrapping
- summary: Long chat messages stayed on one line instead of wrapping, so the conversation UI overflowed horizontally and became hard to read.
- before: https://skrinshoter.ru/s/080426/imGIniKz.png?view=1
- after: https://s3.wpmix.net/main/SCR-20260415-pxq.png
- prompt: Fix long chat message wrapping in the conversation UI. Right now oversized messages stay on one line, overflow the container, and hurt readability. Update the message bubble styles so long text wraps onto the next line, preserves normal spacing, and stays fully readable on both desktop and mobile without changing the rest of the chat layout.
- proof: https://skr.sh/savimGIniKz
- notes: Verified and fixed. This case is meant to show a small but real UI polish issue that a human reviewer can spot quickly and turn into an actionable prompt.
