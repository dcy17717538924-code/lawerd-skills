---
name: functionality-guide
description: |
  粽宝全部技能的总目录与路由索引。当 AI 在现有技能列表中找不到合适的工具或技能完成任务时，读取本文件定位目标技能。
  不要用于：具体案件内容、法律工作规范、用户背景信息。
---

# 技能黄页

粽宝技能总目录。AI 日常办案优先匹配各 Skill 的 description；当找不到合适技能时，翻本目录定位目标。

## 架构

架构见 `references/architecture.md`。

## 路由表

### 法律工作引擎

| 技能 | 用途 |
|------|------|
| `case-management-index`（project memory） | 法律任务强制入口，自执行路由 |

### 案件处理与文书

| 技能 | 用途 |
|------|------|
| [[skills/process-cases]] | 案件全流程处理（轻咨询+深度分析） |
| [[skills/draft-legal-docs]] | 起草法律文书（6 步渐进式披露） |
| [[skills/contract-review-pro]] | 合同审核（七步工作流） |
| [[skills/word-docx]] | Word 文档创建/编辑/格式转换 |
| [[skills/docx]] | DOCX 脚本库（Track Changes/Comments/OOXML） |

### 格式转换

| 技能 | 用途 |
|------|------|
| [[skills/markitdown]] | 文件格式转换（PDF/Office/HTML/CSV/JSON/EPUB → Markdown） |
| [[skills/mineru-ocr]] | 精准解析（扫描件/图片/复杂版式 PDF → Markdown） |

### 庭审辅助

| 技能 | 用途 |
|------|------|
| [[skills/legal-debate-simulation-mctmilk]] | 庭前辩论模拟（对方律师视角五维攻击） |
| [[skills/legal-evidence-mapping-mctmilk]] | 证据作战地图（要件→事实→证据对应） |
| [[skills/mock-trial-review]] | 模拟庭审审查（严苛裁判者极限施压） |

### 报告与归档

| 技能 | 用途 |
|------|------|
| [[skills/case-study-report]] | 撰写案例分析报告 |
| [[skills/case-progress-archive]] | 案件进度归档 |
| [[skills/case-archive-orchestrator]] | 纸质卷宗订卷归档 |
| [[skills/manage-legal-knowledge]] | 专题知识整理 |

### 集成与通讯

| 技能 | 用途 |
|------|------|
| [[skills/court-sms]] | 法院短信识别与文书下载 |
| [[skills/law086]] | 案件云操作（查询/更新/排期/客户） |

### 实务工具

| 技能 | 用途 |
|------|------|
| [[skills/practice-guide]] | 办案实操指南 |
| [[skills/invoice-management]] | 发票全生命周期管理 |
| [[skills/excel-xlsx]] | Excel 表格处理 |

### 开发与规范

| 技能 | 用途 |
|------|------|
| [[skills/skill-evolution]] | Skill 演进管理 + 用词词典 |

---

## 变更历史

见 [CHANGELOG.md](./CHANGELOG.md)

--
- 作者：杜重阳律师（微信Dcylawer8888）
- 版本：3.0.0
- 许可证：MIT
