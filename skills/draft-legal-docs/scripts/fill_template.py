#!/usr/bin/env python3
"""模板填充脚本 — 直接 OOXML 文本替换，零格式损耗

用法: python fill_template.py 模板.docx 输出.docx --data data.json
      或逐项: python fill_template.py 模板.docx 输出.docx --set "【占位符】" "值" --set "【占位符2】" "值2"
"""

import zipfile, re, json, shutil, sys, argparse
from pathlib import Path

T_RE = re.compile(rb'<[^>]*:?t[^>]*>([^<]*)</[^>]*:?t>')


def fill_template(template: str, output: str, replacements: dict):
    """复制模板 → XML 级别替换占位符 → 保存"""
    shutil.copy(template, output)
    
    with zipfile.ZipFile(output, 'r') as zin:
        items = {item.filename: zin.read(item.filename) for item in zin.infolist()}
    
    xml = items['word/document.xml']
    count = 0
    
    def replace_t(m):
        nonlocal count
        text = m.group(1).decode('utf-8', errors='ignore')
        for old, new in replacements.items():
            if old in text:
                count += 1
                text = text.replace(old, new)
        return m.group(0).replace(m.group(1), text.encode('utf-8'))
    
    items['word/document.xml'] = T_RE.sub(replace_t, xml)
    
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zout:
        for name, data in items.items():
            zout.writestr(name, data)
    
    return count


def main():
    parser = argparse.ArgumentParser(description='lawerD 模板填充')
    parser.add_argument('template', help='模板路径')
    parser.add_argument('output', help='输出路径')
    parser.add_argument('--data', help='JSON 数据文件（key=占位符，value=替换值）')
    parser.add_argument('--set', nargs=2, action='append', metavar=('OLD', 'NEW'),
                        help='逐项替换（可多次使用）')
    args = parser.parse_args()
    
    replacements = {}
    if args.data:
        with open(args.data, 'r', encoding='utf-8') as f:
            replacements = json.load(f)
    if args.set:
        for old, new in args.set:
            replacements[old] = new
    
    if not replacements:
        print('❌ 请提供 --data 或 --set')
        sys.exit(1)
    
    n = fill_template(args.template, args.output, replacements)
    print(f'✅ 替换 {n} 处 → {args.output}')


if __name__ == '__main__':
    main()
