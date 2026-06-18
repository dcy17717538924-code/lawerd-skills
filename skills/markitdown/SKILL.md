---
name: markitdown
author: Microsoft
version: "1.2.0"
license: MIT
description: |
  MarkItDown|文档转Markdown|PDF转Markdown|Word转Markdown|Excel转Markdown|PPTX转Markdown|格式转换|文本提取。Use when用户要求"MarkItDown"、"文档转Markdown"、"PDF转Markdown"、"Word转Markdown"、"Excel转Markdown"、"PPTX转Markdown"、"办公文档格式转换"、"文本提取"。功能：基于 Microsoft 开源 MarkItDown(本地处理无需 API),支持 PDF/DOCX/DOC/PPTX/XLSX/EPUB/HTML/CSV/JSON/ZIP/YouTube/音频 等格式转换为 Markdown,保留表格、标题、列表结构。**本 skill 只做"有文字层文档"提取;扫描件 / 图片 OCR 走粽宝 IDE 多模态读图,不在本 skill 范围。**
  不要用于:法律分析(走 process-cases)、证据梳理(走 legal-evidence-mapping-mctmilk)、文书起草(走 draft-legal-docs)、扫描件 OCR(走 IDE 多模态读图)。
---

# MarkItDown

## 激活条件

- 律师提供 PDF / Word / PPT / Excel 等**有文字层**材料时
- 需要把任意文档格式转 Markdown 喂给 process-cases / case-management 经验库时

## 不在范围(2026-06-05 明确边界)

| 类型 | 走哪 |
|---|---|
| 扫描件 PDF(无文字层) | **粽宝 IDE 多模态读图** —— {{USER_SHORT_NAME}}把扫描页**直接发图**给我 |
| 单张图片 OCR | 同上,直接发图 |
| 嵌入图片的 PDF / Word(混合型) | markitdown 提文字,嵌入图手动发 |
| 法律分析 / 文书起草 | 走 process-cases / draft-legal-docs,不走本 skill |

**历史注脚**:v1.1.0 曾挂过 `markitdown-ocr` 插件 + LLM vision(MiniMax-M3)兜底链路,因接口 502 不稳 + IDE 多模态可直接发图触发,v1.2.0 砍掉,改用纯本地文本提取。`markitdown-ocr` 包仍留在环境中,以后真需要再临时启用。

## 功能特点

- **多格式支持**:PDF / DOCX / PPTX / XLSX / EPUB / HTML / CSV / JSON / XML / ZIP / YouTube URL / 音频(wav/mp3,可选)
- **保留结构**:标题、列表、表格、链接原样保留为 Markdown,非纯文本堆砌
- **本地处理**:`pip install "markitdown[pdf,docx,xlsx,pptx]"` 一次,无需 API key,无需云端
- **扫描件友好**:遇到无文字层输入,**stderr 明确报"扫描件,无文字层"**,不静默返回空字符串误导下游
- **微软维护**:Microsoft AutoGen 团队持续更新,GitHub 14万+ 星,MIT 协议
- **轻量**:Python 3.10+,无复杂环境依赖

## 与原 OCR 方案的关系(2026-06-05 重构)

| 维度 | 原 OCR(local-ocr) | 当前 MarkItDown |
|------|-------------------|-----------------|
| 引擎 | 百度 OCR / MinerU / PaddleOCR 三级 | `markitdown[pdf,docx,xlsx,pptx]` 纯本地 |
| 网络依赖 | 百度 / MinerU 需联网 | **完全本地** |
| API Key | 需百度 API Key / MinerU Token | **无需任何 key** |
| 文档结构 | 纯文本(无表格/标题) | Markdown(完整结构) |
| 格式覆盖 | 图片 + 扫描件 PDF | **有文字层** PDF + Office + ... |
| 扫描件 / 图片 OCR | 走百度 / MinerU | **走粽宝 IDE 多模态**(不归本 skill) |

**重构原因**:OCR 方案只解决"图片转文字"一个问题;MarkItDown 一个工具覆盖所有格式,且输出 LLM 友好的 Markdown,直接喂 process-cases / case-management 经验库。扫描件 OCR 走 IDE 多模态,链路更短、更稳。

## 安装(用户手动)

```powershell
& "{{CODEX_PYTHON}}" -m pip install "markitdown[pdf,docx,xlsx,pptx]"
```

**当前状态**(2026-06-05 17:20):✅ **纯本地文本提取就绪;扫描件走 IDE 多模态发图**
- `markitdown 0.1.6` ✅(本地 PDF / Office / HTML / 文本 提取)
- `pdfplumber 0.11.9` + `pdfminer.six` + `python-docx` + `python-pptx` + `openpyxl` ✅(markitdown 子依赖)
- ⚠️ `markitdown-ocr 0.1.0` 仍装在环境中(历史),**默认不启用、不读 .env、不传 LLM 凭证**
- ⚠️ `openai 2.41.0` 仍装在环境中(历史),同上
- ⚠️ `.env` 文件保留(不删除),但脚本不再读取,密钥不参与运行

## 使用方式

### 命令行(基础模式)

```powershell
# 单文件
python "{{REASONIX_SKILLS}}markitdown\scripts\markitdown_run.py" 案件.pdf

# 输出到指定文件
python "...\markitdown_run.py" 案件材料.pdf -o 案件材料.md

# 批量
python "...\markitdown_run.py" "{{CASE_ROOT}}张三--------合同纠纷\" --output "D:\md_output\"
```

**扫描件 PDF** 跑完后会在 stderr 看到:

```
[完成] xxx.pdf → xxx.md (0 chars) [扫描件,无文字层]
```

→ 此时请把扫描页**直接发图**给我,IDE 多模态读图链路处理。

### Python API

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert_local("判决书.pdf")
print(result.text_content)
# 扫描件返回空字符串,自行判断
```

## 桥接脚本(`scripts/markitdown_run.py`)

- 支持单文件/批量
- 支持自定义输出路径
- 失败容错:单文件失败不中断
- 扫描件 stderr 明确提示,无静默吞异常
- 跨平台(Windows / macOS / Linux)

**参数速查**:

| 参数 | 默认 | 说明 |
|------|------|------|
| `input` | 必填 | 文件或文件夹路径 |
| `-o` / `--output` | 输入同名 .md | 输出文件/文件夹 |
| `--version` | - | 显示 markitdown 版本 |

> v1.1.0 时代的 `--enable-plugins` / `--llm-*` / `--no-llm` / `--list-plugins` 已在 v1.2.0 移除。脚本不再读 `.env`、不构造 LLM 客户端、不加载 markitdown-ocr 插件。

## 在粽宝体系中的位置

- **被调用方**:case-management 经验库流程的"步骤 0 预处理"
- **调用方**:Mavis 律师助理(agent-lawyer-assistant)
- **关联 skill**:`process-cases` / `draft-legal-docs` / `case-study-report` 等需要 Markdown 文本输入的下游 skill
- **扫描件分流**:发现无文字层 → 提示{{USER_SHORT_NAME}}改发图,不喂下游,避免空 .md 误导 process-cases

详见 `memory/project/case-management/` 下的经验子文档。

## 变更历史

见 [CHANGELOG.md](./CHANGELOG.md)
