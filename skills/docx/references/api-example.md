# API 示例

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
