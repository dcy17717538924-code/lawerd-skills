#!/usr/bin/env python3
"""{{ASSISTANT_NAME}}技能脱敏脚本 — 将个人信息替换为占位符

使用方法:
  python3 desensitize.py --src ~/.reasonix/skills/ --dst lawerd-skills/skills/
  python3 desensitize.py --src ~/.reasonix/memory/global/ --dst lawerd-skills/memory/ --mode memory

排除:
  - law086/ (案件云)
  - case-study-report/ (案例分析报告)
  - archive/ 目录
  - .git/ 目录
  - LICENSE / LICENSE.txt (版权文件不碰)
"""

import os
import re
import shutil
import sys
from pathlib import Path

# ── 替换规则 ──────────────────────────────────────
# 顺序重要：长的先匹配，避免部分替换

REPLACEMENTS = [
    # 路径
    (r"C:\\Users\\13062\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python\.exe",
     "{{CODEX_PYTHON}}"),
    (r"C:\\Users\\13062\\.reasonix\\skills\\",
     "{{REASONIX_SKILLS}}"),
    (r"D:\\wpsyunpan\\229601413\\WPS云盘\\案件管理\\",
     "{{CASE_ROOT}}"),
    (r"D:\\anzhuang\\Reasonix",
     "{{REASONIX_INSTALL}}"),
    (r"C:\\Users\\13062",
     "{{HOME_WIN}}"),
    
    # 个人信息（长的先匹配）
    ("杜重阳律师", "{{USER_FULL_NAME}}"),
    ("杜重阳", "{{USER_FULL_NAME}}"),
    ("杜律师", "{{USER_SHORT_NAME}}"),
    ("上海申沪律师事务所", "{{USER_FIRM}}"),
    ("Dcylawer8888", "{{USER_WECHAT}}"),
    
    # 邮箱/电话（如有）
    # 这些需要具体匹配
]

# 版权保护：不碰这些行的替换
COPYRIGHT_BLACKLIST = re.compile(
    r"^\s*(author:|license:|Copyright|©)",
    re.IGNORECASE
)

SKIP_FILES = {"LICENSE", "LICENSE.txt", "LICENSE.md"}

EXCLUDE_SKILLS = {"law086", "case-study-report"}


def desensitize_file(filepath: str, dstpath: str) -> int:
    """替换文件内容，返回替换次数"""
    if os.path.basename(filepath) in SKIP_FILES:
        return 0
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        # 二进制文件，直接复制
        os.makedirs(os.path.dirname(dstpath), exist_ok=True)
        shutil.copy2(filepath, dstpath)
        return 0
    
    lines = content.split("\n")
    count = 0
    
    for i, line in enumerate(lines):
        if COPYRIGHT_BLACKLIST.search(line):
            continue
        
        for pattern, replacement in REPLACEMENTS:
            new_line = re.sub(pattern, replacement, line)
            if new_line != line:
                count += 1
                line = new_line
        lines[i] = line
    
    if count > 0:
        os.makedirs(os.path.dirname(dstpath), exist_ok=True)
        with open(dstpath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
    else:
        os.makedirs(os.path.dirname(dstpath), exist_ok=True)
        shutil.copy2(filepath, dstpath)
    
    return count


def desensitize_dir(srcdir: str, dstdir: str, mode: str = "skills"):
    """递归处理目录"""
    total_files = 0
    total_replacements = 0
    
    for root, dirs, files in os.walk(srcdir):
        # 跳过排除目录
        dirs[:] = [d for d in dirs if d != ".git" and d != "archive"]
        
        if mode == "skills":
            # 在 skills 模式下，跳过排除的 skill
            rel = os.path.relpath(root, srcdir)
            top = rel.split(os.sep)[0] if rel != "." else ""
            if top in EXCLUDE_SKILLS:
                dirs[:] = []
                continue
        
        for filename in files:
            srcfile = os.path.join(root, filename)
            relpath = os.path.relpath(srcfile, srcdir)
            dstfile = os.path.join(dstdir, relpath)
            
            n = desensitize_file(srcfile, dstfile)
            total_files += 1
            total_replacements += n
    
    return total_files, total_replacements


def main():
    if len(sys.argv) < 5:
        print("用法: python3 desensitize.py --src <源目录> --dst <目标目录> [--mode skills|memory]")
        sys.exit(1)
    
    args = sys.argv[1:]
    src = args[args.index("--src") + 1] if "--src" in args else None
    dst = args[args.index("--dst") + 1] if "--dst" in args else None
    mode = args[args.index("--mode") + 1] if "--mode" in args else "skills"
    
    if not src or not dst:
        print("缺少 --src 或 --dst 参数")
        sys.exit(1)
    
    print(f"脱敏模式: {mode}")
    print(f"源目录: {src}")
    print(f"目标目录: {dst}")
    print()
    
    nf, nr = desensitize_dir(src, dst, mode)
    print(f"✅ 完成: {nf} 个文件，{nr} 处替换")
    print(f"⛔ 版权行 (author/license/Copyright/©) 和 LICENSE 文件已跳过")
    print(f"🚫 已排除: law086/, case-study-report/, archive/")


if __name__ == "__main__":
    main()
