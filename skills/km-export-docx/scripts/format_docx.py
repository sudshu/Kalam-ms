#!/usr/bin/env python3
"""Post-process a pandoc-generated DOCX with publication-ready formatting.

Applies: 11pt body text, double spacing by default, centred footer page numbers, 2cm
margins, continuous line numbers, image resizing, figure-caption separators,
three-line academic tables, and paragraph spacing.

Optional --cover-letter keeps cover-letter spacing at 1.15 and omits page numbers.
"""

import argparse

from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.oxml.ns import qn
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from lxml import etree


def add_page_number(section):
    """Add an idempotent centred PAGE field to a section footer."""
    footer = section.footer
    if any(
        (node.text or "").strip() == "PAGE"
        for node in footer._element.iter(qn("w:instrText"))
    ):
        return

    paragraph = footer.paragraphs[0]
    if paragraph.text.strip() or paragraph._element.findall(qn("w:r")):
        paragraph = footer.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    run = paragraph.add_run()
    begin = etree.SubElement(run._r, qn("w:fldChar"))
    begin.set(qn("w:fldCharType"), "begin")
    instruction = etree.SubElement(run._r, qn("w:instrText"))
    instruction.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    instruction.text = " PAGE "
    separate = etree.SubElement(run._r, qn("w:fldChar"))
    separate.set(qn("w:fldCharType"), "separate")
    run._r.append(etree.Element(qn("w:t")))
    run._r[-1].text = "1"
    end = etree.SubElement(run._r, qn("w:fldChar"))
    end.set(qn("w:fldCharType"), "end")


def format_docx(filepath, cover_letter=False, full_width_figures=False,
                line_spacing=None, body_font=None):
    doc = Document(filepath)

    # --- A. Page layout ---
    for section in doc.sections:
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(2)
        section.right_margin = Cm(2)
        # Continuous line numbers
        sectPr = section._sectPr
        for ln in sectPr.findall(qn('w:lnNumType')):
            sectPr.remove(ln)
        lnNumType = etree.SubElement(sectPr, qn('w:lnNumType'))
        lnNumType.set(qn('w:countBy'), '1')
        lnNumType.set(qn('w:restart'), 'continuous')
        if not cover_letter:
            add_page_number(section)

    # --- B. Font size: 11pt body, headings untouched ---
    for para in doc.paragraphs:
        if not para.style.name.startswith("Heading"):
            for run in para.runs:
                if not run._element.findall(qn('w:drawing')):
                    run.font.size = Pt(11)
                    if body_font:
                        run.font.name = body_font
            # Paragraph-level default
            pPr = para._element.get_or_add_pPr()
            rPr = pPr.find(qn('w:rPr'))
            if rPr is None:
                rPr = etree.SubElement(pPr, qn('w:rPr'))
            sz = rPr.find(qn('w:sz'))
            if sz is None:
                sz = etree.SubElement(rPr, qn('w:sz'))
            sz.set(qn('w:val'), '22')  # 11pt = 22 half-points

    # --- C. Resize images ---
    MAX_W_CM, MAX_H_CM = 14.0, 16.0
    section = doc.sections[0]
    page_width = section.page_width or Inches(8.5)
    text_width = int(page_width - section.left_margin - section.right_margin)
    for para in doc.paragraphs:
        for run in para.runs:
            for d in run._element.findall(qn('w:drawing')):
                for ext in d.findall('.//' + qn('wp:extent')):
                    cx, cy = int(ext.get('cx', 0)), int(ext.get('cy', 0))
                    if cx <= 0 or cy <= 0:
                        continue
                    if full_width_figures:
                        scale = text_width / cx
                    else:
                        w_cm, h_cm = cx / 360000, cy / 360000
                        scale = min(
                            1.0,
                            MAX_W_CM / max(w_cm, 0.1),
                            MAX_H_CM / max(h_cm, 0.1),
                        )
                    if full_width_figures or scale < 1.0:
                        new_cx, new_cy = int(round(cx * scale)), int(round(cy * scale))
                        ext.set('cx', str(new_cx))
                        ext.set('cy', str(new_cy))
                        for ie in d.findall('.//' + qn('a:ext')):
                            if int(ie.get('cx', 0)) == cx and int(ie.get('cy', 0)) == cy:
                                ie.set('cx', str(new_cx))
                                ie.set('cy', str(new_cy))
                        if full_width_figures:
                            para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # --- D. Paragraph spacing ---
    for para in doc.paragraphs:
        pf = para.paragraph_format
        if para.style.name.startswith("Heading"):
            pf.space_before = Pt(8)
            pf.space_after = Pt(4)
        else:
            pf.space_before = Pt(2)
            pf.space_after = Pt(10)  # visible gap between paragraphs
        pf.line_spacing = (line_spacing if line_spacing is not None
                           else (1.15 if cover_letter else 2.0))

    # --- E. Tables: clean three-line academic style ---
    for table in doc.tables:
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl = table._element
        tblPr = tbl.find(qn('w:tblPr'))
        if tblPr is None:
            tblPr = etree.SubElement(tbl, qn('w:tblPr'))

        # Full page width
        for old in tblPr.findall(qn('w:tblW')):
            tblPr.remove(old)
        tblW = etree.SubElement(tblPr, qn('w:tblW'))
        tblW.set(qn('w:w'), '5000')
        tblW.set(qn('w:type'), 'pct')

        # Tight cell padding
        for old in tblPr.findall(qn('w:tblCellMar')):
            tblPr.remove(old)
        tblCellMar = etree.SubElement(tblPr, qn('w:tblCellMar'))
        for side in ['top', 'bottom']:
            m = etree.SubElement(tblCellMar, qn(f'w:{side}'))
            m.set(qn('w:w'), '15')
            m.set(qn('w:type'), 'dxa')
        for side in ['left', 'right']:
            m = etree.SubElement(tblCellMar, qn(f'w:{side}'))
            m.set(qn('w:w'), '40')
            m.set(qn('w:type'), 'dxa')

        # Three-line borders: top, header-bottom, table-bottom
        for old in tblPr.findall(qn('w:tblBorders')):
            tblPr.remove(old)
        borders = etree.SubElement(tblPr, qn('w:tblBorders'))
        for bname in ['top', 'bottom']:
            b = etree.SubElement(borders, qn(f'w:{bname}'))
            b.set(qn('w:val'), 'single')
            b.set(qn('w:sz'), '6')
            b.set(qn('w:color'), '000000')
        for bname in ['left', 'right', 'insideH', 'insideV']:
            b = etree.SubElement(borders, qn(f'w:{bname}'))
            b.set(qn('w:val'), 'none')

        # Header row: bold, black text, bottom border
        header_row = table.rows[0]
        for cell in header_row.cells:
            tcPr = cell._element.get_or_add_tcPr()
            for old in tcPr.findall(qn('w:shd')):
                tcPr.remove(old)
            tcBorders = tcPr.find(qn('w:tcBorders'))
            if tcBorders is None:
                tcBorders = etree.SubElement(tcPr, qn('w:tcBorders'))
            for old in tcBorders.findall(qn('w:bottom')):
                tcBorders.remove(old)
            b = etree.SubElement(tcBorders, qn('w:bottom'))
            b.set(qn('w:val'), 'single')
            b.set(qn('w:sz'), '6')
            b.set(qn('w:color'), '000000')
            for para in cell.paragraphs:
                para.alignment = WD_ALIGN_PARAGRAPH.LEFT
                para.paragraph_format.space_before = Pt(1)
                para.paragraph_format.space_after = Pt(1)
                para.paragraph_format.line_spacing = 1.0
                for run in para.runs:
                    run.font.size = Pt(8)
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(0, 0, 0)

        # Data rows: 8pt, no shading, bold for "selected" rows
        for i, row in enumerate(table.rows[1:], 1):
            # Detect selected rows: any cell containing "Yes"
            is_selected = any('Yes' in p.text
                              for c in row.cells for p in c.paragraphs)
            for j, cell in enumerate(row.cells):
                tcPr = cell._element.get_or_add_tcPr()
                for old in tcPr.findall(qn('w:shd')):
                    tcPr.remove(old)
                for para in cell.paragraphs:
                    para.paragraph_format.space_before = Pt(0)
                    para.paragraph_format.space_after = Pt(0)
                    para.paragraph_format.line_spacing = 1.0
                    # Right-align last column (typically Pearson r)
                    if j == len(row.cells) - 1:
                        para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                    for run in para.runs:
                        run.font.size = Pt(8)
                        run.font.bold = is_selected
                        run.font.color.rgb = RGBColor(0, 0, 0)

    # --- F. Add separator line between figures and captions ---
    # Pandoc renders ![caption](image) as an image paragraph followed by a
    # caption paragraph. Insert a thin horizontal rule between them so figures
    # and their legends are visually distinct in the Word document.
    paragraphs = list(doc.paragraphs)
    for i, para in enumerate(paragraphs):
        has_image = any(
            run._element.findall(qn('w:drawing'))
            for run in para.runs
        )
        if not has_image:
            continue
        # Look ahead: next non-empty paragraph is likely the caption
        for j in range(i + 1, min(i + 3, len(paragraphs))):
            next_para = paragraphs[j]
            if next_para.text.strip():
                # Insert a thin bottom border on the image paragraph
                pPr = para._element.get_or_add_pPr()
                pBdr = pPr.find(qn('w:pBdr'))
                if pBdr is None:
                    pBdr = etree.SubElement(pPr, qn('w:pBdr'))
                for old in pBdr.findall(qn('w:bottom')):
                    pBdr.remove(old)
                bottom = etree.SubElement(pBdr, qn('w:bottom'))
                bottom.set(qn('w:val'), 'single')
                bottom.set(qn('w:sz'), '4')       # thin line (0.5pt)
                bottom.set(qn('w:space'), '6')     # 6pt gap below line
                bottom.set(qn('w:color'), 'AAAAAA')  # light grey
                # Add a bit of space after the image paragraph
                para.paragraph_format.space_after = Pt(6)
                break

    doc.save(filepath)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Post-process a pandoc-generated DOCX with publication-ready formatting.'
    )
    parser.add_argument('filepath', help='Path to the .docx file to format')
    parser.add_argument(
        '--cover-letter',
        action='store_true',
        help='After formatting, override line spacing to 1.15 (for cover letters)'
    )
    parser.add_argument(
        '--full-width-figures',
        action='store_true',
        help='Expand embedded figures to the usable text width (main manuscripts)'
    )
    parser.add_argument(
        '--line-spacing',
        type=float,
        default=None,
        help=('Body line spacing; default 2.0 (1.15 with --cover-letter). Use 1.5 to match a '
              'PDF built with \\onehalfspacing, or 1.0 for single spacing.')
    )
    parser.add_argument(
        '--body-font',
        default=None,
        help=('Body typeface, e.g. "Cambria". Left unchanged if omitted. Choose a face the '
              'recipients will have installed, or Word will substitute.')
    )
    args = parser.parse_args()

    format_docx(
        args.filepath,
        cover_letter=args.cover_letter,
        full_width_figures=args.full_width_figures,
        line_spacing=args.line_spacing,
        body_font=args.body_font,
    )

    if args.cover_letter:
        print(f'Formatted (cover letter mode): {args.filepath}')
    else:
        print(f'Formatted: {args.filepath}')
