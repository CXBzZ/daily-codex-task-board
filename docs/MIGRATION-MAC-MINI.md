# 迁移方案：把每日自动化迁到 Mac Mini

## 背景

WorkBuddy 的自动化存储在**本地** SQLite 数据库（`~/.workbuddy/workbuddy.db`），不会跨设备同步。迁移到 Mac Mini 需要在新机器上重建自动化。本方案把自动化配置和项目代码都做成可移植的，实现平滑迁移。

## 前置条件清单

在 Mac Mini 上需要准备：

| 依赖 | 要求 | 检查命令 |
|------|------|----------|
| Node.js | >= 20 | `node --version` |
| git | 任意版本 | `git --version` |
| GitHub 推送权限 | 对 `CXBzZ/daily-codex-task-board` 仓库有 write 权限 | 见下方「Git 推送权限」 |
| WorkBuddy | 已安装并登录 | 打开 WorkBuddy app |

## 迁移步骤

### 第 1 步：在 Mac Mini 上克隆项目

```bash
cd ~
mkdir -p workspace
cd workspace
git clone https://github.com/CXBzZ/daily-codex-task-board.git
cd daily-codex-task-board
```

### 第 2 步：验证构建

```bash
npm test
npm run build
```

两个命令都应该成功。如果报错，先解决依赖问题。

### 第 3 步：配置 Git 推送权限

自动化需要 push 到 GitHub。推荐用 SSH key 或 GitHub CLI：

**方案 A — SSH key（推荐长期使用）：**
```bash
# 在 Mac Mini 上生成 SSH key
ssh-keygen -t ed25519 -C "mac-mini"
# 把公钥添加到 GitHub: Settings → SSH and GPG keys
cat ~/.ssh/id_ed25519.pub
# 切换远程为 SSH
git remote set-url origin git@github.com:CXBzZ/daily-codex-task-board.git
# 验证
git fetch origin
```

**方案 B — GitHub CLI：**
```bash
brew install gh
gh auth login
# 验证
gh auth status
```

### 第 4 步：确认 Mac Mini 上的项目路径

```bash
# 在项目根目录运行
pwd
# 输出类似: /Users/<用户名>/workspace/daily-codex-task-board
```

记下这个路径，下一步要用。

### 第 5 步：在 Mac Mini 的 WorkBuddy 中重建自动化

打开 Mac Mini 上的 WorkBuddy，在对话中发送以下指令（把 `<你的路径>` 替换为第 4 步得到的路径）：

> 请根据 `docs/automation-niche-opc-industry.json` 创建一个每日自动化，工作目录改为 `<你的路径>`。

或者手动在 WorkBuddy 的自动化管理界面创建，填入以下配置：

| 字段 | 值 |
|------|-----|
| 名称 | 每日小众赚钱行业调研（OPC/数字游民） |
| 调度 | 每天 09:00 |
| 工作目录 | `<你的路径>` |
| 状态 | ACTIVE |

Prompt 内容见 `docs/automation-niche-opc-industry.json` 中的 `prompt` 字段（完整复制）。

### 第 6 步：验证自动化已创建

在 Mac Mini 的 WorkBuddy 中确认自动化出现在列表中，状态为 ACTIVE。

### 第 7 步：暂停旧机器上的自动化

回到当前 MacBook，暂停自动化避免重复执行：

> 在 WorkBuddy 中告诉助手：「暂停每日小众赚钱行业调研自动化」

或者让助手用 automation_update 工具将状态改为 PAUSED。

### 第 8 步：等待首次运行验证

等 Mac Mini 上的自动化首次执行（下一个 09:00）。检查：
- `runs-workbuddy/` 下是否出现了新的 JSON 文件
- GitHub 仓库是否有新的 commit
- 看板的 WorkBuddy tab 是否展示了新内容

## 回滚方案

如果 Mac Mini 上的自动化跑不起来：

1. 在当前 MacBook 上恢复自动化状态为 ACTIVE
2. 在 Mac Mini 上暂停或删除自动化
3. 排查 Mac Mini 上的问题（Node 版本、git 权限、路径等）

## 注意事项

- **`.workbuddy/` 目录不迁移**：这是本地工作数据（记忆、日志），已在 `.gitignore` 中排除，不会通过 git 同步
- **时区**：自动化使用 `BYHOUR=9`，即设备本地时间 09:00。确保 Mac Mini 的时区设置为 Asia/Shanghai
- **不重复运行**：迁移期间同一时间只有一台机器的自动化处于 ACTIVE 状态
- **配置文件已提交到仓库**：`docs/automation-niche-opc-industry.json` 已经在 git 中，Mac Mini clone 后直接可用
