# Changelog

> 作者：杜重阳律师（微信Dcylawer8888）
> 许可证：MIT

## [2.1.0] - 2026-06-04
### 新增（双路径 docx 写入架构）
- **scripts/router.py** — 统一写入入口 `write_docx(content, output_path, template_path=None)`。有 `template_path` → 调 `win32com_doc.write`（按模板格式渲染）；无 `template_path` → 调 `python_doc.write`（按 `styles.py` 配置套样式）。
- **scripts/word_pool.py** — 常驻 `Word.Application` 单例池（线程安全单例 + 自动重启），消除反复 DispatchEx 的开销。
- **scripts/win32com_doc.py** — 有模板写入器：复制模板到输出路径 → `Documents.Open` → 在文档末尾追加段落（title 套用模板的"标题 1"样式）→ `SaveAs2` → `Close(SaveChanges=False)`。
- **scripts/python_doc.py** — 无模板写入器：`Document()` + `apply_to_document()` 套样式 + 按 `type` 字段加段落。
- **scripts/styles.py** — {{USER_SHORT_NAME}}默认排版配置（单一信息源，LAYOUT 字典与 `word-docx/SKILL.md` 的"{{USER_SHORT_NAME}}默认排版配置"章节严格一一对应）：仿宋/三号 16pt 标题/四号 14pt 正文/24 磅固定行距/2.54×1.91cm 边距/首行缩进 2 字符/居中"第 X 页"页脚。
- **scripts/test_basic.py** — `python_doc` 基本测试：仿宋、Normal 14pt、24 磅固定行距、PAGE 域、文本写入。
- **scripts/test_fixtures/sample_template.docx** — 真实样例模板（用于有模板路径的 E2E 验证）。
### 移除
- **scripts/document.py** — 旧的 OOXML 直写实现（XmlEditor + Document 类，处理 Track Changes / Comments）。无外部调用方，通过 `mavis-trash` 移到回收站（可恢复）。后续如需 Track Changes / Comments 能力应通过 `win32com_doc` 路径或 `ooxml/scripts/` 工具链实现。
### 依赖
- 新增 `python-docx`（>=0.8.11，实测 1.2.0）— 无模板路径的写入器依赖。
- 新增 `pywin32`（实测已装）— 有模板路径的 Word COM 写入器依赖。
- 保留 `lxml`（原有，未使用）。
### 调用方式
```python
from router import write_docx
# 给了 template_path → win32com 路径（按模板格式渲染）
write_docx(
    content=[{"type": "title", "text": "..."}, {"type": "body", "text": "..."}],
    output_path="/abs/path/to/output.docx",
    template_path="/abs/path/to/template.docx",
)
# 没给 template_path → python-docx 路径（按 styles.py 套样式）
write_docx(
    content=[{"type": "title", "text": "..."}, {"type": "body", "text": "..."}],
    output_path="/abs/path/to/output.docx",
)
```
### 端到端验证
- 有模板（`sample_template.docx`）→ `output_with_template.docx`：25831 bytes，32 段落（29 模板原文 + 3 新段），新段最后 3 段为"强制执行申请书（测试）"/"申请执行人：张三"/"被申请执行人：李四"，title 套用"标题 1"样式。
- 无模板 → `output_no_template.docx`：37462 bytes，仿宋写入 styles.xml，Normal sz=28 (14pt) / lineRule=exact / line=480 (24pt)，title sz=32 (16pt) 居中加粗。
## [2.0.0] - 2026-06-02
### 新增
- Frontmatter 补齐 3 个必填字段:`author`({{USER_FULL_NAME}}) / `version`(SEMVER) / `license`(MIT)
- 新增 LICENSE.txt(MIT)
- SKILL.md 末尾"Mavis 本地化适配说明(2026-06-02)"段迁出
- SKILL.md 末尾"## 变更历史"段统一指向 [CHANGELOG.md](./CHANGELOG.md)
### 修改
- 修复 v1.0.0 条目"对齐 SKILL-DEV-GUIDE"声明与实际不一致的问题(本版本补齐)
### 迁移记录(原 SKILL.md 末尾 Mavis 适配说明段)
- 路径:全部从 `{{HOME_WIN}}\.Mavis\` 刷为 `~/.mavis/`
- 移除:双机协同 / WPS 云盘 / 符号链接相关内容(Mavis 单机,不需要)
- Frontmatter 移除 author / license / version 字段(后由 v2.0.0 规范化重新补回)
- 路由入口:仍以 workflow-orchestrator 为法律工作唯一入口
- 核心流程未变,所有 scripts/ 和 references/ 子文件原样保留
## [1.0.0] - 2026-05-31
### 新增
- 对齐 SKILL-DEV-GUIDE 书写规范，补全 Frontmatter（author/version/license/负向条件）