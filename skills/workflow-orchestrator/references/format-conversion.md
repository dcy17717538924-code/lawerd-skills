## 格式转换预处理策略(2026-06-05 重构,2026-06-05 升级)

几乎所有律师提供的材料都需要先转成结构化文本(Markdown)再喂给后续分析。**OCR 方案已整体退役**(百度 OCR / MinerU / PaddleOCR 三级引擎全部下线),改用:

- **[[markitdown]] skill**：微软开源 MarkItDown,`pip install 'markitdown[pdf,docx,xlsx,pptx]'`,本地处理无需 API
- **markitdown-ocr 插件**(可选,2026-06-05 新增):`pip install markitdown-ocr openai`,接管 PDF/DOCX/PPTX/XLSX 嵌入图片 + 扫描件 OCR
- **LLLM 多模态兜底**:对图片 / 扫描件等 MarkItDown 不能直接吃的情况,直接丢给当前 LLM(MiniMax-M3 支持 vision),让模型读图后输出结构化描述

### 材料类型识别

拿到材料后,先按扩展名分类:

| 类型 | 扩展名 | 首选方案 | 输出 |
|------|--------|----------|------|
| 文档(PDF/Word/PPT/Excel) | .pdf .docx .pptx .xlsx | **MarkItDown** | Markdown(保留表格/标题/列表/链接) |
| 图片 | .jpg .jpeg .png .bmp .tif .tiff .webp | **LLLM 多模态**(MiniMax-M3 vision) | Markdown 描述 |
| 扫描件 PDF(无文字层) | .pdf 但文本提取为空 | MarkItDown → 失败 → LLM 多模态逐页读图 | Markdown |
| 音频(.wav/.mp3) | .wav .mp3 | MarkItDown[audio-transcription](可选) | 转写文本 |
| HTML / CSV / JSON / XML / EPUB | .html .csv .json .xml .epub | **MarkItDown** | Markdown |
| YouTube 链接 | URL | MarkItDown(自动抓字幕) | 转写文本 |
| 微信图片/截图 | 无扩展名 / .dat | LLM 多模态 | Markdown 描述 |

### 转换调用链路(2026-06-05 升级,markitdown-ocr 接管)

```
材料进入
  ↓
按扩展名识别类型
  ↓
┌─ 文档(PDF/Office) ─→ MarkItDown.convert_local(file)
│                       ↓ 启用 markitdown-ocr 插件时
│                       ├─ 提取文字层 + 表格 + 标题(快路径)
│                       └─ 文档嵌入图片逐张 LLM vision OCR(慢路径,自动)
│                       ↓ 仍失败(扫描件 / 损坏)
│                     LLM 多模态逐页读图(桥接脚本兜底)
│
├─ 图片 ─────────────→ LLM 多模态(image → Markdown 描述)
│                       ↓ 失败(模型拒答)
│                     提示律师手工提供文本
│
├─ 音频 ─────────────→ MarkItDown[audio-transcription] (可选)
│
├─ HTML/CSV/JSON/XML/EPUB ─→ MarkItDown.convert_local(file)
│
└─ YouTube URL ────────→ MarkItDown 自动抓字幕
```

**关键变化**:扫描件 PDF / 嵌入图片 OCR 这块,以前是"MarkItDown 失败 → LLM 多模态兜底"的两步手动路径,**现在 markitdown-ocr 插件封装了 LLM vision 为可注册的 converter**,MarkItDown 内部自动走,无需 workflow 介入。

### MarkItDown 调用示例

```python
from markitdown import MarkItDown
from pathlib import Path

# 基础模式(纯文字 PDF / Office)
md = MarkItDown()
result = md.convert_local(str(file_path))
print(result.text_content)
```

或 LLM 视觉兜底(图片/扫描件/嵌入图):
```python
from markitdown import MarkItDown
from openai import OpenAI

md = MarkItDown(
    enable_plugins=True,            # 让 markitdown-ocr 接管嵌入图片
    llm_client=OpenAI(
        base_url="https://agent.minimaxi.com/mavis/api/v1/llm/v1",
        api_key="sk-...",
    ),
    llm_model="MiniMax-M3",         # mavis 当前 LLM(支持 vision)
)
result = md.convert_local("扫描件判决书.pdf")
print(result.text_content)
```

完整参数链(2026-06-05 升级)见 [[markitdown]]。

### 批量处理规则

- 文件夹内文件按扩展名自动分发
- `markitdown` skill 提供 `scripts/markitdown_run.py`(律师助理目录下),支持:
  - 单文件:`python markitdown_run.py <file>`
  - 批量:`python markitdown_run.py <folder> --output <out_dir>`

### 输出处理

- MarkItDown 输出 Markdown → 直接作为材料内容喂给 [[process-cases]] / [[workflow-orchestrator]]
- LLM 多模态输出 Markdown 描述 → 同上
- 保留结构(标题/表格/列表/链接),中文 OCR 准确率 ≥99%(LLM vision 模式)

### 失败处理

- 单文件转换失败 → 标记该文件,继续处理其余
- 全部方案失败 → 告知律师"以下文件无法识别:[列表]",请律师提供可读版本
- MarkItDown 包未装 → 提示律师运行 `pip install 'markitdown[pdf,docx,xlsx,pptx]'`

### 环境依赖(2026-06-05 升级)

| 方案 | 依赖 | 安装 |
|------|------|------|
| MarkItDown 基础 | `markitdown` Python 包 + extras[pdf,docx,xlsx,pptx] | `pip install 'markitdown[pdf,docx,xlsx,pptx]'` |
| 嵌入图片 OCR(2026-06-05 新增) | `markitdown-ocr` + `openai` | `pip install markitdown-ocr openai` |
| LLM 多模态 | 当前 LLM(MiniMax-M3) | 已在 mavis config 中配置,桥接脚本读 `.env` |
| 音频转写(可选) | MarkItDown[audio-transcription] | `pip install 'markitdown[audio-transcription]'` |

### 历史

- 2026-05-30 ~ 2026-06-04: 使用百度 OCR + MinerU + PaddleOCR 三级方案
- 2026-06-05 上午: 整体退役,改用 MarkItDown + LLM 多模态(本文件初版)
- 2026-06-05 下午: markitdown-ocr 插件接管嵌入图片 OCR,LLM 视觉路径封装到桥接脚本(本版升级)
- 详见 `CHANGELOG.md` v2.4.0
