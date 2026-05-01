"""
PDF Renderer for Qalam Language using ReportLab
محرك توليد PDF للغة قلم
"""

import os
import re
from typing import List, Dict, Any, Optional
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak as PLPageBreak, Image, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

import arabic_reshaper
from bidi.algorithm import get_display

from .ast_nodes import (
    Document, Chapter, Section, Subsection, Environment, 
    Paragraph as ParaNode, Figure, 
    Equation, Quote, Definition, Note, PageBreak, Comment
)


def rtl_text(text: str) -> str:
    """Convert Arabic text to RTL display format"""
    if not text:
        return ""
    try:
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    except:
        return text


class QalamPDFRenderer:
    """
    PDF Renderer for Qalam documents
    Generates professional academic PDFs with Navy/Gold theme
    """
    
    # Theme colors
    NAVY = colors.HexColor('#1B2A4A')
    GOLD = colors.HexColor('#C9A84C')
    LIGHT_GOLD = colors.HexColor('#E8D68C')
    WHITE = colors.white
    LIGHT_GRAY = colors.HexColor('#F5F5F5')
    DARK_GRAY = colors.HexColor('#333333')
    
    def __init__(self, output_path: str):
        self.output_path = output_path
        self.doc = None
        self.styles = None
        self.story = []
        self.page_number = 1
        self.total_pages = 0
        self.metadata = {}
        
        # Register fonts
        self._register_fonts()
    
    def _register_fonts(self):
        """Register Arabic-compatible fonts"""
        # Try to use DejaVu Sans which supports Arabic
        try:
            # Check if we have a suitable font
            from reportlab.lib.fonts import addMapping
            pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
        except:
            pass
    
    def render(self, document: Document) -> str:
        """Render document to PDF"""
        self.metadata = document.metadata
        
        # Create the PDF document
        self.doc = SimpleDocTemplate(
            self.output_path,
            pagesize=A4,
            rightMargin=2.5*cm,
            leftMargin=2.5*cm,
            topMargin=3*cm,
            bottomMargin=2.5*cm,
            title=document.metadata.get('title', 'Qalam Document'),
            author=document.metadata.get('student', ''),
        )
        
        # Build styles
        self._build_styles()
        
        # Generate cover page
        self._generate_cover_page(document)
        
        # Add table of contents placeholder
        self.story.append(PLPageBreak())
        
        # Generate content
        self._generate_content(document)
        
        # Build PDF
        self.doc.build(self.story, onFirstPage=self._add_header_footer,
                      onLaterPages=self._add_header_footer)
        
        return self.output_path
    
    def _build_styles(self):
        """Build paragraph styles"""
        self.styles = getSampleStyleSheet()
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='QalamTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=self.NAVY,
            alignment=TA_CENTER,
            spaceAfter=30,
            fontName='Helvetica-Bold'
        ))
        
        # Chapter style
        self.styles.add(ParagraphStyle(
            name='QalamChapter',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=self.NAVY,
            spaceBefore=20,
            spaceAfter=15,
            fontName='Helvetica-Bold'
        ))
        
        # Section style
        self.styles.add(ParagraphStyle(
            name='QalamSection',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=self.DARK_GRAY,
            spaceBefore=15,
            spaceAfter=10,
            fontName='Helvetica-Bold'
        ))
        
        # Subsection style
        self.styles.add(ParagraphStyle(
            name='QalamSubsection',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=self.DARK_GRAY,
            spaceBefore=12,
            spaceAfter=8,
            fontName='Helvetica-Bold'
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='QalamBody',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=self.DARK_GRAY,
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            leading=16,
        ))
        
        # Quote style
        self.styles.add(ParagraphStyle(
            name='QalamQuote',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=self.DARK_GRAY,
            leftIndent=2*cm,
            rightIndent=2*cm,
            spaceBefore=15,
            spaceAfter=15,
            borderLeftWidth=3,
            borderLeftColor=self.GOLD,
            italic=True,
        ))
        
        # Definition style
        self.styles.add(ParagraphStyle(
            name='QalamDefinition',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=self.DARK_GRAY,
            backColor=colors.HexColor('#E8F4F8'),
            leftIndent=1*cm,
            rightIndent=1*cm,
            spaceBefore=12,
            spaceAfter=12,
            borderLeftWidth=4,
            borderLeftColor=self.NAVY,
        ))
        
        # Note style
        self.styles.add(ParagraphStyle(
            name='QalamNote',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=self.DARK_GRAY,
            backColor=colors.HexColor('#FFF9E6'),
            leftIndent=1*cm,
            rightIndent=1*cm,
            spaceBefore=12,
            spaceAfter=12,
            borderLeftWidth=4,
            borderLeftColor=colors.orange,
        ))
    
    def _generate_cover_page(self, document: Document):
        """Generate an impressive cover page"""
        metadata = document.metadata
        
        # University header
        university = metadata.get('university', '')
        faculty = metadata.get('faculty', '')
        
        if university:
            self.story.append(Spacer(1, 2*cm))
            uni_para = Paragraph(rtl_text(university), 
                                style=self.styles['QalamTitle'])
            uni_para.style.alignment = TA_CENTER
            uni_para.style.fontSize = 16
            uni_para.style.textColor = self.NAVY
            self.story.append(uni_para)
        
        if faculty:
            fac_para = Paragraph(rtl_text(faculty),
                                style=self.styles['QalamBody'])
            fac_para.style.alignment = TA_CENTER
            fac_para.style.fontSize = 12
            self.story.append(fac_para)
        
        self.story.append(Spacer(1, 1*cm))
        
        # Gold decorative line
        self.story.append(Table([[None]], style=TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 3, self.GOLD),
            ('LINEBELOW', (0, 0), (-1, 0), 1, self.NAVY),
        ])))
        
        self.story.append(Spacer(1, 3*cm))
        
        # Document title
        title = metadata.get('title', 'Untitled')
        title_para = Paragraph(rtl_text(title),
                              style=self.styles['QalamTitle'])
        title_para.style.alignment = TA_CENTER
        title_para.style.fontSize = 20
        self.story.append(title_para)
        
        self.story.append(Spacer(1, 2*cm))
        
        # Student and supervisor info
        student = metadata.get('student', '')
        supervisor = metadata.get('supervisor', '')
        degree = metadata.get('degree', '')
        year = metadata.get('year', '')
        
        info_data = []
        if student:
            info_data.append([rtl_text(f"إعداد الطالب: {student}")])
        if supervisor:
            info_data.append([rtl_text(f"إشراف الأستاذ: {supervisor}")])
        if degree:
            info_data.append([rtl_text(f"درجة: {degree}")])
        if year:
            info_data.append([rtl_text(f"السنة: {year}")])
        
        if info_data:
            info_table = Table(info_data, colWidths=[15*cm])
            info_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('TEXTCOLOR', (0, 0), (-1, -1), self.NAVY),
                ('SPACEAFTER', (0, 0), (-1, -1), 10),
            ]))
            self.story.append(info_table)
        
        self.story.append(Spacer(1, 3*cm))
        
        # Bottom decorative element
        self.story.append(Table([[None]], style=TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 2, self.NAVY),
            ('LINEBELOW', (0, 0), (-1, 0), 3, self.GOLD),
        ])))
        
        self.story.append(PLPageBreak())
    
    def _generate_content(self, document: Document):
        """Generate document content"""
        for child in document.children:
            self._render_node(child)
    
    def _render_node(self, node):
        """Render a single AST node"""
        if isinstance(node, Chapter):
            self._render_chapter(node)
        elif isinstance(node, Section):
            self._render_section(node)
        elif isinstance(node, Subsection):
            self._render_subsection(node)
        elif isinstance(node, Environment):
            self._render_environment(node)
        elif isinstance(node, ParaNode):
            self._render_paragraph(node)
        elif isinstance(node, PageBreak):
            # removed
            self.story.append(PLPageBreak())
    
    def _render_chapter(self, chapter: Chapter):
        """Render chapter with colored banner"""
        # Chapter banner
        chapter_num = chapter.number or ""
        chapter_title = rtl_text(chapter.title)
        
        # Create banner table
        banner_data = [[Paragraph(f"{chapter_num} {chapter_title}", 
                                  self.styles['QalamChapter'])]]
        banner = Table(banner_data, colWidths=[16*cm])
        banner.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.NAVY),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.WHITE),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('LEFTPADDING', (0, 0), (-1, 0), 20),
            ('RIGHTPADDING', (0, 0), (-1, 0), 20),
        ]))
        
        self.story.append(banner)
        self.story.append(Spacer(1, 0.5*cm))
        
        # Render children
        for child in chapter.children:
            self._render_node(child)
    
    def _render_section(self, section: Section):
        """Render section"""
        section_title = rtl_text(section.title)
        sec_para = Paragraph(section_title, self.styles['QalamSection'])
        self.story.append(sec_para)
        
        for child in section.children:
            self._render_node(child)
    
    def _render_subsection(self, subsection: Subsection):
        """Render subsection"""
        subsec_title = rtl_text(subsection.title)
        subsec_para = Paragraph(subsec_title, self.styles['QalamSubsection'])
        self.story.append(subsec_para)
        
        for child in subsection.children:
            self._render_node(child)
    
    def _render_environment(self, env: Environment):
        """Render environment based on type"""
        env_type = env.env_type.lower()
        
        if env_type == 'quote':
            self._render_quote(env)
        elif env_type == 'definition':
            self._render_definition(env)
        elif env_type == 'note':
            self._render_note(env)
        elif env_type == 'table':
            self._render_table(env)
        elif env_type == 'abstract':
            self._render_abstract(env)
        elif env_type == 'introduction':
            self._render_introduction(env)
        elif env_type == 'conclusion':
            self._render_conclusion(env)
        elif env_type == 'list':
            self._render_list(env)
        else:
            # Generic environment
            content = rtl_text(env.content)
            para = Paragraph(content, self.styles['QalamBody'])
            self.story.append(para)
    
    def _render_quote(self, env: Environment):
        """Render quote environment"""
        content = rtl_text(env.content)
        ref = env.reference or ""
        
        quote_text = f"«{content}»"
        if ref:
            quote_text += f"\n— {rtl_text(ref)}"
        
        quote_para = Paragraph(quote_text, self.styles['QalamQuote'])
        self.story.append(quote_para)
    
    def _render_definition(self, env: Environment):
        """Render definition environment"""
        content = rtl_text(env.content)
        def_para = Paragraph(content, self.styles['QalamDefinition'])
        self.story.append(def_para)
    
    def _render_note(self, env: Environment):
        """Render note environment"""
        content = rtl_text(env.content)
        note_para = Paragraph(content, self.styles['QalamNote'])
        self.story.append(note_para)
    
    def _render_table(self, env: Environment):
        """Render table environment"""
        content = env.content
        caption = env.properties.get('caption', '') or env.reference or ''
        
        # Parse table from content
        rows = []
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('|') and line.endswith('|'):
                cells = [cell.strip() for cell in line[1:-1].split('|')]
                rows.append([rtl_text(cell) for cell in cells])
        
        if not rows:
            return
        
        # Create table
        num_cols = len(rows[0])
        table = Table(rows, colWidths=[14*cm/num_cols] * num_cols)
        
        # Style table
        table_style = [
            ('BACKGROUND', (0, 0), (-1, 0), self.NAVY),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.WHITE),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, self.LIGHT_GRAY),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [self.WHITE, self.LIGHT_GRAY]),
        ]
        
        table.setStyle(TableStyle(table_style))
        self.story.append(table)
        
        # Add caption
        if caption:
            caption_para = Paragraph(rtl_text(f"جدول: {caption}"),
                                    self.styles['QalamBody'])
            caption_para.style.alignment = TA_CENTER
            caption_para.style.fontSize = 9
            self.story.append(Spacer(1, 0.2*cm))
            self.story.append(caption_para)
    
    def _render_abstract(self, env: Environment):
        """Render abstract"""
        self.story.append(Paragraph(rtl_text("الملخص"), self.styles['QalamSection']))
        content = rtl_text(env.content)
        para = Paragraph(content, self.styles['QalamBody'])
        self.story.append(para)
        self.story.append(PLPageBreak())
    
    def _render_introduction(self, env: Environment):
        """Render introduction"""
        self.story.append(Paragraph(rtl_text("المقدمة"), self.styles['QalamSection']))
        content = rtl_text(env.content)
        para = Paragraph(content, self.styles['QalamBody'])
        self.story.append(para)
    
    def _render_conclusion(self, env: Environment):
        """Render conclusion"""
        self.story.append(Paragraph(rtl_text("الخاتمة"), self.styles['QalamSection']))
        content = rtl_text(env.content)
        para = Paragraph(content, self.styles['QalamBody'])
        self.story.append(para)
    
    def _render_list(self, env: Environment):
        """Render list"""
        content = env.content
        items = []
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('- '):
                items.append(line[2:])
        
        for item in items:
            item_text = f"• {rtl_text(item)}"
            para = Paragraph(item_text, self.styles['QalamBody'])
            para.style.leftIndent = 1*cm
            self.story.append(para)
    
    def _render_paragraph(self, para: ParaNode):
        """Render paragraph"""
        content = rtl_text(para.text)
        p = Paragraph(content, self.styles['QalamBody'])
        self.story.append(p)
    
    def _add_header_footer(self, canvas, doc):
        """Add header and footer to each page"""
        canvas.saveState()
        
        # Header
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(self.NAVY)
        
        title = self.metadata.get('title', '')[:50]
        canvas.drawString(2.5*cm, 28*cm, rtl_text(title))
        
        # Page number
        canvas.drawString(17*cm, 28*cm, f"صفحة {self.page_number}")
        
        # Footer with gold line
        canvas.setStrokeColor(self.GOLD)
        canvas.setLineWidth(2)
        canvas.line(2.5*cm, 1.5*cm, 18.5*cm, 1.5*cm)
        
        canvas.restoreState()
        self.page_number += 1
