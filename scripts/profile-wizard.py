#!/usr/bin/env python3
"""{{ASSISTANT_NAME}}律师助理 — 个人信息配置向导 (跨平台)

交互式问答，收集律师个人信息和案件路径，
生成 ~/.reasonix/skills/personalization.yaml，
供 apply-personalization.py 使用。
"""

import os
import sys
from pathlib import Path

HOME = Path.home()
OUTPUT = HOME / ".reasonix" / "skills" / "personalization.yaml"

DEFAULTS = {
    "USER_FULL_NAME": "",
    "USER_SHORT_NAME": "",
    "USER_WECHAT": "",
    "USER_FIRM": "",
    "USER_CITY": "上海",
    "USER_PHONE": "",
    "USER_EMAIL": "",
    "CASE_ROOT": "",
    "ARCHIVE_ROOT": "",
    "WPS_ROOT": "",
    "MINERU_TOKEN_PATH": "",
}


def ask(prompt: str, default: str = "") -> str:
    if default:
        value = input(f"  {prompt} [{default}]: ").strip()
    else:
        value = input(f"  {prompt}: ").strip()
    return value if value else default


def validate():
    """收集并验证所有字段"""
    print()
    print("=" * 60)
    print("  {{ASSISTANT_NAME}}律师助理 — 个人信息配置")
    print("=" * 60)
    print()
    print("请输入以下信息（直接回车使用默认值）：")
    print()

    values = {}

    # ── 个人信息 ───────────────────────────────
    print("── 基本信息 ──")
    values["USER_FULL_NAME"] = ask("您的全名（如"张伟律师"）")
    values["USER_SHORT_NAME"] = ask("日常怎么称呼您（如"张律师"）")
    values["USER_WECHAT"] = ask("微信号")
    values["USER_FIRM"] = ask("律所全称")
    values["USER_CITY"] = ask("所在城市", DEFAULTS["USER_CITY"])
    print()
    print("── 联系方式 ──")
    values["USER_PHONE"] = ask("联系电话")
    values["USER_EMAIL"] = ask("电子邮箱")
    print()

    # ── 路径配置 ───────────────────────────────
    print("── 工作路径 ──")

    # 根据平台给不同的默认路径提示
    if sys.platform == "win32":
        case_hint = f"{HOME}\\Documents\\案件\\"
        archive_hint = f"{HOME}\\Documents\\归档\\"
    else:
        case_hint = f"{HOME}/Documents/案件/"
        archive_hint = f"{HOME}/Documents/归档/"

    values["CASE_ROOT"] = ask(f"案件文件存放根目录", case_hint)
    values["ARCHIVE_ROOT"] = ask(f"结案归档根目录", archive_hint)
    wps_hint = f"{HOME}\\Documents\\WPS云盘\\" if sys.platform == "win32" else f"{HOME}/Documents/WPS云盘/"
    values["WPS_ROOT"] = ask(f"WPS 云盘根目录", wps_hint)
    print()
    print("── 外部服务 ──")
    mineru_default = f"{HOME}/Desktop/mineru.txt"
    values["MINERU_TOKEN_PATH"] = ask(f"MinerU OCR Token 文件路径", mineru_default)

    # ── 确认 ───────────────────────────────────
    print()
    print("── 确认信息 ──")
    print()
    for key, value in values.items():
        print(f"  {key}: {value}")
    print()

    confirm = input("  以上信息确认无误？[Y/n]: ").strip().lower()
    if confirm and confirm not in ("y", "yes", ""):
        print()
        print("  已取消。请重新运行本向导。")
        sys.exit(0)

    return values


def generate(values: dict):
    """生成 personalization.yaml"""
    lines = [
        "# {{ASSISTANT_NAME}}律师助理 — 个性化配置",
        f"# 生成时间: {__import__('datetime').datetime.now().isoformat()}",
        "# 此文件包含个人敏感信息，请勿提交到公开仓库。",
        "#",
        "# 占位符 → 实际值 映射表",
        "# apply-personalization.py 读取此文件，替换所有 skill/memory 中的占位符。",
        "",
    ]
    for key, value in values.items():
        lines.append(f"{key}: \"{value}\"")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print()
    print("=" * 60)
    print(f"  ✅ 配置已保存到 {OUTPUT}")
    print("=" * 60)
    print()
    print("  下一步：运行 apply-personalization.py 将配置注入 skill 和 memory 文件。")
    print()
    print("  ⚠️  安装完成后，AG 读取 du-lawyer-profile.md 时会触发 5 个硬钩子：")
    print("     HOOK-1  基本信息确认")
    print("     HOOK-2  执业领域确认（增/删/改）")
    print("     HOOK-3  个人背景确认（逐条保留/删除/修改）")
    print("     HOOK-4  工作习惯确认（影响 AG 回复风格）")
    print("     HOOK-5  配合模式确认（工作节奏）")
    print("     以上均不可跳过。")
    print()


def main():
    values = validate()
    generate(values)


if __name__ == "__main__":
    main()
