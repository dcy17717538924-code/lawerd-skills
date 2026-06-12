# Changelog

## [2.0.0] - 2026-06-02

### 新增

- Frontmatter 补齐 3 个必填字段:`author`({{USER_FULL_NAME}}) / `version`(SEMVER) / `license`(MIT)
- LICENSE.txt 重新写入(MIT)
- SKILL.md 末尾"Mavis 本地化适配说明(2026-06-02)"段迁出(本 CHANGELOG 条目即原适配说明)
- "调用方式"章节强化:本 skill 是法律工作**唯一入口**,所有其他法律 skill 必经本 skill 路由

### 修改

- CHANGELOG.md 顶部"## [1.2.1]"段与下方"## [1.2.0]"段间的"## Changelog"重复标题清理
- 修复 v1.0.0 条目"SKILL.md 新增 Frontmatter"声明与实际不一致的问题(本版本补齐)

### 迁移记录(原 SKILL.md 末尾 Mavis 适配说明段)

- 路径:全部从 `{{HOME_WIN}}\.Mavis\` 刷为 `~/.mavis/`
- 移除:双机协同 / WPS 云盘 / 符号链接相关内容(Mavis 单机,不需要)
- Frontmatter 移除 author / license / version 字段(后由 v2.0.0 规范化重新补回,符合 SKILL-DEV-GUIDE 规范)
- 路由入口:仍以 workflow-orchestrator 为法律工作唯一入口(详见 lawyer-assistant/agent.md)
- 核心流程未变,所有 references/ 子文件原样保留

## [1.2.1] - 2026-05-31
### 修复
- 路由表 legal-debate-simulation / legal-evidence-mapping 补全 -mctmilk 后缀，修复路由名称不匹配

## [1.2.0] - 2026-05-31
### 修改
- 路由表：具体法条问题路由目标从 analyze-legal-issues 改为 process-cases
- 架构图移除 analyze-legal-issues 节点
- description 去除 analyze-legal-issues 引用

## [1.1.0] - 2026-05-30
### 新增
- OCR 预处理链路：references/ocr-strategy.md，定义百度 OCR / MinerU / PaddleOCR 三级策略与兜底逻辑
- 流程一新增步骤 0（OCR 预处理），步骤 2 补充策略分析五要素模板，步骤 3 补全文书类型清单，步骤 4 增加修改循环（≤3 轮）
- 流程二新增步骤 0（OCR 预处理），步骤 1 增加日志不存在兜底规则
- 路由表新增：意图不明→追问、证据梳理→legal-evidence-mapping

### 修改
- SKILL.md 流程详情拆至 references/flow-01-new-case.md、flow-02-existing-case.md
- 路由表各条目标注 OCR 预处理环节

## [1.0.0] - 2026-05-30
### 新增
- CHANGELOG.md、LICENSE.txt 补齐
- SKILL.md 新增 Frontmatter（author / version / license）、负向条件、功能概述、调用方式

### 修改
- description 改为第三人称 + 负向条件，对齐 SKILL-DEV-GUIDE
