#!/usr/bin/env python3
"""{{ASSISTANT_NAME}}律师助理 — 占位符替换引擎 (跨平台)

读取 personalization.yaml，遍历 skills/ 和 memory/ 目录，
将所有 {{PLACEHOLDER}} 替换为用户实际值。

署名保护黑名单（硬编码，不可通过参数覆盖）：
- 跳过 author: 行
- 跳过 license: 行
- 跳过 Copyright / © 行
- 跳过 LICENSE / LICENSE.txt 文件

用法:
  python3 apply-personalization.py --dict personalization.yaml --skills skills/ --memory memory/global/

  注意：--memory 指向全局记忆目录（memory/global/）。项目记忆（memory/project/）不通过本脚本处理，
  安装时由 AG 通过 remember 工具逐条写入。
"""

import argparse
import os
import re
import sys
from pathlib import Path

# ── 署名保护黑名单 ──────────────────────────────────
# 这些行/文件在任何情况下都不允许被修改

COPYRIGHT_BLACKLIST_LINES = [
    re.compile(r"^\s*author:", re.IGNORECASE),
    re.compile(r"^\s*license:", re.IGNORECASE),
    re.compile(r"Copyright", re.IGNORECASE),
    re.compile(r"©"),
    re.compile(r"作者："),
    re.compile(r"许可证："),
]

COPYRIGHT_BLACKLIST_FILES = {
    "LICENSE",
    "LICENSE.txt",
    "LICENSE.md",
}

PLACEHOLDER_RE = re.compile(r"\{\{(\w+)\}\}")


def load_dict(path: str) -> dict:
    """加载 personalization.yaml → {PLACEHOLDER: value}"""
    mapping = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                key, _, value = line.partition(":")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                mapping[key] = value
    return mapping


def is_copyright_line(line: str) -> bool:
    """检查行是否属于版权保护范围"""
    return any(pattern.search(line) for pattern in COPYRIGHT_BLACKLIST_LINES)


def should_skip_file(filepath: Path) -> bool:
    """检查文件是否属于版权保护范围"""
    return filepath.name in COPYRIGHT_BLACKLIST_FILES


def replace_in_file(filepath: Path, mapping: dict) -> int:
    """替换文件中的占位符，返回替换次数"""
    if should_skip_file(filepath):
        return 0

    try:
        original = filepath.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return 0  # 跳过二进制文件

    lines = original.split("\n")
    count = 0

    for i, line in enumerate(lines):
        if is_copyright_line(line):
            continue

        def replacer(match):
            nonlocal count
            key = match.group(1)
            if key in mapping:
                count += 1
                return mapping[key]
            return match.group(0)

        new_line = PLACEHOLDER_RE.sub(replacer, line)
        if new_line != line:
            lines[i] = new_line

    if count > 0:
        filepath.write_text("\n".join(lines), encoding="utf-8")

    return count


def replace_in_dir(dirpath: str, mapping: dict) -> tuple:
    """递归替换目录下所有文件的占位符，返回 (文件数, 替换次数)"""
    total_files = 0
    total_replacements = 0

    for root, dirs, files in os.walk(dirpath):
        # 跳过 .git 目录
        dirs[:] = [d for d in dirs if d != ".git"]
        for filename in files:
            filepath = Path(root) / filename
            n = replace_in_file(filepath, mapping)
            total_files += 1
            total_replacements += n

    return total_files, total_replacements


def main():
    parser = argparse.ArgumentParser(description="{{ASSISTANT_NAME}}律师助理 — 占位符替换引擎")
    parser.add_argument("--dict", required=True, help="personalization.yaml 路径")
    parser.add_argument("--skills", required=True, help="skills/ 目录路径")
    parser.add_argument("--memory", required=True, help="memory/global/ 目录路径（全局记忆）")
    args = parser.parse_args()

    # 加载映射表
    mapping = load_dict(args.dict)
    if not mapping:
        print("❌ personalization.yaml 为空，请先运行 profile-wizard.py", file=sys.stderr)
        sys.exit(1)

    print()
    print("=" * 60)
    print("  {{ASSISTANT_NAME}}律师助理 — 占位符替换")
    print("=" * 60)
    print()

    # 预览替换表
    print("  占位符 → 实际值：")
    for key, value in mapping.items():
        print(f"    {{{{ {key} }}}} → {value}")
    print()

    # 替换 skills/
    if os.path.isdir(args.skills):
        nf, nr = replace_in_dir(args.skills, mapping)
        print(f"  ✅ skills/: {nf} 个文件，{nr} 处替换")
    else:
        print(f"  ⚠️  skills/ 目录不存在: {args.skills}")

    # 替换 memory/
    if os.path.isdir(args.memory):
        nf, nr = replace_in_dir(args.memory, mapping)
        print(f"  ✅ memory/: {nf} 个文件，{nr} 处替换")
    else:
        print(f"  ⚠️  memory/ 目录不存在: {args.memory}")

    print()
    print(f"  ⛔ 署名行 (author/license/Copyright/©) 和 LICENSE 文件已自动跳过，未被修改。")
    print()
    print(f"  💡 项目记忆（memory/project/）不通过本脚本部署，安装后由 AG 使用 remember 工具写入。")
    print()
    print("=" * 60)
    print("  替换完成 ✅")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
