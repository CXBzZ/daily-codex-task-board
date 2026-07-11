# Daily Codex Task Board

This repository stores results produced by Codex, WorkBuddy, and other personal assistant agents. It publishes them as a static GitHub Pages dashboard with separate tabs for dedicated boards and one shared multi-agent board.

## How It Works

1. Each Codex automation writes one JSON result into `runs/YYYY-MM-DD/`.
2. Each WorkBuddy automation writes one JSON result into `runs-workbuddy/YYYY-MM-DD/`.
3. Any other personal assistant agent writes one JSON result into `runs-agents/YYYY-MM-DD/`.
4. `npm run build` regenerates the static site in `public/`, rendering all boards.
5. GitHub Pages publishes the `public/` directory.
6. The repository keeps all result JSON files and generated HTML as history.

Read [AUTOMATION_CONTRACT.md](AUTOMATION_CONTRACT.md) before creating a new Codex automation.
Read [WORKBUDDY_CONTRACT.md](WORKBUDDY_CONTRACT.md) before creating a new WorkBuddy automation.
Read [AGENT_BOARD_CONTRACT.md](AGENT_BOARD_CONTRACT.md) before connecting any other personal assistant agent.

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

runs-agents/                   # shared personal assistant agent results
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
  agents.html                  # shared Agents tab
  agent-history.html           # shared Agents history
  agent-days/                  # shared Agents day pages
  agent-tasks/                 # shared Agents task pages
  data/
    runs.json                  # Codex data feed
    workbuddy-runs.json        # WorkBuddy data feed
    agent-runs.json            # shared Agents data feed
```

## Connecting Another Personal Agent

Give the agent this instruction:

```text
After completing your task, write a result JSON file that follows AGENT_BOARD_CONTRACT.md.
Use the Asia/Shanghai date and write to runs-agents/YYYY-MM-DD/<agent-id>--<task-id>.json.
Then run npm run build.
Commit the result JSON and generated public/ files together.
Do not edit public/ directly.
```

## GitHub Pages

The workflow in `.github/workflows/pages.yml` deploys `public/` on pushes to `main` and on manual dispatch.

In GitHub, set **Settings -> Pages -> Build and deployment -> Source** to **GitHub Actions**.
