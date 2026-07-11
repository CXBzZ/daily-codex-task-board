import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");

export const DEFAULT_TIME_ZONE = "Asia/Shanghai";
export const RESERVED_AGENT_IDS = new Set(["codex", "workbuddy"]);

export const STATUS_META = {
  success: { label: "Success", className: "success" },
  failure: { label: "Failure", className: "failure" },
  running: { label: "Running", className: "running" },
  skipped: { label: "Skipped", className: "skipped" },
  needs_attention: { label: "Needs attention", className: "needs-attention" }
};

// Board configuration objects.
// Each board describes one source of automation results and controls
// how its pages are rendered and linked. Adding a new board only
// requires a new config + a results directory — the rendering pipeline
// is fully parameterized.
export const CODEX_BOARD = {
  key: "codex",
  agentName: "Codex",
  agentRole: "Codex automation agent",
  sourceLabel: "Codex",
  eyebrow: "Codex Automation Board",
  title: "Codex",
  lede: "A generated dashboard for Codex automations, daily runs, and historical outcomes.",
  dayDir: "days",
  taskDir: "tasks",
  indexFile: "index.html",
  historyFile: "history.html",
  dataFile: "runs.json",
  indexActive: "today",
  historyActive: "history",
  taskActive: "tasks",
  historyEyebrow: "History",
  historyTitle: "All recorded days",
  dayEyebrow: "Day",
  taskEyebrow: "Task",
  emptyMessage: "No Codex automation results have been reported for today yet.",
  historyEmptyMessage: "No history has been generated yet."
};

export const WORKBUDDY_BOARD = {
  key: "workbuddy",
  agentName: "WorkBuddy",
  agentRole: "WorkBuddy automation agent",
  sourceLabel: "WorkBuddy",
  eyebrow: "WorkBuddy Automation Board",
  title: "WorkBuddy",
  lede: "A generated dashboard for WorkBuddy automations, daily runs, and historical outcomes.",
  dayDir: "workbuddy-days",
  taskDir: "workbuddy-tasks",
  indexFile: "workbuddy.html",
  historyFile: "workbuddy-history.html",
  dataFile: "workbuddy-runs.json",
  indexActive: "workbuddy",
  historyActive: "workbuddy",
  taskActive: "workbuddy",
  historyEyebrow: "WorkBuddy History",
  historyTitle: "All recorded WorkBuddy days",
  dayEyebrow: "WorkBuddy Day",
  taskEyebrow: "WorkBuddy Task",
  emptyMessage: "No WorkBuddy automation results have been reported for today yet.",
  historyEmptyMessage: "No WorkBuddy history has been generated yet."
};

export const AGENTS_BOARD = {
  key: "agents",
  sourceLabel: "Personal Agent",
  eyebrow: "Multi-Agent Task Board",
  title: "Personal agent tasks",
  lede: "A shared dashboard for any personal assistant agent that reports structured task results.",
  dayDir: "agent-days",
  taskDir: "agent-tasks",
  indexFile: "agents.html",
  historyFile: "agent-history.html",
  dataFile: "agent-runs.json",
  indexActive: "agents",
  historyActive: "agents",
  taskActive: "agents",
  historyEyebrow: "Agent History",
  historyTitle: "All recorded agent days",
  dayEyebrow: "Agent Day",
  taskEyebrow: "Agent Task",
  emptyMessage: "No personal agent results have been reported for today yet.",
  historyEmptyMessage: "No personal agent history has been generated yet."
};

const TASK_ID_PATTERN = /^[a-z0-9][a-z0-9._-]{1,80}$/;
const DATE_PATTERN = /^\d{4}-\d{2}-\d{2}$/;

export function dateInTimeZone(date = new Date(), timeZone = DEFAULT_TIME_ZONE) {
  const parts = new Intl.DateTimeFormat("en", {
    timeZone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit"
  }).formatToParts(date);

  const byType = Object.fromEntries(parts.map((part) => [part.type, part.value]));
  return `${byType.year}-${byType.month}-${byType.day}`;
}

export function escapeHtml(value = "") {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

export function slugifyTaskId(taskId) {
  const slug = String(taskId || "").trim().toLowerCase();
  if (!TASK_ID_PATTERN.test(slug)) {
    throw new Error(
      `Invalid taskId "${taskId}". Use lowercase letters, numbers, dots, underscores, or hyphens.`
    );
  }
  return slug;
}

export function assertIsoTimestamp(value, fieldName, filePath) {
  if (value === undefined || value === null || value === "") {
    return null;
  }

  const timestamp = new Date(value);
  if (Number.isNaN(timestamp.getTime())) {
    throw new Error(`${filePath}: ${fieldName} must be a valid ISO-8601 timestamp.`);
  }

  return value;
}

export function normalizeRun(raw, filePath, rootDir = ROOT, options = {}) {
  const date = path.basename(path.dirname(filePath));
  if (!DATE_PATTERN.test(date)) {
    throw new Error(`${filePath}: parent folder must be a YYYY-MM-DD date.`);
  }

  for (const fieldName of ["taskId", "taskName", "status", "summary"]) {
    if (!raw[fieldName] || typeof raw[fieldName] !== "string") {
      throw new Error(`${filePath}: missing required string field "${fieldName}".`);
    }
  }

  const taskId = slugifyTaskId(raw.taskId);
  const status = raw.status.trim();
  if (!STATUS_META[status]) {
    throw new Error(
      `${filePath}: status must be one of ${Object.keys(STATUS_META).join(", ")}.`
    );
  }

  const labels = normalizeStringArray(raw.labels, "labels", filePath);
  const nextSteps = normalizeStringArray(raw.nextSteps, "nextSteps", filePath);
  const artifacts = normalizeArtifacts(raw.artifacts, filePath);
  const startedAt = assertIsoTimestamp(raw.startedAt, "startedAt", filePath);
  const finishedAt = assertIsoTimestamp(raw.finishedAt, "finishedAt", filePath);
  const agentId = normalizeAgentId(raw.agentId, filePath, options);
  const agentName = normalizeOptionalString(raw.agentName, "agentName", filePath);
  const agentRole = normalizeOptionalString(raw.agentRole, "agentRole", filePath);
  if (options.requireAgent && !agentName) {
    throw new Error(`${filePath}: missing required string field "agentName".`);
  }

  return {
    date,
    taskId,
    agentId,
    agentName,
    agentRole,
    taskName: raw.taskName.trim(),
    status,
    summary: raw.summary.trim(),
    details: typeof raw.details === "string" ? raw.details.trim() : "",
    startedAt,
    finishedAt,
    duration: formatDuration(startedAt, finishedAt),
    sourceThread: typeof raw.sourceThread === "string" ? raw.sourceThread.trim() : "",
    labels,
    nextSteps,
    artifacts,
    sourceFile: path.relative(rootDir, filePath).split(path.sep).join("/")
  };
}

function normalizeAgentId(value, filePath, options) {
  if (value === undefined || value === null || value === "") {
    if (options.requireAgent) {
      throw new Error(`${filePath}: missing required string field "agentId".`);
    }
    return "";
  }

  if (typeof value !== "string") {
    throw new Error(`${filePath}: agentId must be a string.`);
  }

  const agentId = slugifyTaskId(value);
  if (options.requireAgent && RESERVED_AGENT_IDS.has(agentId)) {
    throw new Error(filePath + ': reserved agentId "' + agentId + '" cannot be used in runs-agents.');
  }
  return agentId;
}

function normalizeOptionalString(value, fieldName, filePath) {
  if (value === undefined || value === null || value === "") {
    return "";
  }

  if (typeof value !== "string") {
    throw new Error(`${filePath}: ${fieldName} must be a string.`);
  }

  return value.trim();
}

function normalizeStringArray(value, fieldName, filePath) {
  if (value === undefined || value === null) {
    return [];
  }

  if (!Array.isArray(value) || value.some((item) => typeof item !== "string")) {
    throw new Error(`${filePath}: ${fieldName} must be an array of strings.`);
  }

  return value.map((item) => item.trim()).filter(Boolean);
}

function normalizeArtifacts(value, filePath) {
  if (value === undefined || value === null) {
    return [];
  }

  if (!Array.isArray(value)) {
    throw new Error(`${filePath}: artifacts must be an array.`);
  }

  return value.map((artifact, index) => {
    if (!artifact || typeof artifact !== "object") {
      throw new Error(`${filePath}: artifacts[${index}] must be an object.`);
    }

    if (typeof artifact.label !== "string" || typeof artifact.path !== "string") {
      throw new Error(`${filePath}: artifacts[${index}] requires string label and path.`);
    }

    return {
      label: artifact.label.trim(),
      path: artifact.path.trim()
    };
  });
}

function formatDuration(startedAt, finishedAt) {
  if (!startedAt || !finishedAt) {
    return "";
  }

  const start = new Date(startedAt).getTime();
  const finish = new Date(finishedAt).getTime();
  const seconds = Math.max(0, Math.round((finish - start) / 1000));

  if (seconds < 60) {
    return `${seconds}s`;
  }

  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  return remainingSeconds ? `${minutes}m ${remainingSeconds}s` : `${minutes}m`;
}

export async function collectRuns(runsDir = path.join(ROOT, "runs"), rootDir = ROOT, options = {}) {
  const files = await listJsonFiles(runsDir);
  const runs = [];

  for (const filePath of files) {
    const raw = JSON.parse(await fs.readFile(filePath, "utf8"));
    runs.push(normalizeRun(raw, filePath, rootDir, options));
  }

  return runs.sort(compareRunsDescending);
}

async function listJsonFiles(dir) {
  try {
    const entries = await fs.readdir(dir, { withFileTypes: true });
    const files = [];

    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        files.push(...(await listJsonFiles(fullPath)));
      } else if (entry.isFile() && entry.name.endsWith(".json")) {
        files.push(fullPath);
      }
    }

    return files;
  } catch (error) {
    if (error.code === "ENOENT") {
      return [];
    }
    throw error;
  }
}

function compareRunsDescending(a, b) {
  return (
    b.date.localeCompare(a.date) ||
    compareTimestampDescending(a.finishedAt || a.startedAt, b.finishedAt || b.startedAt) ||
    a.taskName.localeCompare(b.taskName)
  );
}

function compareTimestampDescending(a, b) {
  const left = a ? new Date(a).getTime() : 0;
  const right = b ? new Date(b).getTime() : 0;
  return right - left;
}

export async function buildSite({
  runsDir = path.join(ROOT, "runs"),
  workbuddyRunsDir,
  agentsRunsDir,
  outDir = path.join(ROOT, "public"),
  now = new Date(),
  timeZone = DEFAULT_TIME_ZONE
} = {}) {
  const rootDir = path.resolve(runsDir, "..");
  const workbuddyDir = workbuddyRunsDir || path.join(rootDir, "runs-workbuddy");
  const agentsDir = agentsRunsDir || path.join(rootDir, "runs-agents");

  const codexRuns = await collectRuns(runsDir, rootDir);
  const workbuddyRuns = await collectRuns(workbuddyDir, rootDir);
  const agentRuns = await collectRuns(agentsDir, rootDir, { requireAgent: true });

  const today = dateInTimeZone(now, timeZone);
  const generatedAt = now.toISOString();

  const codexByDay = groupBy(codexRuns, (run) => run.date);
  const codexByTask = groupBy(codexRuns, (run) => run.taskId);
  const workbuddyByDay = groupBy(workbuddyRuns, (run) => run.date);
  const workbuddyByTask = groupBy(workbuddyRuns, (run) => run.taskId);
  const agentsByDay = groupBy(agentRuns, (run) => run.date);
  const agentsByTask = groupBy(agentRuns, (run) => run.taskId);

  await fs.rm(outDir, { recursive: true, force: true });
  await fs.mkdir(path.join(outDir, "assets"), { recursive: true });
  await fs.mkdir(path.join(outDir, "data"), { recursive: true });

  await fs.writeFile(path.join(outDir, "assets", "styles.css"), stylesheet(), "utf8");

  await fs.writeFile(
    path.join(outDir, "data", CODEX_BOARD.dataFile),
    `${JSON.stringify({ generatedAt, timeZone, runs: codexRuns }, null, 2)}${os.EOL}`,
    "utf8"
  );
  await fs.writeFile(
    path.join(outDir, "data", WORKBUDDY_BOARD.dataFile),
    `${JSON.stringify({ generatedAt, timeZone, runs: workbuddyRuns }, null, 2)}${os.EOL}`,
    "utf8"
  );
  await fs.writeFile(
    path.join(outDir, "data", AGENTS_BOARD.dataFile),
    `${JSON.stringify({ generatedAt, timeZone, runs: agentRuns }, null, 2)}${os.EOL}`,
    "utf8"
  );

  await renderBoardPages({
    runs: codexRuns,
    groupedByDay: codexByDay,
    groupedByTask: codexByTask,
    board: CODEX_BOARD,
    outDir,
    today,
    generatedAt,
    timeZone
  });

  await renderBoardPages({
    runs: workbuddyRuns,
    groupedByDay: workbuddyByDay,
    groupedByTask: workbuddyByTask,
    board: WORKBUDDY_BOARD,
    outDir,
    today,
    generatedAt,
    timeZone
  });

  await renderBoardPages({
    runs: agentRuns,
    groupedByDay: agentsByDay,
    groupedByTask: agentsByTask,
    board: AGENTS_BOARD,
    outDir,
    today,
    generatedAt,
    timeZone
  });

  return {
    generatedAt,
    runCount: codexRuns.length,
    dayCount: codexByDay.size,
    taskCount: codexByTask.size,
    workbuddyRunCount: workbuddyRuns.length,
    workbuddyDayCount: workbuddyByDay.size,
    workbuddyTaskCount: workbuddyByTask.size,
    agentRunCount: agentRuns.length,
    agentDayCount: agentsByDay.size,
    agentTaskCount: agentsByTask.size
  };
}

async function renderBoardPages({ runs, groupedByDay, groupedByTask, board, outDir, today, generatedAt, timeZone }) {
  await fs.mkdir(path.join(outDir, board.dayDir), { recursive: true });
  await fs.mkdir(path.join(outDir, board.taskDir), { recursive: true });

  await fs.writeFile(
    path.join(outDir, board.indexFile),
    renderIndex({ runs, groupedByDay, today, generatedAt, timeZone, board }),
    "utf8"
  );
  await fs.writeFile(
    path.join(outDir, board.historyFile),
    renderHistory({ groupedByDay, generatedAt, timeZone, board }),
    "utf8"
  );

  for (const [date, dayRuns] of groupedByDay) {
    await fs.writeFile(
      path.join(outDir, board.dayDir, `${date}.html`),
      renderDay({ date, runs: dayRuns, generatedAt, timeZone, board }),
      "utf8"
    );
  }

  for (const [taskId, taskRuns] of groupedByTask) {
    await fs.writeFile(
      path.join(outDir, board.taskDir, `${taskId}.html`),
      renderTask({ taskId, runs: taskRuns, generatedAt, timeZone, board }),
      "utf8"
    );
  }
}

function groupBy(items, getKey) {
  const groups = new Map();

  for (const item of items) {
    const key = getKey(item);
    if (!groups.has(key)) {
      groups.set(key, []);
    }
    groups.get(key).push(item);
  }

  return groups;
}

export function createDiscoveredAgentBoards(runs) {
  return [...groupBy(runs, (run) => run.agentId).entries()]
    .map(([agentId, agentRuns]) => {
      const latest = agentRuns[0];
      const agentName = latest.agentName;
      const agentRole = latest.agentRole || "Personal assistant agent";
      const prefix = "agents/" + agentId;

      return {
        board: {
          key: agentId,
          agentName,
          agentRole,
          sourceLabel: agentName,
          eyebrow: "Personal Agent",
          title: agentName,
          lede: latest.agentRole || "Daily automation results and historical outcomes.",
          dayDir: prefix + "/days",
          taskDir: prefix + "/tasks",
          indexFile: prefix + "/index.html",
          historyFile: null,
          dataFile: "agents/" + agentId + ".json",
          historyEyebrow: agentName + " History",
          historyTitle: "All recorded " + agentName + " days",
          dayEyebrow: agentName + " Day",
          taskEyebrow: agentName + " Task",
          emptyMessage: "No " + agentName + " automation results have been reported for today yet.",
          historyEmptyMessage: "No " + agentName + " history has been generated yet."
        },
        runs: agentRuns
      };
    })
    .sort((left, right) => left.board.agentName.localeCompare(right.board.agentName));
}

function renderIndex({ runs, groupedByDay, today, generatedAt, timeZone, board }) {
  const todayRuns = groupedByDay.get(today) || [];
  const latestDate = groupedByDay.keys().next().value;
  const latestRuns = latestDate ? groupedByDay.get(latestDate) : [];

  const body = `
    <section class="hero">
      <div>
        <p class="eyebrow">${escapeHtml(board.eyebrow)}</p>
        <h1>${escapeHtml(board.title)}</h1>
        <p class="lede">${escapeHtml(board.lede)}</p>
      </div>
      <dl class="stats">
        <div><dt>Total runs</dt><dd>${runs.length}</dd></div>
        <div><dt>Tracked days</dt><dd>${groupedByDay.size}</dd></div>
        <div><dt>Today</dt><dd>${todayRuns.length}</dd></div>
      </dl>
    </section>

    <section class="section">
      <div class="section-heading">
        <div>
          <p class="eyebrow">Today</p>
          <h2>${today}</h2>
        </div>
        ${todayRuns.length ? `<a class="text-link" href="${board.dayDir}/${today}.html">Open day</a>` : ""}
      </div>
      ${todayRuns.length ? renderRunGrid(todayRuns, "", board) : renderEmptyState(board.emptyMessage)}
    </section>

    ${
      latestDate && latestDate !== today
        ? `<section class="section">
            <div class="section-heading">
              <div>
                <p class="eyebrow">Latest recorded day</p>
                <h2>${latestDate}</h2>
              </div>
              <a class="text-link" href="${board.dayDir}/${latestDate}.html">Open day</a>
            </div>
            ${renderRunGrid(latestRuns, "", board)}
          </section>`
        : ""
    }
  `;

  return layout({ title: board.title, active: board.indexActive, body, generatedAt, timeZone, base: "" });
}

function renderHistory({ groupedByDay, generatedAt, timeZone, board }) {
  const rows = [...groupedByDay.entries()]
    .map(([date, runs]) => {
      const counts = countByStatus(runs);
      return `
        <a class="history-row" href="${board.dayDir}/${date}.html">
          <span class="history-date">${date}</span>
          <span class="history-summary">${runs.length} run${runs.length === 1 ? "" : "s"}</span>
          <span class="status-strip">${renderStatusPills(counts)}</span>
        </a>
      `;
    })
    .join("");

  const body = `
    <section class="page-title">
      <p class="eyebrow">${escapeHtml(board.historyEyebrow)}</p>
      <h1>${escapeHtml(board.historyTitle)}</h1>
    </section>
    <section class="history-list">
      ${rows || renderEmptyState(board.historyEmptyMessage)}
    </section>
  `;

  return layout({ title: board.historyTitle, active: board.historyActive, body, generatedAt, timeZone, base: "" });
}

function renderDay({ date, runs, generatedAt, timeZone, board }) {
  const body = `
    <section class="page-title">
      <p class="eyebrow">${escapeHtml(board.dayEyebrow)}</p>
      <h1>${date}</h1>
      <p class="lede">${runs.length} ${escapeHtml(board.sourceLabel)} automation result${runs.length === 1 ? "" : "s"} recorded.</p>
    </section>
    ${renderRunGrid(runs, "../", board)}
  `;

  return layout({ title: date, active: board.historyActive, body, generatedAt, timeZone, base: "../" });
}

function renderTask({ taskId, runs, generatedAt, timeZone, board }) {
  const taskName = runs[0]?.taskName || taskId;
  const body = `
    <section class="page-title">
      <p class="eyebrow">${escapeHtml(board.taskEyebrow)}</p>
      <h1>${escapeHtml(taskName)}</h1>
      <p class="lede">${runs.length} historical result${runs.length === 1 ? "" : "s"} for <code>${escapeHtml(taskId)}</code>.</p>
    </section>
    ${renderRunGrid(runs, "../", board)}
  `;

  return layout({ title: taskName, active: board.taskActive, body, generatedAt, timeZone, base: "../" });
}

function layout({ title, active, body, generatedAt, timeZone, base }) {
  return `<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>${escapeHtml(title)} · Daily Codex Task Board</title>
    <link rel="stylesheet" href="${base}assets/styles.css">
  </head>
  <body>
    <header class="site-header">
      <a class="brand" href="${base}index.html">Daily Codex Task Board</a>
      <nav aria-label="Primary">
        <a ${active === "today" ? 'aria-current="page"' : ""} href="${base}index.html">Today</a>
        <a ${active === "history" ? 'aria-current="page"' : ""} href="${base}history.html">History</a>
        <a ${active === "workbuddy" ? 'aria-current="page"' : ""} href="${base}workbuddy.html">WorkBuddy</a>
        <a ${active === "agents" ? 'aria-current="page"' : ""} href="${base}agents.html">Agents</a>
      </nav>
    </header>
    <main>
      ${body}
    </main>
    <footer class="site-footer">
      <span>Generated ${escapeHtml(formatTimestamp(generatedAt, timeZone))}</span>
      <span>Source of truth: <code>runs/</code> · <code>runs-workbuddy/</code> · <code>runs-agents/</code></span>
    </footer>
  </body>
</html>
`;
}

function renderRunGrid(runs, base, board) {
  return `<div class="run-grid">${runs.map((run) => renderRunCard(run, base, board)).join("")}</div>`;
}

function renderRunCard(run, base, board) {
  const status = STATUS_META[run.status];
  const details = run.details ? `<div class="details">${escapeHtml(run.details)}</div>` : "";
  const labels = run.labels.length
    ? `<div class="labels">${run.labels.map((label) => `<span>${escapeHtml(label)}</span>`).join("")}</div>`
    : "";
  const nextSteps = run.nextSteps.length
    ? `<div class="subsection"><h3>Next steps</h3><ul>${run.nextSteps.map((step) => `<li>${escapeHtml(step)}</li>`).join("")}</ul></div>`
    : "";
  const artifacts = run.artifacts.length
    ? `<div class="subsection"><h3>Artifacts</h3><ul>${run.artifacts.map((artifact) => renderArtifact(artifact)).join("")}</ul></div>`
    : "";
  const sourceThread = run.sourceThread
    ? `<p class="meta-line"><span>Source</span>${escapeHtml(run.sourceThread)}</p>`
    : "";
  const agent = run.agentName || run.agentId
    ? `<p class="meta-line"><span>Agent</span>${escapeHtml(run.agentName || run.agentId)}${run.agentRole ? ` · ${escapeHtml(run.agentRole)}` : ""}</p>`
    : "";

  return `
    <article class="run-card">
      <div class="run-card-header">
        <div>
          <a class="task-link" href="${base}${board.taskDir}/${run.taskId}.html">${escapeHtml(run.taskName)}</a>
          <p class="meta-line"><span>Date</span><a href="${base}${board.dayDir}/${run.date}.html">${run.date}</a></p>
        </div>
        <span class="status ${status.className}">${status.label}</span>
      </div>
      <p class="summary">${escapeHtml(run.summary)}</p>
      ${details}
      <div class="run-meta">
        ${agent}
        ${run.startedAt ? `<p class="meta-line"><span>Started</span>${escapeHtml(formatTimestamp(run.startedAt))}</p>` : ""}
        ${run.finishedAt ? `<p class="meta-line"><span>Finished</span>${escapeHtml(formatTimestamp(run.finishedAt))}</p>` : ""}
        ${run.duration ? `<p class="meta-line"><span>Duration</span>${escapeHtml(run.duration)}</p>` : ""}
        ${sourceThread}
        <p class="meta-line"><span>File</span><code>${escapeHtml(run.sourceFile)}</code></p>
      </div>
      ${labels}
      ${nextSteps}
      ${artifacts}
    </article>
  `;
}

function renderArtifact(artifact) {
  const isUrl = /^https?:\/\//.test(artifact.path);
  const label = escapeHtml(artifact.label);
  const target = escapeHtml(artifact.path);
  return isUrl
    ? `<li><a href="${target}">${label}</a></li>`
    : `<li><code>${target}</code> ${label}</li>`;
}

function renderStatusPills(counts) {
  return Object.entries(STATUS_META)
    .filter(([status]) => counts[status])
    .map(([status, meta]) => `<span class="status ${meta.className}">${meta.label}: ${counts[status]}</span>`)
    .join("");
}

function countByStatus(runs) {
  return runs.reduce((counts, run) => {
    counts[run.status] = (counts[run.status] || 0) + 1;
    return counts;
  }, {});
}

function renderEmptyState(message) {
  return `<div class="empty-state">${escapeHtml(message)}</div>`;
}

function formatTimestamp(value, timeZone = DEFAULT_TIME_ZONE) {
  if (!value) {
    return "";
  }

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return new Intl.DateTimeFormat("en-GB", {
    timeZone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false
  }).format(date);
}

function stylesheet() {
  return `:root {
  color-scheme: light;
  --bg: #f7f7f4;
  --panel: #ffffff;
  --text: #1f2528;
  --muted: #667178;
  --line: #dfe3dd;
  --accent: #216869;
  --accent-strong: #164b4c;
  --success: #1b7f4d;
  --failure: #b42318;
  --running: #7a4b00;
  --skipped: #59636b;
  --attention: #9a3412;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
}

a {
  color: inherit;
}

code {
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
  font-size: 0.92em;
}

.site-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 20px clamp(20px, 5vw, 56px);
  border-bottom: 1px solid var(--line);
  background: rgba(255, 255, 255, 0.82);
  position: sticky;
  top: 0;
  z-index: 5;
  backdrop-filter: blur(12px);
}

.brand {
  font-weight: 750;
  text-decoration: none;
}

nav {
  display: flex;
  gap: 8px;
}

nav a {
  border-radius: 6px;
  color: var(--muted);
  padding: 8px 10px;
  text-decoration: none;
}

nav a[aria-current="page"] {
  background: #e5eeee;
  color: var(--accent-strong);
}

main {
  width: min(1180px, calc(100vw - 40px));
  margin: 0 auto;
  padding: 36px 0 56px;
}

.hero {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(280px, 420px);
  gap: 32px;
  align-items: end;
  padding: 32px 0 36px;
}

.eyebrow {
  color: var(--accent);
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0;
  margin: 0 0 8px;
  text-transform: uppercase;
}

h1,
h2,
h3,
p {
  overflow-wrap: anywhere;
}

h1 {
  font-size: clamp(2.4rem, 6vw, 5rem);
  line-height: 0.95;
  margin: 0;
}

h2 {
  font-size: 1.8rem;
  margin: 0;
}

h3 {
  font-size: 0.95rem;
  margin: 0 0 8px;
}

.lede {
  color: var(--muted);
  font-size: 1.08rem;
  line-height: 1.7;
  max-width: 680px;
}

.stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1px;
  margin: 0;
  overflow: hidden;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--line);
}

.stats div {
  background: var(--panel);
  padding: 18px;
}

.stats dt {
  color: var(--muted);
  font-size: 0.78rem;
}

.stats dd {
  font-size: 2rem;
  font-weight: 800;
  margin: 4px 0 0;
}

.section,
.page-title {
  margin-top: 34px;
}

.section-heading {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 18px;
  margin-bottom: 16px;
}

.text-link {
  color: var(--accent-strong);
  font-weight: 700;
  text-decoration: none;
}

.run-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 340px), 1fr));
  gap: 16px;
}

.run-card {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 18px;
}

.run-card-header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
}

.task-link {
  font-size: 1.08rem;
  font-weight: 800;
  text-decoration: none;
}

.status {
  align-self: flex-start;
  border: 1px solid currentColor;
  border-radius: 999px;
  display: inline-flex;
  font-size: 0.76rem;
  font-weight: 800;
  line-height: 1;
  padding: 6px 8px;
  white-space: nowrap;
}

.status.success {
  color: var(--success);
}

.status.failure {
  color: var(--failure);
}

.status.running {
  color: var(--running);
}

.status.skipped {
  color: var(--skipped);
}

.status.needs-attention {
  color: var(--attention);
}

.summary {
  font-size: 1rem;
  line-height: 1.6;
  margin: 16px 0;
}

.details {
  background: #f3f6f4;
  border-radius: 6px;
  color: #374146;
  line-height: 1.6;
  padding: 12px;
  white-space: pre-wrap;
}

.run-meta {
  border-top: 1px solid var(--line);
  display: grid;
  gap: 6px;
  margin-top: 16px;
  padding-top: 14px;
}

.meta-line {
  color: var(--muted);
  font-size: 0.88rem;
  margin: 0;
}

.meta-line span {
  color: var(--text);
  display: inline-block;
  font-weight: 750;
  min-width: 74px;
}

.labels {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 14px;
}

.labels span {
  background: #eef0ec;
  border-radius: 999px;
  color: #4b565c;
  font-size: 0.78rem;
  padding: 5px 8px;
}

.subsection {
  margin-top: 16px;
}

.subsection ul {
  margin: 0;
  padding-left: 20px;
}

.subsection li {
  line-height: 1.6;
}

.history-list {
  display: grid;
  gap: 10px;
  margin-top: 24px;
}

.history-row {
  align-items: center;
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 8px;
  display: grid;
  gap: 12px;
  grid-template-columns: minmax(130px, 180px) minmax(120px, 1fr) minmax(0, 2fr);
  padding: 14px 16px;
  text-decoration: none;
}

.history-date {
  font-weight: 800;
}

.history-summary {
  color: var(--muted);
}

.status-strip {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  justify-content: flex-end;
}

.empty-state {
  background: var(--panel);
  border: 1px dashed var(--line);
  border-radius: 8px;
  color: var(--muted);
  padding: 24px;
}

.site-footer {
  border-top: 1px solid var(--line);
  color: var(--muted);
  display: flex;
  flex-wrap: wrap;
  gap: 12px 24px;
  justify-content: space-between;
  padding: 20px clamp(20px, 5vw, 56px);
}

@media (max-width: 760px) {
  .site-header,
  .hero,
  .section-heading,
  .run-card-header,
  .site-footer {
    align-items: flex-start;
    flex-direction: column;
  }

  .hero {
    display: flex;
  }

  .stats {
    width: 100%;
  }

  .history-row {
    grid-template-columns: 1fr;
  }

  .status-strip {
    justify-content: flex-start;
  }
}
`;
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  buildSite()
    .then((result) => {
      console.log(
        `Generated ${result.runCount} Codex runs across ${result.dayCount} days and ${result.taskCount} tasks, ${result.workbuddyRunCount} WorkBuddy runs across ${result.workbuddyDayCount} days and ${result.workbuddyTaskCount} tasks, ${result.agentRunCount} shared agent runs across ${result.agentDayCount} days and ${result.agentTaskCount} tasks.`
      );
    })
    .catch((error) => {
      console.error(error.message);
      process.exitCode = 1;
    });
}
