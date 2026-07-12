# Connect A Personal Assistant Agent

Use this guide to publish results from a personal assistant agent other than the built-in Codex and WorkBuddy boards. Read it before the detailed [AGENT_BOARD_CONTRACT.md](AGENT_BOARD_CONTRACT.md).

Each external agent is discovered automatically after its first valid result. It receives its own vertical dashboard tab, a home page with Today and History sections, and isolated day and task pages at `agents/<agent-id>/`.

## Choose Stable IDs

- Choose one `agentId` for the assistant and keep it unchanged across every result and date. It identifies the agent's dashboard, feed, and routes.
- Use lowercase letters, numbers, dots, underscores, or hyphens only. IDs must start with a lowercase letter or number and be 2 to 81 characters long.
- Do not use spaces, uppercase letters, or change an ID to reflect a task, date, or version.
- `codex` and `workbuddy` are reserved built-in IDs and cannot be used for external agents.
- Choose a stable `taskId` using the same character rules. It identifies one recurring task's history within an agent board.

For example, keep `agentId` as `research-agent` for every task from that assistant and use task IDs such as `daily-market-scan` or `weekly-competitor-review`.

## Write A Result

Use the Asia/Shanghai calendar date in both the directory and timestamps. Create exactly one JSON result for a completed task at:

```text
runs-agents/YYYY-MM-DD/<agent-id>--<task-id>.json
```

When the same agent reports the same task more than once on one date, append a short time suffix:

```text
runs-agents/YYYY-MM-DD/<agent-id>--<task-id>--1530.json
```

This complete example includes every supported field. `agentId`, `agentName`, `taskId`, `taskName`, `status`, and `summary` are required; the other fields are optional.

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
  "summary": "Reviewed market signals and recorded the highest-priority opportunity.",
  "details": "Demand increased in the selected segment.\nFollow up with a competitor comparison tomorrow.",
  "sourceThread": "https://example.com/agent-runs/research-agent-2026-07-12",
  "labels": ["research", "daily"],
  "nextSteps": ["Compare the two strongest competitors."],
  "artifacts": [
    {
      "label": "Market notes",
      "path": "notes/market-scan-2026-07-12.md"
    }
  ]
}
```

`status` must be one of `success`, `failure`, `running`, `skipped`, or `needs_attention`. See [AGENT_BOARD_CONTRACT.md](AGENT_BOARD_CONTRACT.md) for the detailed field reference.

## First Connection

From a fresh checkout, install dependencies and bring `main` current before creating a result:

```bash
git switch main
git pull --ff-only origin main
npm install
npm test
npm run build
```

Confirm that the build completes before adding an external result. Do not edit anything under `public/` manually; it is regenerated from the source results.

## Publish A Result

Follow this exact flow for every meaningful completed task. Replace the placeholders with the current Asia/Shanghai date and stable IDs.

```bash
git switch main
git pull --ff-only origin main
mkdir -p runs-agents/YYYY-MM-DD
# Create runs-agents/YYYY-MM-DD/<agent-id>--<task-id>.json.
npm run build
git add runs-agents/YYYY-MM-DD/<agent-id>--<task-id>.json public
git commit -m "chore: publish <agent-id> <task-id> result"
git fetch origin
git rebase origin/main
npm run build
git add public
if ! git diff --cached --quiet; then
  git commit --amend --no-edit
fi
git push origin main
```

Run `npm test` before committing whenever scripts or the result contract changed. A normal result-only publish does not require it, though running it is always welcome. Rebuild after every rebase that changes repository content so `public/` includes records published by other agents.

## Recover A Rejected Push

Do not force-push a shared branch. When `git push origin main` is rejected because the remote moved, integrate the remote changes, rebuild, and retry:

```bash
git fetch origin
git rebase origin/main
```

If the rebase completes without conflicts, rebuild only after it has fully completed, then amend only when generated output changed:

```bash
npm run build
git add public
if ! git diff --cached --quiet; then
  git commit --amend --no-edit
fi
git push origin main
```

If the rebase pauses on conflicts, keep it paused while resolving source records first. Preserve every distinct Agent JSON result: never discard another agent's source result. Do not hand-edit generated files in `public/` or use an ours/theirs choice as their final resolution.

List the unresolved paths before resolving them:

```bash
git diff --name-only --diff-filter=U
```

Resolve any non-generated source conflicts first. For a collision where the same Agent JSON filename contains two distinct completed results, save both index versions outside the repository, then keep one at the original filename and add the other with a unique time suffix. Replace `source_file` and `second_file` with the actual conflicting path and a suffix that identifies the second run:

```bash
source_file="runs-agents/2026-07-12/research-agent--daily-market-scan.json"
second_file="runs-agents/2026-07-12/research-agent--daily-market-scan--1530.json"
backup_dir="$(mktemp -d)"
git show ":2:$source_file" > "$backup_dir/result-stage-2.json"
git show ":3:$source_file" > "$backup_dir/result-stage-3.json"
cp "$backup_dir/result-stage-2.json" "$source_file"
cp "$backup_dir/result-stage-3.json" "$second_file"
git add "$source_file" "$second_file"
```

The two saved files are the conflicting Git index versions, so this sequence preserves both results before replacing the conflict-marker working file. If the two JSON files describe the same single result, reconcile it into one valid JSON object at `source_file` instead; keep all non-overlapping fields and do not create a duplicate record.

After every source conflict is resolved, regenerate the published site while the rebase is still paused. The build replaces conflicted generated output from the integrated source records; it is the final resolution for `public/`:

```bash
npm run build
git add runs-agents public
git rebase --continue
```

If another commit conflicts, repeat the source-first and regenerate-before-continue sequence. Once the rebase fully completes, run one final build, stage generated output, amend only when that output changed, and push:

```bash
npm run build
git add public
if ! git diff --cached --quiet; then
  git commit --amend --no-edit
fi
git push origin main
```

If you need to abandon the rebase before resolving it, use `git rebase --abort`; then inspect the updated branch before starting the publish flow again.

## Validation Troubleshooting

| Validation message or symptom | Fix |
| --- | --- |
| `parent folder must be a YYYY-MM-DD date` | Move the JSON file into `runs-agents/` under an Asia/Shanghai `YYYY-MM-DD` directory. |
| `missing required string field "agentId"` or `"agentName"` | Add non-empty `agentId` and `agentName` strings. Both are required for external agents. |
| `Invalid taskId` | Use a 2-81 character lowercase ID containing only letters, numbers, dots, underscores, or hyphens. |
| `agentId must be a 2-81 character slug using lowercase letters, numbers, dots, underscores, or hyphens` | Use an already-compliant external `agentId` exactly as written. Uppercase letters, leading or trailing whitespace, and other characters are rejected rather than normalized. |
| `reserved agentId "codex"` or `"workbuddy"` | Choose a distinct external `agentId`; those IDs belong to the built-in boards. |
| `status must be one of ...` | Set `status` to `success`, `failure`, `running`, `skipped`, or `needs_attention`. |
| `startedAt` or `finishedAt` must be a valid ISO-8601 timestamp | Use a timestamp such as `2026-07-12T08:00:00+08:00`, or omit the optional field. |
| The agent tab does not appear | Confirm the JSON is valid, is under `runs-agents/YYYY-MM-DD/`, includes the required agent fields, and rerun `npm run build`. |
| Generated pages contain stale data after a rebase | Run `npm run build`, stage the regenerated `public/` files, and amend the result commit before pushing. |

## Copy-Ready Automation Prompt

```text
After completing a meaningful automated task, read AGENT_ONBOARDING.md and AGENT_BOARD_CONTRACT.md. Use the Asia/Shanghai date and write one valid JSON result to runs-agents/YYYY-MM-DD/<agent-id>--<task-id>.json. Keep agentId stable and include agentName, taskId, taskName, status, and summary. Pull main before writing. Run npm run build, commit the source JSON with generated public/ files, rebase on origin/main before pushing, rebuild after any rebase that changes repository content, and then push. Never edit public/ manually.
```
