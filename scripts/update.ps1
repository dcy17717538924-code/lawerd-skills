# {{ASSISTANT_NAME}}律师助理 — 一键更新脚本 (Windows PowerShell)
# 用法: powershell -File scripts/update.ps1
#
# 从 GitHub 拉取最新 skills，保留个人配置 (~/.reasonix/skills/personalization.yaml)

$ErrorActionPreference = "Stop"

$RepoUrl = "https://github.com/dcy17717538924-code/lawerd-skills.git"
$HomeDir = $env:USERPROFILE
$TmpDir = "$env:TEMP\lawerd-skills-$PID"
$Personal = "$HomeDir\.reasonix\skills\personalization.yaml"

Write-Host ""
Write-Host "=" * 60
Write-Host "  {{ASSISTANT_NAME}}律师助理 — 一键更新 (Windows)"
Write-Host "=" * 60
Write-Host ""

# ── 检查依赖 ──
$missing = @()
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { $missing += "git" }
if (-not (Get-Command python3 -ErrorAction SilentlyContinue) -and -not (Get-Command python -ErrorAction SilentlyContinue)) { $missing += "python3/python" }

if ($missing.Count -gt 0) {
    Write-Host "  ❌ 缺少: $($missing -join ', ')，请先安装。"
    exit 1
}

# ── 检查 personalization.yaml ──
if (-not (Test-Path $Personal)) {
    Write-Host "  ❌ 未找到 $Personal"
    Write-Host "     请先运行 python3 scripts/profile-wizard.py 生成配置。"
    exit 1
}

Write-Host "  ✅ 环境检查通过"
Write-Host ""

# ── 1. 克隆最新版 ──
Write-Host "  [1/4] 拉取最新版本..."
git clone --depth 1 $RepoUrl $TmpDir
Write-Host "  ✅ 已克隆到 $TmpDir"
Write-Host ""

# ── 确定 python 命令 ──
$python = if (Get-Command python3 -ErrorAction SilentlyContinue) { "python3" } else { "python" }

# ── 2. 注入个人配置 ──
Write-Host "  [2/4] 注入个人配置..."
& $python "$TmpDir/scripts/apply-personalization.py" `
    --dict $Personal `
    --skills "$TmpDir/skills/" `
    --memory "$TmpDir/memory/global/"
Write-Host ""

# ── 3. 合并覆盖 ──
Write-Host "  [3/4] 合并覆盖到 ~/.reasonix/..."
New-Item -ItemType Directory -Force -Path "$HomeDir\.reasonix\skills" | Out-Null
New-Item -ItemType Directory -Force -Path "$HomeDir\.reasonix\memory\global" | Out-Null
Copy-Item -Recurse -Force "$TmpDir/skills/*"        "$HomeDir\.reasonix\skills\"
Copy-Item -Recurse -Force "$TmpDir/memory/global/*" "$HomeDir\.reasonix\memory\global\"
Write-Host "  ✅ 合并完成（personalization.yaml 不受影响）"
Write-Host ""

# ── 4. 清理 ──
Write-Host "  [4/4] 清理临时文件..."
Remove-Item -Recurse -Force $TmpDir -ErrorAction SilentlyContinue
Write-Host "  ✅ 清理完成"
Write-Host ""

Write-Host "=" * 60
Write-Host "  更新完成 ✅  你的个人配置完好无损。"
Write-Host "=" * 60
Write-Host ""
