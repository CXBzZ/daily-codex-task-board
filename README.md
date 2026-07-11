# Daily Codex Task Board

This repository stores results produced by Codex and WorkBuddy automations and publishes them as a static GitHub Pages dashboard with separate tabs for each source.

## How It Works

1. Each Codex automation writes one JSON result into `runs/YYYY-MM-DD/`.
2. Each WorkBuddy automation writes one JSON result into `runs-workbuddy/YYYY-MM-DD/`.
3. `npm run build` regenerates the static site in `public/`, rendering both boards.
4. GitHub Pages publishes the `public/` directory.
5. The repository keeps all result JSON files and generated HTML as history.

Read [AUTOMATION_CONTRACT.md](AUTOMATION_CONTRACT.md) before creating a new Codex automation.
Read [WORKBUDDY_CONTRACT.md](WORKBUDDY_CONTRACT.md) before creating a new WorkBuddy automation.

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

public/                        # generated static site
  index.html                   # Codex "Today" tab
  history.html                 # Codex "History" tab
  days/                        # Codex day pages
  tasks/                       # Codex task pages
  workbuddy.html               # WorkBuddy tab
  workbuddy-history.html       # WorkBuddy history
  workbuddy-days/              # WorkBuddy day pages
  workbuddy-tasks/             # WorkBuddy task pages
  data/
    runs.json                  # Codex data feed
    workbuddy-runs.json        # WorkBuddy data feed
```

## GitHub Pages

The workflow in `.github/workflows/pages.yml` deploys `public/` on pushes to `main` and on manual dispatch.

In GitHub, set **Settings -> Pages -> Build and deployment -> Source** to **GitHub Actions**.

