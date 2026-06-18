# 短信助手

## 功能入口

收到法院12368短信（文书送达、立案通知、开庭提醒等）时进入本流程。

本功能委托 `run_skill("court-sms")` 完整执行。本文件仅定义触发条件和 court-sms 执行完毕后的衔接规则。

## 前置条件

- 律师提供短信内容文本或送达链接
- `run_skill("court-sms")` 可正常调用

## 执行

1. 加载 `错误经验.md`，注入上下文避免重复踩坑
2. 委托 `run_skill("court-sms")` 完整执行。court-sms 内部含：
   - 输入解析：识别短信类型、提取案号/当事人/下载链接
   - 确定归档目录：案件管理 `{当事人}/` 目录
   - 文书下载：调用对应送达平台 API 下载文书
   - 归档保存：文书归档 + 上诉期限计算 + 结构化汇报
3. court-sms 执行完毕后，根据下载的文书类型执行衔接动作

## 衔接动作分发表

| 下载的文书类型 | 衔接动作 | 路由目标 |
|-------------|---------|---------|
| 判决书 / 裁定书 | "是否需要我对该判决/裁定进行分析？（上诉策略/履行评估/申请执行）" | `read_file("memory/project/case-management/新案件办理/index.md")` |
| 传票（开庭通知） | "是否需要我协助庭前准备？（证据梳理/攻防演练/庭审模拟）" | `run_skill("legal-evidence-mapping-mctmilk")` 或 `run_skill("legal-debate-simulation-mctmilk")` |
| 起诉状 / 上诉状（对方） | "是否需要我分析对方主张并准备答辩策略？" | `read_file("memory/project/case-management/新案件办理/index.md")` |
| 举证通知书 | "是否需要我按举证通知梳理证据清单？" | `run_skill("legal-evidence-mapping-mctmilk")` |
| 其他文书 | "是否需要我对该文书进行法律分析？" | 按文书类型路由 |
| 多种文书混合 | 逐项列出，让律师选择优先处理哪份 | 按选择路由 |

## 兜底

无论何种文书类型，归档完成后**必须**询问："是否需要更新案件进展日志？" → `run_skill("case-progress-archive")`

## 异常处理

- `IF` court-sms 下载失败（网络/验证码/平台限制） `THEN` 在汇报中说明后正常结束，不触发衔接询问
- `IF` 短信内容无法解析 `THEN` 请律师手动提供案号或链接

## 参考

- 路由表：[[memory/project/case-management/通用/路由表]]
- 错误处理：[[memory/project/case-management/通用/错误处理总则]]

--
- 作者：{{USER_FULL_NAME}}（微信{{USER_WECHAT}}）
- 版本：1.0.0
- 许可证：MIT
