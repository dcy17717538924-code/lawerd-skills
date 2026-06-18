---
name: mineru-ocr
description: 通过 MinerU 精准解析 API 把 PDF/Docx/PPT/Excel/扫描件/图片批量转 Markdown(支持表格、公式、多栏版式)。专攻中文扫描件和复杂版式 PDF,单批 ≤50 个文件、≤200MB/200 页。触发词:扫描件 OCR、复杂版式、批量解析、MinerU、表格识别、公式识别、mineru、PDF转Markdown批量、扫面件转文字、证物卷宗转文本、合同扫描件识别。
---

# mineru-ocr — MinerU 精准解析 skill

> 粽宝自创。用于替代历史 MCP 服务 `mineru-ocr`(已进回收站)。
> 设计目标:让律师助理在案件流程里**一条命令**完成"扫描件/复杂 PDF → 结构化 Markdown"。

## 何时用它

| 场景 | 用谁 |
|------|------|
| 中文扫描件、扫描版合同、证物照片 | **mineru-ocr**(本 skill,精准解析,vlm 模式 + 强制 OCR) |
| 复杂版式 PDF(多栏、表格、公式) | **mineru-ocr**(vlm 模式) |
| 批量处理(几十几百个文件) | **mineru-ocr**(支持 ≤200 个/批) |
| 普通可复制 PDF/Docx | `markitdown` skill(本地,免 token) |
| 单纯图片发问(单张识别) | 主 mavis 多模态发图(IDE vision) |

## 调用入口(给律师助理)

律师助理由 case-management 经验库路由后,可直接调用底层 CLI:

```bash
# 批量解析案件材料目录
python scripts/mineru_parse.py batch "D:\wpsyunpan\...\案件材料" ^
  --output "D:\wpsyunpan\...\案件材料\_parsed" ^
  --is-ocr ^
  --model vlm

# 单个 PDF
python scripts/mineru_parse.py file "D:\...\起诉状.pdf" --is-ocr
```

Windows 一键:

```bat
mineru_parse.bat batch "D:\...\材料目录" --is-ocr
```

## 三种模式

| 命令 | 用途 | 接口 |
|------|------|------|
| `url <URL>` | 远程文件(CDN/网盘分享) | `POST /api/v4/extract/task` |
| `file <PATH>` | 本地单文件 | `POST /api/v4/file-urls/batch` |
| `batch <DIR>` | 本地目录批量(单批 ≤50) | `POST /api/v4/file-urls/batch` × N 批 |

## Token

默认读 `~/Desktop/mineru.txt`({{USER_SHORT_NAME}}的 MinerU Token 存放位置)。
可通过 `--token-file <PATH>` 或环境变量 `MINERU_TOKEN` 覆盖。

## 输出

- 批量:`<output>/<batch_timestamp>/<原文件名>/full.md` + 同名 `*_content_list.json`
- 单文件:`<output>/<原文件名>/full.md`
- 默认模型:`vlm`(推荐);可切 `pipeline`(快) / `MinerU-HTML`(HTML 文件)

## 限额(每日)

- 文件大小 ≤ 200MB,页数 ≤ 200 页
- 单账号每天 1000 页优先额度
- 超出后任务仍会处理,只是优先级降低

## 错误码

详见 `scripts/mineru_parse.py --help` 输出。常见:A0202(Token 错)/ A0211(过期)/ -60005(超大)/ -60006(超页)。

## 完整文档

CLI 参数全表见 [README.md](./README.md)。
