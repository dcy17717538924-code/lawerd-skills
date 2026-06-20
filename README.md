# LawerD 律师助理体系

一站式 AI 律师助理技能包。基于 Reasonix Code 运行，覆盖民商事诉讼全流程，由实务中提炼，经过长期打磨形成的稳定适用版。

> **v3.0 — 2026-06-18 架构大升级**：渐进式披露（SKILL.md 能力签名 + steps/ 执行体）、项目记忆经验文档树（5 大功能链路编排 skill）、全局经验演进引擎（四类信号收集→阈值软Hook→升级项管理）。

## 3 步上手

1. 把 `lawerd-install.md` 放入 `~/.reasonix/skills/`
2. 对 AG 说："运行 lawerd-install"
3. 按提示填写个人信息，AG 自动完成剩余步骤

## 已安装用户更新

### Windows（PowerShell）

```powershell
iwr -Uri 'https://github.com/dcy17717538924-code/lawerd-skills/archive/refs/heads/master.zip' -OutFile "$env:TEMP\lawerd-skills.zip"
Expand-Archive "$env:TEMP\lawerd-skills.zip" -DestinationPath "$env:TEMP\lawerd-skills-update" -Force
$src = "$env:TEMP\lawerd-skills-update\lawerd-skills-master"
python "$src\scripts\apply-personalization.py" --dict "$env:USERPROFILE\.reasonix\skills\personalization.yaml" --skills "$src\skills\" --memory "$src\memory\global\"
Copy-Item -Recurse -Force "$src\skills\*" "$env:USERPROFILE\.reasonix\skills\"
Copy-Item -Recurse -Force "$src\memory\global\*" "$env:USERPROFILE\.reasonix\memory\global\"
Remove-Item -Recurse -Force "$env:TEMP\lawerd-skills.zip", "$env:TEMP\lawerd-skills-update"
```

### macOS / Linux（终端）

```bash
curl -L -o /tmp/lawerd-skills.tar.gz https://github.com/dcy17717538924-code/lawerd-skills/archive/refs/heads/master.tar.gz
tar -xzf /tmp/lawerd-skills.tar.gz -C /tmp/
python3 /tmp/lawerd-skills-master/scripts/apply-personalization.py --dict ~/.reasonix/skills/personalization.yaml --skills /tmp/lawerd-skills-master/skills/ --memory /tmp/lawerd-skills-master/memory/global/
cp -r /tmp/lawerd-skills-master/skills/* ~/.reasonix/skills/
cp -r /tmp/lawerd-skills-master/memory/global/* ~/.reasonix/memory/global/
rm -rf /tmp/lawerd-skills.tar.gz /tmp/lawerd-skills-master
```

> personalization.yaml 不会动，放心。

## 技能清单（20 + 1 stub）

### 入口

| Skill | 说明 |
|-------|------|
| `case-management-index` (project memory) | ⛔ 法律任务强制入口，自执行路由表，编排 5 大功能链路 |

### 案件处理与文书

| Skill | 说明 |
|-------|------|
| `process-cases` | 案件全流程处理：轻咨询 + 深度分析 |
| `draft-legal-docs` | 起草法律文书（6 步渐进式披露） |
| `case-progress-archive` | 案件进度跨会话管理 |

### 集成与通讯

| Skill | 说明 |
|-------|------|
| `court-sms` | 法院 12368 短信处理 |
| `law086` | 案件云操作（需单独 API Token） |

### 庭审辅助

| Skill | 说明 |
|-------|------|
| `legal-evidence-mapping-mctmilk` | 证据作战地图 |
| `legal-debate-simulation-mctmilk` | 庭前辩论模拟 |
| `mock-trial-review` | 模拟庭审审查 |

### 归档与知识

| Skill | 说明 |
|-------|------|
| `case-archive-orchestrator` | 纸质卷宗订卷归档 |
| `manage-legal-knowledge` | 专题法律知识管理 |

### 工具与格式

| Skill | 说明 |
|-------|------|
| `markitdown` | 文档转 Markdown |
| `mineru-ocr` | 中文扫描件/复杂版式 PDF OCR |
| `docx` | DOCX 文档处理脚本库 |
| `word-docx` | Word 文档创建与编辑 |
| `excel-xlsx` | Excel 工作表处理 |
| `invoice-management` | 发票管理：下载 → 归类 → 凑票 |

### 开发与规范

| Skill | 说明 |
|-------|------|
| `skill-evolution` | 经验演进引擎（信号收集 + 升级管理） |
| `functionality-guide` | 技能总目录与路由索引 |

> ⚠️ **contract-review-pro**（合同审核）由陈石律师独立开发，需单独安装。

## 目录结构

```
lawerd-skills/
├── lawerd-install.md           # 安装入口
├── skills/                     # 20 个技能（+ 1 stub）
├── memory/
│   ├── MEMORY.md               # 全局记忆索引
│   ├── du-lawyer-profile.md
│   ├── lawerd-identity.md
│   ├── tech-environment.md
│   ├── skill-evolution.md      # 经验演进引擎（auto-injected）
│   ├── skill-evolution-references/
│   └── project/
│       └── case-management/    # 5 大功能经验文档树
├── scripts/
│   ├── desensitize.py
│   ├── apply-personalization.py
│   ├── profile-wizard.py
│   ├── env-check.sh
│   └── env-check.ps1
├── LICENSE                     # MIT
└── README.md
```

## 许可证

MIT License — 详见 [LICENSE](./LICENSE)。
