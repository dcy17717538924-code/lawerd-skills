# {{ASSISTANT_NAME}}律师助理 — 环境自检 (Windows PowerShell)
# 用法: powershell -File env-check.ps1

$ErrorActionPreference = "SilentlyContinue"

$Home = $env:USERPROFILE
$ReasonixDir = "$Home\.reasonix"
$SkillsDir = "$ReasonixDir\skills"
$MineruToken = "$Home\Desktop\mineru.txt"
$WhisperModel = "$Home\.cache\whisper\medium.pt"

$checks = @()

function Add-Check($name, $ok, $detail, $hint) {
    $global:checks += @{ Name = $name; Ok = $ok; Detail = $detail; Hint = $hint }
}

# ── 检查项 ───────────────────────────────────────────

# Reasonix Code
if (Test-Path $ReasonixDir) {
    Add-Check "Reasonix Code" $true $ReasonixDir ""
} else {
    Add-Check "Reasonix Code" $false "未找到 ~\.reasonix\" "请先安装 Reasonix Code"
}

# skills 目录
if (Test-Path $SkillsDir) {
    Add-Check "skills 目录" $true $SkillsDir ""
} else {
    Add-Check "skills 目录" $false "未找到 ~\.reasonix\skills\" "mkdir ~\.reasonix\skills"
}

# Python 3
$python = Get-Command python3 -ErrorAction SilentlyContinue
if (-not $python) { $python = Get-Command python -ErrorAction SilentlyContinue }
if ($python) {
    $ver = & $python.Source --version 2>&1
    Add-Check "Python 3" $true "$($python.Source) -> $ver" ""
} else {
    Add-Check "Python 3" $false "python3 不可用" "从 https://python.org 下载安装"
}

# Git
$git = Get-Command git -ErrorAction SilentlyContinue
if ($git) {
    $ver = & git --version 2>&1
    Add-Check "Git" $true $ver ""
} else {
    Add-Check "Git" $false "git 不可用" "从 https://git-scm.com 下载安装"
}

# mineru token
if (Test-Path $MineruToken) {
    Add-Check "mineru token (OCR)" $true $MineruToken ""
} else {
    Add-Check "mineru token (OCR)" $false "未找到 mineru token" "将 token 文件放到 ~\Desktop\mineru.txt（可选）"
}

# whisper 模型
if (Test-Path $WhisperModel) {
    $size = [math]::Round((Get-Item $WhisperModel).Length / 1MB)
    Add-Check "whisper 模型 (语音)" $true "$WhisperModel ($size MB)" ""
} else {
    Add-Check "whisper 模型 (语音)" $false "未下载 whisper 模型" "下载到 ~\.cache\whisper\medium.pt（可选）"
}

# ── 输出表格 ─────────────────────────────────────────

Write-Host ""
Write-Host "=" * 60
Write-Host "  {{ASSISTANT_NAME}}律师助理 — 环境自检 (Windows)"
Write-Host "=" * 60
Write-Host ""

$allOk = $true
foreach ($c in $checks) {
    if ($c.Ok) {
        $icon = "[OK]"
    } elseif ($c.Name -match "可选") {
        $icon = "[WARN]"
    } else {
        $icon = "[FAIL]"
        $allOk = $false
    }
    Write-Host "  $icon $($c.Name): $($c.Detail)"
    if (-not $c.Ok -and $c.Hint) {
        Write-Host "     -> $($c.Hint)"
    }
}

Write-Host ""
if ($allOk) {
    Write-Host "  全部必需项通过 [OK]  可以继续安装。"
} else {
    Write-Host "  [FAIL] 存在未通过项，请处理后再继续。"
}
Write-Host ""
