"""python_doc.py 基本测试: 生成带 title + body 的 docx, 验证可写可读。"""
import os
import sys
import zipfile

# 把 scripts 目录加入路径, 这样可以 import styles 和 python_doc
SCRIPTS_DIR = r"{{HOME_WIN}}\.mavis\agents\lawyer-assistant\skills\docx\scripts"
sys.path.insert(0, SCRIPTS_DIR)

from python_doc import write  # noqa: E402


def main():
    output = r"{{HOME_WIN}}\AppData\Local\Temp\test_python_doc.docx"
    # 清理旧文件, 保证是本次写入
    if os.path.exists(output):
        os.remove(output)

    result_path = write(
        content=[
            {"type": "title", "text": "测试起诉状"},
            {"type": "body", "text": "原告诉称：这是一段测试正文。"},
        ],
        output_path=output,
    )

    assert os.path.exists(result_path), f"文件未生成: {result_path}"
    assert os.path.getsize(result_path) > 0, "文件为空"

    # 验证是合法 zipfile
    assert zipfile.is_zipfile(result_path), f"不是合法 zipfile: {result_path}"

    # 验证 styles.xml 含"仿宋"
    with zipfile.ZipFile(result_path) as z:
        with z.open("word/styles.xml") as f:
            styles_xml = f.read().decode("utf-8")
    assert "仿宋" in styles_xml, f"styles.xml 中未找到'仿宋'字样"
    # 验证 w:eastAsia 用了仿宋
    assert "w:eastAsia=\"仿宋\"" in styles_xml, "w:eastAsia 字体未设置为仿宋"

    # 验证 document.xml 包含输入文本
    with zipfile.ZipFile(result_path) as z:
        with z.open("word/document.xml") as f:
            doc_xml = f.read().decode("utf-8")
    assert "测试起诉状" in doc_xml, "标题文本未写入"
    assert "原告诉称：这是一段测试正文。" in doc_xml, "正文文本未写入"

    # 验证页脚"第 X 页"
    footer_files = [n for n in zipfile.ZipFile(result_path).namelist() if "footer" in n]
    assert footer_files, "未找到 footer part"
    with zipfile.ZipFile(result_path) as z:
        for f_name in footer_files:
            with z.open(f_name) as f:
                footer_xml = f.read().decode("utf-8")
            assert " PAGE " in footer_xml, f"{f_name} 缺 PAGE 域"
            assert "第" in footer_xml and "页" in footer_xml, f"{f_name} 缺第/页字样"

    print(
        f"python_doc OK: {result_path}, size={os.path.getsize(result_path)}, "
        f"footer_parts={len(footer_files)}"
    )


if __name__ == "__main__":
    main()
