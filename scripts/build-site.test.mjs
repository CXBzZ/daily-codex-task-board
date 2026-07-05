import assert from "node:assert/strict";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { buildSite, collectRuns, dateInTimeZone, normalizeRun } from "./build-site.mjs";

test("dateInTimeZone returns the Asia/Shanghai calendar date", () => {
  const date = new Date("2026-07-04T18:00:00.000Z");
  assert.equal(dateInTimeZone(date, "Asia/Shanghai"), "2026-07-05");
});

test("normalizeRun validates and normalizes a result file", () => {
  const filePath = path.join(os.tmpdir(), "runs", "2026-07-05", "daily-review.json");
  const run = normalizeRun(
    {
      taskId: "daily-review",
      taskName: "Daily Review",
      status: "needs_attention",
      startedAt: "2026-07-05T08:00:00+08:00",
      finishedAt: "2026-07-05T08:01:30+08:00",
      summary: "Review needs follow-up.",
      details: "One item needs a decision.",
      labels: ["review"],
      nextSteps: ["Decide the owner."],
      artifacts: [{ label: "Notes", path: "notes.md" }]
    },
    filePath,
    path.join(os.tmpdir())
  );

  assert.equal(run.date, "2026-07-05");
  assert.equal(run.taskId, "daily-review");
  assert.equal(run.duration, "1m 30s");
  assert.deepEqual(run.labels, ["review"]);
  assert.equal(run.sourceFile, "runs/2026-07-05/daily-review.json");
});

test("collectRuns reads nested result JSON files in descending order", async () => {
  const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), "codex-runs-"));
  const runsDir = path.join(tempDir, "runs");

  await writeJson(path.join(runsDir, "2026-07-04", "older.json"), {
    taskId: "older-task",
    taskName: "Older Task",
    status: "success",
    summary: "Older result"
  });

  await writeJson(path.join(runsDir, "2026-07-05", "newer.json"), {
    taskId: "newer-task",
    taskName: "Newer Task",
    status: "success",
    summary: "Newer result"
  });

  const runs = await collectRuns(runsDir, tempDir);
  assert.equal(runs.length, 2);
  assert.equal(runs[0].taskId, "newer-task");
  assert.equal(runs[1].taskId, "older-task");
});

test("buildSite writes root, history, day, task, and data files", async () => {
  const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), "codex-site-"));
  const runsDir = path.join(tempDir, "runs");
  const outDir = path.join(tempDir, "public");

  await writeJson(path.join(runsDir, "2026-07-05", "example-task.json"), {
    taskId: "example-task",
    taskName: "Example Task",
    status: "success",
    startedAt: "2026-07-05T08:00:00+08:00",
    finishedAt: "2026-07-05T08:02:00+08:00",
    summary: "Example completed.",
    details: "Everything finished normally."
  });

  const result = await buildSite({
    runsDir,
    outDir,
    now: new Date("2026-07-05T02:00:00.000Z"),
    timeZone: "Asia/Shanghai"
  });

  assert.equal(result.runCount, 1);
  await assertFileContains(path.join(outDir, "index.html"), "Example Task");
  await assertFileContains(path.join(outDir, "history.html"), "2026-07-05");
  await assertFileContains(path.join(outDir, "days", "2026-07-05.html"), "Example completed.");
  await assertFileContains(path.join(outDir, "tasks", "example-task.html"), "historical result");
  await assertFileContains(path.join(outDir, "data", "runs.json"), "example-task");
});

async function writeJson(filePath, value) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}

async function assertFileContains(filePath, expected) {
  const content = await fs.readFile(filePath, "utf8");
  assert.match(content, new RegExp(expected.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")));
}

