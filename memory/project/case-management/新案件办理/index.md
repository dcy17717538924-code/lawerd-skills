# 新案件办理

## 功能入口

收到完整案情材料时进入本流程。全流程覆盖：材料预处理→案情分析→策略确认→起草→定稿→归档。

## 步骤序列

| 步骤 | 动作 | 委托 skill |
|------|------|-----------|
| 01 | 预处理与分析 | `run_skill("markitdown")` / `run_skill("mineru-ocr")` / whisper → `run_skill("process-cases")` |
| 02 | 策略确认 | `IF` 律师确认策略 `THEN` 进入起草步骤 |
| 03 | 起草文件 | `run_skill("draft-legal-docs")` |
| 04 | 定稿交付 | `run_skill("draft-legal-docs")` → `run_skill("docx")` |
| 05 | 归档 | `run_skill("case-progress-archive")` |

## 前置条件

- 律师提供案件材料（PDF / 图片 / Office 文档 / 文本）
- 材料经过 markitdown / mineru-ocr / whisper 预处理，输出 Markdown 文本

## 参考

- 路由表：[[memory/project/case-management/通用/路由表]]
- Hooks 规则：[[memory/project/case-management/通用/hooks参考]]
- 错误处理：[[memory/project/case-management/通用/错误处理总则]]

--
- 作者：{{USER_FULL_NAME}}（微信{{USER_WECHAT}}）
- 版本：1.0.0
- 许可证：MIT
