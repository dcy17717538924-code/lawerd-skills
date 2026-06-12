#!/usr/bin/env python3
"""{{ASSISTANT_NAME}}体系 — 环境自检 (macOS/Linux)"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

HOME = Path.home()
REASONIX_DIR = HOME / ".reasonix"
SKILLS_DIR = REASONIX_DIR / "skills"
MINERU_TOKEN = HOME / "Desktop" / "mineru.txt"
WHISPER_MODEL = HOME / ".cache" / "whisper" / "medium.pt"

CHECKS = []

def check(name: str, fn, fix_hint: str = ""):
    try:
        ok, detail = fn()
    except Exception as e:
        ok, detail = False, str(e)
    CHECKS.append((name, ok, detail, fix_hint))

# ── 检查项 ───────────────────────────────────────────

def _reasonix():
    ok = REASONIX_DIR.is_dir()
    return ok, str(REASONIX_DIR) if ok else "未找到 ~/.reasonix/"

def _skills_dir():
    ok = SKILLS_DIR.is_dir()
    return ok, str(SKILLS_DIR) if ok else "未找到 ~/.reasonix/skills/"

def _python():
    for cmd in ("python3", "python"):
        p = shutil.which(cmd)
        if p:
            try:
                ver = subprocess.check_output([p, "--version"], stderr=subprocess.STDOUT, text=True).strip()
                return True, f"{p} → {ver}"
            except Exception:
                continue
    return False, "python3 不可用。请安装: brew install python3"

def _git():
    p = shutil.which("git")
    if p:
        try:
            ver = subprocess.check_output([p, "--version"], text=True).strip()
            return True, ver
        except Exception:
            pass
    return False, "git 不可用。请安装: brew install git 或下载 Xcode CLT"

def _mineru():
    ok = MINERU_TOKEN.is_file()
    return ok, str(MINERU_TOKEN) if ok else "未找到 mineru token（可选，用于 OCR）"

def _whisper():
    ok = WHISPER_MODEL.is_file()
    size = WHISPER_MODEL.stat().st_size // (1024 * 1024) if ok else 0
    return ok, f"{WHISPER_MODEL} ({size} MB)" if ok else "未下载 whisper 模型（可选，用于语音识别）"

# ── 执行 ─────────────────────────────────────────────

check("Reasonix Code", _reasonix, "请先安装 Reasonix Code")
check("skills 目录", _skills_dir, "mkdir -p ~/.reasonix/skills")
check("Python 3", _python, "brew install python3")
check("Git", _git, "brew install git")
check("mineru token (OCR)", _mineru, "将 token 文件放到 ~/Desktop/mineru.txt（可选）")
check("whisper 模型 (语音)", _whisper, "下载 medium.pt 到 ~/.cache/whisper/（可选）")

# ── 输出表格 ─────────────────────────────────────────

PASS = "✅"
FAIL = "❌"
WARN = "⚠️"

print()
print("=" * 60)
print("  {{ASSISTANT_NAME}}律师助理 — 环境自检 (macOS)")
print("=" * 60)
print()

all_ok = True
for name, ok, detail, hint in CHECKS:
    icon = PASS if ok else (WARN if "可选" in name else FAIL)
    if not ok and "可选" not in name:
        all_ok = False
    print(f"  {icon} {name}: {detail}")
    if not ok and hint:
        print(f"     → {hint}")

print()
if all_ok:
    print("  全部必需项通过 ✅  可以继续安装。")
else:
    print("  ❌ 存在未通过项，请处理后再继续。")
print()
