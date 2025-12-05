#!/usr/bin/env python3
"""Convert Markdown documentation to PDF with Farsi support."""

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_RIGHT, TA_LEFT
import arabic_reshaper
from bidi.algorithm import get_display

# Read markdown
with open('Code_Documentation_FA.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Create PDF
pdf_file = "Code_Documentation_FA.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=A4)
story = []

# Styles
styles = getSampleStyleSheet()
normal_style = ParagraphStyle(
    'Normal',
    parent=styles['Normal'],
    fontSize=10,
    leading=16,
    alignment=TA_RIGHT,
)

heading_style = ParagraphStyle(
    'Heading',
    parent=styles['Heading1'],
    fontSize=14,
    leading=20,
    alignment=TA_RIGHT,
    textColor='#1f4788',
)

code_style = ParagraphStyle(
    'Code',
    parent=styles['Code'],
    fontSize=9,
    leading=12,
    alignment=TA_LEFT,
    fontName='Courier',
)

# Process content
lines = content.split('\n')
for line in lines:
    if not line.strip():
        story.append(Spacer(1, 0.2*inch))
        continue
    
    # Headings
    if line.startswith('###'):
        text = line.replace('###', '').strip()
        if any('\u0600' <= c <= '\u06FF' for c in text):  # Contains Farsi
            reshaped = arabic_reshaper.reshape(text)
            bidi_text = get_display(reshaped)
            story.append(Paragraph(bidi_text, heading_style))
        else:
            story.append(Paragraph(text, heading_style))
        story.append(Spacer(1, 0.1*inch))
    
    elif line.startswith('##'):
        text = line.replace('##', '').strip()
        if any('\u0600' <= c <= '\u06FF' for c in text):
            reshaped = arabic_reshaper.reshape(text)
            bidi_text = get_display(reshaped)
            story.append(Paragraph(bidi_text, heading_style))
        else:
            story.append(Paragraph(text, heading_style))
        story.append(Spacer(1, 0.15*inch))
    
    elif line.startswith('#'):
        text = line.replace('#', '').strip()
        story.append(PageBreak())
        if any('\u0600' <= c <= '\u06FF' for c in text):
            reshaped = arabic_reshaper.reshape(text)
            bidi_text = get_display(reshaped)
            story.append(Paragraph(bidi_text, heading_style))
        else:
            story.append(Paragraph(text, heading_style))
        story.append(Spacer(1, 0.2*inch))
    
    # Code blocks
    elif line.startswith('```'):
        continue
    
    # Normal text
    else:
        if any('\u0600' <= c <= '\u06FF' for c in line):  # Contains Farsi
            reshaped = arabic_reshaper.reshape(line)
            bidi_text = get_display(reshaped)
            story.append(Paragraph(bidi_text, normal_style))
        else:
            story.append(Paragraph(line, code_style if line.startswith('  ') else normal_style))

# Build PDF
doc.build(story)
print(f"✅ PDF created: {pdf_file}")
