# 配置模板

## user-config.json

存放邮箱凭据和路径配置，位于 skill 外部：

```
{发票根目录}\.workbuddy\skills\invoice-management\config\user-config.json
```

### 结构

```json
{
  "email": {
    "address": "your_email@163.com",
    "imap_server": "imap.163.com",
    "imap_port": 993,
    "password": "IMAP授权码（非邮箱密码）"
  },
  "paths": {
    "save_dir": "{{WPS_ROOT}}01 - 法律工作文件\\报销发票\\未使用",
    "xlsx_path": "{{WPS_ROOT}}01 - 法律工作文件\\报销发票\\发票统计表.xlsx",
    "work_dir": "{{WPS_ROOT}}01 - 法律工作文件\\报销发票"
  },
  "fetch": {
    "search_keyword": "发票",
    "days": 30,
    "mark_read": false,
    "attachment_types": [".pdf", ".ofd", ".jpg", ".png", ".jpeg"]
  }
}
```

### 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `email.address` | ✅ | 163 邮箱完整地址 |
| `email.password` | ✅ | IMAP 授权码，16 位字母数字 |
| `paths.save_dir` | 否 | 发票保存目录，默认 `{发票根目录}\未使用` |
| `paths.xlsx_path` | 否 | 统计表路径 |
| `fetch.search_keyword` | 否 | 邮件搜索关键词，默认"发票" |
| `fetch.days` | 否 | 搜索最近 N 天，默认 30 |

## 获取 163 邮箱 IMAP 授权码

1. 登录 [mail.163.com](https://mail.163.com)
2. 顶部 → **设置** → **POP3/SMTP/IMAP**
3. 开启 **IMAP/SMTP 服务**
4. 点 **新增授权码** → 短信验证
5. 复制生成的 16 位授权码（关掉页面后无法再次查看）

⚠️ 授权码 ≠ 邮箱密码。授权码是一次性显示的。
