# codex-engineer(skill,非 agent)

> **2026-06-05 重要变更**:原 `codex-engineer` **子 agent** 已合并至 `coder` 技术顾问子 agent。本 reference 描述的是 `coder/skills/codex-engineer/` 下的**同名 skill**(原工程师综合入口,作为 skill 保留)。

**功能**:工程师综合入口 — Skill 增改适配 / Mavis 配置排查 / 技术故障处理

**触发词**:
- Skill 创建/修改/删除/适配(不涉及 `skill-creator` / `skill-vetter` / `skill-dev-guide` 已能处理的子任务时)
- Mavis/CodeX 配置问题排查(agent.md 层级、路径、权限)
- 技术档案维护
- 单机技术方案

**适用场景**:
- 复杂 skill 适配(从 codex 体系迁到 Mavis 体系)
- Mavis daemon 故障排查
- agent.md / config.yaml 层级问题
- 跨 agent 路由配置

**不要用于**:
- 法律案件分析、文书起草(走 `process-cases` / `draft-legal-docs`)
- 案件进度管理(走 `case-progress-archive`)
- 找技能(走 `find-skills`)
- Skill 安全审查(走 `skill-vetter`)
- 批量合规扫描(走 `scan-compliance`)
- Skill 开发规范查询(走 `skill-dev-guide`)
- Skill 目录创建/打包(走 `skill-creator`)

**完整说明**:见 `coder/skills/codex-engineer/SKILL.md`

**架构说明**:
- 本 skill 位于 `~/.mavis/agents/coder/skills/codex-engineer/`
- 由 `coder` 技术顾问子 agent(原 codex-engineer 子 agent 合并)拥有
- Mavis 主 agent 路由"技术问题"到 `coder/agent.md`
