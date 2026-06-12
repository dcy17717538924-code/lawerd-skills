#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
mineru_parse.py — MinerU 精准解析 API CLI 客户端({{ASSISTANT_NAME}}适配版)

接口文档: https://mineru.net/apiManage/docs
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import zipfile
from io import BytesIO
from pathlib import Path
from typing import Iterable

# MinerU API endpoint
BASE_URL = "https://mineru.net/api/v4"

# 默认 Token 文件位置({{USER_SHORT_NAME}}工作约定)
DEFAULT_TOKEN_FILE = Path.home() / "Desktop" / "mineru.txt"

# 单批最大文件数(MinerU 限制)
MAX_BATCH_SIZE = 50

# 支持的扩展名
SUPPORTED_EXTS = {
    ".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx",
    ".png", ".jpg", ".jpeg", ".jp2", ".webp", ".gif", ".bmp",
    ".html", ".htm",
}


# ---------------------------------------------------------------------------
# Token 读取
# ---------------------------------------------------------------------------

def read_token(token_file: Path | None) -> str:
    """按优先级读 token:显式文件 → 环境变量 → 默认 Desktop/mineru.txt。"""
    # 1. 显式文件
    if token_file and token_file.exists():
        for line in token_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                return line
        raise SystemExit(f"Token 文件 {token_file} 为空或全是注释")

    # 2. 环境变量直接给值
    env = os.environ.get("MINERU_TOKEN", "").strip()
    if env:
        return env

    # 3. 默认位置
    if DEFAULT_TOKEN_FILE.exists():
        for line in DEFAULT_TOKEN_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                return line

    raise SystemExit(
        f"找不到 Token。请确认:\n"
        f"  1) {DEFAULT_TOKEN_FILE} 存在且非空,或\n"
        f"  2) 环境变量 MINERU_TOKEN 已设,或\n"
        f"  3) --token-file 指向的文件存在"
    )


# ---------------------------------------------------------------------------
# HTTP 封装
# ---------------------------------------------------------------------------

def _headers(token: str) -> dict:
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }


def _post(path: str, token: str, payload: dict) -> dict:
    import requests
    res = requests.post(f"{BASE_URL}{path}", headers=_headers(token), json=payload, timeout=30)
    res.raise_for_status()
    return res.json()


def _get(path: str, token: str) -> dict:
    import requests
    res = requests.get(f"{BASE_URL}{path}", headers=_headers(token), timeout=30)
    res.raise_for_status()
    return res.json()


def _put_file(url: str, file_path: Path) -> int:
    """PUT 上传到 MinerU 给的预签名 URL。"""
    import requests
    with file_path.open("rb") as f:
        res = requests.put(url, data=f, timeout=300)
    return res.status_code


# ---------------------------------------------------------------------------
# URL 模式(单文件)
# ---------------------------------------------------------------------------

def parse_url(url: str, token: str, *, model_version: str, language: str,
              is_ocr: bool, enable_formula: bool, enable_table: bool,
              page_ranges: str | None, extra_formats: list[str],
              timeout: int, interval: int) -> dict | None:
    """远程 URL 单文件解析。返回 full_zip_url 或 None。"""
    payload = {
        "url": url,
        "model_version": model_version,
        "language": language,
        "is_ocr": is_ocr,
        "enable_formula": enable_formula,
        "enable_table": enable_table,
    }
    if page_ranges:
        payload["page_ranges"] = page_ranges
    if extra_formats:
        payload["extra_formats"] = extra_formats

    print(f"[submit] {url}")
    res = _post("/extract/task", token, payload)
    if res.get("code") != 0:
        print(f"[error] 提交失败: {res.get('msg')}", file=sys.stderr)
        return None
    task_id = res["data"]["task_id"]
    print(f"[task] {task_id}")

    return _poll_task(task_id, token, timeout, interval)


# ---------------------------------------------------------------------------
# 本地文件上传(单文件 + 批量)
# ---------------------------------------------------------------------------

def _upload_files_and_get_batch(file_paths: list[Path], token: str, *,
                                 model_version: str, language: str,
                                 is_ocr: bool, enable_formula: bool,
                                 enable_table: bool, page_ranges: str | None,
                                 extra_formats: list[str]) -> str:
    """申请 batch 上传 URL,PUT 文件,返回 batch_id。"""
    files_payload = []
    for p in file_paths:
        item: dict = {"name": p.name}
        if is_ocr:
            item["is_ocr"] = True
        if page_ranges:
            item["page_ranges"] = page_ranges
        files_payload.append(item)

    payload = {
        "files": files_payload,
        "model_version": model_version,
        "language": language,
        "enable_formula": enable_formula,
        "enable_table": enable_table,
    }
    if extra_formats:
        payload["extra_formats"] = extra_formats

    print(f"[submit] {len(file_paths)} 文件,首件: {file_paths[0].name}")
    res = _post("/file-urls/batch", token, payload)
    if res.get("code") != 0:
        raise RuntimeError(f"申请上传链接失败: {res.get('msg')}")

    batch_id = res["data"]["batch_id"]
    urls = res["data"]["file_urls"]

    # PUT 上传
    for i, (path, url) in enumerate(zip(file_paths, urls), 1):
        print(f"[upload {i}/{len(file_paths)}] {path.name} ...", end=" ", flush=True)
        code = _put_file(url, path)
        if code in (200, 201):
            print("ok")
        else:
            print(f"FAIL({code})")
            raise RuntimeError(f"上传失败: {path}")

    print(f"[batch] {batch_id},等待系统自动提交解析任务...")
    return batch_id


def _poll_batch(batch_id: str, token: str, timeout: int, interval: int) -> list[dict]:
    """轮询批量任务,返回每个文件的最终结果(包含 full_zip_url 或 err_msg)。"""
    import requests
    start = time.time()
    state_labels = {
        "waiting-file": "等待文件",
        "pending": "排队中",
        "running": "解析中",
        "converting": "格式转换",
    }
    while time.time() - start < timeout:
        res = requests.get(
            f"{BASE_URL}/extract-results/batch/{batch_id}",
            headers=_headers(token),
            timeout=30,
        )
        res.raise_for_status()
        data = res.json()
        if data.get("code") != 0:
            print(f"[error] 查询失败: {data.get('msg')}", file=sys.stderr)
            return []

        results = data["data"]["extract_result"]
        states = [r["state"] for r in results]
        elapsed = int(time.time() - start)
        done_count = sum(1 for s in states if s == "done")
        fail_count = sum(1 for s in states if s == "failed")
        active = [s for s in states if s not in ("done", "failed")]
        active_label = state_labels.get(active[0], active[0]) if active else "-"
        print(f"[poll {elapsed:>3}s] done={done_count} fail={fail_count} active={active_label}")

        if all(s in ("done", "failed") for s in states):
            return results

        time.sleep(interval)

    print(f"[timeout] {timeout}s 内未完成。请用 batch_id={batch_id} 手动查询。", file=sys.stderr)
    return results  # 返还未完成的部分


def _poll_task(task_id: str, token: str, timeout: int, interval: int) -> dict | None:
    """轮询单任务,返回包含 full_zip_url 的结果。"""
    import requests
    start = time.time()
    state_labels = {
        "pending": "排队中",
        "running": "解析中",
        "converting": "格式转换",
    }
    while time.time() - start < timeout:
        res = requests.get(
            f"{BASE_URL}/extract/task/{task_id}",
            headers=_headers(token),
            timeout=30,
        )
        res.raise_for_status()
        data = res.json()
        if data.get("code") != 0:
            print(f"[error] 查询失败: {data.get('msg')}", file=sys.stderr)
            return None

        d = data["data"]
        state = d["state"]
        elapsed = int(time.time() - start)
        if state == "done":
            print(f"[poll {elapsed:>3}s] 完成")
            return d
        if state == "failed":
            print(f"[poll {elapsed:>3}s] 失败: {d.get('err_msg')}", file=sys.stderr)
            return None
        print(f"[poll {elapsed:>3}s] {state_labels.get(state, state)}")
        time.sleep(interval)

    print(f"[timeout] {timeout}s 内未完成。task_id={task_id}", file=sys.stderr)
    return None


# ---------------------------------------------------------------------------
# 下载 + 解压
# ---------------------------------------------------------------------------

def _download_and_extract(zip_url: str, out_dir: Path) -> Path | None:
    """下载 zip 并解压到 out_dir。返回 out_dir。"""
    import requests
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"[download] {zip_url[:80]}...")
    res = requests.get(zip_url, timeout=300)
    res.raise_for_status()
    with zipfile.ZipFile(BytesIO(res.content)) as zf:
        zf.extractall(out_dir)
    print(f"[extract] → {out_dir}")
    return out_dir


# ---------------------------------------------------------------------------
# 目录批量
# ---------------------------------------------------------------------------

def _iter_files(directory: Path, recursive: bool) -> Iterable[Path]:
    if recursive:
        for p in sorted(directory.rglob("*")):
            if p.is_file() and p.suffix.lower() in SUPPORTED_EXTS:
                yield p
    else:
        for p in sorted(directory.iterdir()):
            if p.is_file() and p.suffix.lower() in SUPPORTED_EXTS:
                yield p


def cmd_batch(args):
    token = read_token(args.token_file)
    in_dir = Path(args.directory).resolve()
    if not in_dir.is_dir():
        raise SystemExit(f"目录不存在: {in_dir}")

    out_root = Path(args.output).resolve() if args.output else in_dir.parent / f"{in_dir.name}_parsed"
    out_root.mkdir(parents=True, exist_ok=True)
    batch_root = out_root / f"batch_{time.strftime('%Y%m%d_%H%M%S')}"
    batch_root.mkdir(parents=True, exist_ok=True)

    files = list(_iter_files(in_dir, args.recursive))
    if not files:
        print(f"目录内没有支持的文件({in_dir})。支持: {', '.join(sorted(SUPPORTED_EXTS))}")
        return

    print(f"[scan] 共 {len(files)} 个待解析文件")
    extra = [f.strip() for f in args.extra_formats.split(",") if f.strip()] if args.extra_formats else []

    success = 0
    fail = 0
    for i in range(0, len(files), MAX_BATCH_SIZE):
        chunk = files[i:i + MAX_BATCH_SIZE]
        print(f"\n=== 批次 {i // MAX_BATCH_SIZE + 1} / {(len(files) + MAX_BATCH_SIZE - 1) // MAX_BATCH_SIZE} ({len(chunk)} 个) ===")
        try:
            batch_id = _upload_files_and_get_batch(
                chunk, token,
                model_version=args.model,
                language=args.language,
                is_ocr=args.is_ocr,
                enable_formula=not args.no_formula,
                enable_table=not args.no_table,
                page_ranges=args.page_ranges,
                extra_formats=extra,
            )
            results = _poll_batch(batch_id, token, args.timeout, args.interval)
        except Exception as e:
            print(f"[error] 批次失败: {e}", file=sys.stderr)
            fail += len(chunk)
            continue

        for r in results:
            if r["state"] != "done":
                print(f"[fail] {r['file_name']}: {r.get('err_msg', '?')}", file=sys.stderr)
                fail += 1
                continue
            stem = Path(r["file_name"]).stem
            target_dir = batch_root / stem
            try:
                _download_and_extract(r["full_zip_url"], target_dir)
                success += 1
            except Exception as e:
                print(f"[fail] {r['file_name']} 下载/解压失败: {e}", file=sys.stderr)
                fail += 1

    print(f"\n=== 汇总 ===")
    print(f"成功: {success} / 失败: {fail} / 总: {len(files)}")
    print(f"输出根目录: {batch_root}")


def cmd_file(args):
    token = read_token(args.token_file)
    p = Path(args.path).resolve()
    if not p.is_file():
        raise SystemExit(f"文件不存在: {p}")
    if p.suffix.lower() not in SUPPORTED_EXTS:
        raise SystemExit(f"不支持的扩展名: {p.suffix}")

    out_root = Path(args.output).resolve() if args.output else p.parent / f"{p.stem}_parsed"
    out_root.mkdir(parents=True, exist_ok=True)
    target = out_root / p.stem

    extra = [f.strip() for f in args.extra_formats.split(",") if f.strip()] if args.extra_formats else []
    batch_id = _upload_files_and_get_batch(
        [p], token,
        model_version=args.model,
        language=args.language,
        is_ocr=args.is_ocr,
        enable_formula=not args.no_formula,
        enable_table=not args.no_table,
        page_ranges=args.page_ranges,
        extra_formats=extra,
    )
    results = _poll_batch(batch_id, token, args.timeout, args.interval)
    if not results or results[0]["state"] != "done":
        raise SystemExit(f"解析失败: {results[0].get('err_msg') if results else 'no result'}")
    _download_and_extract(results[0]["full_zip_url"], target)
    print(f"\n[ok] {target / 'full.md'}")


def cmd_url(args):
    token = read_token(args.token_file)
    out_root = Path(args.output).resolve() if args.output else Path.cwd() / "mineru_parsed"
    out_root.mkdir(parents=True, exist_ok=True)
    target = out_root / f"url_{int(time.time())}"

    extra = [f.strip() for f in args.extra_formats.split(",") if f.strip()] if args.extra_formats else []
    res = parse_url(
        args.url, token,
        model_version=args.model,
        language=args.language,
        is_ocr=args.is_ocr,
        enable_formula=not args.no_formula,
        enable_table=not args.no_table,
        page_ranges=args.page_ranges,
        extra_formats=extra,
        timeout=args.timeout,
        interval=args.interval,
    )
    if not res:
        raise SystemExit("URL 解析失败")
    _download_and_extract(res["full_zip_url"], target)
    print(f"\n[ok] {target / 'full.md'}")


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

def _add_common(p: argparse.ArgumentParser):
    p.add_argument("--model", default="vlm", choices=["vlm", "pipeline", "MinerU-HTML"],
                   help="模型版本(默认 vlm,推荐)")
    p.add_argument("--language", default="ch",
                   help="文档语言(默认 ch;其他常用:ch_server/en/japan/korean)")
    p.add_argument("--is-ocr", action="store_true", help="扫描件必开(默认关)")
    p.add_argument("--no-formula", action="store_true", help="关闭公式识别")
    p.add_argument("--no-table", action="store_true", help="关闭表格识别")
    p.add_argument("--page-ranges", help='指定页码,例 "1-10,20-30"')
    p.add_argument("--extra-formats", help='追加导出格式,例 "docx,html"')
    p.add_argument("--output", help="输出目录(默认:输入旁 _parsed)")
    p.add_argument("--token-file", type=Path, help="Token 文件路径(默认 ~/Desktop/mineru.txt)")
    p.add_argument("--interval", type=int, default=3, help="轮询间隔秒(默认 3)")
    p.add_argument("--timeout", type=int, default=600, help="单任务超时秒(默认 600)")


def main():
    parser = argparse.ArgumentParser(
        prog="mineru_parse.py",
        description="MinerU 精准解析 CLI({{ASSISTANT_NAME}}适配版)— 批量把 PDF/扫描件/图片转 Markdown",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_url = sub.add_parser("url", help="远程 URL 单文件解析")
    p_url.add_argument("url", help="文件 URL(支持 PDF/Office/图片/HTML)")
    _add_common(p_url)
    p_url.set_defaults(func=cmd_url)

    p_file = sub.add_parser("file", help="本地单文件解析")
    p_file.add_argument("path", help="本地文件路径")
    _add_common(p_file)
    p_file.set_defaults(func=cmd_file)

    p_batch = sub.add_parser("batch", help="本地目录批量解析(自动分批 ≤50)")
    p_batch.add_argument("directory", help="待解析目录")
    p_batch.add_argument("--recursive", action="store_true", help="递归子目录")
    _add_common(p_batch)
    p_batch.set_defaults(func=cmd_batch)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
