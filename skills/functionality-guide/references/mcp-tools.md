# MCP 工具服务 — 底层能力供给

> **2026-06-05 更新**:原 baidu-ocr / mineru-ocr MCP 服务已退役(随 OCR 方案整体下线),文档解析由 `markitdown` skill 接管,扫描件/图片走 Mavis 当前 LLM(MiniMax-M3)vision 多模态。

Mavis 体系当前用到的 MCP 工具由 Codex 配置文件管理,无需独立 SKILL.md。本文件仅记录在用工具,退役工具已删。

---

## markitdown — 一站式文档解析

**功能**:Microsoft 开源 MarkItDown — 把 PDF/Word/PPT/Excel/HTML/CSV/JSON/XML/EPUB/ZIP/YouTube/音频 转 Markdown,本地处理无需 API

**工具**:`scripts/markitdown_run.py`(单文件/批量)

**支持格式**:
- 文档:`[pdf]` `.pdf` / `[docx]` `.docx` / `[pptx]` `.pptx` / `[xlsx]` `.xlsx`
- 多媒体:`[audio-transcription]` `.wav` `.mp3` / `[youtube-transcription]` YouTube URL
- 文本:`.html` `.csv` `.json` `.xml` `.epub` `.zip`

**适用场景**:
- 律师办公文档批量转 Markdown 喂 AI 分析
- 法院 PDF 判决书提取全文
- Excel 表格转 Markdown
- 替代原 baidu-ocr / mineru-ocr 全部场景

**完整说明**:见 `markitdown.md` reference

---

## LLM 多模态 — 扫描件/图片兜底

**功能**:Mavis 当前 LLM(MiniMax-M3)vision 接口,直接读图输出结构化 Markdown 描述

**工具**:`markitdown --use-plugins` 配合 `llm_client` / `llm_model`,或直接调 mavis 的 LLM vision 端点

**支持格式**:`.jpg` `.jpeg` `.png` `.bmp` `.tif` `.tiff` `.webp`

**适用场景**:
- MarkItDown 转换失败(扫描件 PDF 无文字层)
- 微信截图/无扩展名图片
- 需要中文 OCR 但不想走第三方云引擎

**前置条件**:
- `pip install markitdown-ocr`(可选,OCR 增强插件)
- `pip install openai`(或任何 OpenAI 兼容客户端)
- Mavis 当前 LLM API Key 已配置

**完整说明**:见 `markitdown.md` reference + `agent-lawyer-assistant/skills/workflow-orchestrator/references/format-conversion.md`

---

## everything-search — Windows 文件秒搜

**功能**:调用 Everything 引擎在 Windows 中按文件名秒搜

**工具**:`search_files(query, max_results=30)` — 关键词搜索,返回匹配路径

**适用场景**:
- 快速定位文件
- 查找特定格式文件
- 全局文件名检索

---

## 格式转换选择策略(2026-06-05 更新)

| 场景 | 推荐 | 原因 |
|------|------|------|
| PDF 判决书/合同/法规 | `markitdown` | 保留表格/标题/列表,本地处理 |
| Word 文档 | `markitdown` | 结构完整 |
| PPT/Excel 表格 | `markitdown` | 表格转 Markdown 表格 |
| 扫描件 PDF(无文字层) | `markitdown` → 失败 → **LLM vision** | 两层兜底 |
| 图片 OCR | **LLLM vision**(MiniMax-M3) | 中文识别精度高,无需 API key |
| 微信截图/无扩展名 | **LLM vision** | 直接读图 |
| 音频转写 | `markitdown[audio-transcription]` | 可选,whisper 集成 |
| YouTube 链接 | `markitdown[youtube-transcription]` | 自动抓字幕 |
| 旧 OCR 引擎(baidu/mineru/paddle) | ❌ **已退役**,别用 | 2026-06-05 整体下线 |

**优先级**:`markitdown` 优先 → LLM vision 兜底 → 都不行再告知律师
