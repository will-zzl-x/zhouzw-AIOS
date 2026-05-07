---
name: mid-week-capture
description: Captures a note, thought, or event to journals/inbox.md without synthesis. Triggered by "capture this", "log this", "remember this", or any explicit flag to save something for the weekly reflection.
---

## Goal

Append a timestamped entry to `journals/inbox.md`. Nothing more.

## Reads

- `journals/inbox.md` — current inbox

## Writes

- `journals/inbox.md` — appends new entry

## Steps

1. Take whatever Will shared.
2. Append to `journals/inbox.md` in this format:
   ```
   ---
   **[Day, Date, Time]** — [Will's capture verbatim or lightly cleaned]
   ```
3. Confirm: "Captured."

## Rules

- Do not evaluate, analyze, or summarize the capture.
- Do not ask questions unless the capture is completely ambiguous.
- Do not suggest actions based on the capture.
- Just log it. It gets reviewed and synthesized Sunday.
