---
name: invoice-management
author: 杜重阳律师（微信Dcylawer8888）
version: "1.0.0"
license: MIT
description: |
  本技能应在{{USER_SHORT_NAME}}需要管理报销发票时使用：从163邮箱下载发票附件、PDF解析金额与用途分类、归档到未使用目录并更新统计表、按目标金额凑票组合、查库存。
  触发词："拉发票""下载发票""凑发票""凑XX元发票""发票库存""看发票""整理发票"。
  不要用于：非发票的邮件附件下载、合同审核、税务申报。
---

# 发票管理

## 功能概述

管理报销发票的完整生命周期：**邮件下载 → PDF解析 → 重命名归档 → 凑票组合 → 查库存**。

工作目录：`D:\wpsyunpan\229601413\WPS云盘\01 - 法律工作文件\报销发票\`（以下简称 `{发票根目录}`）。

## 触发路由

根据用户输入关键词，路由到对应流程：

| 关键词 | 流程 | 详见 |
|--------|------|------|
| 拉发票、下载发票 | 流程二：邮件下载 | `references/02-workflow-email-fetch.md` |
| 整理发票 | 流程一：初始整理 | `references/01-workflow-initial-sort.md` |
| 凑发票、凑XX元发票 | 流程三：凑票 | `references/03-workflow-match-invoices.md` |
| 发票库存、看发票 | 流程四：查库存 | `references/04-workflow-check-stock.md` |

如用户输入跨流程（如"下载发票然后凑2000元"），按顺序执行流程二→流程三。

## 工作流总览

```
邮件下载（流程二）
  ↓ PDF 附件保存到 未使用/
  ↓ pdfplumber 提取金额 + 用途
  ↓ 重命名为 "用途+金额.pdf"
  ↓ openpyxl 追加行到 发票统计表.xlsx
  ↓
凑票（流程三）
  ↓ {{USER_SHORT_NAME}}说 "凑XX元发票"
  ↓ 从 发票统计表.xlsx 筛选未使用
  ↓ 贪心算法选取组合覆盖目标金额
  ↓ 创建 {日期}+{金额}/ 文件夹
  ↓ move 选中发票 → 更新统计表状态
```

### 流程一：初始整理

已有 PDF 发票散落在根目录时，批量解析 + 建表 + 归档。详见 `references/01-workflow-initial-sort.md`。

### 流程二：邮件下载 ★

通过 IMAP 连接 163 邮箱，搜索含"发票"关键词的邮件，下载 PDF/OFD/图片附件，解析后归档到 `未使用/`。详见 `references/02-workflow-email-fetch.md`。

### 流程三：凑票

按目标金额从 `未使用/` 中选取发票组合，创建日期文件夹移入，更新统计表。详见 `references/03-workflow-match-invoices.md`。

### 流程四：查库存

读取 `发票统计表.xlsx`，列出未使用发票清单，按用途分类汇总。详见 `references/04-workflow-check-stock.md`。

## 目录约定

```
{发票根目录}/
├── 发票统计表.xlsx          ← 主数据表
├── 未使用/                  ← 已重命名的可用发票
├── {YYYY-MM-DD}+{金额}/     ← 某次凑票的已使用发票（流程三创建）
└── extract_invoices.py      ← 遗留脚本（不再使用）
```

## 命名规则

文件名格式：`{用途类型}{金额}.pdf`，小数点保留 2 位。

示例：`交通费1050.00.pdf`、`餐饮费218.00.pdf`、`通讯费1062.86.pdf`

## 用途分类

详见 `references/category-rules.md`。核心映射：

| 发票关键词 | 用途类型 |
|-----------|---------|
| 交通卡充值、客运服务费、滴滴 | 交通费 |
| 餐饮服务 | 餐饮费 |
| 通信服务费、电信服务、联通 | 通讯费 |
| 住宿 | 住宿费 |

## 统计表列说明

`发票统计表.xlsx` 列结构（9 列）：

| 列 | 名称 | 示例 |
|----|------|------|
| A | 序号 | 1 |
| B | 新文件名 | 交通费1050.00.pdf |
| C | 用途类型 | 交通费 |
| D | 金额（元） | 1050.00 |
| E | 发票详情 | 交通卡充值 |
| F | 原文件名 | dzfp_26312000003391736386_...pdf |
| G | 状态 | 未使用 / 已使用 |
| H | 使用日期 | 2026-06-09 |
| I | 使用备注 | 案件差旅费 |

## 配置

### 邮箱凭据（流程二）

凭据存放在 skill 外部，不纳入版本管理：

```
{发票根目录}\.workbuddy\skills\invoice-management\config\user-config.json
```

或运行时由{{USER_SHORT_NAME}}提供。需三个字段：
- `email`：163 邮箱地址
- `password`：IMAP 授权码（非邮箱密码，在 mail.163.com → 设置 → POP3/SMTP/IMAP 生成）
- `save_dir`：发票保存目录，默认 `{发票根目录}\未使用\`

详见 `references/config-template.md`。

### 依赖

- Python 3.12+（codex runtime：`{{CODEX_PYTHON}}`）
- `pdfplumber`：PDF 文字提取
- `openpyxl`：xlsx 读写
- `imaplib` + `email`：Python 标准库，无需额外安装

首次使用前检查：
```powershell
& "{{CODEX_PYTHON}}" -c "import pdfplumber, openpyxl" 2>$null
```
若报错：
```powershell
& "{{CODEX_PYTHON}}" -m pip install pdfplumber openpyxl
```

## 与其他技能配合

本 skill 独立使用，无上下游依赖。不经过 workflow-orchestrator。

## 变更历史

见 [CHANGELOG.md](./CHANGELOG.md)
