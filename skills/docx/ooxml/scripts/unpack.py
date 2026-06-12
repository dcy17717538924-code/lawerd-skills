"""
OOXML unpack — 将 .docx (ZIP) 解压为 XML 目录结构
"""

import sys
import os
import zipfile
from pathlib import Path


def unpack_document(docx_path: str, output_dir: str):
    """解压 .docx 到目录"""
    docx_path = Path(docx_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(str(docx_path), "r") as z:
        z.extractall(str(output_dir))

    print(f"[unpack] 解压完成: {docx_path} -> {output_dir}")
    return str(output_dir)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python unpack.py <input.docx> <output_dir>")
        sys.exit(1)

    docx_path = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.isfile(docx_path):
        print(f"错误: 文件不存在 {docx_path}")
        sys.exit(1)

    unpack_document(docx_path, output_dir)
