"""{{USER_SHORT_NAME}}默认排版配置。来源: word-docx/SKILL.md "{{USER_SHORT_NAME}}默认排版配置"章节。"""

# 单一信息源(Single Source of Truth):
# 本文件中的 LAYOUT 字典与 word-docx/SKILL.md 的"{{USER_SHORT_NAME}}默认排版配置"章节
# 严格一一对应。修改时必须同步更新 SKILL.md，反之亦然。

LAYOUT = {
    # 页面布局 (cm)
    "margin_top_cm": 2.54,
    "margin_bottom_cm": 2.54,
    "margin_left_cm": 1.91,
    "margin_right_cm": 1.91,
    # 字体
    "font_main": "仿宋",
    # 字号 (pt)
    "font_size_title_pt": 16,   # 三号
    "font_size_body_pt": 14,    # 四号
    # 段落
    "line_spacing_pt": 24,      # 固定值 24 磅
    "indent_first_line_chars": 2,  # 首行缩进 2 字符
    "space_before_pt": 0,       # 段落间无空行
    "space_after_pt": 0,
    # 页脚
    "footer_centered_page_number": True,
    "footer_page_number_format": "第 X 页",  # X 替换为 PAGE 域
}


def apply_to_document(doc):
    """把 LAYOUT 配置套到 Document 对象上。"""
    from docx.shared import Pt, Cm
    from docx.enum.text import WD_LINE_SPACING, WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement

    # --- Normal 样式 (作为正文默认) ---
    normal = doc.styles["Normal"]
    normal.font.name = LAYOUT["font_main"]
    normal.font.size = Pt(LAYOUT["font_size_body_pt"])

    # 中文字体: python-docx 不会自动设中文字体, 必须手动写 w:eastAsia
    rpr = normal.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    rfonts.set(qn("w:eastAsia"), LAYOUT["font_main"])
    rfonts.set(qn("w:ascii"), LAYOUT["font_main"])
    rfonts.set(qn("w:hAnsi"), LAYOUT["font_main"])

    # 段落格式: 行距 24 磅固定值, 段落间无空行
    pf = normal.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = Pt(LAYOUT["line_spacing_pt"])
    pf.space_before = Pt(LAYOUT["space_before_pt"])
    pf.space_after = Pt(LAYOUT["space_after_pt"])
    # 默认首行缩进 2 字符 (14pt 字体 × 2 字符 = 28pt 缩进)
    pf.first_line_indent = Pt(
        LAYOUT["font_size_body_pt"] * LAYOUT["indent_first_line_chars"]
    )

    # --- 页面边距 ---
    for section in doc.sections:
        section.top_margin = Cm(LAYOUT["margin_top_cm"])
        section.bottom_margin = Cm(LAYOUT["margin_bottom_cm"])
        section.left_margin = Cm(LAYOUT["margin_left_cm"])
        section.right_margin = Cm(LAYOUT["margin_right_cm"])

    # --- 页脚: "第 X 页" 居中 ---
    if LAYOUT["footer_centered_page_number"]:
        section = doc.sections[0]
        footer = section.footer
        # 确保页脚有一个空段落可用
        if not footer.paragraphs:
            footer.add_paragraph()
        p = footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        # 清空页脚段落已有的 run
        for existing_run in list(p.runs):
            existing_run._r.getparent().remove(existing_run._r)

        # 写入: "第 <PAGE> 页"
        # "第 "
        run_prefix = p.add_run("第 ")
        _apply_run_font(run_prefix)
        # PAGE 域
        run_page = p.add_run()
        _apply_run_font(run_page)
        fldChar1 = OxmlElement("w:fldChar")
        fldChar1.set(qn("w:fldCharType"), "begin")
        instrText = OxmlElement("w:instrText")
        instrText.text = " PAGE "
        instrText.set(qn("xml:space"), "preserve")
        fldChar2 = OxmlElement("w:fldChar")
        fldChar2.set(qn("w:fldCharType"), "end")
        run_page._r.append(fldChar1)
        run_page._r.append(instrText)
        run_page._r.append(fldChar2)
        # " 页"
        run_suffix = p.add_run(" 页")
        _apply_run_font(run_suffix)


def _apply_run_font(run):
    """把 LAYOUT 字体字号套到 run 上 (用于页脚 PAGE 域文字)。"""
    from docx.shared import Pt
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement

    run.font.name = LAYOUT["font_main"]
    run.font.size = Pt(LAYOUT["font_size_body_pt"])
    rpr = run._r.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    rfonts.set(qn("w:eastAsia"), LAYOUT["font_main"])
    rfonts.set(qn("w:ascii"), LAYOUT["font_main"])
    rfonts.set(qn("w:hAnsi"), LAYOUT["font_main"])
