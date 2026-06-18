"""双路径 docx 写入路由 — 模板路径走 COM，非模板路径走 python-docx。"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import win32com_doc, python_doc


def write_docx(content, output, template=None, **kwargs):
    if template:
        return win32com_doc.write(content, output, template, **kwargs)
    else:
        return python_doc.write(content, output, **kwargs)


def export_pdf(docx_path, pdf_path=None):
    """通过 Word/WPS COM 导出 PDF。"""
    from pathlib import Path
    docx_path = Path(docx_path)
    if pdf_path is None:
        pdf_path = docx_path.with_suffix('.pdf')

    import win32com.client
    word = win32com.client.DispatchEx("Word.Application")
    try:
        doc = word.Documents.Open(str(docx_path.resolve()))
        doc.SaveAs(str(Path(pdf_path).resolve()), FileFormat=17)
        doc.Close()
    finally:
        word.Quit()

    return str(pdf_path)
