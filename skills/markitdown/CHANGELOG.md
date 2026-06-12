# Changelog

## [1.2.0] - 2026-06-05

### 修改

- **砍 LLM 凭证链路**:`scripts/markitdown_run.py` 不再读 `.env`、不再构造 LLM 客户端、不再加载 `markitdown-ocr` 插件
- **移除参数**:`--enable-plugins` / `--llm-base-url` / `--llm-api-key` / `--llm-model` / `--no-llm` / `--list-plugins` 全部移除,脚本退化为"纯本地 markitdown 基础提取"
- **扫描件明确报错**:遇无文字层输入时,stderr 明确报"扫描件,无文字层",不再静默返回空字符串误导下游 process-cases
- **`SKILL.md` 重写**:description / 激活条件 / 边界表 / 与原 OCR 方案关系表 全部对齐"纯本地 + 扫描件走 IDE 多模态"的新定位
- **依赖简化**:`markitdown-ocr 0.1.0` / `openai 2.41.0` 包仍装在环境中(历史),但默认不启用、不参与运行

### 修复

- 修复"markitdown-ocr `_ocr_service.extract_text` 静默吞异常"的潜在误导:扫描件 LLM vision 失败时,曾经只输出空字符串而不暴露根因(实测 MiniMax-M3 接口 502 Bad Gateway)

### 安全

- ⚠️ **强烈建议 rotate `.env` 里的 LLM API key**:v1.1.0 时代的明文 key 已在 chat log + 本 CHANGELOG 历史里暴露,虽然 v1.2.0 不再读 `.env`,但**revoke + 重发**仍是正确做法(详见 minimaxi 后台)。本次更新**不**在仓库里再次写出该明文 key。

## [1.1.0] - 2026-06-05

### 新增

- **markitdown-ocr 插件集成**:`scripts/markitdown_run.py` 加 `--enable-plugins` 参数,装上 `markitdown-ocr` + `openai` 后自动接管 PDF/DOCX/PPTX/XLSX 嵌入图片 OCR
- **LLM 视觉兜底**:`scripts/markitdown_run.py` 加 `--llm-base-url` / `--llm-api-key` / `--llm-model` / `--no-llm` 参数,默认从 `.env` 读(`MARKITDOWN_LLM_*`)
- **`.env` 自动加载**:同 skill 目录下 `.env` 文件,被 `~/.mavis/.gitignore` 覆盖不会被 commit
- **`--list-plugins`**:列出已装的 markitdown 插件

### 修改

- `scripts/markitdown_run.py` 重写:支持 LLM 视觉兜底完整参数链
- `SKILL.md` 文档升级:三层 OCR/视觉策略图、`.env` 配置说明、Python API + CLI 双示例
- 桥接脚本依赖链:基础 MarkItDown + 可选 markitdown-ocr(嵌入图片 OCR)+ 可选 openai(LLM 客户端)

### 已知 TODO(用户手动) — 2026-06-05 16:50 已完成

- ~~装 `markitdown-ocr` + `openai`~~ ✅ 2026-06-05 16:50 已装(`markitdown-ocr 0.1.0` / `openai 2.41.0`)
- 三链路全通:基础转换 / LLM 视觉兜底 / 嵌入图片 OCR
- ⚠️ **API key 需 rotate**:该 key 在 v1.1.0 编写时明文出现在本 CHANGELOG 与 chat log 中,v1.2.0 已从仓库删除明文,但**revoke + 重发**仍是正确做法(详见 minimaxi 后台)

## [1.0.0] - 2026-06-05

### 新增

- 新建 `markitdown` skill,落地于 `agent-lawyer-assistant/skills/markitdown/`
  - 依赖 Microsoft 开源 MarkItDown(`pip install "markitdown[pdf,docx,xlsx,pptx]"`,用户手动装)
  - 桥接脚本 `scripts/markitdown_run.py`:支持单文件/批量转换,跨平台
  - 输入格式:PDF / Word / PPT / Excel / HTML / CSV / JSON / XML / EPUB / ZIP / YouTube / 音频(可选)
  - 输出:Markdown(保留标题/表格/列表/链接结构)
- OCR 方案整体退役,原 `coder/skills/local-ocr/` 已 `mavis-trash` 回收
  - 替换:文档(PDF/Office)走 MarkItDown,图片/扫描件走 mavis 当前 LLM(MiniMax-M3)vision 多模态
  - 详见律师助理的 `workflow-orchestrator/references/format-conversion.md`(本版本由原 `ocr-strategy.md` 重构)

### 历史背景

- 2026-05-30 ~ 2026-06-04:OCR 方案基于 百度 OCR / MinerU / PaddleOCR 三级引擎,在 `coder/skills/local-ocr/` 下
- 2026-06-05:{{ASSISTANT_NAME}}体系重构,MarkItDown 一站式替换 OCR + 文档解析,本地处理无需 API
