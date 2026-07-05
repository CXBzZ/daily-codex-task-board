# Codex Automation Result Contract

This repository is the shared result board for Codex automations.

Every automation may do different work, but every automation must report its outcome in the same format so the static dashboard can refresh reliably.

## Required Behavior

When a Codex automation finishes meaningful work:

1. Create or update one JSON file under `runs/YYYY-MM-DD/`.
2. Use the Asia/Shanghai calendar date for `YYYY-MM-DD`.
3. Run `npm run build`.
4. Prefer running `npm test` before committing if the automation changed scripts or result shape.
5. Commit the JSON result and generated `public/` files together.
6. Push the commit if the automation has push permission.

Do not edit files in `public/` by hand. They are generated from `runs/`.

## File Naming

Use a stable lowercase task id:

```text
runs/2026-07-05/<task-id>.json
```

If the same task reports more than once on the same date, add a short suffix:

```text
runs/2026-07-05/<task-id>--1530.json
```

## JSON Schema

```json
{
  "taskId": "daily-review",
  "taskName": "Daily Review",
  "status": "success",
  "startedAt": "2026-07-05T08:00:00+08:00",
  "finishedAt": "2026-07-05T08:05:00+08:00",
  "summary": "Short human-readable result.",
  "details": "Longer result details. Markdown-like plain text is fine.",
  "sourceThread": "Optional Codex thread id or URL.",
  "labels": ["optional", "short-tags"],
  "nextSteps": ["Optional next action."],
  "artifacts": [
    {
      "label": "Optional artifact",
      "path": "relative/path/or/url"
    }
  ]
}
```

## Required Fields

- `taskId`: stable kebab-case id using lowercase letters, numbers, dots, underscores, or hyphens.
- `taskName`: display name for the task.
- `status`: one of `success`, `failure`, `running`, `skipped`, or `needs_attention`.
- `summary`: one or two sentences for the dashboard.

## Optional Fields

- `startedAt` and `finishedAt`: ISO-8601 timestamps.
- `details`: longer plain text. New lines are preserved in the dashboard.
- `sourceThread`: Codex thread id, local note, or URL.
- `labels`: short strings used as visual tags.
- `nextSteps`: follow-up actions.
- `artifacts`: related links or repository paths.

## Automation Prompt Template

Use this in future Codex automations:

```text
After completing your task, write a result JSON file that follows AUTOMATION_CONTRACT.md.
Use the Asia/Shanghai date and write to runs/YYYY-MM-DD/<task-id>.json.
Then run npm run build.
If scripts or result structure changed, run npm test too.
Commit the result JSON and generated public/ files together.
Do not edit public/ directly.
```

