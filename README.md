# 杜律师自用的律师助理体系

一站式 AI 律师助理技能包。基于 Reasonix Code 运行，覆盖民商事诉讼全流程，由实务中提炼，经过长期打磨形成的稳定适用版。

## ⚠️ 版权声明

**本体系所有 skill 和 memory 文件的作者版权信息（`author` 字段、署名行、LICENSE 文件）不可修改。** 安装脚本会自动跳过版权相关行。MIT 许可证涵盖代码部分，版权署名归属原作者。

## 3 步上手

1. 把 `lawerd-install.md` 放入 `~/.reasonix/skills/`
2. 对 AG 说："运行 lawerd-install"
3. 按提示填写个人信息，AG 自动完成剩余步骤

## 技能清单

| Skill | 说明 |
|---|---|
| `workflow-orchestrator` | 统一路由入口，所有法律请求经此分发 |
| `process-cases` | 案件全流程处理：事实梳理 → 法律定性 → 分析输出 |
| `draft-legal-docs` | 起草法律文书：起诉状、答辩状、质证意见等 |
| `court-sms` | 法院 12368 短信处理：文书下载归档 + 待办创建 |
| `case-archive-orchestrator` | 结案纸质卷宗归档：归类入卷 → 案卷目录 → 办案小结 |
| `case-progress-archive` | 案件进度跨会话管理 |
| `legal-evidence-mapping-mctmilk` | 法条 → 证据清单映射，生成证据作战地图 |
| `legal-debate-simulation-mctmilk` | 庭前沙盘推演：对方攻击路径 → 防御策略 |
| `mock-trial-review` | 模拟庭审审查：法官视角压力测试 |
| `manage-legal-knowledge` | 专题法律知识管理 |
| `case-archive-orchestrator` | 纸质卷宗归档编排 |
| `functionality-guide` | 技能总目录与路由索引 |
| `skill-dev-guide` | Skill 开发规范手册 |
| `scan-compliance` |技能合规批量扫描|
| `markitdown` | 文档转 Markdown（PDF/Word/Excel/PPTX） |
| `mineru-ocr` | 中文扫描件/复杂版式 PDF OCR 识别 |
| `docx` | DOCX 文档处理脚本库 |
| `word-docx` | Word 文档创建与编辑 |
| `excel-xlsx` | Excel 工作表创建与编辑 |
| `invoice-management` | 发票管理：下载 → 归类 → 凑票组合 |

> ⚠️ **contract-review-pro**（合同审核）由陈石律师独立开发，需单独安装：
> `git clone https://github.com/CSlawyer1985/contract-review-pro.git`

## 目录结构

```
lawerd-skills/
├── lawerd-install.md          # 安装入口
├── skills/                     # 19 个技能（+ 1 个独立安装指引）
├── memory/                     # 预配置 memory 文件
│   ├── MEMORY.md
│   ├── du-lawyer-profile.md
│   ├── lawerd-identity.md
│   ├── lawerd-work-principles.md
│   ├── tech-environment.md
│   └── court-sms-lessons.md
├── scripts/
│   ├── env-check.sh            # macOS 环境自检
│   ├── env-check.ps1           # Windows 环境自检
│   ├── profile-wizard.py       # 个人信息交互式问答
│   └── apply-personalization.py # 占位符替换引擎
├── LICENSE                     # MIT（不可修改）
└── README.md                   # 本文件
```

## 许可证

MIT License — 详见 [LICENSE](./LICENSE)。
