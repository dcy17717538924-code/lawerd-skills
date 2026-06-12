from pathlib import Path
import shutil
from word_pool import WORD_POOL


def write(content, output_path, template_path):
    """按模板格式渲染新文档。

    Args:
        content: list of dict，每个含 type (title|body) 和 text
        output_path: 输出 docx 路径
        template_path: 模板 docx 路径
    """
    word = WORD_POOL.get()
    output = Path(output_path).resolve()
    template = Path(template_path).resolve()

    shutil.copy(str(template), str(output))
    doc = word.Documents.Open(str(output))
    try:
        for block in content:
            text = block.get("text", "")
            block_type = block.get("type", "body")
            rng = doc.Range(doc.Content.End - 1, doc.Content.End - 1)
            # 用模板里已定义的样式
            if block_type == "title":
                try:
                    rng.Style = "标题 1"
                except Exception:
                    pass
            rng.Text = text
            rng.InsertParagraphAfter()
        doc.SaveAs2(str(output))
    finally:
        doc.Close(SaveChanges=False)
    return str(output)
