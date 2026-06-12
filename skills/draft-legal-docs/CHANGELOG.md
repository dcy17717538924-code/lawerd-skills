# Changelog

## [3.2.0] - 2026-06-11

### 重大重构

- **步骤 3 重写为 OfficeCLI 模板填充**：有模板路径从"调 docx skill 的 router.write_docx"改为"复制模板 → OfficeCLI `view text` 读结构 → `batch set` 填充 → `view html` 预览"。模板即格式权威——只替换文本，中间层不触碰 OOXML 样式。
- **要素式表格 vs 传统段落双轨**：要素式模板（如强制执行申请书）走单元格路径 `/body/tbl[1]/tr[N]/tc[1]` 完美填充；传统段落模板（如诉状）走段落路径 `/body/p[N]`，段落数不匹配时空编号行属可接受瑕疵。
- **无模板路径降级**：保留 python-docx 生成，但强制走 OfficeCLI 格式预览。

## [3.1.0] - 2026-06-10

### 新增

- **步骤 3 格式预览（OfficeCLI）**：定稿后强制用 OfficeCLI `view html` 渲染预览，检查标题字体（黑体/方正小标宋）、正文字体（仿宋）、页边距、落款位、段间距，格式无误再交付。解决"Agent 看不到自己排版"的痛点。

## [3.0.0] - 2026-06-11

### 重大重构

- **模板驱动路径**：步骤 1 新增模板匹配，步骤 1.5 新增占位符信息映射
- **双路径起草**：有模板走填充（占位符→真实信息），无模板走自由起草（参照范文）
- **知识闭环**：步骤 4 新增软 Hook 沉淀入口
- **新增 references**：`placeholder-dictionary.md` + `template-matching.md`
- **新增 templates/README.md**：11 个模板的索引

## [2.2.0] - 2026-06-11

### 新增

- **步骤 0：知识库搜索** — 起草前自动搜索 `D:\Agent知识库`，匹配同类型+同案由的既往文书，参照其结构和句式风格起草
- **步骤 3 尾：Obsidian CLI 打开** — 定稿输出后自动调用 Obsidian CLI 打开 DOCX，供律师在 Obsidian 中审阅

## [2.1.0] - 2026-06-04

### 修改

- **步骤 3 改写**：DOCX 写入调用从 `word-docx` 技能改为 `docx` 技能的 `router.write_docx`。**传入 `template_path`（如有）**——给了模板走 win32com 路径（按模板格式渲染），没给模板走 python-docx 路径（按 styles.py 的「{{USER_SHORT_NAME}}默认排版配置」套样式）。
- **核验提示第 3 条调整**：「格式核验」从"已按 word-docx {{USER_SHORT_NAME}}默认排版配置执行排版"改为"已按 docx 技能的双路径写入完成（给了模板时按模板样式，未给模板时按{{USER_SHORT_NAME}}默认排版配置）"。

## [2.0.0] - 2026-06-02

### 新增

- Frontmatter 补齐 3 个必填字段:`author`({{USER_FULL_NAME}}) / `version`(SEMVER) / `license`(MIT)
- 新增 LICENSE.txt(MIT)
- SKILL.md 末尾"Mavis 本地化适配说明(2026-06-02)"段迁出(本 CHANGELOG 条目即原适配说明)
- SKILL.md 末尾"## 变更历史"段统一指向 [CHANGELOG.md](./CHANGELOG.md)

### 修改

- 修复 v1.0.0 条目"补全 Frontmatter"声明与实际不一致的问题(本版本补齐)

### 迁移记录(原 SKILL.md 末尾 Mavis 适配说明段)

- 路径:全部从 `{{HOME_WIN}}\.Mavis\` 刷为 `~/.mavis/`
- 移除:双机协同 / WPS 云盘 / 符号链接相关内容(Mavis 单机,不需要)
- Frontmatter 移除 author / license / version 字段(后由 v2.0.0 规范化重新补回)
- 路由入口:仍以 workflow-orchestrator 为法律工作唯一入口
- 核心流程未变,所有 references/ 子文件原样保留

## [1.0.1] - 2026-05-31
### 修复
- description 负向条件移除已删除的 analyze-legal-issues，改为 process-cases 简易模式

# Changelog

## [1.0.0] - 2026-05-31
### 新增
- 对齐 SKILL-DEV-GUIDE 书写规范，补全 Frontmatter（author/version/license/负向条件）
