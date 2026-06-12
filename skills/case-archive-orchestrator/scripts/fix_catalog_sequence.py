"""Normalize material numbers and merged category cells in 案卷目录.docx.

The law-firm catalog template has merged/irregular cells. Fill the physical
table cells directly and extend rows when materials exceed the template's
default 15 lines.

Important: the first column is the law-firm catalog item number, not an
auto-incrementing per-category sequence. Provide it explicitly as `seq`.
Consecutive rows with the same `seq` are vertically merged in column 0.
Consecutive rows with the same `category` are vertically merged in column 1.
"""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path

from docx import Document
from docx.oxml import OxmlElement
from docx.table import _Cell


def set_vmerge(tc, value: str | None) -> None:
    tc_pr = tc.get_or_add_tcPr()
    for old in list(tc_pr.findall("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}vMerge")):
        tc_pr.remove(old)
    if value is not None:
        node = OxmlElement("w:vMerge")
        node.set("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val", value)
        tc_pr.append(node)


def fix_catalog(catalog_path: Path, materials: list[dict]) -> None:
    doc = Document(str(catalog_path))
    table = doc.tables[0]

    while len(table.rows) < 9 + len(materials):
        table._tbl.append(deepcopy(table.rows[-1]._tr))

    total_pages = sum(int(m.get("pages") or 0) for m in materials)
    if len(table.rows) > 5 and len(table.rows[5].cells) > 2:
        table.rows[5].cells[2].text = str(total_pages)

    for idx, item in enumerate(materials):
        seq = str(item["seq"])
        cat = str(item["category"])
        row = table.rows[9 + idx]
        tcs = list(row._tr.tc_lst)

        def set_tc(i: int, text) -> None:
            _Cell(tcs[i], table).text = "" if text is None else str(text)

        set_tc(0, seq)
        set_tc(1, cat)
        set_tc(2, item["name"])
        set_tc(3, item.get("pages", ""))
        set_tc(4, item.get("copies", "1"))
        set_tc(5, item.get("note", ""))

        prev = materials[idx - 1] if idx else None
        next_item = materials[idx + 1] if idx + 1 < len(materials) else None

        if prev and str(prev["seq"]) == seq:
            set_vmerge(tcs[0], "continue")
        elif next_item and str(next_item["seq"]) == seq:
            set_vmerge(tcs[0], "restart")
        else:
            set_vmerge(tcs[0], None)

        if prev and str(prev["category"]) == cat:
            set_vmerge(tcs[1], "continue")
        elif next_item and str(next_item["category"]) == cat:
            set_vmerge(tcs[1], "restart")
        else:
            set_vmerge(tcs[1], None)

    doc.save(str(catalog_path))


def main() -> None:
    parser = argparse.ArgumentParser(description="修正案卷目录材料清单序号")
    parser.add_argument("catalog", help="案卷目录.docx 路径")
    parser.add_argument("materials_json", help="UTF-8 JSON，数组字段：seq/category/name/pages/copies/note")
    args = parser.parse_args()
    with Path(args.materials_json).open("r", encoding="utf-8") as f:
        materials = json.load(f)
    fix_catalog(Path(args.catalog), materials)
    print(f"已修正: {args.catalog}")


if __name__ == "__main__":
    main()
