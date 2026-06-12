---
name: tech-environment
description: 技术环境：Python 3.12.13 完整路径 + mineru-ocr 调用方式 + markitdown 用法 + 文件清理方案
type: reference
scope: global
created: 2026-06-08
priority: high
---
# 技术环境

## Python 运行环境

> **重要**：`python` 不在系统 PATH 中（PATH 里的 `python.exe` 是 Microsoft Store 占位符，不可用）。运行 Python 脚本必须使用完整路径。

| 环境 | 完整路径 | 版本 | 用途 |
|------|----------|------|------|
| **codex runtime** | `{{CODEX_PYTHON}}` | 3.12.13 | 通用 Python 脚本 |

- codex runtime 是单文件便携 Python，标准库完整
- 已装第三方包：`python-docx`、`lxml`、`beautifulsoup4`、`cryptography`、`dateutil`、`defusedxml` 等
- 需要未安装的第三方包时，用 `{{CODEX_PYTHON}} -m pip install <pkg>` 安装

## OCR 方案

> **背景**：当前运行的 deepseek-v4-pro 无多模态/视觉能力，无法直接识图。使用以下两套 OCR 方案互补。

| 方案 | 适用场景 | 调用方式 |
|------|----------|----------|
| **mineru-ocr**（主） | 中文扫描件、复杂版式 PDF、批量处理 | `{{CODEX_PYTHON}} scripts/mineru_parse.py batch "<目录>" --is-ocr --model vlm` |
| **markitdown**（辅） | 普通可复制 PDF/Docx/PPTX | `{{CODEX_PYTHON}} -m markitdown "<文件>"` |

### mineru-ocr 调用要点
- Token 存放位置：`{{MINERU_TOKEN_PATH}}`（默认 `~/Desktop/mineru.txt`，可通过 `--token-file` 或环境变量 `MINERU_TOKEN` 覆盖）
- 三种模式：`url <URL>`（远程）/ `file <PATH>`（单文件）/ `batch <DIR>`（批量，单批 ≤50 个文件）
- 限额：文件 ≤200MB，页数 ≤200 页，每天 1000 页优先额度
- 默认模型 `vlm`（推荐），可切 `pipeline`（快）或 `MinerU-HTML`
- Windows 一键：`mineru_parse.bat batch "D:\...\材料目录" --is-ocr`

### markitdown 调用要点
- 支持格式：PDF/DOCX/DOC/PPTX/XLSX/EPUB/HTML/CSV/JSON → Markdown
- 保留表格、标题、列表结构
- 本地处理，无需 API

## 语音识别

> `openai-whisper` (20250625) + `medium.pt` 模型，本地运行，无需联网。

| 项目 | 路径 |
|------|------|
| Python 解释器 | `{{CODEX_PYTHON}}` |
| 模型文件 | `~/.cache/whisper/medium.pt` (1.53 GB) |

调用示例：
```python
import whisper
model = whisper.load_model("medium")  # 自动从 ~/.cache/whisper/ 读取
result = model.transcribe("音频文件.mp3")
print(result["text"])
```

模型文件全局共享，所有项目用同一个解释器路径即可调用。

## 文件清理

| 平台 | 命令 |
|------|------|
| **Windows** | PowerShell VB.NET FileIO 走回收站 |
| **macOS** | `osascript -e 'tell app "Finder" to delete POSIX file "$path"'` 或 `trash` 命令 |

Windows 示例（可恢复）：
```powershell
Add-Type -AssemblyName Microsoft.VisualBasic
[Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile($path, 'OnlyErrorDialogs', 'SendToRecycleBin')
[Microsoft.VisualBasic.FileIO.FileSystem]::DeleteDirectory($path, 'OnlyErrorDialogs', 'SendToRecycleBin')
```
