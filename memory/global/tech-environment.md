---
name: tech-environment
description: 技术环境自检指引：检测→缺则安装→验证，覆盖 Python、pip 包、whisper、文件清理、OCR
type: reference
scope: global
created: 2026-06-08
priority: high
---

# 技术环境自检

> 安装 lawerd-skills 后按以下顺序逐项检测，缺则安装，装完验证。

## 1. Python 运行环境

### 检测
```bash
{{CODEX_PYTHON}} --version
```
预期输出：`Python 3.12.x`（或其他 ≥3.10 版本）。

若 `{{CODEX_PYTHON}}` 不可用，检查 Reasonix Code 安装目录下的内置 Python：
- Windows：`C:\Users\<用户名>\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`
- macOS / Linux：`~/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`

### 安装（若缺失）
- Windows：从 https://www.python.org/downloads/ 下载 Python 3.10+，安装时勾选 "Add Python to PATH"
- macOS：`brew install python@3.12`
- Linux：`sudo apt install python3.12 python3.12-venv`

### 验证
```bash
{{CODEX_PYTHON}} -c "import sys; print(sys.version)"
```

---

## 2. 必需 pip 包

以下包被多个 skill 依赖：`python-docx`、`lxml`、`pypdf`、`openpyxl`、`Pillow`、`beautifulsoup4`、`cryptography`、`python-dateutil`、`defusedxml`。

### 检测
```bash
{{CODEX_PYTHON}} -c "import docx, lxml, pypdf, openpyxl, PIL, bs4, cryptography, dateutil, defusedxml; print('OK')"
```
若输出 `OK` 则全部就绪。若报 `ModuleNotFoundError`，记下缺失的包名。

### 安装
```bash
{{CODEX_PYTHON}} -m pip install python-docx lxml pypdf openpyxl Pillow beautifulsoup4 cryptography python-dateutil defusedxml
```

### 验证
重新运行检测命令，确认输出 `OK`。

---

## 3. 语音识别（Whisper）

> `openai-whisper` + `medium.pt` 模型，本地运行无需联网。模型约 1.5GB。

### 检测
```bash
{{CODEX_PYTHON}} -c "import whisper; whisper.load_model('medium'); print('Whisper OK')"
```
若输出 `Whisper OK` 则就绪。若报模型不存在，仅需下载模型。

### 安装
```bash
{{CODEX_PYTHON}} -m pip install openai-whisper
```

模型首次调用时自动下载到 `{{HOME_WIN}}\.cache\whisper\medium.pt`，或手动：
```bash
{{CODEX_PYTHON}} -c "import whisper; whisper.load_model('medium')"
```

### 验证
```bash
{{CODEX_PYTHON}} -c "import whisper; m=whisper.load_model('medium'); print(type(m).__name__)"
```
预期：`Whisper`

---

## 4. 文件清理

跨平台走回收站（避免 `rm` 误删）。

### Windows（PowerShell）
```powershell
Add-Type -AssemblyName Microsoft.VisualBasic
[Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile($path, 'OnlyErrorDialogs', 'SendToRecycleBin')
```

### macOS
```bash
osascript -e "tell app \"Finder\" to delete POSIX file \"$path\""
```

### Linux
```bash
gio trash "$path"  # GNOME
kioclient move "$path" trash:/  # KDE
```

---

## 5. OCR / 格式转换

### MinerU OCR Token

#### 检测
检查 `~/Desktop/mineru.txt` 是否存在且非空。

#### 安装
从 MinerU 平台获取 API token，写入 `~/Desktop/mineru.txt`。

#### 验证
调用方式见 `skills/mineru-ocr/SKILL.md`。

### MarkItDown

通过 pip 安装，调用方式见 `skills/markitdown/SKILL.md`。
