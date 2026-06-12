"""
OOXML pack — 将 XML 目录结构打包为 .docx (ZIP)
"""

import os
import zipfile
from pathlib import Path


def pack_document(unpacked_dir: str, output_path: str, validate: bool = False):
    """将解压后的目录打包为 .docx

    严格遵循 OOXML 包规范:
    - [Content_Types].xml 必须在 ZIP 第一个条目
    - 使用 ZIP_DEFLATED 压缩
    """
    unpacked_dir = Path(unpacked_dir)
    output_path = Path(output_path)

    if not unpacked_dir.is_dir():
        raise FileNotFoundError(f"解压目录不存在: {unpacked_dir}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(str(output_path), "w", zipfile.ZIP_DEFLATED) as z:
        # [Content_Types].xml 必须在首位
        content_types = unpacked_dir / "[Content_Types].xml"
        if content_types.exists():
            z.write(str(content_types), "[Content_Types].xml")

        # 写入其他文件
        for root, dirs, files in os.walk(str(unpacked_dir)):
            for fname in sorted(files):
                full_path = os.path.join(root, fname)
                rel_path = os.path.relpath(full_path, str(unpacked_dir))

                # 跳过 [Content_Types].xml（已写）
                if rel_path == "[Content_Types].xml":
                    continue

                # 统一为正斜杠路径（ZIP 规范）
                rel_path = rel_path.replace("\\", "/")
                z.write(full_path, rel_path)

    print(f"[pack] 打包完成: {output_path}")
    return str(output_path)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("用法: python pack.py <unpacked_dir> <output.docx>")
        sys.exit(1)

    pack_document(sys.argv[1], sys.argv[2])
