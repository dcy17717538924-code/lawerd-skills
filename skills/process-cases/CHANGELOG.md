# Changelog

## [2.0.0] - 2026-06-02

### 新增

- Frontmatter 补齐 3 个必填字段:`author`({{USER_FULL_NAME}}) / `version`(SEMVER) / `license`(MIT)
- 4 个新章节按 SKILL-DEV-GUIDE §3.4 结构模板补全:功能概述 / 调用方式 / 与其他技能配合 / 配置
- 新增 LICENSE.txt(MIT)
- 新增 references/ 子目录(扁平),4 个子文件:
  - `01-simple-mode.md` —— 简易模式(场景 A 轻分析 + 场景 B 快审)
  - `02-deep-mode.md` —— 深度模式(6 阶段)
  - `03-report-template.md` —— 案件分析报告模板
  - `04-rules-and-prohibitions.md` —— 检索引用规则 + 禁止项 + 红线
- "调用方式"章节明确:本 skill **不**接受直接调用,必须经由 `workflow-orchestrator` 路由

### 修改

- SKILL.md 主入口从 158 行精简到约 60 行,详细内容按需 Read references
- "Mavis 本地化适配说明(2026-06-02)"段从 SKILL.md 末尾迁出(本 CHANGELOG v2.0.0 段即原适配说明内容)
- description 负向条件补充:"直接响应用户法律请求(必须经由 workflow-orchestrator 路由)"

### 迁移记录(原 SKILL.md L148-158 段)

- 本 skill 已从 `{{HOME_WIN}}\.Mavis\skills\` 迁移至 `~/.mavis/agents/lawyer-assistant/skills/`,适配 Mavis(MiniMax)体系
- 路径:全部从 `{{HOME_WIN}}\.Mavis\` 刷为 `~/.mavis/`
- 移除:双机协同 / WPS 云盘 / 符号链接相关内容(Mavis 单机,不需要)
- Frontmatter 移除 author / license / version 字段(后由 v2.0.0 规范化重新补回,符合 SKILL-DEV-GUIDE 规范)
- 路由入口:仍以 workflow-orchestrator 为法律工作唯一入口(详见 lawyer-assistant/agent.md)
- 核心流程未变,所有 references/ 子文件原 references 内容已拆出

## [1.1.0] - 2026-05-31
### 修改
- 整合 analyze-legal-issues：简易模式新增入口问询与双分支（场景A轻分析三步 / 场景B快审三轮）
- description 更新为覆盖两大场景

## [1.0.0] - 2026-05-31
### 新增
- 对齐 SKILL-DEV-GUIDE 书写规范，补全 Frontmatter（author/version/license/负向条件）
