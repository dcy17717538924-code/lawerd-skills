"""无模板时，按 styles.py 配置生成 docx。

入口: write(content, output_path)
- content: list of dict, 每个含 type (title|body|section_heading) 和 text
- output_path: 输出 docx 路径 (绝对路径)

返回: 写入文件的绝对路径 (str)
"""
from pathlib import Path

from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

from styles import LAYOUT, apply_to_document


def write(content, output_path):
    """无模板生成 docx。"""
    doc = Document()
    apply_to_document(doc)

    for block in content:
        text = block.get("text", "")
        block_type = block.get("type", "body")
        p = doc.add_paragraph()
        _format_paragraph(p, block_type)
        run = p.add_run(text)
        _format_run(run, block_type)

    # 确保父目录存在
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    resolved = str(output.resolve())
    doc.save(resolved)
    return resolved


def _format_paragraph(p, block_type):
    """根据 block 类型设置段落格式。"""
    if block_type == "title":
        # 文书主标题: 加粗居中, 不要首行缩进
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Pt(0)
        p.paragraph_format.line_spacing_rule = None  # 继承 Normal
    elif block_type == "section_heading":
        # 正文内各节标题: 不居中, 不首行缩进 (按 SKILL.md 加粗即可, 缩进由 Normal 提供)
        p.paragraph_format.first_line_indent = Pt(0)
    else:  # body
        # 正文: 继承 Normal 的首行缩进
        pass


def _format_run(run, block_type):
    """根据 block 类型设置 run 格式。"""
    if block_type == "title":
        run.bold = True
        run.font.size = Pt(LAYOUT["font_size_title_pt"])
    elif block_type == "section_heading":
        run.bold = True
        run.font.size = Pt(LAYOUT["font_size_body_pt"])
    else:  # body
        # 继承 Normal 的 14pt
        pass
