# Personal Assistant Agent Result Contract

Use this contract for personal assistant agents that are neither the primary Codex board nor the dedicated WorkBuddy board. Start with [AGENT_ONBOARDING.md](AGENT_ONBOARDING.md) for the connection and publishing workflow.

Each valid external agent result is grouped by `agentId`. The generator automatically creates one independent vertical dashboard tab for each discovered agent, with that agent's own Today, History, day, and task pages. No registry or generator change is needed to connect a new agent.

## When To Use This Contract

Write external personal assistant results to `runs-agents/` when the source is not Codex or WorkBuddy. Results from different external agents can share the directory because the generator separates them by their stable `agentId`.

Use [AUTOMATION_CONTRACT.md](AUTOMATION_CONTRACT.md) for primary Codex automations and [WORKBUDDY_CONTRACT.md](WORKBUDDY_CONTRACT.md) for WorkBuddy automations.

## Required Behavior

When an external agent finishes meaningful work:

1. Create or update one JSON file under `runs-agents/YYYY-MM-DD/`.
2. Use the Asia/Shanghai calendar date for `YYYY-MM-DD`.
3. Keep `agentId` stable across every report from the same assistant.
4. Run `npm run build`.
5. Run `npm test` before committing if the agent changed scripts or this result contract.
6. Commit the source JSON and generated `public/` files together.
7. Rebase on `origin/main` before pushing; if the rebase changes repository content, rerun `npm run build` and update the generated `public/` files before pushing.

Do not edit files in `public/` by hand. They are generated from `runs-agents/`.

## File Naming

Use stable lowercase agent and task IDs:

```text
runs-agents/2026-07-12/<agent-id>--<task-id>.json
```

If the same agent reports the same task more than once on the same date, add a short time suffix:

```text
runs-agents/2026-07-12/<agent-id>--<task-id>--1530.json
```

## JSON Schema

External agent records use the same base schema as [AUTOMATION_CONTRACT.md](AUTOMATION_CONTRACT.md), with required agent attribution.

```json
{
  "agentId": "research-agent",
  "agentName": "Research Agent",
  "agentRole": "Market and opportunity scanner",
  "taskId": "daily-market-scan",
  "taskName": "Daily Market Scan",
  "status": "success",
  "startedAt": "2026-07-12T08:00:00+08:00",
  "finishedAt": "2026-07-12T08:05:00+08:00",
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

- `agentId`: stable 2-81 character ID using lowercase letters, numbers, dots, underscores, or hyphens. It must not be `codex` or `workbuddy`.
- `agentName`: display name for the agent.
- `taskId`: stable 2-81 character ID using lowercase letters, numbers, dots, underscores, or hyphens.
- `taskName`: display name for the task.
- `status`: one of `success`, `failure`, `running`, `skipped`, or `needs_attention`.
- `summary`: one or two sentences for the dashboard.

## Optional Fields

- `agentRole`: short description of what the agent is responsible for.
- `startedAt` and `finishedAt`: ISO-8601 timestamps.
- `details`: longer plain text. New lines are preserved in the dashboard.
- `sourceThread`: thread id, run id, local note, or URL.
- `labels`: short strings used as visual tags.
- `nextSteps`: follow-up actions.
- `artifacts`: related links or repository paths.

## Generated Routes

After an external agent publishes its first valid result and the site is rebuilt, its dashboard is generated at:

```text
agents/<agent-id>/index.html
agents/<agent-id>/days/YYYY-MM-DD.html
agents/<agent-id>/tasks/<task-id>.html
data/agents/<agent-id>.json
```

The legacy `agents.html` and `agent-history.html` entry points redirect to the first discovered external agent, or to Codex when no external agent result exists. The combined `data/agent-runs.json` feed remains available for compatibility.

## Existing Boards

| Board | Source directory | Primary route | Use for |
| --- | --- | --- | --- |
| Codex | `runs/` | `index.html` | Primary Codex automations |
| WorkBuddy | `runs-workbuddy/` | `workbuddy.html` | Dedicated WorkBuddy automations |
| External agent | `runs-agents/` | `agents/<agent-id>/index.html` | Any other personal assistant agent |
