# Changelog

> 作者：杜重阳律师（微信Dcylawer8888）
> 许可证：MIT

## [3.0.0] - 2026-06-05

### 重大变更

- **OCR 方案整体退役**:baidu-ocr / MinerU / PaddleOCR 三级引擎下线,MarkItDown 一站式接管
- **codex-engineer 子 agent 合并至 coder**:技术顾问子 agent(`coder`,基于 software engineer 内核)统一承担原 codex-engineer 全部职责
- **新增 markitdown skill**:Microsoft 开源 MarkItDown 桥接,落地于 `agent-lawyer-assistant/skills/markitdown/`
- **主+2 子架构清晰化**:`mavis`(Tier 1 主 agent) + `agent-lawyer-assistant`(律师助理 Tier 2) + `coder`(技术顾问 Tier 2)

### 新增

- `references/markitdown.md` — MarkItDown 桥接说明
- `SKILL.md` 新章节"格式转换"、"主+2 子架构速查"、"已退役"表

### 修改

- `SKILL.md` 路由表重组:法律/案件/庭审/报告/知识/集成/技术/MCP 八分类,移除 4 个过时条目
- `references/mcp-tools.md` 重写:baidu-ocr / mineru-ocr 退役,新增 markitdown 主入口 + LLM vision 兜底
- `references/manage-legal-knowledge.md` 移除 `practice-notes` 引用
- `references/find-skills.md` 把"codex-engineer"改为"coder 技术顾问子 agent"
- 路由选择策略表更新为 MarkItDown + LLM vision 优先

### 删除

- `references/local-ocr.md` — OCR 路由 skill 已退役
- `references/codex-engineer.md` — 子 agent 合并至 coder
- `references/wechat-article-adapt.md` — 实际未使用
- `references/practice-notes.md` — 实际未使用
- Reference 总数:24 → 24(净变化 0;删 4 / 加 markitdown / 加 skill-dev-guide / 重建 codex-engineer)

## [2.0.0] - 2026-05-31

### 重大变更

- 重大重构:263 行 → 78 行
- 改为按需加载兜底机制
- 24 个技能独立 reference
- 新增 MCP 基础设施层

## [1.1.0] - 2026-05-31

### 新增

- MCP 工具服务章节(baidu-ocr / mineru-ocr / everything-search),含选择策略与调用逻辑

## [1.0.0] - 2026-05-30

### 新增

- 从 `config/` 平铺文件迁移为独立子目录,对齐 SKILL-DEV-GUIDE 目录规范
- 新增 CHANGELOG.md、LICENSE.txt
