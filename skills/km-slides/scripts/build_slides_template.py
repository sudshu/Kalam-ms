#!/usr/bin/env python3
"""
Kalam — Slide deck builder template using python-pptx.
Customize this script for each manuscript and stage.
"""

import os
import sys
from pathlib import Path

try:
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor
except ImportError:
    print("python-pptx not installed. Run: pip install python-pptx")
    sys.exit(1)


def create_title_slide(prs, title, subtitle, authors):
    """Create the title slide."""
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = title
    slide.placeholders[1].text = f"{authors}\n{subtitle}"
    return slide


def create_content_slide(prs, title, bullets):
    """Create a slide with title and bullet points."""
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = title
    body = slide.placeholders[1]
    tf = body.text_frame
    tf.clear()
    for i, bullet in enumerate(bullets):
        if i == 0:
            tf.paragraphs[0].text = bullet
        else:
            p = tf.add_paragraph()
            p.text = bullet
        tf.paragraphs[i].font.size = Pt(18)
    return slide


def create_figure_slide(prs, title, figure_path, message_bullets=None):
    """Create a slide with a figure and optional message bullets."""
    slide = prs.slides.add_slide(prs.slide_layouts[5])  # blank layout

    # Add title
    from pptx.util import Inches, Pt
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(9), Inches(0.6))
    tf = txBox.text_frame
    tf.text = title
    tf.paragraphs[0].font.size = Pt(24)
    tf.paragraphs[0].font.bold = True

    # Add figure
    if os.path.exists(figure_path):
        slide.shapes.add_picture(
            figure_path,
            Inches(0.5), Inches(1.0),
            width=Inches(6), height=Inches(4.5)
        )
    else:
        txBox2 = slide.shapes.add_textbox(Inches(1), Inches(2.5), Inches(8), Inches(1))
        txBox2.text_frame.text = f"[Figure: {figure_path}]"

    # Add message bullets on the right
    if message_bullets:
        txBox3 = slide.shapes.add_textbox(Inches(6.8), Inches(1.0), Inches(3), Inches(4.5))
        tf3 = txBox3.text_frame
        tf3.word_wrap = True
        for i, bullet in enumerate(message_bullets):
            if i == 0:
                tf3.paragraphs[0].text = f"• {bullet}"
            else:
                p = tf3.add_paragraph()
                p.text = f"• {bullet}"
            tf3.paragraphs[i].font.size = Pt(14)

    return slide


def build_ideation_deck(
    output_path,
    title="Paper Title",
    authors="Author List",
    research_question="",
    motivation_bullets=None,
    figures=None,
    narrative_arc="",
    open_questions=None,
):
    """Build a Stage 1 (Ideation) discussion deck."""
    prs = Presentation()

    # Slide 1: Title
    create_title_slide(prs, title, "Discussion Draft — Ideation", authors)

    # Slide 2: Research Question
    bullets = [research_question]
    if motivation_bullets:
        bullets.extend(motivation_bullets)
    create_content_slide(prs, "Research Question & Motivation", bullets)

    # Slides 3–N: Figures
    if figures:
        for fig in figures:
            create_figure_slide(
                prs,
                fig.get("title", "Figure"),
                fig.get("path", ""),
                fig.get("messages", []),
            )

    # Narrative arc slide
    if narrative_arc:
        create_content_slide(prs, "Proposed Narrative Arc", [narrative_arc])

    # Open questions slide
    if open_questions:
        create_content_slide(prs, "Open Questions for Discussion", open_questions)

    prs.save(output_path)
    print(f"Saved: {output_path}")


def build_skeleton_deck(
    output_path,
    title="Paper Title",
    authors="Author List",
    core_claim="",
    target_journal="",
    structure_bullets=None,
    figures=None,
    reference_strategy=None,
    feedback_needed=None,
    timeline="",
):
    """Build a Stage 2 (Skeleton) discussion deck."""
    prs = Presentation()

    # Slide 1: Title
    create_title_slide(prs, title, "Skeleton Review", authors)

    # Slide 2: Core claim + journal
    create_content_slide(prs, "Core Claim", [core_claim, f"Target: {target_journal}"])

    # Slide 3: Structure
    if structure_bullets:
        create_content_slide(prs, "Paper Structure", structure_bullets)

    # Slides 4–N: Figures with captions
    if figures:
        for fig in figures:
            create_figure_slide(
                prs,
                fig.get("title", "Figure"),
                fig.get("path", ""),
                fig.get("messages", []),
            )

    # Reference strategy
    if reference_strategy:
        create_content_slide(prs, "Reference Strategy", reference_strategy)

    # Feedback needed
    if feedback_needed:
        create_content_slide(prs, "Feedback Needed", feedback_needed)

    # Timeline
    if timeline:
        create_content_slide(prs, "Timeline", [timeline])

    prs.save(output_path)
    print(f"Saved: {output_path}")


# --- Example usage (customize for each manuscript) ---
if __name__ == "__main__":
    # This is a template. The kalam-slides skill will generate a customized
    # version of this script for each manuscript.
    print("This is a template. Customize for your manuscript.")
    print("See kalam-slides/SKILL.md for instructions.")
