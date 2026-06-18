#!/usr/bin/env bash
# {{ASSISTANT_NAME}}律师助理 — 一键更新脚本 (macOS/Linux)
# 用法: bash scripts/update.sh
#
# 从 GitHub 拉取最新 skills，保留个人配置 (~/.reasonix/skills/personalization.yaml)
set -euo pipefail

REPO_URL="https://github.com/dcy17717538924-code/lawerd-skills.git"
TMP_DIR="/tmp/lawerd-skills-$$"
PERSONAL="$HOME/.reasonix/skills/personalization.yaml"

echo ""
echo "============================================================"
echo "  {{ASSISTANT_NAME}}律师助理 — 一键更新"
echo "============================================================"
echo ""

# ── 检查依赖 ──
for cmd in git python3; do
    if ! command -v "$cmd" &>/dev/null; then
        echo "  ❌ $cmd 未安装，请先安装。"
        exit 1
    fi
done

# ── 检查 personalization.yaml ──
if [ ! -f "$PERSONAL" ]; then
    echo "  ❌ 未找到 $PERSONAL"
    echo "     请先运行 python3 scripts/profile-wizard.py 生成配置。"
    exit 1
fi

echo "  ✅ 环境检查通过"
echo ""

# ── 1. 克隆最新版 ──
echo "  [1/4] 拉取最新版本..."
git clone --depth 1 "$REPO_URL" "$TMP_DIR"
echo "  ✅ 已克隆到 $TMP_DIR"
echo ""

# ── 2. 注入个人配置 ──
echo "  [2/4] 注入个人配置..."
python3 "$TMP_DIR/scripts/apply-personalization.py" \
    --dict "$PERSONAL" \
    --skills "$TMP_DIR/skills/" \
    --memory "$TMP_DIR/memory/global/"
echo ""

# ── 3. 合并覆盖 ──
echo "  [3/4] 合并覆盖到 ~/.reasonix/..."
mkdir -p "$HOME/.reasonix/skills" "$HOME/.reasonix/memory/global"
cp -r "$TMP_DIR/skills/"*        "$HOME/.reasonix/skills/"
cp -r "$TMP_DIR/memory/global/"* "$HOME/.reasonix/memory/global/"
echo "  ✅ 合并完成（personalization.yaml 不受影响）"
echo ""

# ── 4. 清理 ──
echo "  [4/4] 清理临时文件..."
rm -rf "$TMP_DIR"
echo "  ✅ 清理完成"
echo ""

echo "============================================================"
echo "  更新完成 ✅  你的个人配置完好无损。"
echo "============================================================"
echo ""
