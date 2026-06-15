#!/usr/bin/env python3
"""证据目录 XLSX 模板填充脚本 — openpyxl 文本替换 + 动态行管理 (v2 简化版)

用法:
  python fill_template_xlsx.py 证据目录.template.xlsx 输出.xlsx --data data.json
  python fill_template_xlsx.py 证据目录.template.xlsx 输出.xlsx --提交人 "原告张三" --日期 "2026-06-15"

JSON 数据格式:
{
  "提交人": "原告：张三",
  "目录制作日期": "2026-06-15",
  "证据列表": [
    {"名称": "借款合同", "证明目的": "证明双方存在借贷合意", "页码": "1-7"},
    {"名称": "银行转账凭证", "证明目的": "证明原告已履行出借义务", "页码": "8-11"}
  ]
}

每项一行，自动中文编号（一/二/三…），A+B 合并写编号，C 写名称，D 写证明目的。
"""

import openpyxl, json, sys, argparse, shutil
from openpyxl.styles import Font, Alignment, Border, Side

# ── 中文数字（支持到九十九） ──────────────────────────────────
_CN = '零一二三四五六七八九十'
def _cn_num(n: int) -> str:
    if n <= 10:
        return _CN[n]
    if n < 20:
        return '十' + _CN[n - 10]
    tens = n // 10
    ones = n % 10
    s = _CN[tens] + '十'
    if ones:
        s += _CN[ones]
    return s


# ── 样式 ────────────────────────────────────────────────────
THIN_BORDER = Border(
    left=Side(style='thin'), right=Side(style='thin'),
    top=Side(style='thin'), bottom=Side(style='thin'))
FONT_DEFAULT = Font(name='宋体', size=12)
FONT_DATE    = Font(name='宋体', size=11)
ALIGN_CENTER       = Alignment(horizontal='center', vertical='center')
ALIGN_CENTER_WRAP  = Alignment(horizontal='center', vertical='center', wrap_text=True)
ALIGN_LEFT_WRAP    = Alignment(horizontal='left',   vertical='center', wrap_text=True)
ALIGN_RIGHT        = Alignment(horizontal='right',  vertical='center')
NO_BORDER = Border()


def _apply(cell, value=None, font=FONT_DEFAULT, alignment=ALIGN_CENTER,
           border=THIN_BORDER, number_format='General'):
    cell.value = value
    cell.font = font
    cell.alignment = alignment
    cell.border = border
    cell.number_format = number_format


# ═══════════════════════════════════════════════════════════
#  核心
# ═══════════════════════════════════════════════════════════

def fill_xlsx(template_path: str, output_path: str,
              submitter: str = None, date_str: str = None,
              items: list = None):
    shutil.copy(template_path, output_path)
    wb = openpyxl.load_workbook(output_path)
    ws = wb.active

    # ── 1. 提交人 ──
    if submitter:
        ws['A2'] = f'提交人 ： {submitter}'
        _apply(ws['A2'], ws['A2'].value, font=FONT_DEFAULT,
               alignment=ALIGN_LEFT_WRAP, border=NO_BORDER)

    # ── 2. 解除旧数据区合并 ──
    _unmerge_data_rows(ws)
    DATA_START = 4
    DATA_END   = 12

    # ── 3. 逐行写入 ──
    if items:
        current_row = DATA_START
        for i, it in enumerate(items, 1):
            name = it.get('名称', '')
            证明目的 = it.get('证明目的', '')
            页码     = it.get('页码', '')
            _write_row(ws, current_row, _cn_num(i), name, 证明目的, 页码)
            current_row += 1
    else:
        current_row = DATA_START

    # ── 4. 清理多余旧行 ──
    _clear_rows(ws, current_row, max(DATA_END, 13))

    # ── 5. 日期落款 ──
    date_row = current_row + 1
    _apply(ws.cell(row=date_row, column=4),
           value=f'目录制作日期：{date_str or "YY-MM-DD"}',
           font=FONT_DATE, alignment=ALIGN_RIGHT, border=NO_BORDER)

    wb.save(output_path)
    return output_path


def _unmerge_data_rows(ws):
    for mc in list(ws.merged_cells.ranges):
        if mc.min_row >= 4:
            ws.unmerge_cells(str(mc))


def _write_row(ws, row, 编号: str, name: str, 证明目的: str, 页码: str):
    """写入一行：A+B 合并写中文编号，C 写名称，D 写证明目的。"""
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=2)
    _apply(ws.cell(row=row, column=1), value=编号, alignment=ALIGN_CENTER_WRAP)
    _apply(ws.cell(row=row, column=3), value=name)
    _apply(ws.cell(row=row, column=4), value=证明目的, alignment=ALIGN_CENTER_WRAP)
    _apply(ws.cell(row=row, column=5), value=页码, number_format='@')
    ws.row_dimensions[row].height = 38


def _clear_rows(ws, from_row, up_to_row):
    for r in range(from_row, up_to_row + 1):
        for c in range(1, 6):
            try:
                cell = ws.cell(row=r, column=c)
                cell.value = None
                cell.border = NO_BORDER
                cell.font = FONT_DEFAULT
            except AttributeError:
                pass  # MergedCell


# ═══════════════════════════════════════════════════════════
#  CLI
# ═══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description='证据目录 XLSX 模板填充 (v2)')
    parser.add_argument('template', help='模板路径（.xlsx）')
    parser.add_argument('output',   help='输出路径（.xlsx）')
    parser.add_argument('--data',   help='JSON 数据文件')
    parser.add_argument('--提交人', help='证据提交方')
    parser.add_argument('--日期',   help='目录制作日期（YYYY-MM-DD）')
    args = parser.parse_args()

    submitter = args.提交人
    date_str  = args.日期
    items     = None

    if args.data:
        with open(args.data, 'r', encoding='utf-8') as f:
            d = json.load(f)
        submitter = d.get('提交人', submitter)
        date_str  = d.get('目录制作日期', date_str)
        items     = d.get('证据列表') or d.get('证据分组')

    if not items:
        print('WARNING: no evidence items provided, only title placeholders replaced.')

    out = fill_xlsx(args.template, args.output,
                    submitter=submitter, date_str=date_str, items=items)
    print(f'Done: {out}')


if __name__ == '__main__':
    main()
