# step-00：依赖检查

## 目的

验证 Python 依赖包 `pdfplumber` 和 `openpyxl` 已安装。

## 执行

```powershell
& "{{CODEX_PYTHON}}" -c "import pdfplumber, openpyxl" 2>$null
```

## 异常处理

`IF` 报错 `THEN` 安装：
```powershell
& "{{CODEX_PYTHON}}" -m pip install pdfplumber openpyxl
```
