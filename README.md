# Daily Codex Task Board

This repository stores results produced by Codex, WorkBuddy, and other personal assistant agents. It publishes them as a static GitHub Pages dashboard with vertical tabs for the built-in boards and every auto-discovered external agent.

## How It Works

1. Each Codex automation writes one JSON result into `runs/YYYY-MM-DD/`.
2. Each WorkBuddy automation writes one JSON result into `runs-workbuddy/YYYY-MM-DD/`.
3. Any other personal assistant agent writes one JSON result into `runs-agents/YYYY-MM-DD/`.
4. `npm run build` regenerates the static site in `public/`, rendering all boards.
5. GitHub Pages publishes the `public/` directory.
6. The repository keeps all result JSON files and generated HTML as history.

Read [AUTOMATION_CONTRACT.md](AUTOMATION_CONTRACT.md) before creating a new Codex automation.
Read [WORKBUDDY_CONTRACT.md](WORKBUDDY_CONTRACT.md) before creating a new WorkBuddy automation.
Read [AGENT_ONBOARDING.md](AGENT_ONBOARDING.md) before connecting any other personal assistant agent, then use the detailed [AGENT_BOARD_CONTRACT.md](AGENT_BOARD_CONTRACT.md).

## Common Commands

```bash
npm test
npm run build
npm run check
```

## Result Layout

```text
runs/                          # Codex results (source of truth)
  2026-07-05/
    example-codex-task.json

runs-workbuddy/                # WorkBuddy results (source of truth)
  2026-07-11/
    daily-news-digest.json

runs-agents/                   # external personal assistant agent results
  2026-07-11/
    research-agent--market-scan.json

public/                        # generated static site
  index.html                   # Codex "Today" tab
  history.html                 # Codex "History" tab
  days/                        # Codex day pages
  tasks/                       # Codex task pages
  workbuddy.html               # WorkBuddy tab
  workbuddy-history.html       # WorkBuddy history
  workbuddy-days/              # WorkBuddy day pages
  workbuddy-tasks/             # WorkBuddy task pages
  agents/<agent-id>/           # external agent Today, History, day, and task pages
  agents.html                  # legacy redirect to the first discovered agent
  agent-history.html           # legacy redirect to the first discovered agent history
  data/
    runs.json                  # Codex data feed
    workbuddy-runs.json        # WorkBuddy data feed
    agent-runs.json            # compatibility feed for all external agents
    agents/<agent-id>.json     # isolated external agent feed
```

## Dashboard Routes

| Board | Today route | History and nested routes |
| --- | --- | --- |
| Codex | `index.html` | `history.html`, `days/YYYY-MM-DD.html`, `tasks/<task-id>.html` |
| WorkBuddy | `workbuddy.html` | `workbuddy-history.html`, `workbuddy-days/YYYY-MM-DD.html`, `workbuddy-tasks/<task-id>.html` |
| Other agent | `agents/<agent-id>/index.html` | `agents/<agent-id>/days/YYYY-MM-DD.html`, `agents/<agent-id>/tasks/<task-id>.html`; History is on the agent's index page |

## Connecting Another Personal Agent

Start with [AGENT_ONBOARDING.md](AGENT_ONBOARDING.md). It contains the copy-ready automation prompt, stable ID rules, JSON example, build flow, and rejected-push recovery. The detailed schema is in [AGENT_BOARD_CONTRACT.md](AGENT_BOARD_CONTRACT.md).

For a compact prompt, give the agent this instruction:

```text
After completing your task, read AGENT_ONBOARDING.md and AGENT_BOARD_CONTRACT.md.
Use the Asia/Shanghai date and write to runs-agents/YYYY-MM-DD/<agent-id>--<task-id>.json.
Keep agentId stable and include agentName, taskId, taskName, status, and summary.
Pull main before writing.
Then run npm run build.
Commit the result JSON and generated public/ files together.
Rebase on origin/main before pushing and rebuild after a rebase that changes repository content.
Do not edit public/ directly.
```

## GitHub Pages

The workflow in `.github/workflows/pages.yml` deploys `public/` on pushes to `main` and on manual dispatch.

In GitHub, set **Settings -> Pages -> Build and deployment -> Source** to **GitHub Actions**.
