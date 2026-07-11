# WorkBuddy Automation Result Contract

This repository also hosts results produced by **WorkBuddy** automations, displayed in a separate "WorkBuddy" tab on the dashboard.

WorkBuddy automations use the **same JSON schema** as Codex automations (see [AUTOMATION_CONTRACT.md](AUTOMATION_CONTRACT.md)), but write their results to a **separate directory** so the two pipelines never interfere.

## Required Behavior

When a WorkBuddy automation finishes meaningful work:

1. Create or update one JSON file under `runs-workbuddy/YYYY-MM-DD/`.
2. Use the Asia/Shanghai calendar date for `YYYY-MM-DD`.
3. Run `npm run build`.
4. Prefer running `npm test` before committing if the automation changed scripts or result shape.
5. Commit the JSON result and generated `public/` files together.
6. Push the commit if the automation has push permission.

Do not edit files in `public/` by hand. They are generated from `runs-workbuddy/`.

## File Naming

Use a stable lowercase task id:

```text
runs-workbuddy/2026-07-05/<task-id>.json
```

If the same task reports more than once on the same date, add a short suffix:

```text
runs-workbuddy/2026-07-05/<task-id>--1530.json
```

## JSON Schema

Identical to the Codex contract. See [AUTOMATION_CONTRACT.md](AUTOMATION_CONTRACT.md#json-schema) for the full schema.

Required fields: `taskId`, `taskName`, `status`, `summary`.

Optional fields: `startedAt`, `finishedAt`, `details`, `sourceThread`, `labels`, `nextSteps`, `artifacts`.

## Automation Prompt Template

Use this in WorkBuddy automations:

```text
After completing your task, write a result JSON file that follows WORKBUDDY_CONTRACT.md.
Use the Asia/Shanghai date and write to runs-workbuddy/YYYY-MM-DD/<task-id>.json.
Then run npm run build.
If scripts or result structure changed, run npm test too.
Commit the result JSON and generated public/ files together.
Do not edit public/ directly.
```

## How Codex and WorkBuddy Coexist

| Aspect             | Codex                     | WorkBuddy                     |
| ------------------ | ------------------------- | ----------------------------- |
| Results directory  | `runs/`                   | `runs-workbuddy/`             |
| Dashboard tab      | Today / History           | WorkBuddy                     |
| Generated pages    | `index.html`, `history.html`, `days/`, `tasks/` | `workbuddy.html`, `workbuddy-history.html`, `workbuddy-days/`, `workbuddy-tasks/` |
| Data feed          | `data/runs.json`          | `data/workbuddy-runs.json`    |
| JSON schema        | shared                    | shared                        |

The two pipelines are fully independent: a Codex automation writing to `runs/` will never affect WorkBuddy results, and vice versa.
