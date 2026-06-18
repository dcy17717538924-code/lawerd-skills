# 老案件跟进

## 功能入口

已有案件进展日志的案件，收到补充材料后进入本流程。
覆盖：加载历史→分析新材→起草→定稿→归档。

## 步骤序列

| 步骤 | 动作 | 委托 skill / 引用 |
|------|------|------------------|
| 01 | 加载历史 | `IF` 日志存在 `THEN` 加载案件背景 `ELSE` 基于当前材料+对话上下文继续 |
| 02 | 分析新材 | 策略五要素分析 |
| 03 | 起草归档 | 引用 new-case step-03→04→05 |

## 前置条件

- 律师提供补充材料（文件或文本）
- 律师自有知识库中存有该案案件进展日志（`IF` 不存在 `THEN` 不阻塞，按兜底规则处理）

## 参考

- 路由表：[[memory/project/case-management/common/routing]]
- Hooks 规则：[[memory/project/case-management/common/hooks]]
- 错误处理：[[memory/project/case-management/common/errors]]

--
- 作者：{{USER_FULL_NAME}}（微信{{USER_WECHAT}}）
- 版本：1.0.0
- 许可证：MIT
