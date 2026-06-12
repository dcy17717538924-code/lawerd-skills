# markitdown

**功能**：Microsoft 开源 MarkItDown 桥接 — 一站式把 PDF/Word/PPT/Excel/HTML/CSV/JSON/XML/EPUB/ZIP/YouTube/音频 全部转 Markdown,本地处理无需 API

**触发词**：MarkItDown、文档转 Markdown、PDF 转 Markdown、Word 转 Markdown、Excel 转 Markdown、PPTX 转 Markdown、办公文档格式转换、文本提取、扫描件提取

**适用场景**：
- 律师提供 PDF 判决书/合同/法规全文 → 转 Markdown 喂 process-cases / workflow-orchestrator
- 法院 PDF 判决书批量提取文字
- 扫描件/图片走 LLM vision 兜底
- Excel 表格转 Markdown 表格
- PowerPoint 提取内容
- 音频文件转写(可选)
- 旧 OCR 方案的整体替代(2026-06-05 退役)

**支持格式**(取决于 pip install 时的 extras)：
- 文档:`[pdf]` `.pdf` / `[docx]` `.docx` / `[pptx]` `.pptx` / `[xlsx]` `.xlsx`
- 多媒体:`[audio-transcription]` `.wav` `.mp3`(可选) / `[youtube-transcription]` YouTube URL(可选)
- 文本:`.html` `.csv` `.json` `.xml` `.epub` `.zip`
- 图片:走 LLM vision(Mavis 当前 LLM:MiniMax-M3 支持),不走本 skill 桥接

**安装**(用户手动,2026-06-05 落地时尚未自动装)：
```powershell
& "{{CODEX_PYTHON}}" -m pip install "markitdown[pdf,docx,xlsx,pptx]"
```

**使用方式**：
```powershell
# 单文件
python "{{HOME_WIN}}\.mavis\agents\agent-lawyer-assistant\skills\markitdown\scripts\markitdown_run.py" 案件.pdf

# 批量
python "...\markitdown_run.py" "{{CASE_ROOT}}张三--------合同纠纷\" --output "D:\md_output\"
```

**在{{ASSISTANT_NAME}}体系中的位置**：
- **被调用方**:`workflow-orchestrator` 流程一/二/三的"步骤 0 预处理"
- **关联 skill**:`process-cases` / `draft-legal-docs` / `case-study-report` 等需要 Markdown 文本输入的下游 skill
- **关联策略文档**:`agent-lawyer-assistant/skills/workflow-orchestrator/references/format-conversion.md`

**不要用于**：
- 法律分析(走 `process-cases`)
- 证据梳理(走 `legal-evidence-mapping-mctmilk`)
- 文书起草(走 `draft-legal-docs`)
- 案件归档(走 `case-progress-archive`)
- 已废弃的 OCR 路由(本 skill 取代)

**完整说明**：见 `agent-lawyer-assistant/skills/markitdown/SKILL.md`
