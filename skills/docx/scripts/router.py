"""双路径 docx 写入路由。

- 有模板 → 调 win32com_doc.write（按模板格式渲染）
- 无模板 → 调 python_doc.write（按 styles.py 配置套样式）
"""
from pathlib import Path
import win32com_doc
import python_doc


def write_docx(content, output_path, template_path=None, **kwargs):
    """统一写入入口。

    Args:
        content: list of dict，每个含 type (title|body) 和 text
        output_path: 输出 docx 路径
        template_path: 模板 docx 路径（可选）
        **kwargs: 透传给 win32com_doc.write
    """
    if template_path and Path(template_path).is_file():
        return win32com_doc.write(
            content, output_path, template_path, **kwargs
        )
    return python_doc.write(content, output_path)
