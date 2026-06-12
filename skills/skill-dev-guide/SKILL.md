---
name: skill-dev-guide
author: 杜重阳律师（微信Dcylawer8888）
version: "1.0.0"
license: MIT
description: |
  本技能提供{{ASSISTANT_NAME}}体系下 Skill 的开发规范——目录结构、SKILL.md 写作、CHANGELOG、渐进式加载、归档格式、协作规范。
  当用户(或子 agent)需要新建、修改、审阅{{ASSISTANT_NAME}}体系 Skill 时使用。
  不要用于：通用 skill 创建方法论(请用 skill-creator);具体业务 skill 的实现内容(请用对应业务 skill)。
---

# Skill 开发指南({{ASSISTANT_NAME}}体系)

## 功能概述

{{ASSISTANT_NAME}}体系下 Skill 的本地化规范手册,基于 Reasonix SKILL-DEV-GUIDE 改造。
讲清"{{ASSISTANT_NAME}}体系的 skill 必须长什么样、怎么维护、怎么发布"。

## 调用方式

**触发条件**:
- 用户说"新建一个 skill"、"改一个 skill"、"审一下这个 skill 符不符合规范"
- coder 技术顾问子 agent 在做 skill 增/改/适配时,需要先查本地规范
- 新 skill 走 `package_skill.py` 打包前的合规检查

**调用入口**:
- 主入口:本文件(SKILL.md)
- 详细规范:`references/` 下 6 个子文件,按需 Read

## 跟 skill-creator 的差异

| [[skill-creator]] | skill-dev-guide(本 skill) |
|---|---|
| 来源:Anthropic 官方 | 来源:{{ASSISTANT_NAME}}本地化({{USER_SHORT_NAME}}定制) |
| 讲"什么是 skill、怎么写" | 讲"{{ASSISTANT_NAME}}体系下 skill 必须遵守的本地规范" |
| 通用方法论 | 本地规范(目录、CHANGELOG、归档、协作) |
| 触发:用户想创建 skill | 触发:任何{{ASSISTANT_NAME}}体系 skill 的增/改/审 |
| 配套:有 init/package/validate 脚本 | 不带脚本,只规范行为 |

**互补使用**:新建 skill 时,先看 [[skill-creator]] 学会"怎么写",再看本 skill 学会"{{ASSISTANT_NAME}}体系下要怎么写才合规"。

## 目录结构(本 skill 自身示范)

```
skill-dev-guide/
├── SKILL.md              # 主入口(本文件)
├── CHANGELOG.md          # 变更记录
├── LICENSE.txt           # MIT
└── references/           # 详细规范
    ├── 01-directory-spec.md
    ├── 02-skillmd-spec.md
    ├── 03-changelog-spec.md
    ├── 04-progressive-load.md
    ├── 05-coordination-spec.md
    └── 06-archive-spec.md
```

**注意**:本 skill 用编号前缀(`01-` / `02-` ...)模拟"完全扁平",既符合{{ASSISTANT_NAME}}规范的"references/ 下无嵌套目录"精神(只对律师助理体系 skill 强制),又给工程师库下的本 skill 保留清晰组织。

## 工作流

按{{ASSISTANT_NAME}}规范创建/修改一个 skill 的标准流程:

1. **读规范** —— 触发本 skill,Read `references/02-skillmd-spec.md` 和 `references/01-directory-spec.md`
2. **设计** —— 决定 skill 名、frontmatter、目录、references/scripts
3. **写 SKILL.md** —— 按 §3 规范,YAML frontmatter 必填 `name` / `author` / `version` / `license` / `description`,description 含触发+负向条件
4. **加资源** —— `references/` 完全扁平(律师助理体系);`scripts/` 提供可执行代码
5. **写 CHANGELOG** —— 每次修改在 CHANGELOG.md 顶部新增记录,SEMVER 规则
6. **同步 CHANGELOG 到 agent** —— 若该 skill 属于某 agent,修改后**同步追加到该 agent 的 `CHANGELOG.md`**
7. **打包** —— 用 `package_skill.py` 校验+打 `.skill` 包(skill-creator 自带)
8. **归档** —— 需追溯的操作在 `archive/` 存 JSON 记录

## 与其他技能配合

- **上游**:[[workflow-orchestrator]]({{ASSISTANT_NAME}}体系)
- **同级**:[[skill-creator]](方法论),[[skill-vetter]](校验),[[archive-skill-update]](归档)
- **下游**:本 skill 产出的 skill,可能被任意业务 skill 引用

**协作模式**:
- 改 skill 流程:[[workflow-orchestrator]] → 本 skill(查规范) → [[skill-creator]](用方法论) → [[skill-vetter]](校验) → [[archive-skill-update]](归档)
- 完整流程见 `coder/skills/codex-engineer/SKILL.md` 的"Skill 维护路由"表

## 适用边界

本 skill 描述的规范**主要适用于{{ASSISTANT_NAME}}律师助理体系**(`~/.reasonix/skills/`),包括:

- ✅ "references/ 必须完全扁平,禁止子目录"
- ✅ "scripts/ / templates/ / archive/ 同样扁平"
- ✅ "author 固定为{{USER_FULL_NAME}}(微信 {{USER_WECHAT}})"

**不适用于**:
- ❌ Reasonix 全局 skill 需符合自身体系规范（如本 skill 自身）

## 修改权限：第三方 Skill vs 自有 Skill

| 类型 | 修改规则 | 示例 |
|---|---|---|
| **clawic 第三方 Skill**（从 clawic/skillsmp 安装） | **除了本地化适配外，任何内容都不动。** 包括 frontmatter、正文、references/、scripts/、CHANGELOG。本地化适配仅限：路径调整、中文 display name 映射、与{{ASSISTANT_NAME}}运行环境的兼容性修正。 | `markitdown`、`mineru-ocr`、`excel-xlsx`、`word-docx` |
| **Anthropic 官方 Skill**（Claude 官方发布） | 同 clawic 第三方：只做本地化适配，不动任何实质内容。 | `skill-creator` |
| **自有 Skill**（{{ASSISTANT_NAME}}体系自己开发的） | 随时可根据本规范（skill-dev-guide）进行调整和优化。 | `court-sms`、`workflow-orchestrator`、`draft-legal-docs` 等 |

**判定方法**（与 `scan-compliance` 脚本一致）：检查 SKILL.md frontmatter——

- 含 `slug:` / `homepage: https://clawic.com` / `clawhub` / `skillhub` / `ClawdHub` → **clawic 第三方**
- 含 `Claude` / `Anthropic` / `extends Claude` → **Anthropic 官方**
- 以上全无 → **自有 Skill**

## 配置

**外部依赖**:
- `skill-creator` 自带的 Python 脚本:`init_skill.py` / `package_skill.py` / `quick_validate.py`
- Python 解释器路径:`python`(不在系统 PATH 中需用完整路径,见 skill-creator SKILL.md)

## 变更历史

见 [CHANGELOG.md](./CHANGELOG.md)
