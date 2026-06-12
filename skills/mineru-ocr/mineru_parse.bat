@echo off
REM mineru_parse.bat — Windows 一键启动器
REM 用 codex runtime(自带 requests 2.34.2),无需手动配置
REM
REM 用法:
REM   mineru_parse.bat url "https://example.com/file.pdf"
REM   mineru_parse.bat file "D:\scan\contract.pdf" --is-ocr
REM   mineru_parse.bat batch "D:\scan" --is-ocr --recursive

setlocal

set "SCRIPT_DIR=%~dp0"
set "PY={{CODEX_PYTHON}}"
set "PY_SCRIPT=%SCRIPT_DIR%scripts\mineru_parse.py"

if not exist "%PY%" (
  echo [error] codex runtime Python 不存在: %PY%
  exit /b 1
)

if not exist "%PY_SCRIPT%" (
  echo [error] 找不到脚本: %PY_SCRIPT%
  exit /b 1
)

"%PY%" "%PY_SCRIPT%" %*

endlocal
