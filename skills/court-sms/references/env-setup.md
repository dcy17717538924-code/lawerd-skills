# court-sms 环境装配与踩坑笔记

> **适用范围**：court-sms skill v2.1.0-ds 及之后版本,第四步 zxfw 文书下载前置环境。
> **最后更新**:2026-06-03 {{USER_SHORT_NAME}}适配版(第五次修订)落盘时整理。
> **目标读者**:worker / orchestrator / 接手维护本 skill 的同学。

本文件记录 2026-06-03 这次会话里把 zxfw 文书下载跑通所踩的坑,以及环境该怎么装。**SKILL.md 里只写"做什么"和"判断逻辑",细节都在这里。**

---

## 目录

- [3.1 playwright + chromium 装在哪](#31-playwright--chromium-装在哪)
- [3.2 PowerShell 5.1 console 编码问题](#32-powershell-51-console-编码问题)
- [3.3 PowerShell 5.1 调 Python 时 JSON 字符串被去双引号](#33-powershell-51-调-python-时-json-字符串被去双引号)
- [3.4 zxfw 真实 API 调用方式](#34-zxfw-真实-api-调用方式)
- [3.5 完整 zxfw 下载脚本骨架](#35-完整-zxfw-下载脚本骨架)

---

## 3.1 playwright + chromium 装在哪

### 3.1.1 唯一可用的 Python 解释器

```
{{CODEX_PYTHON}}
```

- **位置说明**:codex primary runtime 自带的 Python,**不在系统 PATH** 里。
- **版本**:Python 3.12.13(2026-06-03 当下)。
- **不能用的 Python**:`py`(launcher)、系统 `C:\Python311\python.exe`、`{{HOME_WIN}}\AppData\Local\Programs\Python\Python312\python.exe`(如有)等其它解释器,均未装 playwright。

worker 调起 Python 时,**显式用绝对路径**,不要 `py` / 不要 `python` / 不要 `python3`。

### 3.1.2 装 playwright

```powershell
& "{{CODEX_PYTHON}}" -m pip install --quiet playwright
```

- `--quiet` 抑制大量输出,真正出错才看得到。
- 不加 `--user`(已经是 user 目录的 runtime,不需要)。
- 不加 `--break-system-packages`(Python 3.12 + 普通 user pip 没必要)。

### 3.1.3 装 chromium

```powershell
& "{{CODEX_PYTHON}}" -m playwright install chromium
```

**注意**:`playwright install chromium` **实际装的是 chrome-headless-shell**,不是完整版 Chrome。

### 3.1.4 chromium 实际落地路径

```
{{HOME_WIN}}\AppData\Local\ms-playwright\chromium_headless_shell-1223\
```

- 路径里的 `1223` 是 chromium revision,会随 playwright 版本变。
- 真实可执行文件是 `chrome-win\headless_shell.exe`,不带 UI、无沙箱。
- `playwright install chromium` 会顺带装 ffmpeg、winldd 到同一目录。

### 3.1.5 验证装好

最小自检脚本(直接 `python check.py`):

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page()
    page.goto("https://example.com", wait_until="domcontentloaded", timeout=15000)
    print("title:", page.title())
    b.close()
```

期望输出:`title: Example Domain`。

如果 `ModuleNotFoundError: No module named 'playwright'` → 3.1.2 没跑成功。
如果 `playwright._impl._errors.Error: Executable doesn't exist at ... chromium_headless_shell-1223\...` → 3.1.3 没跑成功。

---

## 3.2 PowerShell 5.1 console 编码问题

### 3.2.1 现象

- 跑 Python 脚本,输出中文全是乱码:`鍒ゆ柇` 之类。
- 实际数据是对的(写到文件里、传到 API 都是真中文),只是 console 显示乱码。

### 3.2.2 原因

- Windows PowerShell 5.1(系统内置)默认 console codepage = **GBK**(CP936)。
- Python 3 默认 stdout 编码 = **UTF-8**。
- 两者不一致 → 中文 GBK 解码 UTF-8 字节 → 乱码。

### 3.2.3 解决(每个新 shell 跑一次)

```powershell
chcp 65001; [Console]::OutputEncoding = [System.Text.Encoding]::UTF8; $OutputEncoding = [System.Text.Encoding]::UTF8
```

- `chcp 65001` → console 切到 UTF-8 codepage。
- `[Console]::OutputEncoding = UTF8` → 让 .NET console 用 UTF-8 写字节流。
- `$OutputEncoding = UTF8` → 让 PowerShell 把外部命令输出当 UTF-8 解码。

**注意**:这只是**显示**问题。数据(文件名、PDF 内容、API 响应、写到 `archive/*.json` 的内容)始终是真中文,操作不受影响。**不要因为显示乱码就去改 Python 代码加 `print(repr(...))`**。

### 3.2.4 验证

```powershell
chcp 65001; [Console]::OutputEncoding = [System.Text.Encoding]::UTF8; $OutputEncoding = [System.Text.Encoding]::UTF8
& "{{CODEX_PYTHON}}" -c "print('中文测试')"
```

期望:终端原样输出 `中文测试`(4 个汉字)。

---

## 3.3 PowerShell 5.1 调 Python 时 JSON 字符串被去双引号

### 3.3.1 现象

```powershell
& python api.py POST /calendar '{"a":"b"}'
```

Python 进程收到的不是 `{"a":"b"}`,而是 `{a:b}` → JSON 解析失败。

### 3.3.2 原因

PowerShell 5.1 把单引号字符串里的内容**当表达式求值**,双引号被识别为"字符串边界标记"但行为不一致(取决于 PSReadLine / 历史扩展设置)。这是 PS5.1 长期未修的兼容性问题,Win11 默认 `powershell.exe`(5.1)就是有这个问题。PS 7 (`pwsh.exe`) 已修。

### 3.3.3 解决:JSON 写文件,Python 从文件读

**不要**用命令行参数传 JSON 字符串。

**模式 A:wrapper 脚本读 body 文件**

```python
# create_todo.py(参考,2026-06-03 当下能用的版本)
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# (law086 参考代码已移除 — 本分发版不包含案件云集成)
sys.path.insert(0, SCRIPT_DIR)
from api import make_request, load_env

body_file = sys.argv[1]
with open(body_file, 'r', encoding='utf-8') as f:
    body = json.load(f)

base_url, token = load_env()
result = make_request('POST', base_url, token, '/calendar', body)
print(json.dumps(result, ensure_ascii=False, indent=2))
```

worker 端:

```powershell
$body = @{ title = "陈莉-开庭"; htime = "2026-06-12 13:45"; endtime = "2026-06-12 15:45"; type = 1; linkid = "abc123" } | ConvertTo-Json -Depth 10
$body | Out-File -FilePath "todo_body.json" -Encoding utf8
& "{{CODEX_PYTHON}}" create_todo.py todo_body.json
```

**模式 B:subprocess 模式(更稳)**

```python
import json, subprocess, sys
body = {"a": "b"}
result = subprocess.run(
    [r"{{CODEX_PYTHON}}",
     "helper.py"],
    input=json.dumps(body, ensure_ascii=False),
    capture_output=True, text=True, encoding='utf-8'
)
```

`subprocess.run` + `text=True` + `encoding='utf-8'` 直接传字符串,**不经过 PowerShell**,完全规避 PS5.1 去双引号问题。

**模式 C:用 here-string 但要注意转义**

```powershell
$body = @'
{"a":"b"}
'@
```

`@'...'@`(单引号 here-string)是字面量,不会展开变量也不会去引号,但**注意行尾换行符**。Python 端 `json.loads` 容忍首尾空白,但用 `ConvertFrom-Json` 反而要小心 BOM。

**推荐**:模式 A(写文件)最稳,跨 PS 5.1 / 7 / pwsh 都行。

---

## 3.4 zxfw 真实 API 调用方式

### 3.4.1 端点

```
POST https://zxfw.court.gov.cn/yzw/yzw-zxfw-sdfw/api/v1/sdfw/getWsListBySdbhNew
```

- **Content-Type**:`application/json`
- **请求体**:`{ "qdbh": "...", "sdbh": "...", "sdsin": "..." }`
- 三个参数全部从短信 URL 提取:

```
https://zxfw.court.gov.cn/zxfw/#/pagesAjkj/app/wssd/index?qdbh=<qdbh>&sdbh=<sdbh>&sdsin=<sdsin>
```

**完全和 `references/sms-patterns.json` 描述一致**。之前怀疑 sms-patterns.json 错了,实际上**sms-patterns.json 是对的**,只是裸 curl 调不通(见 3.4.4)。

### 3.4.2 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | int | 业务码,200=成功,非 200 看 `message` |
| `message` | string | 业务消息 |
| `data[].c_wsmc` | string | 文书名称(如 "传票(倪约翰, 2026年06月12日)") |
| `data[].c_wsbh` | string | 文书编号(hash) |
| `data[].c_fymc` | string | 法院名称 |
| `data[].c_fybh` | string | 法院编号 |
| `data[].wjlj` | string | **OSS 签名下载 URL**(阿里云政务云,1 小时过期) |
| `data[].dt_cjsj` | string | 送达记录创建时间(ISO 8601,作为 sent_at 用) |
| `data[].c_wjgs` | string | 文件格式(通常 "pdf") |

### 3.4.3 `wjlj` 是阿里云政务云 OSS 签名 URL

- 域名示例:`https://zxfy2-oss.oss-cn-north-2-gov-1.aliyuncs.com/...`
- 签名有效期:**约 1 小时**
- 拿到 `wjlj` 立刻 `curl -sL -o xxx.pdf "{wjlj}"`,**不要 sleep、不要先解析别的**
- 过期后只能重新跑 playwright 抓响应

### 3.4.4 ⚠️ 必须从浏览器上下文调,裸 curl 会 400

**关键发现**:`getWsListBySdbhNew` 后端做了**链路校验**(Referer / Cookie / 签名 token / 客户端指纹),**裸 curl 直接 POST 会返回 `400 RMFY109904`**。

具体表现为:

- `curl -X POST -H "Content-Type: application/json" -d '{"qdbh":"...","sdbh":"...","sdsin":"..."}' "https://zxfw.court.gov.cn/yzw/yzw-zxfw-sdfw/api/v1/sdfw/getWsListBySdbhNew"` → **400**,响应里带 `RMFY109904`。
- 同一个 body,从 playwright 打开 `https://zxfw.court.gov.cn/zxfw/#/pagesAjkj/app/wssd/index?qdbh=...&sdbh=...&sdsin=...` 触发 H5 内部 fetch → **200**,拿到完整 `data`。

所以方案一(sms-patterns.json 描述的"API 直连")在**实际环境跑不通**,SKILL.md 第四步方案一应当被理解为"在 playwright 上下文里监听到这个 API 的 response,再 curl 它的 `wjlj`"。

**方案二(Playwright CLI/无头)实际就是方案一的实现方式**——打开 H5 → 监听 fetch → 抓 response → 解析 `data[].wjlj` → curl。

### 3.4.5 修正后的方案一/方案二关系

- **方案一(API 直连)**:概念上的"直接拿 API"。**实际不可用**(400 RMFY109904),保留为文档说明,代码不实现。
- **方案二(无头浏览器)**:实际唯一可用的下载路径。playwright headless 打开 H5 → 监听 `getWsListBySdbhNew` response → 解析 `data[].wjlj` → curl 下载。
- **方案三(交互式浏览器)**:MCP 浏览器兜底,给需要人工介入的场景(验证码、账号模式等)。

---

## 3.5 完整 zxfw 下载脚本骨架

参考 `download_zxfw.py`(本次会话验证可用的版本),核心流程:

1. **playwright 打开短信 URL**:
   ```python
   page = ctx.new_page()
   page.on("response", on_response)  # 监听 fetch
   page.on("request", on_request)    # 记录 request body
   page.goto(URL, wait_until="domcontentloaded", timeout=30000)
   page.wait_for_timeout(5000)  # 等 JS 渲染 + fetch 完成
   ```

2. **监听 network,捕获 `getWsListBySdbhNew` response**:
   ```python
   def on_response(response):
       if "getWsListBySdbhNew" in response.url and response.request.method == "POST":
           captured["body_text"] = response.text()
   ```

3. **解析 response 拿 `wjlj`**:
   ```python
   body = json.loads(captured["body_text"])
   for doc in body["data"]:
       wjlj = doc["wjlj"]
       c_wsmc = doc["c_wsmc"]
       dt_cjsj = doc["dt_cjsj"]
   ```

4. **curl `wjlj` 落盘到目标目录**:
   ```python
   import subprocess
   r = subprocess.run(
       ["curl.exe", "-sL", "-o", str(out_path), wjlj],
       capture_output=True, text=True, timeout=60
   )
   ```
   - 目标目录:`{{CASE_ROOT}}{当事人}\`(第三步确定)
   - 文件名:`{title}({当事人})_{YYYYMMDD}收.pdf`,清理 `< > : " | ? * \ /`

5. **PyMuPDF 解析 PDF 首页**(可选,5.2 节文书解析):
   ```python
   import fitz  # PyMuPDF
   doc = fitz.open(out_path)
   page1_text = doc[0].get_text()
   # 提取开庭时间/法庭/案号/当事人
   ```

6. **归档元数据到 `archive/`**:
   ```python
   archive_record = {
       "id": "20260603_010343_6616",
       "timestamp": "2026-06-03T01:03:43+08:00",
       "sms_raw": "...",
       "parsed": { ... },
       "download": { ... },
       "document": { ... },
       "archive": { ... },
   }
   with open("archive/{id}.json", "w", encoding="utf-8") as f:
       json.dump(archive_record, f, ensure_ascii=False, indent=2)
   ```

完整可运行参考见 session workspace 的 `download_zxfw.py`(本 skill 之外,本仓库 `~/.mavis/sessions/<root>/workspace/` 下的同名文件)。

### 3.5.1 关键参数

| 参数 | 值 | 说明 |
|------|----|------|
| viewport | `{width: 414, height: 896}` | 手机视口,跟短信发送方一致 |
| user_agent | iPhone Safari 17 | 移动端 UA,跟短信链接打开的客户端一致 |
| wait_until | `domcontentloaded` | 不等 load(移动端 SPA 永远不会 fire load) |
| timeout | 30000ms | goto 超时 |
| wait_for_timeout | 5000ms | 等 JS 渲染 + 内部 fetch 完成 |

### 3.5.2 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `ModuleNotFoundError: No module named 'playwright'` | 走错解释器 | 改用 3.1.1 的 codex-python |
| `Executable doesn't exist at ...chromium_headless_shell-1223\...` | 没装 chromium | 跑 3.1.3 |
| `playwright._impl._errors.TimeoutError: Timeout exceeded while waiting for "domcontentloaded"` | 网络抖动 | 重试,或加 timeout 到 60s |
| 抓不到 `getWsListBySdbhNew` response | `wait_for_timeout` 不够,或手机视口不对 | 加到 10000ms,确认 UA 是移动端 |
| `data` 字段是 dict 不是 list | 不同短信场景,后端有时返回 dict 包 list | 见 download_zxfw.py 第 89 行的兜底 |
| curl 下载 0 字节 | `wjlj` 已过期(>1h) | 重新跑 playwright 抓 response |

---

## 附录:本 skill 涉及的外部资源

- **zxfw 文书下载**(步骤三):见本文 3.4 / 3.5
- **PyMuPDF PDF 解析**(5.2):`pip install pymupdf`,`import fitz`
- **archive 归档格式**:见 `references/archive-format.md`
- **report 汇报格式**:见 `references/report-format.md`
