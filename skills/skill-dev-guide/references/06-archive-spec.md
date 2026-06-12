# 操作归档规范

需要操作追溯的 Skill,在 `archive/` 下保存每次操作记录。

## 文件命名

```
archive/YYYYMMDD_HHMMSS_{标识}.json
```

例:`archive/20260602_223000_ocr-batch-001.json`

## 必含字段

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | string | 唯一标识 |
| `timestamp` | string | ISO 8601 时间 |
| `input` | any | 原始输入 |
| `output` | any | 处理结果摘要 |
| `status` | string | `success` / `failed` / `skipped` |

## 示例

```json
{
  "id": "ocr-batch-001",
  "timestamp": "2026-06-02T22:30:00+08:00",
  "input": {
    "files": ["evidence-01.pdf", "evidence-02.pdf"],
    "engine": "paddleocr"
  },
  "output": {
    "recognized": 23,
    "errors": 0,
    "duration_seconds": 45
  },
  "status": "success"
}
```

## 何时归档

- 涉及批量处理(多文件、多步骤)
- 涉及外部副作用(写入文件、调 API、发消息)
- 涉及资金/法律/合同等高敏感操作
- 需要事后审计或回溯

## 何时不需要归档

- 纯查询操作(只读)
- 一次性临时操作
- 内部状态变更(不外溢)

## 归档保留期

- 高敏感操作:永久保留
- 一般操作:1 年
- 临时归档:30 天

## 跟 CHANGELOG 的区别

- **CHANGELOG**:Skill 自身的版本变更记录(代码/文档改了)
- **archive**:Skill 被使用时,每次操作实例的运行记录(运行时数据)

两者互补,不要混用。
