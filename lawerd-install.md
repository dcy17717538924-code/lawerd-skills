---
name: lawerd-install
version: "3.0.0"
license: MIT
description: |-
  {{ASSISTANT_NAME}}律师助理体系一键安装入口。clone GitHub 仓库 → 环境检查 → 个人信息配置 → 部署完成。
  不要用于：日常法律工作（安装完成后由 case-management-index 自动路由）。
---

# {{ASSISTANT_NAME}}律师助理 — 一键安装

> **v3.0 — 2026-06-18**：架构大升级。`workflow-orchestrator` 退役，改为 `case-management-index` project memory 自执行路由。渐进式披露（SKILL.md 能力签名 + steps/ 执行体）。经验演进引擎（skill-evolution）迁入全局记忆。

## 安装流程

安装者只需把本文件放入 `~/.reasonix/skills/`，然后对 AG 说："运行 lawerd-install"。AG 按以下 6 步自动执行：

### 第一步：获取安装包

```bash
git clone https://github.com/{{REPO_OWNER}}/lawerd-skills.git /tmp/lawerd-skills
```

> 如果 Git 不可用，手动下载 ZIP 解压到 `/tmp/lawerd-skills/`。

### 第二步：环境自检

根据当前操作系统，AG 自动选择对应脚本运行：

| 平台 | 脚本 |
|------|------|
| Windows | `powershell -File /tmp/lawerd-skills/scripts/env-check.ps1` |
| macOS / Linux | `bash /tmp/lawerd-skills/scripts/env-check.sh` |

自检项：Reasonix Code 已安装、Python 3 可用、Git 可用、`~/.reasonix/skills/` 目录存在。

脚本输出 ✅/❌ 表格。有 ❌ 的项目，按提示手动处理后重试。

### 第三步：个人信息配置

```bash
python3 /tmp/lawerd-skills/scripts/profile-wizard.py
```

交互式问答收集：律师全名、日常称呼、微信号、律所全称、所在城市、联系电话、电子邮箱、案件文件根目录、结案归档根目录、WPS云盘根目录。

填写完成后，自动生成 `~/.reasonix/skills/personalization.yaml`。

### 第四步：占位符替换

```bash
python3 /tmp/lawerd-skills/scripts/apply-personalization.py \
  --dict ~/.reasonix/skills/personalization.yaml \
  --skills /tmp/lawerd-skills/skills/ \
  --memory /tmp/lawerd-skills/memory/
```

此脚本读取 personalization.yaml，遍历所有 skill 和 memory 文件，将 `{{USER_FULL_NAME}}` 等占位符替换为用户实际值。**自动跳过**版权行（`author:`、`license:`、`Copyright`、`LICENSE` 文件）。

### 第五步：部署

```bash
# 合并 skills
cp -r /tmp/lawerd-skills/skills/* ~/.reasonix/skills/

# 合并全局记忆
cp -r /tmp/lawerd-skills/memory/global/* ~/.reasonix/memory/global/
```

> 项目记忆（`memory/project/`）不通过 `cp` 部署。安装完成后，AG 自动读取 `memory/project/` 下的文件并通过 `remember` 工具逐条写入项目级记忆。

### 第六步：验证

```bash
# 检查 skill 数量
ls ~/.reasonix/skills/ | wc -l
```

预期：所有 skill 就位。然后确认 `case-management-index` 已自动注入全局记忆。

## 完成

安装完成后，AG 输出：

```
✅ {{ASSISTANT_NAME}}律师助理体系安装完成

   已部署 20 个 skill
   已配置 4 个全局记忆文件 + project/case-management/ 经验文档树
   个人信息已注入

   现在起，所有法律工作通过 case-management-index（project memory）自动路由。
   AG 会自称"{{ASSISTANT_NAME}}"，以你的律师助理身份工作。
```

## 安装后清理

```bash
rm -rf /tmp/lawerd-skills/
```
