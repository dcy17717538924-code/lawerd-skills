# mineru-ocr CLI 用法

> 基于 MinerU 精准解析 API。详细 API 文档: https://mineru.net/apiManage/docs

## 快速开始

```bash
# 1) 远程 URL(测试连通)
python scripts/mineru_parse.py url "https://cdn-mineru.openxlab.org.cn/demo/example.pdf"

# 2) 本地单文件
python scripts/mineru_parse.py file "D:\卷宗\起诉状.pdf" --is-ocr

# 3) 批量目录(单批 ≤50 个,自动分批)
python scripts/mineru_parse.py batch "D:\卷宗" --is-ocr --output "D:\卷宗\_parsed"
```

## Windows 一键(自动拉 requests)

```bat
mineru_parse.bat file "D:\卷宗\起诉状.pdf" --is-ocr
```

## 公共参数

| 参数 | 默认 | 说明 |
|------|------|------|
| `--model {vlm\|pipeline\|MinerU-HTML}` | vlm | 模型版本。中文扫描件 + 复杂版式 → vlm;英文快解析 → pipeline |
| `--language {ch\|ch_server\|en\|...}` | ch | 文档语言,影响 OCR |
| `--is-ocr` | False | 扫描件务必打开。打开后会对图片内容做识别 |
| `--no-formula` | - | 关闭公式识别(默认开) |
| `--no-table` | - | 关闭表格识别(默认开) |
| `--extra-formats docx,html` | - | 追加 docx/html 输出(默认仅 md+json) |
| `--page-ranges "1-10,20-30"` | 全部 | 指定页码 |
| `--output DIR` | `<输入>_parsed` | 输出目录 |
| `--token-file PATH` | `~/Desktop/mineru.txt` | Token 文件 |
| `--interval N` | 3 | 轮询间隔(秒) |
| `--timeout N` | 600 | 单任务轮询超时(秒) |

## 输出结构

### `batch DIR` 模式

```
<output>/
└── batch_20260608_001234/
    ├── 起诉状/
    │   ├── full.md
    │   ├── 起诉状_content_list.json
    │   ├── 起诉状_middle.json
    │   └── 起诉状_model.json
    ├── 合同1/
    │   ├── full.md
    │   └── ...
    └── 扫描件A/
        └── ...
```

### `file PATH` 模式

```
<output>/
└── <原文件名>/
    ├── full.md
    └── ...
```

## Token 优先级

1. `--token-file` 显式指定
2. 环境变量 `MINERU_TOKEN_FILE` 指定的文件
3. 环境变量 `MINERU_TOKEN` 直接给值
4. 默认 `~/Desktop/mineru.txt`({{USER_SHORT_NAME}}的工作约定)

## 限额(每日/账号)

- **1000 页** 最高优先级
- 单文件 ≤ **200MB / 200 页**
- 批量单次申请上传链接 ≤ **50 个**,系统自动 ≤200 个文件分批

## 常见错误

| 错误码 | 含义 | 处理 |
|--------|------|------|
| A0202 | Token 错 | 检查 Token 是否有 `Bearer ` 前缀或换新 |
| A0211 | Token 过期 | 重新到 mineru.net/apiManage 创建 |
| -60005 | 文件超大 | 拆分或转 docx |
| -60006 | 页数超 | 拆分或用 `page-ranges` |
| -60018 | 今日额度用完 | 明天再来 |
