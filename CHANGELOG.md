# 更新记录 (CHANGELOG)

> 记录 lawerd-skills workspace 中 **非技术工具** 的全部变更。
> 技术工具（mineru-ocr / markitdown / docx / excel-xlsx / word-docx）不含在此记录中。
> 版本号跟随仓库 Git 提交时间线。

---

## 2026-06-19 — Memory 全量 ASCII 化

### memory — 修复
- **命名规则 bug 修复**：6 个中文子目录 → ASCII 目录
  - `归档助手/` → `archive/`
  - `新案件办理/` → `new-case/`
  - `案件云助手/` → `casecloud/`（随后删除）
  - `短信助手/` → `sms/`
  - `老案件跟进/` → `followup/`
  - `通用/` → `common/`
- **中文文件名修复**：`错误经验.md` → `errors.md`、`hooks参考.md` → `hooks.md`、`路由表.md` → `routing.md`、`错误处理总则.md` → `errors.md`
- **交叉引用更新**：14 个文件中所有中文路径引用已更换为 ASCII
- **全局 memory 修复**：`待升级.md` → `upgrade-queue.md`，同步 `skill-evolution.md` 引用
- **新增** `memory-naming-lessons.md`：记录 Memory 命名三条硬规则（纯ASCII / 平铺 / 同步引用）

### memory — 删除
- **案件云助手全部移除**：`casecloud/` 目录及 Reasonix workspace 中的 `case-management-casecloud-*.md`（4 个文件），`index.md` 路由表条目同步移除
- **Reasonix 案件管理 workspace 同步修复**：6 个 `case-management-*.md` 中 12 处过期中文文件引用已更正为扁平化引用

### scripts — 新增
- `update.sh`：macOS/Linux 一键更新脚本（clone → 注入个人配置 → 合并 → 清理）
- `update.ps1`：Windows PowerShell 一键更新脚本

---

## 2026-06-18 — v3.0 署名体系重构 + 内部文件清理

### memory — 重构
- **目录分离**：`memory/` 拆分为 `memory/global/`（跨项目共享）和 `memory/project/`（项目专属）
  - `global/`：du-lawyer-profile.md、lawerd-identity.md、tech-environment.md、skill-evolution.md、MEMORY.md
  - `project/case-management/`：案件管理经验库全部内容
- **新增 `memory/global/skill-evolution.md`**：软Hook信号驱动升级流程
- **新增 `memory/global/skill-evolution-references/`**：
  - `signal-rubric.md`：信号场景→决策映射
  - `term-dictionary.md`：术语词典
  - `lawerd-list.md`：升级清单模板
  - `upgrade-queue.md`（原`待升级.md`）：待融合升级项
- **新增 `memory/project/case-management/` 完整经验库**：
  - `index.md`：功能路由表（新案件办理 / 老案件跟进 / 短信助手 / 案件云助手 / 归档助手）
  - `common/`：路由表、Hooks 参考、错误处理总则
  - `new-case/`：5 步骤（预处理与分析 → 策略确认 → 起草文件 → 定稿交付 → 归档）+ 错误经验
  - `followup/`：3 步骤（加载历史 → 分析新材 → 起草归档）+ 错误经验
  - `sms/`：短信助手入口 + 错误经验
  - `archive/`：归档助手入口 + 错误经验
- **删除**：`memory/lawerd-work-principles.md`（8条原则已内化到 AI 系统提示词）
- **新增**：`{{WPS_ROOT}}` 占位符，修复多个文件中的硬编码路径残留

### scripts — 更新
- `apply-personalization.py`：新增 `USER_EMAIL`、`USER_PHONE`、`WPS_ROOT` 占位符支持
- `desensitize.py`：脱敏白名单扩展，中文模式补充
- `profile-wizard.py`：收集 `WPS_ROOT` 路径

### skills — 新增
- **contract-review-pro**：合同审查完整Skill（陈石律师贡献）
  - 七步审查工作流 + 智能评分 + 三观分析 + 条款提取 + DOCX生成
  - Python 脚本集：`contract_analyzer.py`、`risk_assessment.py`、`clause_extractor.py`、`docx_generator.py`、`intelligent_scoring.py`、`sanguan_analysis.py`、`revision_router.py` 等
  - 数据文件：审查清单、风险模板、条款标准、合同类型
- **skill-evolution**：软Hook信号驱动升级机制
- **practice-guide**：办案实操指南（调口卡、工商内档、申请流程等）

### skills — 重构
- **case-archive-orchestrator**：新增 step 分解（归类与改名 / 生成定卷文件），引用 local-scripts 模式
- **case-progress-archive**：更新触发条件，关联 case-study-report
- **draft-legal-docs**：拆分为 6 步骤（搜索知识库 → 确认文书类型 → 信息映射 → 生成初稿 → 定稿导出 → 知识沉淀），撤销委托逻辑
- **court-sms**：更新 workflow 引用路径
- **functionality-guide**：重写为纯路由，新增 architecture.md、mcp-tools.md、练习指引；移除 skill-dev-guide 引用
- **invoice-management**：新增 step-00-依赖检查、workflow-diagram.md、directory-structure.md
- **process-cases**：更新报告模板引用、规则与禁止项引用

### skills — 删除
- **skill-dev-guide**：完整移除（含 6 个 references、2 个 scripts）
- **scan-compliance**：完整移除（含 README、2 个 PowerShell 脚本）
- **workflow-orchestrator**：完整移除（含 7 个 references、CHANGELOG）
- **skill-ownership**：移除

### skills — 署名修正
- **contract-review-pro**：署名 → 陈石律师
- **markitdown**：署名 → Microsoft
- 全部 skill 文件的 `author`/`version`/`license` 移至文件末尾 `--` 签名区

---

## 2026-06-15 — 证据目录模板

### skills — 新增
- **draft-legal-docs** 新增功能：
  - `证据目录.template.xlsx` 模板
  - `fill_template_xlsx.py` 填充脚本
  - `fill_template.py` DOCX 文本替换脚本

### skills — 重构
- **draft-legal-docs 证据目录模板 v2 简化**：
  - 取消大/小类型纵向合并，统一单行 A+B 合并模式
  - 填充脚本去掉复杂分组逻辑，改为逐行填充
  - JSON 格式：证据分组 → 证据列表，每项一行

---

## 2026-06-12 — 初始版本

- lawerD v1.0 仓库初始化
- 基础技能骨架：case-archive-orchestrator、case-progress-archive、court-sms、draft-legal-docs、functionality-guide、invoice-management、legal-debate-simulation-mctmilk、legal-evidence-mapping-mctmilk、manage-legal-knowledge、mock-trial-review、practice-guide、process-cases
- 安装流程：lawerd-install.md、profile-wizard.py、apply-personalization.py、desensitize.py
