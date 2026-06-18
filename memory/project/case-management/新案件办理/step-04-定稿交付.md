# step-04：定稿交付

## 目的

在对话中展示初稿供律师审阅，经修改确认后生成定稿 DOCX。

## 输入

- step-03 产出的初稿文本
- 律师的审阅反馈

## 输出

- 定稿 DOCX 文件

## 前置条件

- step-03 已完成，初稿已生成

## 执行

1. 在对话中直接展示初稿正文（不用 MD 文件预览）
2. 等待律师反馈：
   - `IF` 律师确认 `THEN` 进入步骤 3
   - `IF` 律师提出修改意见 `THEN` 修改后重新展示，二次确认
   - `IF` 修改循环 ≥ 3 轮仍未定稿 `THEN` 提示律师面谈确认关键争议点
3. 定稿后调 `run_skill("draft-legal-docs")` 生成 DOCX，委托 `run_skill("docx")` 处理格式转换。`IF` 需要模板或格式预览 `THEN` 可用 `run_skill("word-docx")` 作为备选路径
4. `IF` 有模板 `THEN` 复制模板 → 填充占位符 → PDF 导出预览 → 确认格式
5. `IF` 无模板 `THEN` python-docx 按默认排版配置生成 → PDF 导出预览 → 确认格式
6. 格式确认后进入 step-05

## 异常处理

- `IF` DOCX 生成失败 `THEN` 提示重新生成
- `IF` 格式预览发现异常 `THEN` 调整后重新导出

--
- 作者：{{USER_FULL_NAME}}（微信{{USER_WECHAT}}）
- 版本：1.0.0
- 许可证：MIT
