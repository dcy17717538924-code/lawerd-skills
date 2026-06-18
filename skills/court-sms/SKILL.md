---
name: court-sms
author: 杨卫薪律师（微信 ywxlaw）
version: "2.1.0-ds"
license: MIT
description: 本技能应在用户收到法院12368短信（文书送达、开庭提醒等）时使用，自动提取案号并完成文书下载归档+待办创建。 不要用于：合同审查、法律咨询、普通文件处理。
---

# 法院短信识别与文书下载

## 功能概述

处理法院短信的完整流程：**粘贴短信 → 解析内容 → 下载文书 → 智能归档**。

支持两种触发方式：

**方式一：粘贴短信原文**

```text
收到法院短信，内容如下：
【xx市人民法院】张三，您好！您有（2025）苏0981民初1234号案件文书送达，请点击链接查收：https://zxfw.court.gov.cn/zxfw/#/pagesAjkj/app/wssd/index?qdbh=DEMO1&sdbh=DEMO2&sdsin=DEMO3
```

**方式二：直接发送送达链接**

用户可能直接粘贴送达链接（非完整短信文本），此时跳过短信文本解析，直接从 URL 中提取 `qdbh`、`sdbh`、`sdsin` 参数，进入第四步下载流程。

```text
https://zxfw.court.gov.cn/zxfw/#/pagesAjkj/app/wssd/index?qdbh=xxx&sdbh=xxx&sdsin=xxx
```

## 短信类型分类

| 类型 | 特征 | 含下载链接 | 处理方式 |
| --- | --- | --- | --- |
| 文书送达 | 含送达平台链接 + 案号 | 是 | 下载文书并归档到案件目录 |
| 立案通知 | 含"已立案"等关键词 | 可能有 | 展示解析结果 |
| 信息通知 | 无链接，纯信息 | 否 | 展示解析结果 |

**支持的送达平台**：`zxfw.court.gov.cn`（全国）、`sd.gdems.com`（广东）、`jysd.10102368.com`（集约送达）、`dzsd.hbfy.gov.cn`（湖北）、`sfpt.cdfy12368.gov.cn`（司法送达网）。同一平台可能使用不同域名（同构异域名），通过 URL 路径特征识别平台。详见 `references/sms-patterns.json`。

---

## 工作流（四步）

### 第一步：输入解析

1. 读取 `references/sms-patterns.json` 作为解析参考
2. **判断输入类型**：
   - **完整短信**：包含法院签名（如 `【xx法院】`）+ 正文 + 链接 → 完整解析流程
   - **纯链接**：用户直接发送送达 URL（如 `https://zxfw.court.gov.cn/...?qdbh=xxx&sdbh=xxx&sdsin=xxx`）→ 跳过短信文本解析，直接从 URL 提取参数，进入第四步下载。案号、当事人等信息在下载文书后从文书内容中提取。
3. 对用户粘贴的短信文本进行分析（纯链接输入跳过此步）：

**a) 短信分类**：根据关键词判断类型
- 文书送达：包含 zxfw.court.gov.cn 链接
- 立案通知：包含"已立案"、"立案通知"等
- 信息通知：其他

**b) 案号提取**：使用正则 `[（(〔[]\d{4}[）)〕]]` 匹配标准案号格式

标准案号格式示例：
- `（2025）苏0981民初1234号`
- `(2024)粤0604执保5678号`
- `〔2025〕京0105民初901号`

**c) 当事人提取（最高优先级）**：从短信文本初步识别，最终以文书内容为准
- **注意**：短信中的称呼（如"张三，您好"）仅为短信接收人，不作为案件当事人
- 公司名称：`xx有限责任公司`、`xx有限公司`、`xx股份有限公司`
- 诉讼对峙：`A与B`、`A诉B`、`原告A 被告B`
- 角色前缀：`原告：xxx`、`被告：xxx` 等
- 下载文书后，以起诉状、传票中的当事人信息为准，覆盖短信阶段的初步判断

**d) 下载链接提取**：识别短信中的送达平台链接并提取参数

| 平台 | 域名 | 下载方式 | 提取参数 |
|------|------|----------|----------|
| 全国法院统一送达平台 | `zxfw.court.gov.cn` | curl API 直连 | qdbh, sdbh, sdsin |
| 广东法院电子送达 | `sd.gdems.com` | 浏览器自动化 | 路径中的送达标识码 |
| 集约送达平台 | `jysd.10102368.com` | 浏览器自动化 | key |
| 湖北电子送达 | `dzsd.hbfy.gov.cn` | HTTP API（免账号）/ 浏览器自动化（账号模式） | 免账号：msg；账号模式：账号+密码从正文提取 |
| 司法送达网 | `sfpt.cdfy12368.gov.cn` | 纯 Playwright（无 API） | 验证码（手机尾号后6位 / 短信验证码） |

**e) 发送时间提取（P0）**：从送达平台 API 响应中提取发送时间，用于后续上诉期限计算
- **优先来源**：zxfw API 响应中的 `dt_cjsj` 字段（送达记录创建时间，ISO 8601 格式）
- 短信网关时间：部分手机短信会显示发送时间，匹配 `发送：YYYY-MM-DD HH:mm` 格式
- 如果无法提取送达时间，展示"送达时间待确认"，不阻塞后续流程
- 记录到归档 JSON 的 `document.sent_at` 字段

> **排除列表**：法院名称、法官姓名、地名、法律术语等不应作为当事人提取。详见 `sms-patterns.json` → `party_extraction.exclude_keywords`。

**输出格式**（向用户展示）：

```text
📋 短信解析结果：
- 类型：文书送达
- 案号：（2025）苏0981民初1234号
- 当事人：张三、xx有限公司
- 下载链接：已提取（zxfw.court.gov.cn）
```

### 第二步：确定归档目录

> 文书归档到案件管理 `{当事人}/` 目录。当事人来源：短信提取（最优先）> 文书内容。

1. **确定当事人**：以第一步从短信中提取的当事人信息为最优先。如短信未提取到，以文书内容中的当事人为准。

2. **⛔ 强制搜索已有目录**（不可跳过）：在创建新目录之前，**必须**先搜索案件管理下是否已有该当事人的文件夹。
   - 列出 `{{CASE_ROOT}}` 下所有子目录
   - 用当事人姓名**模糊匹配**目录名（目录命名格式通常为 `{首字母大写}{当事人名}--------{案件类型}`，如 `Z朱佩英--------经济纠纷/`）
   - **匹配到** → 使用已有目录，不新建
   - **未匹配** → 继续步骤 3 新建

3. **确定归档路径**：
   - 已有目录（步骤 2 匹配到）：直接使用匹配到的完整路径
   - 新目录（步骤 2 未匹配）：`{{CASE_ROOT}}{当事人}\`

4. **创建目录**（仅当步骤 2 未匹配到时自动创建）
5. **不询问用户**，不创建项目根目录下的文件夹。

---

### 环境检查（强制前置）

> 在进入第三步文书下载之前，必须先验证 zxfw 文书下载所需的 playwright 运行环境。**该检查是强制前置**，缺环境则中断整个下载流程，绝不静默降级到方案二（CLI 子进程）或方案三（MCP 浏览器），避免在 sandbox / 受限环境下产生无意义的中间状态。

**检查目标 Python 解释器**：

```
{{CODEX_PYTHON}}
```

该解释器位于 codex-primary-runtime（不在系统 PATH 中），是 zxfw 文书下载链路唯一被验证可用的 Python 3.12.13。

**判断逻辑**：

1. 用目标解释器执行 `import playwright`：
   - **成功**（`import playwright` 无异常）→ 直接进入第四步方案一（playwright + curl 抓 `getWsListBySdbhNew` 响应，详见下方）。
   - **失败**（`ModuleNotFoundError: No module named 'playwright'`）→ `exit 1` 中断当前流程，向用户输出明确提示：
     ```
     ❌ 缺少 playwright 运行环境
     当前解释器: <codex-python>
     缺失依赖: playwright / playwright chromium
     
     请按 references/env-setup.md 第 3.1 节装好 playwright + chromium 后重试:
       <codex-python> -m pip install --quiet playwright
       <codex-python> -m playwright install chromium
     ```
2. 失败时**不要**自动 `pip install`（可能命中网络/沙箱/权限问题），也不要静默回退到裸 `curl` 直连 zxfw API（裸 curl 会 400 RMFY109904，详见 `references/env-setup.md` 3.4 节）。
3. 检查通过后，沿用同一个 `<codex-python>` 启动 worker（`subprocess.run` / `& python` 时显式传绝对路径），不要用 `py` / 系统 `python` / `python3`。

**示例检查脚本**（可直接落地为 `check_playwright_env.py` 放在 skill `scripts/` 或 worker 临时目录）：

```python
"""check_playwright_env.py — court-sms skill 第四步强制前置环境检查

退出码:
  0  playwright 可用,继续走第四步方案一
  1  playwright 缺失或初始化失败,中断流程
"""
import sys
from pathlib import Path

CODEX_PY = Path(
    r"{{CODEX_PYTHON}}"
)

# 强制走目标解释器,避免用错 Python
if Path(sys.executable).resolve() != CODEX_PY.resolve():
    print(f"[FAIL] 当前解释器 {sys.executable} 非 codex-python", file=sys.stderr)
    print(f"        请改用: {CODEX_PY}", file=sys.stderr)
    sys.exit(1)

try:
    import playwright  # noqa: F401
    from playwright.sync_api import sync_playwright  # noqa: F401
except Exception as e:
    print(f"[FAIL] playwright 不可用: {e}", file=sys.stderr)
    print(f"        安装: {CODEX_PY} -m pip install --quiet playwright", file=sys.stderr)
    print(f"        然后: {CODEX_PY} -m playwright install chromium", file=sys.stderr)
    print(f"        详见 references/env-setup.md 3.1 节", file=sys.stderr)
    sys.exit(1)

# 可选:再起一个最小 headless chromium 自检
try:
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        b.close()
except Exception as e:
    print(f"[FAIL] chromium 启动失败: {e}", file=sys.stderr)
    print(f"        安装: {CODEX_PY} -m playwright install chromium", file=sys.stderr)
    sys.exit(1)

print("[OK] playwright + chromium 可用,继续走第四步方案一")
sys.exit(0)
```

worker 端调用方式：

```powershell
& "{{CODEX_PYTHON}}" check_playwright_env.py
if ($LASTEXITCODE -ne 0) { exit 1 }
# 检查通过,继续走第四步
```

**环境装不上的常见原因**（参见 `references/env-setup.md`）：

- 走错解释器（`py` / 系统 `python` 没有 playwright）→ 用绝对路径走 codex-python
- 沙箱/无网 → 先在有网环境装好 `pip install playwright` 和 `playwright install chromium`
- 漏装 chromium → `playwright install chromium`（实际装的是 `chrome-headless-shell`，详见 3.1.4）

---

### 第三步：文书下载

> **平台判断**：根据第一步识别的链接域名，选择下载策略。
> - `zxfw.court.gov.cn` → 方案一（API 直连）→ 方案二 → 方案三
> - `sd.gdems.com` 或 `jysd.10102368.com` → 跳过方案一，直接方案二 → 方案三
> - `dzsd.hbfy.gov.cn` → 湖北专属流程（见下方）
> - `sfpt.cdfy12368.gov.cn`（含广西实例 `171.106.48.55:28083`）→ SFDW 专属流程（见下方）
> - 未知域名但 URL 路径匹配已知平台特征 → 按路径识别平台（同构异域名支持）
> - 完全无法识别 → 提示用户提供链接信息
>
> **⛔ 降级铁律**：严格串行，禁止并行。当前方案成功即停止，绝不降级。禁止"双保险"并行尝试多个方案。

#### 方案一 — API 直连（优先）

完全无头，无需浏览器。直接调用 zxfw 后端 API 获取文书下载链接，再用 curl 下载 PDF。

**API 信息**：

- 端点：`POST https://zxfw.court.gov.cn/yzw/yzw-zxfw-sdfw/api/v1/sdfw/getWsListBySdbhNew`
- Content-Type：`application/json`
- 请求体：`{ "qdbh": "xxx", "sdbh": "xxx", "sdsin": "xxx" }`（从短信 URL 提取）
- 响应字段：`data[].c_wsmc`（文书名称）、`data[].wjlj`（OSS 签名下载链接）、`data[].c_fymc`（法院名称）
- 无需认证、无需浏览器

#### 方案二 — 无头浏览器（Playwright CLI）

当方案一 API 不可用或链接过期时，用 Playwright CLI 无头模式打开页面，拦截网络请求获取下载链接。

#### 方案三 — 交互式浏览器（Playwright MCP）

当方案二不可用时（需要已配置 Playwright MCP），使用浏览器自动化工具手动操作。

#### 失败兜底

当三级均失败时：

```text
⚠️ 自动下载失败，请手动访问以下链接下载：
{原始链接}

下载后请将文件放到对应案件目录中。

我将为您创建待处理记录。
```

---

### 第四步：归档保存

#### 4.1 文书归档

1. **确定目标目录**：第二步已确定 `案件管理/{当事人}/`，直接使用
2. **获取当前日期**：当前系统日期（YYYYMMDD 格式）
3. **确定文书标题**：
   - 优先使用 API 返回的标题
   - 否则根据 `sms-patterns.json` 中的 `document_titles` 映射推断
   - 最后回退到原始文件名（去除扩展名），如仍无法确定则使用 `未知文书`
4. **构建文件名**：`{title}（{当事人}）_{YYYYMMDD}收.pdf`
   - 示例：`受理通知书（张三）_20260404收.pdf`
   - 清理非法字符：`< > : " | ? * \ /`
   - 如同名文件已存在，追加 `_2` 后缀
5. **移入目标目录**：`案件管理/{当事人}/`
6. **写入内部记录**：保存本次处理的完整信息到 skill 内部的 `archive/` 目录（即 `archive/`），格式详见 [`references/archive-format.md`](references/archive-format.md)

#### 4.2 基础文书解析

法院 PDF 通常带文字层（如无文字层则调用 OCR MCP 工具），提取首页文本，快速识别文书类型和关键信息：

- **传票/开庭传票** → 提取开庭时间、地点、法庭、案号
- **通知书/告知书** → 提取缴费期限、举证期限等关键日期
- **起诉状/答辩状** → 提取案由、当事人、诉讼请求概要
- **判决书/裁定书** → 识别文书类型，触发上诉期限计算
- **其他文书** → 展示文书标题和法院名称

如一次下载多份文书，逐一解析，汇总为一份报告。

> 深度分析（如判决书解读、合同审查）不在此技能范围内，请使用 case-management 经验库路由。

#### 4.3 上诉期限计算（P1）

当识别到判决书/裁定书时自动计算：

| 案件类型 | 上诉期限 |
|---------|---------|
| 民事一审判决 | 送达后15天 |
| 民事裁定 | 送达后10天 |
| 行政判决 | 送达后15天 |
| 刑事判决 | 送达后10天 |
| 刑事裁定 | 送达后5天 |

- **计算公式**：`上诉截止日期 = 送达日期 + 上诉期限天数`
- **送达日期来源**：优先 zxfw API 的 `dt_cjsj` 字段 → 短信接收时间 `received_at` → 无法确定时展示"送达时间待确认"
- **归档 JSON 字段**：写入 `document.appeal_deadline` 和 `document.appeal_days_remaining`

#### 4.4 向用户汇报

按 [`references/report-format.md`](references/report-format.md) 输出结构化报告：
- 确认归档完成（案号、法院、当事人、案由、文件数、归档路径）
- 列出所有已归档的文书清单
- 如含传票，⚠️ 高亮提醒开庭时间、地点、审理程序
- 如含判决书/裁定书，⏰ 展示上诉期限信息
- 如部分失败，列出失败文书和原始链接

> **衔接 case-management 经验库**：汇报完成后，由经验库接管。根据下载的文书类型（判决书/传票/起诉状等），经验库将主动询问是否需要后续法律分析或庭前准备。详见 `memory/project/case-management/短信助手/index.md`。

---

### 第五步：PDF 后处理（可选）

> **不默认启用**。仅在检测到文件拆分时主动提示用户。

归档完成后，扫描目标目录中的 PDF 文件，检测是否有同一文书被拆分为多个文件的情况。

#### 读取用户偏好

读取 `config/user-preferences.json` 获取用户的合并和重命名偏好。如文件不存在，使用默认值（参考 `config/user-preferences.example.json`）。

关键偏好项：

| 偏好 | 默认值 | 说明 |
|------|--------|------|
| `merge_strategy` | `per_evidence` | 合并策略：`per_evidence`（按编号分别合并）或 `unified`（统一合并） |
| `merge_options.unified.bookmarks.enabled` | `true` | 统一合并时是否添加 PDF 书签 |
| `rename.enabled` | `true` | 是否精简文件名 |

---

## 内部归档格式

每次处理完成后在 `archive/` 下创建 JSON 记录，格式详见 [`references/archive-format.md`](references/archive-format.md)。

## 常见法院短信格式参考

### 文书送达短信

```text
【xx市人民法院】张三，您好！您有（2025）苏0981民初1234号案件文书送达，
请点击链接查收：
https://zxfw.court.gov.cn/zxfw/#/pagesAjkj/app/wssd/index?qdbh=DEMO1&sdbh=DEMO2&sdsin=DEMO3
如非本人操作请联系法院。
```

### 立案通知短信

```text
【xx市xx区人民法院】您好，您提交的立案材料已审核通过。
案号：（2025）京0105民初54321号
请及时缴纳诉讼费用。
```

### 开庭提醒短信

```text
【xx市xx区人民法院】提醒：您有（2025）苏0508民初567号案件，
定于2025年3月15日上午9:30在第3法庭开庭，请准时到庭。
```

## 故障排除

| 问题 | 解决方案 |
| --- | --- |
| 短信无法识别类型 | 展示原文，请用户确认类型后继续 |
| 案号提取失败 | 手动输入案号 |
| 当事人识别不准 | 提示用户确认/修正当事人列表 |
| 无匹配案件 | 提供三个选项：选已有/新建/暂存 |
| Playwright 下载超时 | 检查网络连接，尝试刷新页面重试 |
| 页面需要验证码 | 通知用户，暂停等待手动处理 |
| 下载文件损坏 | 清理临时目录，重新尝试下载 |
| 目标目录不存在 | 自动创建对应目录 |

## 配置

无额外配置需求。解析规则参考 `references/sms-patterns.json`。

如需修改解析规则（添加新文书标题、调整正则等），编辑该 JSON 文件即可。

## 🔄 变更历史

完整变更日志见 [CHANGELOG.md](CHANGELOG.md)。归属声明见 [references/ATTRIBUTION.md](references/ATTRIBUTION.md)。


---