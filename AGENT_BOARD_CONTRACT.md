# Shared Personal Agent Board Contract

This repository can host results from any personal assistant agent in one shared **Agents** board.

Use this contract for agents that are not the primary Codex board and are not the dedicated WorkBuddy board.

## When To Use This Board

Use `runs-agents/` when:

- multiple personal assistant agents need to report into one shared task board
- the agent is not important enough to deserve its own dedicated tab
- you want one place to compare results from research, scheduling, finance, content, ops, or other helper agents

Use a dedicated directory and board only when an agent has a distinct workflow that should not mix with other assistants.

## Required Behavior

When an agent finishes meaningful work:

1. Create or update one JSON file under `runs-agents/YYYY-MM-DD/`.
2. Use the Asia/Shanghai calendar date for `YYYY-MM-DD`.
3. Run `npm run build`.
4. Prefer running `npm test` before committing if the agent changed scripts or result shape.
5. Commit the JSON result and generated `public/` files together.
6. Push the commit if the agent has push permission.

Do not edit files in `public/` by hand. They are generated from `runs-agents/`.

## File Naming

Use a stable lowercase agent id and task id:

```text
runs-agents/2026-07-11/<agent-id>--<task-id>.json
```

If the same agent reports the same task more than once on the same date, add a short time suffix:

```text
runs-agents/2026-07-11/<agent-id>--<task-id>--1530.json
```

## JSON Schema

Shared agent records use the same base schema as [AUTOMATION_CONTRACT.md](AUTOMATION_CONTRACT.md), with required agent attribution.

```json
{
  "agentId": "research-agent",
  "agentName": "Research Agent",
  "agentRole": "Market and opportunity scanner",
  "taskId": "daily-market-scan",
  "taskName": "Daily Market Scan",
  "status": "success",
  "startedAt": "2026-07-11T08:00:00+08:00",
  "finishedAt": "2026-07-11T08:05:00+08:00",
  "summary": "Short human-readable result.",
  "details": "Longer result details. Markdown-like plain text is fine.",
  "sourceThread": "Optional thread id, agent run id, or URL.",
  "labels": ["research", "daily"],
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

- `agentId`: stable kebab-case id using lowercase letters, numbers, dots, underscores, or hyphens.
- `agentName`: display name for the agent.
- `taskId`: stable kebab-case id using lowercase letters, numbers, dots, underscores, or hyphens.
- `taskName`: display name for the task.
- `status`: one of `success`, `failure`, `running`, `skipped`, or `needs_attention`.
- `summary`: one or two sentences for the dashboard.

## Optional Fields

- `agentRole`: short description of what this agent is responsible for.
- `startedAt` and `finishedAt`: ISO-8601 timestamps.
- `details`: longer plain text. New lines are preserved in the dashboard.
- `sourceThread`: thread id, run id, local note, or URL.
- `labels`: short strings used as visual tags.
- `nextSteps`: follow-up actions.
- `artifacts`: related links or repository paths.

## Agent Prompt Template

Use this in any personal assistant agent that should report to the shared board:

```text
After completing your task, write a result JSON file that follows AGENT_BOARD_CONTRACT.md.
Use the Asia/Shanghai date and write to runs-agents/YYYY-MM-DD/<agent-id>--<task-id>.json.
Include agentId, agentName, taskId, taskName, status, and summary.
Then run npm run build.
If scripts or result structure changed, run npm test too.
Commit the result JSON and generated public/ files together.
Do not edit public/ directly.
```

## Existing Boards

| Board | Source directory | Use for |
| --- | --- | --- |
| Codex | `runs/` | Primary Codex automations |
| WorkBuddy | `runs-workbuddy/` | Dedicated WorkBuddy automations |
| Agents | `runs-agents/` | Any other personal assistant agent |

