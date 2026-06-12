"""Export a ready-to-print archive PDF.

Order:
1. 案卷目录.docx
2. 办案小结(草稿).docx
3. 入卷材料/*.(pdf/docx/jpg/png), sorted by filename

Requires Microsoft Word on Windows for DOCX -> PDF conversion.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from PIL import Image


def ps_quote(path: Path) -> str:
    return "'" + str(path).replace("'", "''") + "'"


def word_to_pdf(docx_path: Path, pdf_path: Path) -> None:
    script = f"""
$ErrorActionPreference = 'Stop'
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$exportOk = $false
try {{
  $doc = $word.Documents.Open({ps_quote(docx_path)})
  try {{
    $doc.ExportAsFixedFormat({ps_quote(pdf_path)}, 17)
    $exportOk = $true
  }} finally {{
    try {{ $doc.Close($false) }} catch {{ if (-not $exportOk) {{ throw }} }}
  }}
}} finally {{
  try {{ $word.Quit() }} catch {{ if (-not (Test-Path {ps_quote(pdf_path)})) {{ throw }} }}
}}
"""
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip())
    if not pdf_path.exists() or pdf_path.stat().st_size == 0:
        raise RuntimeError(f"Word did not create PDF: {pdf_path}")


def repaired_pdf(pdf_path: Path, tmp_dir: Path) -> Path:
    try:
        import fitz
    except Exception as exc:
        raise RuntimeError(f"PDF 结构异常且当前环境缺少 PyMuPDF，无法修复: {pdf_path}") from exc

    repaired = tmp_dir / f"repaired_{pdf_path.name}"
    doc = fitz.open(str(pdf_path))
    try:
        doc.save(str(repaired), garbage=4, deflate=True, clean=True)
    finally:
        doc.close()
    return repaired


def image_to_pdf(image_path: Path, pdf_path: Path) -> None:
    with Image.open(image_path) as img:
        if img.mode in ("RGBA", "LA"):
            bg = Image.new("RGB", img.size, "white")
            bg.paste(img, mask=img.split()[-1])
            img = bg
        else:
            img = img.convert("RGB")
        img.save(pdf_path, "PDF", resolution=150.0)
    if not pdf_path.exists() or pdf_path.stat().st_size == 0:
        raise RuntimeError(f"Image did not convert to PDF: {image_path}")


def material_to_pdf(path: Path, tmp_dir: Path) -> Path:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return path
    out = tmp_dir / f"material_{path.stem}.pdf"
    if suffix == ".docx":
        word_to_pdf(path, out)
        return out
    if suffix in {".jpg", ".jpeg", ".png"}:
        image_to_pdf(path, out)
        return out
    raise ValueError(f"不支持纳入打印版的入卷材料格式: {path}")


def add_pdf(writer: PdfWriter, pdf_path: Path, tmp_dir: Path) -> int:
    try:
        reader = PdfReader(str(pdf_path))
    except Exception:
        reader = PdfReader(str(repaired_pdf(pdf_path, tmp_dir)))
    for page in reader.pages:
        writer.add_page(page)
    return len(reader.pages)


def export_print_pdf(case_path: Path) -> Path:
    archive_dir = case_path / "00-定卷"
    catalog = archive_dir / "案卷目录.docx"
    summary = archive_dir / "办案小结(草稿).docx"
    materials_dir = archive_dir / "入卷材料"
    output = archive_dir / "打印版-案卷目录-办案小结-入卷材料.pdf"

    missing = [p for p in [catalog, summary, materials_dir] if not p.exists()]
    if missing:
        raise FileNotFoundError("缺少归档文件/目录: " + "; ".join(str(p) for p in missing))

    material_files = sorted(
        [p for p in materials_dir.iterdir() if p.is_file() and p.suffix.lower() in {".pdf", ".docx", ".jpg", ".jpeg", ".png"}],
        key=lambda p: p.name,
    )
    if not material_files:
        raise FileNotFoundError(f"入卷材料目录中没有可合并材料: {materials_dir}")

    writer = PdfWriter()
    page_report: list[tuple[str, int]] = []

    with tempfile.TemporaryDirectory(prefix="case_archive_pdf_") as tmp:
        tmp_dir = Path(tmp)
        catalog_pdf = tmp_dir / "01_catalog.pdf"
        summary_pdf = tmp_dir / "02_summary.pdf"
        word_to_pdf(catalog, catalog_pdf)
        word_to_pdf(summary, summary_pdf)

        for pdf in [catalog_pdf, summary_pdf]:
            pages = add_pdf(writer, pdf, tmp_dir)
            page_report.append((pdf.name, pages))

        for material in material_files:
            pdf = material_to_pdf(material, tmp_dir)
            pages = add_pdf(writer, pdf, tmp_dir)
            page_report.append((material.name, pages))

        temp_out = tmp_dir / output.name
        with temp_out.open("wb") as f:
            writer.write(f)
        shutil.copy2(temp_out, output)

    print(f"生成: {output}")
    print("合并顺序:")
    for name, pages in page_report:
        print(f"  {name}: {pages} 页")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="生成案卷打印版合并 PDF")
    parser.add_argument("-CasePath", required=True, help="案件根目录，例如 D:\\申沪\\民事\\朱新妹")
    args = parser.parse_args()
    export_print_pdf(Path(args.CasePath))


if __name__ == "__main__":
    main()
