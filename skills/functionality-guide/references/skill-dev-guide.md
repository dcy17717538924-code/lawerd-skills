# skill-dev-guide

**功能**:Skill 开发规范查询 — 目录结构、SKILL.md 写作、CHANGELOG、渐进式加载、归档格式、协作规范

**触发词**:
- 写新 skill 之前想知道目录怎么搭
- SKILL.md frontmatter 怎么写
- CHANGELOG 格式
- references/ 子文件怎么组织
- Skill 归档格式

**适用场景**:
- {{ASSISTANT_NAME}}自有 skill 的开发规范参考
- agent 的 skill 库规范(律师助理 / 技术顾问)
- 协作开发新 skill

**不要用于**:
- 实际创建 Skill(走 `skill-creator`)
- Skill 安全审查(走 `skill-vetter`)
- 找技能(走 `find-skills`)
- 工程师综合入口(走 `codex-engineer` skill)

**完整说明**:见 `coder/skills/skill-dev-guide/SKILL.md` + 6 个 `references/*.md`

**架构说明**:
- 本 skill 位于 `~/.mavis/agents/coder/skills/skill-dev-guide/`
- 由 `coder` 技术顾问子 agent 拥有
