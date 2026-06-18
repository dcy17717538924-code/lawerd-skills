# step-04：定稿导出

## 目的

将已确认的初稿生成定稿 DOCX，经格式预览确认后交付。

> 核心原则：模板即格式权威。只替换文本，不触碰格式。

## 输入

- 步骤 03 产出的已确认初稿
- `placeholders.json`（由步骤 02 产出）

## 输出

- 定稿 DOCX 文件
- PDF 格式预览

## 执行

### 有模板路径（主路径）

1. 复制模板到案卷目录：
   ```cmd
   copy "{{REASONIX_SKILLS}}draft-legal-docs\templates\[模板名].docx" "[案卷路径]\[文件名].docx"
   ```

2. 调用 `fill_template.py` 填充（OOXML 文本替换，零格式损失）：
   ```cmd
   "{{CODEX_PYTHON}}" "{{REASONIX_SKILLS}}docx/scripts/fill_template.py" "[案卷路径]\[文件名].docx" "[placeholders.json]"
   ```
   - `placeholders.json`：键名为模板中的 `【占位符】` 文本
   - 只替换 `<w:t>` 中的文本，不触碰格式 XML

3. PDF 导出（WPS CLI）：
   ```cmd
   wps writer export-pdf "[定稿路径].docx"
   ```
   检查项：标题字体（黑体/方正小标宋）、正文字体（仿宋）、页边距、落款右对齐位、段间距、表格边框完整性

4. 格式确认后调 Obsidian CLI 打开审阅：
   ```cmd
   "D:\anzhuang\Obsidian\obsidian" open path="[文件名]" vault="Agent知识库"
   ```

### 无模板路径

1. 用 `python-docx` 按{{USER_SHORT_NAME}}默认排版配置生成 DOCX
2. PDF 导出（WPS CLI，同上）
3. 格式预览（同上）

## 异常处理

- `IF` DOCX 生成失败 `THEN` 提示重新生成
- `IF` 格式预览发现异常 `THEN` 调整后重新导出

## 核验提示

法条核验 / 信息补充 / 格式核验（模板填充保真 + PDF 预览已确认）

--
- 作者：杜重阳律师（微信Dcylawer8888）
