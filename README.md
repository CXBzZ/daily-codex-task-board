# Daily Codex Task Board

This repository stores results produced by Codex automations and publishes them as a static GitHub Pages dashboard.

## How It Works

1. Each Codex automation writes one JSON result into `runs/YYYY-MM-DD/`.
2. `npm run build` regenerates the static site in `public/`.
3. GitHub Pages publishes the `public/` directory.
4. The repository keeps all result JSON files and generated HTML as history.

Read [AUTOMATION_CONTRACT.md](AUTOMATION_CONTRACT.md) before creating a new automation.

## Common Commands

```bash
npm test
npm run build
npm run check
```

## Result Layout

```text
runs/
  2026-07-05/
    example-codex-task.json

public/
  index.html
  history.html
  days/
  tasks/
```

## GitHub Pages

The workflow in `.github/workflows/pages.yml` deploys `public/` on pushes to `main` and on manual dispatch.

In GitHub, set **Settings -> Pages -> Build and deployment -> Source** to **GitHub Actions**.

