"""Scan case folder for commonly missed archive materials."""

from __future__ import annotations

import argparse
from pathlib import Path


GROUPS = {
    "律师费发票": ["律师费", "发票", "票据"],
    "律师聘用合同": ["聘用合同", "委托代理合同", "律师合同", "委托合同"],
    "散群截图": ["散群", "退群", "群聊", "已退出"],
    "诉讼案件已结案表": ["诉讼案件已结案表", "已结案表", "结案表"],
}

EXTS = {".pdf", ".doc", ".docx", ".jpg", ".jpeg", ".png", ".xlsx", ".xls"}


def scan(case_path: Path) -> dict[str, list[Path]]:
    files = [p for p in case_path.rglob("*") if p.is_file() and p.suffix.lower() in EXTS]
    result: dict[str, list[Path]] = {}
    for group, keywords in GROUPS.items():
        hits = []
        for p in files:
            haystack = str(p)
            if any(k in haystack for k in keywords):
                hits.append(p)
        result[group] = hits
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="扫描归档必查材料")
    parser.add_argument("-CasePath", required=True, help="案件根目录")
    args = parser.parse_args()

    case_path = Path(args.CasePath)
    result = scan(case_path)
    for group, hits in result.items():
        print(f"\n[{group}] {'已找到' if hits else '未按文件名找到'}")
        for p in hits[:20]:
            print(f"  {p}")
        if len(hits) > 20:
            print(f"  ... 另有 {len(hits) - 20} 项")

    composite_pdfs = [
        p for p in case_path.rglob("*.pdf")
        if any(k in p.name for k in ["卷内", "扫描", "全卷", "材料"])
    ]
    if composite_pdfs and (not result["律师费发票"] or not result["律师聘用合同"]):
        print("\n[综合扫描件提示]")
        print("  律师费发票/律师聘用合同可能在综合扫描 PDF 内，需打开或拆页核对：")
        for p in composite_pdfs[:10]:
            print(f"  {p}")

    interview_images = [
        p for p in case_path.rglob("*")
        if p.is_file()
        and p.suffix.lower() in {".jpg", ".jpeg", ".png"}
        and any(k in str(p) for k in ["面谈", "交接"])
    ]
    if interview_images and not result["律师聘用合同"]:
        print("\n[面谈材料提示]")
        print("  律师聘用合同常以图片形式保存在“面谈材料/面谈交接”目录，文件名可能不含合同字样。请人工查看以下图片：")
        for p in interview_images[:20]:
            print(f"  {p}")

    print("\n提示：散群截图如文件名不明显，应人工查看图片，确认聊天界面含“无法在已退出的群聊中发送消息”等字样。")


if __name__ == "__main__":
    main()
