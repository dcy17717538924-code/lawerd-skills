# 流程二：邮件下载发票

> 通过 IMAP 连接 163 邮箱，搜索含"发票"关键词的邮件，下载附件并解析归档。

## 前置条件

- 163 邮箱已开启 IMAP/SMTP 服务
- 已获取 IMAP 授权码（mail.163.com → 设置 → POP3/SMTP/IMAP → 新增授权码）
- 凭据写入 `user-config.json`（详见 `references/config-template.md`）

## 凭据读取优先级

1. {{USER_SHORT_NAME}}当前对话中直接提供的邮箱+授权码
2. `{发票根目录}\.workbuddy\skills\invoice-management\config\user-config.json`
3. 运行时询问

## 步骤

### 1. 环境检查

```powershell
& "{{CODEX_PYTHON}}" -c "import imaplib, email, pdfplumber, openpyxl; print('OK')"
```

### 2. 执行下载脚本

```powershell
& "{{CODEX_PYTHON}}" scripts/fetch_invoices.py --email "{邮箱}" --password "{授权码}" --save-dir "{发票根目录}\未使用" --search-keyword "发票" --days 30
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--email` | 163 邮箱地址 | 必填 |
| `--password` | IMAP 授权码 | 必填 |
| `--save-dir` | 附件保存目录 | `{发票根目录}\未使用` |
| `--search-keyword` | 邮件搜索关键词 | `发票` |
| `--days` | 搜索最近 N 天的邮件 | `30` |
| `--mark-read` | 下载后标记为已读 | `false` |
| `--xlsx` | 统计表路径 | `{发票根目录}\发票统计表.xlsx` |

### 3. 脚本内部流程

> **协议**：POP3（IMAP 被 163 安全策略拦截，`SELECT` 返回 `Unsafe Login`）。本地去重替代标记已读。

1. `poplib.POP3_SSL('pop.163.com', 995)` 登录
2. 从最新邮件往前扫描，按日期范围 + 主题关键词 "发票" 过滤
3. 本地 `.fetched_ids.json` 去重（基于 Date+Subject 哈希）
4. 只下载 PDF 附件（跳过 OFD、XML、行程报销单）
5. pdfplumber 解析每份 PDF → 提取金额 + 用途分类
6. 重命名为 `用途+金额.pdf`
7. openpyxl 追加行到 `发票统计表.xlsx`
8. 汇报下载清单

### 4. 结果汇报

```text
📧 邮箱发票下载完成
- 搜索邮件：X 封匹配"发票"
- 下载附件：Y 个
- 新增归档：
  ✅ 交通费1050.00.pdf
  ✅ 餐饮费218.00.pdf
- 统计表已更新
```

## 去重规则

下载前检查 `save_dir` 是否已有同名文件（按原始文件名），已存在则跳过。

## 故障排除

| 问题 | 解决 |
|------|------|
| `imaplib.IMAP4.error: b'LOGIN failed'` | 确认使用授权码而非邮箱密码 |
| `pdfplumber` 返回空文本 | 降级 markitdown → mineru-ocr |
| PDF 有密码保护 | 跳过该文件，在汇报中标注 |
