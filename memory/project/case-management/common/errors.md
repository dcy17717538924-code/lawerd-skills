# 错误处理总则

> 迁移自 `workflow-orchestrator/SKILL.md`。适用所有 case-management 子文档中的执行流程。

## 错误模式表

| 失败模式 | 行为 |
|---------|------|
| 路由表 16 条意图之外的模糊请求 | 追问确认意图，不进入主流程 |
| 子 skill（如 process-cases / markitdown）加载失败 | 输出"目标 skill 不可用，请手动指定" |
| 材料缺失 / {{USER_SHORT_NAME}}跳过确认 | 走硬Hook 追问，不向下推进 |
| MarkItDown / LLM 多模态预处理失败 | 降级到"请{{USER_SHORT_NAME}}手写摘要"模式 |
| skill 执行返回异常状态码 | 输出错误详情，询问是否重试或手动处理 |

## 兜底规则

- 以上模式均未覆盖的异常 → 输出错误信息，询问"是否继续处理或转人工"。
- 所有错误信息输出后，如律师选择"跳过"，记录日志后放行。

--
- 作者：{{USER_FULL_NAME}}（微信{{USER_WECHAT}}）
- 版本：1.0.0
- 许可证：MIT
