---
name: functionality-guide
author: 杜重阳律师（微信Dcylawer8888）
version: "3.0.0"
license: MIT
description: |
  {{ASSISTANT_NAME}}全部技能的总目录与路由索引。当 AI 在现有技能列表中找不到合适的工具或技能完成任务时，读取本文件定位目标技能，再按 references/ 路由深入了解。
  2026-06-05 重构:OCR 方案整体退役,MarkItDown 落地,codex-engineer 合并至 coder 技术顾问,新主+2 子架构清晰。
  不要用于:具体案件内容、法律工作规范、用户背景信息。
---

## 功能概述

{{ASSISTANT_NAME}}技能黄页。AI 日常办案优先匹配各 Skill 的 description;当找不到合适技能时,翻本目录定位目标,按 references/ 深入了解后加载对应 SKILL.md。

**当前主+2 子架构**(2026-06-05):
- `mavis` 主 agent(Tier 1,{{ASSISTANT_NAME}}身份)
- `agent-lawyer-assistant` 律师助理子 agent(Tier 2,15 个法律 skill)
- `coder` 技术顾问子 agent(Tier 2,displayName=技术顾问,基于 software engineer 内核,7 个技术 skill)

## 调用方式

AGENTS.md Tier 1 兜底规则:AI 找不到现有可用技能或工具时,读取本文件。

---

## 路由表

### 法律工作引擎(律师助理)

| 技能 | 用途 | 详情 |
|------|------|------|
| [[workflow-orchestrator]] | 法律工作唯一入口,统一接收并路由 | [→](references/workflow-orchestrator.md) |

### 案件处理与文书(律师助理)

| 技能 | 用途 | 详情 |
|------|------|------|
| [[process-cases]] | 案件全流程处理(轻咨询+深度分析) | [→](references/process-cases.md) |
| [[draft-legal-docs]] | 起草法律文书(诉状/答辩状/代理词等) | [→](references/draft-legal-docs.md) |
| *contract-review-pro* | ⚠️ 独立安装 → [陈石律师 GitHub](https://github.com/CSlawyer1985/contract-review-pro) | [→](references/contract-review-pro.md) |
| [[word-docx]] | Word 文档创建/编辑/格式转换/定稿输出 | [→](references/word-docx.md) |
| [[docx]] | DOCX 脚本库(Track Changes/Comments/OOXML) | [→](references/docx.md) |

### 格式转换(律师助理)

| 技能 | 用途 | 详情 |
|------|------|------|
| **[[markitdown]]** | **Microsoft MarkItDown 桥接:PDF/Word/PPT/Excel/HTML/CSV/JSON/XML/EPUB/ZIP/YouTube/音频 → Markdown,本地处理无需 API** | [→](references/markitdown.md) |

### 庭审辅助(律师助理)

| 技能 | 用途 | 详情 |
|------|------|------|
| [[legal-debate-simulation-mctmilk]] | 庭前辩论模拟(对方律师视角五维攻击) | [→](references/legal-debate-simulation-mctmilk.md) |
| [[legal-evidence-mapping-mctmilk]] | 证据作战地图(要件→事实→证据对应) | [→](references/legal-evidence-mapping-mctmilk.md) |
| [[mock-trial-review]] | 模拟庭审审查(严苛裁判者极限施压) | [→](references/mock-trial-review.md) |

### 报告(律师助理)

| 技能 | 用途 | 详情 |
|------|------|------|
| [[case-study-report]] | 撰写专业案例分析报告(8章逐节出稿) | [→](references/case-study-report.md) |

### 知识沉淀与归档(律师助理)

| 技能 | 用途 | 详情 |
|------|------|------|
| [[manage-legal-knowledge]] | 专题知识整理(成体系的法律知识点归纳) | [→](references/manage-legal-knowledge.md) |
| [[case-progress-archive]] | 案件进度归档(跨会话档案管理) | [→](references/case-progress-archive.md) |
| [[archive-skill-update]] | Skill 更新归档(打包上传云盘+MANIFEST 日志) | [→](references/archive-skill-update.md) |

### 集成与通讯(律师助理)

| 技能 | 用途 | 详情 |
|------|------|------|
| [[court-sms]] | 法院短信识别与文书下载(电子送达处理) | [→](references/court-sms.md) |

### 技术工具(技术顾问子 agent `coder`)

| 技能 | 用途 | 详情 |
|------|------|------|
| [[codex-engineer]] | 工程师综合入口(Skill 增改适配/配置排查) | [→](references/codex-engineer.md) |
| [[find-skills]] | 技能发现(搜索和安装 Codex 技能) | [→](references/find-skills.md) |
| [[skill-vetter]] | 技能安全审查(安装前红标/权限检查) | [→](references/skill-vetter.md) |
| [[skill-creator]] | 技能创建工具(新建/更新 Skill 目录结构) | [→](references/skill-creator.md) |
| [[skill-dev-guide]] | Skill 开发规范(目录/frontmatter/CHANGELOG) | [→](references/skill-dev-guide.md) |
| [[scan-compliance]] | 合规扫描(批量检查 skill 4 项合规) | [→](references/scan-compliance.md) |

### 通用工具

| 工具 | 用途 | 详情 |
|------|------|------|
| [[invoice-management]] | 发票全生命周期：163邮箱下载→PDF解析→分类归档→凑票→费用报销单 | [→](references/invoice-management.md) |
| [[excel-xlsx]] | Excel 表格处理(读取/创建/编辑 xlsx,clawic 第三方) | [→](references/excel-xlsx.md) |
| **语音识别(whisper)** | `openai-whisper` + `medium.pt` 本地转写,无需联网 | [→](references/whisper-speech.md) |

### MCP 基础设施

| 工具 | 用途 | 详情 |
|------|------|------|
| [[markitdown]](主入口) | 见"格式转换"分类,MarkItDown 桥接 | [→](references/mcp-tools.md) |
| LLM 多模态 | Mavis 当前 LLM(MiniMax-M3)vision,扫描件/图片兜底 | [→](references/mcp-tools.md) |
| everything-search | Windows 文件秒搜(Everything 引擎) | [→](references/mcp-tools.md) |

### 已退役(2026-06-05 重构下线,留作历史)

| 旧技能 | 退役原因 | 替代 |
|------|------|------|
| ~~local-ocr~~ | 三级 OCR 引擎(百度/MinerU/Paddle)维护成本高,覆盖窄 | `markitdown` + LLM vision |
| ~~codex-engineer 子 agent~~ | 与 `coder` 子 agent 职责重叠 | 合并至 `coder` |
| ~~wechat-article-adapt~~ | 实际未使用,占用维护 | 暂不替代,有需要再独立做 |
| ~~practice-notes~~ | 实际未使用,占用维护 | 暂不替代,记录用 manage-legal-knowledge 即可 |
| ~~baidu-ocr / mineru-ocr MCP~~ | OCR 方案整体下线 | `markitdown` + LLM vision |

---

## Reasonix 单 Agent 架构

{{ASSISTANT_NAME}}律助Agent = 原 Mavis 主 agent（{{ASSISTANT_NAME}}身份+路由）+ 律师助理子 agent（法律执行），融合为单一 agent。技术顾问子 agent 不再保留。

| 组件 | 位置 | 职责 |
|------|------|------|
| 全局记忆（4条） | `~/.reasonix/memory/global/` | 身份/原则/用户档案/技术环境 |
| Skills（20个） | `~/.reasonix/skills/` | 法律案件全流程处理 + 通用工具 |

> 法律任务从 [[workflow-orchestrator]] 进入，该 skill 加载时带入完整工作规范。

---

## 变更历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| **v3.0.0** | **2026-06-05** | **重大重构:OCR 方案整体退役(baidu/MinerU/Paddle 三级→MarkItDown + LLM vision);codex-engineer 子 agent 合并至 coder 技术顾问;新增 markitdown skill(律师助理下);主+2 子架构清晰化;删 4 个过时 reference(local-ocr / codex-engineer-agent / wechat-article-adapt / practice-notes)+ 加 2 个(markitdown / skill-dev-guide)+ 重建 codex-engineer-skill;MCP 工具段重写;24 个 reference 净不变** |
| v2.0.0 | 2026-05-31 | 重大重构:263行→78行;改为按需加载兜底机制;24个技能独立 reference;新增 MCP 基础设施层 |
| v1.1.0 | 2026-05-31 | 新增 MCP 工具服务章节(baidu-ocr / mineru-ocr / everything-search),含选择策略与调用逻辑 |
| v1.0.0 | 2026-05-30 | 对齐 SKILL-DEV-GUIDE 书写规范,新增 Frontmatter,替换 workbuddy→codex |
