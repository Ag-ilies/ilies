"""
Qalam PDF Renderer - Generates professional PDFs using ReportLab
Supports Arabic RTL, custom styling, and academic formatting
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
    PageBreak, Image, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

import arabic_reshaper
from bidi.algorithm import get_display

from .ast_nodes import (
    Document, Chapter, Section, Subsection, Environment,
    Paragraph as ParaNode, TextNode, Table as TableNode,
    Figure, Equation, List as QList, Quote, Definition,
    Note, PageBreak as ASTPageBreak, ReferenceEntry
)


def rtl(text: str) -> str:
    """Process Arabic text for RTL display"""
    if not text:
        return ""
    # Check if text contains Arabic characters
    if any('\u0600' <= c <= '\u06FF' for c in text):
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    return text


class PDFRenderer:
    """
    Renders Qalam AST to PDF using ReportLab
    Features: Navy/Gold theme, Arabic RTL, academic styling
    """
    
    # Colors
    NAVY = colors.HexColor('#1B2A4A')
    GOLD = colors.HexColor('#C9A84C')
    LIGHT_GOLD = colors.HexColor('#E8D89C')
    WHITE = colors.white
    BLACK = colors.black
    LIGHT_BLUE = colors.HexColor('#E3F2FD')
    LIGHT_YELLOW = colors.HexColor('#FFF9C4')
    GRAY = colors.HexColor('#757575')
    
    def __init__(self, output_path: str, metadata: Dict[str, Any] = None):
        self.output_path = output_path
        self.metadata = metadata or {}
        self.doc = None
        self.story = []
        self.styles = {}
        self.chapter_count = 0
        self.section_count = 0
        self.toc_entries = []
        self.figures_list = []
        self.tables_list = []
        
        # Setup document
        self.doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2.5*cm,
            leftMargin=2.5*cm,
            topMargin=2.5*cm,
            bottomMargin=2.5*cm,
            title=self.metadata.get('title', 'Qalam Document'),
            author=self.metadata.get('student', ''),
        )
        
        self._setup_styles()
    
    def _setup_styles(self):
        """Setup paragraph styles"""
        base_style = getSampleStyleSheet()['Normal']
        
        # Try to register Arabic font
        try:
            # Use DejaVu Sans which supports Arabic
            pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
            font_name = 'DejaVu'
        except:
            font_name = 'Helvetica'
        
        # Normal text style
        self.styles['Normal'] = ParagraphStyle(
            'Normal',
            parent=base_style,
            fontName=font_name,
            fontSize=12,
            leading=18,
            alignment=TA_RIGHT,
            spaceAfter=12,
        )
        
        # Chapter style
        self.styles['Chapter'] = ParagraphStyle(
            'Chapter',
            parent=base_style,
            fontName=font_name,
            fontSize=18,
            textColor=self.NAVY,
            alignment=TA_RIGHT,
            spaceBefore=30,
            spaceAfter=20,
            borderWidth=0,
            borderColor=self.GOLD,
            borderPadding=10,
        )
        
        # Section style
        self.styles['Section'] = ParagraphStyle(
            'Section',
            parent=base_style,
            fontName=font_name,
            fontSize=14,
            textColor=self.NAVY,
            alignment=TA_RIGHT,
            spaceBefore=24,
            spaceAfter=12,
        )
        
        # Subsection style
        self.styles['Subsection'] = ParagraphStyle(
            'Subsection',
            parent=base_style,
            fontName=font_name,
            fontSize=12,
            textColor=self.BLACK,
            fontStyle='bold',
            alignment=TA_RIGHT,
            spaceBefore=18,
            spaceAfter=10,
        )
        
        # Quote style
        self.styles['Quote'] = ParagraphStyle(
            'Quote',
            parent=base_style,
            fontName=font_name,
            fontSize=11,
            leftIndent=2*cm,
            rightIndent=2*cm,
            backColor=self.LIGHT_GOLD,
            borderWidth=1,
            borderColor=self.GOLD,
            borderPadding=10,
            alignment=TA_JUSTIFY,
            spaceAfter=15,
        )
        
        # Definition style
        self.styles['Definition'] = ParagraphStyle(
            'Definition',
            parent=base_style,
            fontName=font_name,
            fontSize=11,
            backColor=self.LIGHT_BLUE,
            borderWidth=1,
            borderColor=self.NAVY,
            borderPadding=10,
            alignment=TA_JUSTIFY,
            spaceAfter=15,
        )
        
        # Note style
        self.styles['Note'] = ParagraphStyle(
            'Note',
            parent=base_style,
            fontName=font_name,
            fontSize=11,
            backColor=self.LIGHT_YELLOW,
            borderWidth=1,
            borderColor=self.GOLD,
            borderPadding=10,
            alignment=TA_JUSTIFY,
            spaceAfter=15,
        )
        
        # Caption style
        self.styles['Caption'] = ParagraphStyle(
            'Caption',
            parent=base_style,
            fontName=font_name,
            fontSize=10,
            textColor=self.GRAY,
            alignment=TA_CENTER,
            spaceBefore=6,
            spaceAfter=6,
            fontStyle='italic',
        )
        
        # Abstract/Summary style
        self.styles['Abstract'] = ParagraphStyle(
            'Abstract',
            parent=base_style,
            fontName=font_name,
            fontSize=11,
            leftIndent=1*cm,
            rightIndent=1*cm,
            alignment=TA_JUSTIFY,
            spaceAfter=15,
        )
    
    def render(self, ast: Document):
        """Render the entire document"""
        # Add cover page
        self._add_cover_page()
        self.story.append(PageBreak())
        
        # Process document children
        for child in ast.children:
            self._render_node(child)
        
        # Build PDF
        self.doc.build(self.story)
    
    def _add_cover_page(self):
        """Add professional cover page with Navy/Gold theme"""
        from reportlab.platypus import Frame, PageTemplate
        
        title = rtl(str(self.metadata.get('title', '')))
        student = rtl(str(self.metadata.get('student', '')))
        supervisor = rtl(str(self.metadata.get('supervisor', '')))
        university = rtl(str(self.metadata.get('university', '')))
        faculty = rtl(str(self.metadata.get('faculty', '')))
        year = str(self.metadata.get('year', '2025'))
        degree = rtl(str(self.metadata.get('degree', '')))
        
        # Cover page content
        spacer = Spacer(1, 1*cm)
        
        # University name at top
        if university:
            uni_para = Paragraph(
                f"<b><font color='#1B2A4A' size='14'>{university}</font></b>",
                self.styles['Normal']
            )
            self.story.append(uni_para)
        
        self.story.append(Spacer(1, 0.5*cm))
        
        if faculty:
            fac_para = Paragraph(
                f"<font color='#1B2A4A' size='12'>{faculty}</font>",
                self.styles['Normal']
            )
            self.story.append(fac_para)
        
        self.story.append(Spacer(1, 2*cm))
        
        # Gold decorative line
        self.story.append(self._horizontal_line(self.GOLD, 2))
        self.story.append(Spacer(1, 0.5*cm))
        
        # Document type
        doc_type = rtl(str(self.metadata.get('doc_type', 'مذكرة')))
        type_para = Paragraph(
            f"<b><font color='#C9A84C' size='16'>{doc_type}</font></b>",
            self.styles['Normal']
        )
        self.story.append(type_para)
        self.story.append(Spacer(1, 0.5*cm))
        
        # Main title
        if title:
            title_para = Paragraph(
                f"<b><font color='#1B2A4A' size='22'>{title}</font></b>",
                self.styles['Normal']
            )
            self.story.append(title_para)
        
        self.story.append(Spacer(1, 0.5*cm))
        self.story.append(self._horizontal_line(self.GOLD, 2))
        
        self.story.append(Spacer(1, 3*cm))
        
        # Student and supervisor
        if student:
            student_label = rtl("إعداد الطالب:")
            student_para = Paragraph(
                f"{student_label}<br/><b><font size='14'>{student}</font></b>",
                self.styles['Normal']
            )
            self.story.append(student_para)
            self.story.append(Spacer(1, 0.5*cm))
        
        if supervisor:
            sup_label = rtl("تحت إشراف:")
            sup_para = Paragraph(
                f"{sup_label}<br/><b><font size='14'>{supervisor}</font></b>",
                self.styles['Normal']
            )
            self.story.append(sup_para)
        
        self.story.append(Spacer(1, 3*cm))
        
        # Year and degree
        bottom_text = f"<font size='12'>{year}</font>"
        if degree:
            bottom_text = rtl(str(degree)) + " | " + bottom_text
        
        bottom_para = Paragraph(
            f"<b><font color='#1B2A4A'>{bottom_text}</font></b>",
            self.styles['Normal']
        )
        self.story.append(bottom_para)
    
    def _horizontal_line(self, color, height=1):
        """Create a horizontal line"""
        from reportlab.platypus import Flowable
        
        class Line(Flowable):
            def __init__(self, color, height):
                Flowable.__init__(self)
                self.color = color
                self.height = height
            
            def draw(self):
                self.canv.setStrokeColor(self.color)
                self.canv.setLineWidth(self.height)
                self.canv.line(0, 0, 500, 0)
        
        return Line(color, height)
    
    def _render_node(self, node):
        """Render an AST node"""
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
        elif isinstance(node, TextNode):
            self._render_text(node)
        elif isinstance(node, ASTPageBreak):
            self.story.append(PageBreak())
    
    def _render_chapter(self, chapter: Chapter):
        """Render chapter with banner"""
        self.chapter_count += 1
        
        # Chapter banner
        title = rtl(chapter.title)
        
        # Navy banner with gold accent
        banner_text = f"<b><font color='#FFFFFF' size='16'>{title}</font></b>"
        
        # Create colored background using table trick
        table_data = [[Paragraph(banner_text, self.styles['Chapter'])]]
        table = Table(table_data, colWidths=[16*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.NAVY),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.5*cm))
        
        # Render chapter children
        for child in chapter.children:
            self._render_node(child)
    
    def _render_section(self, section: Section):
        """Render section"""
        self.section_count += 1
        title = rtl(section.title)
        
        sec_para = Paragraph(
            f"<b><font color='#1B2A4A' size='14'>{title}</font></b>",
            self.styles['Section']
        )
        self.story.append(sec_para)
        
        for child in section.children:
            self._render_node(child)
    
    def _render_subsection(self, subsection: Subsection):
        """Render subsection"""
        title = rtl(subsection.title)
        
        sub_para = Paragraph(
            f"<b><font size='12'>{title}</font></b>",
            self.styles['Subsection']
        )
        self.story.append(sub_para)
        
        for child in subsection.children:
            self._render_node(child)
    
    def _render_environment(self, env: Environment):
        """Render environment block"""
        env_type = env.env_type
        
        if env_type in ['abstract', 'ملخص']:
            self._render_abstract(env)
        elif env_type in ['introduction', 'مقدمة']:
            self._render_introduction(env)
        elif env_type in ['conclusion', 'خاتمة']:
            self._render_conclusion(env)
        elif env_type in ['dedication', 'إهداء']:
            self._render_dedication(env)
        elif env_type in ['acknowledgements', 'شكر']:
            self._render_acknowledgements(env)
        elif env_type in ['quote', 'اقتباس']:
            self._render_quote(env)
        elif env_type in ['definition', 'تعريف']:
            self._render_definition(env)
        elif env_type in ['note', 'ملاحظة']:
            self._render_note(env)
        elif env_type in ['table', 'جدول']:
            self._render_table_env(env)
        elif env_type in ['figure', 'شكل']:
            self._render_figure_env(env)
        elif env_type in ['equation', 'معادلة']:
            self._render_equation(env)
        elif env_type in ['list', 'قائمة']:
            self._render_list_env(env)
        elif env_type in ['references', 'مراجع']:
            self._render_references(env)
        else:
            # Generic environment
            content = rtl(str(env.content))
            para = Paragraph(content, self.styles['Normal'])
            self.story.append(para)
    
    def _render_abstract(self, env: Environment):
        """Render abstract/summary"""
        title = rtl("الملخص")
        title_para = Paragraph(
            f"<b><font color='#1B2A4A'>{title}</font></b>",
            self.styles['Section']
        )
        self.story.append(title_para)
        
        content = rtl(str(env.content))
        abs_para = Paragraph(content, self.styles['Abstract'])
        self.story.append(abs_para)
        self.story.append(Spacer(1, 0.5*cm))
    
    def _render_introduction(self, env: Environment):
        """Render introduction"""
        title = rtl("المقدمة")
        title_para = Paragraph(
            f"<b><font color='#1B2A4A'>{title}</font></b>",
            self.styles['Section']
        )
        self.story.append(title_para)
        
        content = rtl(str(env.content))
        intro_para = Paragraph(content, self.styles['Normal'])
        self.story.append(intro_para)
    
    def _render_conclusion(self, env: Environment):
        """Render conclusion"""
        title = rtl("الخاتمة")
        title_para = Paragraph(
            f"<b><font color='#1B2A4A'>{title}</font></b>",
            self.styles['Section']
        )
        self.story.append(title_para)
        
        content = rtl(str(env.content))
        concl_para = Paragraph(content, self.styles['Normal'])
        self.story.append(concl_para)
    
    def _render_dedication(self, env: Environment):
        """Render dedication"""
        content = rtl(str(env.content))
        ded_para = Paragraph(
            f"<i>{content}</i>",
            self.styles['Normal']
        )
        self.story.append(Spacer(1, 2*cm))
        self.story.append(ded_para)
        self.story.append(Spacer(1, 2*cm))
    
    def _render_acknowledgements(self, env: Environment):
        """Render acknowledgements"""
        title = rtl("الشكر والتقدير")
        title_para = Paragraph(
            f"<b><font color='#1B2A4A'>{title}</font></b>",
            self.styles['Section']
        )
        self.story.append(title_para)
        
        content = rtl(str(env.content))
        ack_para = Paragraph(content, self.styles['Normal'])
        self.story.append(ack_para)
    
    def _render_quote(self, env: Environment):
        """Render quote block"""
        content = rtl(str(env.content))
        
        quote_text = f'"{content}"'
        if env.reference:
            quote_text += f"<br/><font size='10' color='#757575'>— {rtl(env.reference)}</font>"
        
        quote_para = Paragraph(quote_text, self.styles['Quote'])
        self.story.append(quote_para)
    
    def _render_definition(self, env: Environment):
        """Render definition block"""
        content = rtl(str(env.content))
        def_para = Paragraph(content, self.styles['Definition'])
        self.story.append(def_para)
    
    def _render_note(self, env: Environment):
        """Render note block"""
        content = rtl(str(env.content))
        note_para = Paragraph(content, self.styles['Note'])
        self.story.append(note_para)
    
    def _render_table_env(self, env: Environment):
        """Render table environment"""
        table_data = env.content
        
        if isinstance(table_data, TableNode):
            headers = [rtl(h) for h in table_data.headers]
            rows = [[rtl(cell) for cell in row] for row in table_data.rows]
            
            data = [headers] + rows
            
            # Create table
            num_cols = len(headers)
            if num_cols == 0:
                return  # Empty table, skip
            
            col_width = (15*cm) / num_cols
            table = Table(data, colWidths=[col_width]*num_cols)
            
            # Style table
            table.setStyle(TableStyle([
                # Header row
                ('BACKGROUND', (0, 0), (-1, 0), self.NAVY),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                
                # Data rows
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.LIGHT_GOLD]),
                ('GRID', (0, 0), (-1, -1), 1, self.GOLD),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            
            self.story.append(table)
            
            # Add caption if exists
            if table_data.caption:
                caption = rtl(f"جدول: {table_data.caption}")
                cap_para = Paragraph(caption, self.styles['Caption'])
                self.story.insert(len(self.story)-1, cap_para)
    
    def _render_figure_env(self, env: Environment):
        """Render figure environment"""
        fig = env.content if isinstance(env.content, Figure) else Figure()
        
        caption = rtl(fig.caption or '')
        path = fig.path
        
        if path and os.path.exists(path):
            try:
                img = Image(path, width=12*cm, height=8*cm)
                self.story.append(img)
            except Exception as e:
                # Image loading failed, show placeholder
                placeholder = Paragraph(
                    f"[{rtl('صورة')}: {path}]",
                    self.styles['Caption']
                )
                self.story.append(placeholder)
        
        if caption:
            cap_text = rtl(f"شكل: {caption}")
            cap_para = Paragraph(cap_text, self.styles['Caption'])
            self.story.append(cap_para)
    
    def _render_equation(self, env: Environment):
        """Render equation"""
        eq = env.content if isinstance(env.content, Equation) else Equation()
        
        content = str(eq.content)
        caption = rtl(eq.caption or '')
        
        # Simple equation rendering (for complex math, would need MathML)
        eq_para = Paragraph(
            f"<i>{content}</i>",
            self.styles['Normal']
        )
        
        # Center equation
        from reportlab.platypus import KeepTogether
        eq_block = KeepTogether([eq_para])
        self.story.append(eq_block)
        
        if caption:
            cap_text = rtl(f"معادلة: {caption}")
            cap_para = Paragraph(cap_text, self.styles['Caption'])
            self.story.append(cap_para)
    
    def _render_list_env(self, env: Environment):
        """Render list environment"""
        qlist = env.content if isinstance(env.content, QList) else QList()
        
        for i, item in enumerate(qlist.items):
            item_text = rtl(str(item))
            bullet = "•" if not qlist.ordered else f"{i+1}."
            
            list_para = Paragraph(
                f"{bullet} {item_text}",
                self.styles['Normal']
            )
            self.story.append(list_para)
    
    def _render_references(self, env: Environment):
        """Render references/bibliography"""
        title = rtl("المراجع")
        title_para = Paragraph(
            f"<b><font color='#1B2A4A'>{title}</font></b>",
            self.styles['Section']
        )
        self.story.append(title_para)
        self.story.append(Spacer(1, 0.5*cm))
        
        # Parse references from content
        content = str(env.content)
        ref_lines = content.split('\n')
        
        for line in ref_lines:
            if line.strip():
                ref_para = Paragraph(
                    rtl(line),
                    self.styles['Normal']
                )
                self.story.append(ref_para)
    
    def _render_paragraph(self, para: ParaNode):
        """Render paragraph"""
        content = rtl(para.content)
        
        # Handle inline formatting
        content = self._process_inline_formatting(content)
        
        para_obj = Paragraph(content, self.styles['Normal'])
        self.story.append(para_obj)
    
    def _render_text(self, text: TextNode):
        """Render text node"""
        content = rtl(text.text)
        
        if text.bold:
            content = f"<b>{content}</b>"
        if text.italic:
            content = f"<i>{content}</i>"
        if text.underline:
            content = f"<u>{content}</u>"
        
        text_para = Paragraph(content, self.styles['Normal'])
        self.story.append(text_para)
    
    def _process_inline_formatting(self, text: str) -> str:
        """Process inline formatting markers"""
        # Bold **text**
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
        # Italic *text*
        text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
        # Underline __text__
        text = re.sub(r'__(.+?)__', r'<u>\1</u>', text)
        
        return text


def render_pdf(ast: Document, output_path: str):
    """Convenience function to render PDF"""
    renderer = PDFRenderer(output_path, ast.metadata)
    renderer.render(ast)
