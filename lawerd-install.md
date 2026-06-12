---
name: lawerd-install
author: 杜重阳律师（微信Dcylawer8888）
version: 1.0.0
license: MIT
description: |-
  {{ASSISTANT_NAME}}律师助理体系一键安装入口。clone GitHub 仓库 → 环境检查 → 个人信息配置 → 部署完成。
  不要用于：日常法律工作（安装完成后用 workflow-orchestrator）。
---

# {{ASSISTANT_NAME}}律师助理 — 一键安装

## ⚠️ 版权声明

本体系所有 skill 和 memory 文件的作者版权信息（`author` 字段、署名行、LICENSE 文件）**不可修改**。安装脚本自动跳过版权相关行，仅替换用户个性化占位符。

## 安装流程

安装者只需把本文件放入 `~/.reasonix/skills/`，然后对 AG 说："运行 lawerd-install"。AG 按以下 6 步自动执行：

### 第一步：获取安装包

```bash
# 克隆仓库到临时目录
git clone https://github.com/{{REPO_OWNER}}/lawerd-skills.git /tmp/lawerd-skills
```

> 如果 Git 不可用，手动下载 ZIP 解压到 `/tmp/lawerd-skills/`。

### 第二步：环境自检

根据当前操作系统，AG 自动选择对应脚本运行：

| 平台 | 脚本 |
|------|------|
| Windows | `powershell -File /tmp/lawerd-skills/scripts/env-check.ps1` |
| macOS / Linux | `bash /tmp/lawerd-skills/scripts/env-check.sh` |

自检项：

- Reasonix Code 已安装（`~/.reasonix/` 存在）
- Python 3 可用
- Git 可用
- `~/.reasonix/skills/` 目录存在

脚本输出 ✅/❌ 表格。有 ❌ 的项目，按提示手动处理后重试。

### 第三步：个人信息配置

```bash
python3 /tmp/lawerd-skills/scripts/profile-wizard.py
```

交互式问答收集：

- 律师全名、日常称呼、微信号
- 律所全称、所在城市
- 联系电话、电子邮箱
- 案件文件根目录、结案归档根目录

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

# 合并 memory
cp -r /tmp/lawerd-skills/memory/* ~/.reasonix/memory/global/
```

> macOS 用户注意：确保目标目录存在，不存在则先 `mkdir -p`。

### 第六步：验证

```bash
# 检查 skill 数量
ls ~/.reasonix/skills/ | wc -l

# 跑合规扫描
python3 ~/.reasonix/skills/scan-compliance/scripts/scan-compliance.ps1  # Windows
# 或手动触发 scan-compliance skill
```

预期输出：21 个 skill，全部合规。然后 AG 自己测试触发 `workflow-orchestrator`，确认路由正常。

## 完成

安装完成后，AG 输出：

```
✅ {{ASSISTANT_NAME}}律师助理体系安装完成

   已部署 21 个 skill
   已配置 6 个 memory 文件
   个人信息已注入

   现在起，所有法律工作通过 workflow-orchestrator 进入。
   AG 会自称"{{ASSISTANT_NAME}}"，以你的律师助理身份工作。
```

## 安装后清理

确认一切正常后：

```bash
rm -rf /tmp/lawerd-skills/
```

## 变更历史

见仓库 CHANGELOG.md。
