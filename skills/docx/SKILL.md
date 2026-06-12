---
name: docx
author: 杜重阳律师（微信Dcylawer8888)
version: "2.1.0"
license: MIT
description: DOCX 文档处理脚本库。被 contract-review-pro 等技能调用，提供 Word 文档的 Track Changes、Comments 生成和 ooxml 打包/解包工具链。 不要用于：独立的法律案件处理、文书起草——本技能仅作为 DOCX 工具库被其他技能调用。
---


## 运行环境

> **Python 不在系统 PATH 中，必须使用完整路径。**

- Python 解释器：`python`
- 已装依赖：`python-docx`、`lxml`

所有 `.py` 脚本需以此 Python 运行，禁止直接使用 `python` 命令。

# DOCX 脚本库

本目录为 **Python 脚本库**，不包含独立的 Skill 流程。

## 用途

被 `contract-review-pro` 的 `docx_generator.py` 调用，提供：

- **scripts/router.py** — 双路径 docx 写入路由（统一入口）
- **scripts/win32com_doc.py** — 有模板时走 Word COM（按模板格式渲染）
- **scripts/python_doc.py** — 无模板时走 python-docx（按 styles.py 配置套样式）
- **scripts/word_pool.py** — 常驻 Word.Application 单例池（自动重启）
- **scripts/styles.py** — {{USER_SHORT_NAME}}默认排版配置（无模板时的回退样式）
- **ooxml/scripts/** — ooxml 打包/解包工具链（unpack.py / pack.py）

## 调用方式

```python
from router import write_docx

# 给了 template_path → 走 win32com 路径（按模板格式渲染）
# 没给 template_path → 走 python-docx 路径（按 styles.py 配置套样式）
write_docx(
    content=[{"type": "title", "text": "..."}, {"type": "body", "text": "..."}],
    output_path="/abs/path/to/output.docx",
    template_path="/abs/path/to/template.docx",  # 可选
)
```

> **本 skill 现在提供双路径写入**：给了模板走 win32com 路径（按模板格式渲染），没给模板走 python-docx 路径（按 styles.py 配置套样式）。

## 关联技能

- [[word-docx]] — 有 SKILL.md 的独立 Word 处理技能，如需要纯 Word 操作请使用那个
- [[contract-review-pro]] — 合同审核技能，依赖本脚本库生成三件套交付物


---

## 变更历史

见 [CHANGELOG.md](./CHANGELOG.md)