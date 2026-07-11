# Multi-Agent Task Board Design

## Goal

Turn the existing Codex, WorkBuddy, and shared-agent pages into one extensible multi-agent dashboard. Each agent gets a dedicated vertical tab with its own current-day results and history. A new personal assistant agent should appear after publishing its first valid result, without requiring generator or registry changes.

## Chosen Approach

Use statically generated, per-agent HTML pages with automatic agent discovery.

The generator continues to read source JSON and produce the complete GitHub Pages site. Agent tabs are ordinary links rather than client-side JavaScript state, so every agent, day, and task page has a stable URL and works when opened directly.

## Result Sources And Discovery

Two agents are built in:

- Codex reads results from `runs/YYYY-MM-DD/` and always appears first.
- WorkBuddy reads results from `runs-workbuddy/YYYY-MM-DD/` and always appears second.

Other personal assistant agents write results to:

```text
runs-agents/YYYY-MM-DD/<agent-id>--<task-id>.json
```

Each shared result requires `agentId` and `agentName`. The generator groups these records by `agentId`; each group becomes one independent agent board. The most recent record supplies the current display name and optional role. Discovered agents appear after the built-in agents in stable display-name order.

An external agent appears only after it has at least one valid result. This keeps onboarding registration-free. The reserved IDs `codex` and `workbuddy` cannot be used by external agents.

## Generated Pages

The existing Codex and WorkBuddy URLs remain valid:

- Codex home: `index.html`
- Codex legacy history: `history.html`
- Codex day and task pages: `days/` and `tasks/`
- WorkBuddy home: `workbuddy.html`
- WorkBuddy legacy history: `workbuddy-history.html`
- WorkBuddy day and task pages: `workbuddy-days/` and `workbuddy-tasks/`

Each discovered agent gets isolated routes:

```text
agents/<agent-id>/index.html
agents/<agent-id>/days/YYYY-MM-DD.html
agents/<agent-id>/tasks/<task-id>.html
data/agents/<agent-id>.json
```

The existing combined `data/agent-runs.json` feed remains available for compatibility. The old mixed `agents.html` and `agent-history.html` entry points no longer render combined results. Each becomes a generated redirect to the first discovered external agent in tab order, or to Codex when no external agent exists.

Including `agentId` in discovered-agent routes prevents two agents with the same `taskId` from sharing task history.

## Page Layout

Every generated page uses the same application shell:

- A compact site header identifies the task board.
- A left-side vertical agent navigation lists Codex, WorkBuddy, and every discovered agent.
- The current agent tab is highlighted with `aria-current="page"`.
- The main area contains only the selected agent's data.

On desktop, the agent navigation is a stable-width left column and the content occupies the remaining width. On mobile, the navigation moves above the content as a vertical list so task cards retain a readable width.

Each agent home contains:

1. A compact heading with agent name, optional role, total result count, tracked-day count, and today's count.
2. A Today section containing that agent's current-day result cards or an empty state.
3. A History section containing that agent's dated history rows and status totals.

History rows link to the selected agent's day pages. Task names link to that agent's task-history pages. Day, task, and legacy history pages retain the same vertical agent navigation.

## Onboarding Guide

Add `AGENT_ONBOARDING.md` as the single quick-start document for future personal assistant agents. It will contain:

- the stable `agentId` and file-naming rules;
- a complete JSON example and required-field reference;
- a copy-ready instruction block for an agent automation;
- first-run dependency and build commands;
- the required Git flow for pulling, writing, rebuilding, committing source JSON with generated HTML, and pushing;
- recovery steps for a rejected or rebased push, including rebuilding after integrating remote changes;
- common validation errors and how to fix them.

`AGENT_BOARD_CONTRACT.md` remains the detailed result contract but is revised to describe independent auto-discovered tabs instead of one shared mixed board. `README.md` and `AGENTS.md` link to the onboarding guide.

## Data Flow

1. An agent pulls the latest `main` branch.
2. It writes one uniquely named result JSON into its source directory.
3. It runs `npm run build` to regenerate the complete site.
4. It commits the source JSON and generated `public/` files together.
5. Before pushing, it rebases on the latest remote branch. If the remote changed, it rebuilds and updates its commit so the generated site includes every agent's latest records.
6. It pushes the commit; GitHub Pages publishes `public/`.

## Validation And Failure Behavior

The build fails with the source file path and a specific message when:

- JSON is malformed;
- a date directory is not `YYYY-MM-DD`;
- a required task or agent field is absent;
- `agentId` or `taskId` is not a safe slug;
- an external record uses a reserved built-in agent ID;
- a status or timestamp is invalid.

A missing current-day record is not an error. The agent remains visible because it has history, its Today section shows an empty state, and its History section remains usable.

## Compatibility And Migration

Existing JSON under `runs/` and `runs-workbuddy/` is not moved or rewritten. Current Codex and WorkBuddy automation prompts remain valid. Existing top-level Codex and WorkBuddy page URLs continue to work, while their layout changes to the unified vertical-agent shell.

The unused mixed-agent presentation is replaced. Future records already following `AGENT_BOARD_CONTRACT.md` remain valid and are grouped into their own agent pages.

## Testing And Acceptance

Automated tests must prove that:

- Codex and WorkBuddy are always present as separate agent tabs;
- multiple external `agentId` values generate separate tabs and pages automatically;
- each agent home contains both Today and History sections;
- an agent without a result today still shows its history;
- identical `taskId` values from different agents remain isolated;
- nested day and task pages calculate navigation links correctly;
- invalid or reserved agent IDs fail with useful errors;
- legacy Codex and WorkBuddy URLs remain generated;
- legacy mixed-agent entry points redirect deterministically without combining agent data;
- data feeds contain only the intended agent's records.

Run `npm test` and `npm run build` before completion. Inspect the generated site at desktop and mobile viewport sizes to verify active tabs, readable cards, non-overlapping content, and usable navigation.
