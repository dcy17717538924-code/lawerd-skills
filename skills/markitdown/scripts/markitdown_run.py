#!/usr/bin/env python3
"""
markitdown_run.py — MarkItDown 桥接脚本(2026-06-05 简化:纯本地文本提取)

调用 Microsoft MarkItDown 把文件转 Markdown,供{{ASSISTANT_NAME}} workflow-orchestrator 流程一/二/三用。

支持的输入格式(取决于 markitdown 包安装时的 extras):
  [pdf]      .pdf
  [docx]     .docx
  [pptx]     .pptx
  [xlsx]     .xlsx
  (基础)     .html .csv .json .xml .epub .zip

OCR / 扫描件不在本脚本范围:
  - 本脚本只走 markitdown 主包本地文本提取(无任何 LLM 凭证、不联网)
  - 扫描件 PDF(无文字层)/ 图片 OCR,走{{ASSISTANT_NAME}} IDE 多模态读图(直接把图发给我)
  - 历史上曾挂过 markitdown-ocr + LLM vision 兜底链路(v1.1.0 时代),因接口不稳 + IDE
    多模态可直接发图触发,于 v1.2.0 砍掉

使用:
  # 单文件
  python markitdown_run.py 案件材料.pdf

  # 输出到指定文件
  python markitdown_run.py 案件材料.pdf -o 案件材料.md

  # 批量(整个文件夹)
  python markitdown_run.py 材料/ --output md_output/

  # 显示版本
  python markitdown_run.py --version
"""
import argparse
import sys
from pathlib import Path


def convert_one(md, src: Path, out: Path) -> None:
    """转换单个文件,结果写到 out(.md)"""
    sys.stderr.write(f"[转换] {src} → {out}\n")
    try:
        result = md.convert_local(str(src))
    except Exception as e:
        sys.stderr.write(f"[失败] {src}: {e}\n")
        return
    text = (result.text_content or "").strip()
    if not text:
        # 扫描件 / 无文字层 PDF / 全是图片的 PPT:脚本层面不报错,
        # 但写到 stderr 明确告知,避免静默返回空 .md 误导下游
        try:
            rel = src.relative_to(Path.cwd())
        except ValueError:
            rel = src
        sys.stderr.write(
            f"[空输出] {rel}:无文字层(扫描件 / 全图片)。\n"
            f"          走{{ASSISTANT_NAME}} IDE 多模态读图:把该 PDF 的扫描页直接发图给我即可。\n"
        )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    sys.stderr.write(
        f"[完成] {src} → {out} ({len(text)} chars){' [扫描件,无文字层]' if not text else ''}\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="MarkItDown 桥接:文件 → Markdown(2026-06-05 简化,纯本地无 API)",
    )
    parser.add_argument("input", nargs="?", help="输入文件或文件夹路径")
    parser.add_argument(
        "-o", "--output",
        help="输出文件/文件夹路径(默认:输入同名的 .md)",
    )
    parser.add_argument("--version", action="store_true", help="显示 markitdown 版本")
    args = parser.parse_args()

    if args.version:
        try:
            from importlib.metadata import version
            print(f"markitdown {version('markitdown')}")
        except Exception:
            print("markitdown (unknown version)")
        return 0

    # 纯本地 markitdown 提取 —— 不读 .env、不构造 LLM 客户端、不加载插件
    from markitdown import MarkItDown
    md = MarkItDown()

    src_path = Path(args.input).resolve()
    if not src_path.exists():
        sys.stderr.write(f"[错误] 输入不存在: {src_path}\n")
        return 1

    # 批量:输入是文件夹
    if src_path.is_dir():
        out_dir = Path(args.output).resolve() if args.output else src_path
        files = [p for p in src_path.rglob("*") if p.is_file()]
        sys.stderr.write(f"[批量] 共 {len(files)} 个文件,输出到 {out_dir}\n")
        for f in files:
            rel = f.relative_to(src_path)
            out = out_dir / rel.with_suffix(".md")
            convert_one(md, f, out)
        return 0

    # 单文件
    out_path = Path(args.output).resolve() if args.output else src_path.with_suffix(".md")
    convert_one(md, src_path, out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
