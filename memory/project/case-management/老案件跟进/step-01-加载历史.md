# step-01：加载历史

## 目的

将新材料转换为 Markdown 文本，加载案件进展日志，合并产出完整的案件背景简报。

## 输入

- 补充材料文件集
- 律师自有知识库路径（"法律"知识库 → 办案 → 对应案件文件夹）

## 输出

- 合并后的案件背景简报（历史 + 新材料）

## 前置条件

- 补充材料路径可用
- `run_skill("markitdown")` 可正常调用
- `run_skill("mineru-ocr")` 可正常调用
- openai-whisper + medium.pt 模型可用（路径：`{{HOME_WIN}}\.cache\whisper\medium.pt`）

## 执行

1. 材料预处理，按类型分发：
   - `IF` 文档（PDF/Office） `THEN` `run_skill("markitdown")` 转换
   - `IF` 图片 `THEN` `run_skill("mineru-ocr")` 转换
   - `IF` 扫描件 PDF `THEN` `run_skill("mineru-ocr")` 转换
   - `IF` 音频 `THEN` whisper model.transcribe("音频文件")，取 `result["text"]` 输出
   - `IF` HTML/CSV/JSON/XML/EPUB `THEN` `run_skill("markitdown")` 转换
2. 在律师自有知识库中查找该案的案件进展日志：
   - `IF` 日志存在 `THEN` 读取完整内容
   - `IF` 日志不存在或无法读取 `THEN` 不阻塞，基于 Markdown 输出 + 对话上下文继续
3. 合并日志内容与新材料

## 异常处理

- `IF` 案件进展日志不存在或无法读取 `THEN` 在 Hook 中提示律师

## Hook

- **硬Hook**：向律师汇报材料理解 + 日志回顾结果，询问——
  - 是否有其他材料需要补充
  - 对当前案件阶段的理解是否有偏差
  - 识别到的新内容是否准确（`IF` 不准确 `THEN` 请律师补充或忽略）

--
- 作者：{{USER_FULL_NAME}}（微信{{USER_WECHAT}}）
- 版本：1.0.0
- 许可证：MIT
