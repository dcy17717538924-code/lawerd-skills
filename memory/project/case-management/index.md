# 案件管理经验库

> ⛔ 当用户消息含法律任务关键词（"看看材料""分析""起草""处理""归档""法院短信""案件云""订卷"）时，查本路由表匹配功能文档，`read_file` 加载后按步骤执行。

> 子文档位于 `memory/project/case-management/`，按需 `read_file` 加载。

## 功能路由表

| 功能 | 路径 | 触发条件 | 委托 skill |
|------|------|---------|-----------|
| 新案件办理 | `new-case/index.md` | 收到完整案情材料，需全流程分析→起草→归档 | process-cases → draft-legal-docs → case-progress-archive |
| 老案件跟进 | `followup/index.md` | 已有案件进展日志，收到补充材料 | 同新案件办理 |
| 短信助手 | `sms/index.md` | 收到法院12368短信（文书送达/开庭提醒） | court-sms |
| 归档助手 | `archive/index.md` | 案件结案后纸质卷宗订卷归档 | case-archive-orchestrator |

## 通用参考

- 路由表：`common/routing.md`
- Hooks 规则：`common/hooks.md`
- 错误处理总则：`common/errors.md`
