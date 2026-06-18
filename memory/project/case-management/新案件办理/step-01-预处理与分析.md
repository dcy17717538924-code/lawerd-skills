# step-01：预处理与分析

## 目的

将律师提供的材料转换为 Markdown 文本，基于分析结果产出案件简报。

## 输入

- 材料文件集（PDF / Office 文档 / 图片 / 音频 / HTML / CSV / JSON）
- 文件路径列表

## 输出

- Markdown 格式的案情文本
- 案件简报（含法律关系定性、请求权基础、举证责任分配、风险识别）

## 前置条件

- 材料文件路径可用
- `run_skill("markitdown")` 可正常调用
- `run_skill("mineru-ocr")` 可正常调用
- openai-whisper + medium.pt 模型可用（路径：`{{HOME_WIN}}\.cache\whisper\medium.pt`）

## 执行

1. 识别材料类型并按策略分发：
   - `IF` 文档（PDF/Office） `THEN` `run_skill("markitdown")` 转换
   - `IF` 图片 `THEN` `run_skill("mineru-ocr")` 转换（vlm 模式 + 强制 OCR）
   - `IF` 扫描件 PDF `THEN` `run_skill("mineru-ocr")` 转换（vlm 模式 + 强制 OCR）
   - `IF` 音频 `THEN` whisper model.transcribe("音频文件")，取 `result["text"]` 输出
   - `IF` HTML/CSV/JSON/XML/EPUB `THEN` `run_skill("markitdown")` 转换
2. 收集转换结果，Markdown 文本作为后续分析的材料内容
3. `run_skill("process-cases")`，仅取其分析输出（案情摘要、法律问题分析），不执行其内部完整交互流程
4. 产出案件简报

## 异常处理

- `IF` 文件转换失败 `THEN` 在 Hook 中列出失败文件清单，提示律师提供可读版本
- `IF` mineru-ocr 失败 `THEN` 降级到 LLM vision 逐页读图
- `IF` whisper 模型加载失败 `THEN` 提示"语音识别模型不可用，请提供文字版"

## Hook

- **软Hook**：转换完成后向律师汇报——"共接收 N 个文件，成功转换 M 个。失败清单：[文件名列表]"
- **硬Hook**：请律师确认以下事项后方可继续——
  - 我方诉讼地位（原告/被告/第三人）
  - 材料内容简要是否准确
  - 是否有其他需要补充的重点
  - 律师目前的诉讼思路
  - 需要起草的材料类型

--
- 作者：{{USER_FULL_NAME}}（微信{{USER_WECHAT}}）
- 版本：1.0.0
- 许可证：MIT
