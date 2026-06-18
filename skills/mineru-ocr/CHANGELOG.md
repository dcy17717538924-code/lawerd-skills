# Changelog — mineru-ocr

> 粽宝自创 skill。全局可用,主 mavis / 律师助理 / 技术顾问都能加载。
> 配套: `MEMORY.md` 索引 + `SKILL.md` 入口 + `scripts/mineru_parse.py` CLI。

## v1.0.0 — 2026-06-08

### 新增
- 首版发布。基于 MinerU 精准解析 API(https://mineru.net/apiManage/docs)
- 支持三种调用模式:
  - `url <URL>` — 远程文件单次解析
  - `file <PATH>` — 本地文件单次解析
  - `batch <DIR>` — 本地文件夹批量解析(单批 ≤50,自动分批)
- 三种模型版本可选:`vlm`(默认,推荐)/ `pipeline`(快)/ `MinerU-HTML`(HTML 文件专用)
- 异步轮询 + zip 下载 + 解压取 `full.md` / `*.json`
- Token 安全读取:默认 `~/Desktop/mineru.txt`,可 `--token-file` 指定
- 限额友好:200MB/200 页/天 1000 页,自动友好提示
- Windows 一键启动器 `mineru_parse.bat`(自动用 uv 拉 `requests` 依赖)

### 文档
- `SKILL.md` — skill 入口(描述 + 触发词 + 调用方式)
- `README.md` — CLI 用法详解
- `.env.example` — token 配置模板

### 配套
- 写入 `tech-environment.md` § 五(粽宝自创 skill 清单 18 → 19)
- 与 `local-ocr` skill 互补:扫描件/复杂版式走本 skill,纯文本走 markitdown
