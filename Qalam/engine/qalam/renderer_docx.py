"""
Qalam Word Renderer - Generates .docx files using python-docx
Supports Arabic RTL, styles, and academic formatting
"""

import os
from typing import Dict, Any, List
from docx import Document as DocxDocument
from docx.shared import Cm, Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

from .ast_nodes import (
    Document, Chapter, Section, Subsection, Environment,
    Paragraph as ParaNode, TextNode, Table as TableNode,
    Figure, Equation, List as QList, Quote, Definition,
    Note, PageBreak as ASTPageBreak, ReferenceEntry
)


def set_rtl(paragraph):
    """Set paragraph to RTL direction"""
    pPr = paragraph._element.get_or_add_pPr()
    bidi = OxmlElement('w:bidi')
    bidi.set(qn('w:val'), '1')
    pPr.append(bidi)
    
    # Also set alignment to right
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT


def set_style_run(run, bold=False, italic=False, underline=False):
    """Apply styling to a run"""
    run.bold = bold
    run.italic = italic
    run.underline = underline


class DOCXRenderer:
    """
    Renders Qalam AST to Word document (.docx)
    Features: Navy/Gold theme, Arabic RTL, proper heading styles
    """
    
    # Colors
    NAVY = RGBColor(27, 42, 74)      # #1B2A4A
    GOLD = RGBColor(201, 168, 76)    # #C9A84C
    
    def __init__(self, output_path: str, metadata: Dict[str, Any] = None):
        self.output_path = output_path
        self.metadata = metadata or {}
        self.doc = DocxDocument()
        
        # Setup default styles
        self._setup_styles()
    
    def _setup_styles(self):
        """Configure document styles"""
        # Set default font
        style = self.doc.styles['Normal']
        font = style.font
        font.name = 'Arial'
        font.size = Pt(12)
        
        # Configure RTL for normal style
        style._element.rPr.rFonts.set(qn('w:eastAsia'), 'Arial')
        
        # Heading 1 (Chapters)
        if 'Heading 1' in self.doc.styles:
            h1 = self.doc.styles['Heading 1']
            h1.font.name = 'Arial'
            h1.font.size = Pt(18)
            h1.font.bold = True
            h1.font.color.rgb = self.NAVY
        
        # Heading 2 (Sections)
        if 'Heading 2' in self.doc.styles:
            h2 = self.doc.styles['Heading 2']
            h2.font.name = 'Arial'
            h2.font.size = Pt(14)
            h2.font.bold = True
            h2.font.color.rgb = self.NAVY
        
        # Heading 3 (Subsections)
        if 'Heading 3' in self.doc.styles:
            h3 = self.doc.styles['Heading 3']
            h3.font.name = 'Arial'
            h3.font.size = Pt(12)
            h3.font.bold = True
    
    def render(self, ast: Document):
        """Render the entire document"""
        # Add cover page
        self._add_cover_page()
        self.doc.add_page_break()
        
        # Process document children
        for child in ast.children:
            self._render_node(child)
        
        # Save document
        self.doc.save(self.output_path)
    
    def _add_cover_page(self):
        """Add professional cover page"""
        title = str(self.metadata.get('title', ''))
        student = str(self.metadata.get('student', ''))
        supervisor = str(self.metadata.get('supervisor', ''))
        university = str(self.metadata.get('university', ''))
        faculty = str(self.metadata.get('faculty', ''))
        year = str(self.metadata.get('year', '2025'))
        degree = str(self.metadata.get('degree', ''))
        doc_type = str(self.metadata.get('doc_type', 'مذكرة'))
        
        # University
        if university:
            p = self.doc.add_paragraph()
            run = p.add_run(university)
            run.bold = True
            run.font.size = Pt(14)
            run.font.color.rgb = self.NAVY
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_rtl(p)
        
        if faculty:
            p = self.doc.add_paragraph()
            run = p.add_run(faculty)
            run.font.size = Pt(12)
            run.font.color.rgb = self.NAVY
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_rtl(p)
        
        # Spacer
        self.doc.add_paragraph()
        self.doc.add_paragraph()
        
        # Document type
        p = self.doc.add_paragraph()
        run = p.add_run(doc_type)
        run.bold = True
        run.font.size = Pt(16)
        run.font.color.rgb = self.GOLD
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_rtl(p)
        
        # Title
        if title:
            p = self.doc.add_paragraph()
            run = p.add_run(title)
            run.bold = True
            run.font.size = Pt(22)
            run.font.color.rgb = self.NAVY
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_rtl(p)
        
        # Spacer
        self.doc.add_paragraph()
        self.doc.add_paragraph()
        self.doc.add_paragraph()
        
        # Student
        if student:
            p = self.doc.add_paragraph()
            run = p.add_run("إعداد الطالب:\n")
            run.font.size = Pt(12)
            run = p.add_run(student)
            run.bold = True
            run.font.size = Pt(14)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_rtl(p)
        
        # Supervisor
        if supervisor:
            p = self.doc.add_paragraph()
            run = p.add_run("تحت إشراف:\n")
            run.font.size = Pt(12)
            run = p.add_run(supervisor)
            run.bold = True
            run.font.size = Pt(14)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_rtl(p)
        
        # Spacer
        self.doc.add_paragraph()
        self.doc.add_paragraph()
        self.doc.add_paragraph()
        
        # Year and degree
        bottom_text = year
        if degree:
            bottom_text = f"{degree} | {year}"
        
        p = self.doc.add_paragraph()
        run = p.add_run(bottom_text)
        run.bold = True
        run.font.size = Pt(12)
        run.font.color.rgb = self.NAVY
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_rtl(p)
    
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
            self.doc.add_page_break()
    
    def _render_chapter(self, chapter: Chapter):
        """Render chapter with Heading 1 style"""
        # Use Heading 1 style
        p = self.doc.add_heading(chapter.title, level=1)
        set_rtl(p)
        
        # Render chapter children
        for child in chapter.children:
            self._render_node(child)
    
    def _render_section(self, section: Section):
        """Render section with Heading 2 style"""
        p = self.doc.add_heading(section.title, level=2)
        set_rtl(p)
        
        for child in section.children:
            self._render_node(child)
    
    def _render_subsection(self, subsection: Subsection):
        """Render subsection with Heading 3 style"""
        p = self.doc.add_heading(subsection.title, level=3)
        set_rtl(p)
        
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
            content = str(env.content)
            p = self.doc.add_paragraph(content)
            set_rtl(p)
    
    def _render_abstract(self, env: Environment):
        """Render abstract"""
        p = self.doc.add_heading("الملخص", level=2)
        set_rtl(p)
        
        content = str(env.content)
        para = self.doc.add_paragraph(content)
        set_rtl(para)
    
    def _render_introduction(self, env: Environment):
        """Render introduction"""
        p = self.doc.add_heading("المقدمة", level=2)
        set_rtl(p)
        
        content = str(env.content)
        para = self.doc.add_paragraph(content)
        set_rtl(para)
    
    def _render_conclusion(self, env: Environment):
        """Render conclusion"""
        p = self.doc.add_heading("الخاتمة", level=2)
        set_rtl(p)
        
        content = str(env.content)
        para = self.doc.add_paragraph(content)
        set_rtl(para)
    
    def _render_dedication(self, env: Environment):
        """Render dedication"""
        content = str(env.content)
        para = self.doc.add_paragraph()
        run = para.add_run(content)
        run.italic = True
        set_rtl(para)
    
    def _render_acknowledgements(self, env: Environment):
        """Render acknowledgements"""
        p = self.doc.add_heading("الشكر والتقدير", level=2)
        set_rtl(p)
        
        content = str(env.content)
        para = self.doc.add_paragraph(content)
        set_rtl(para)
    
    def _render_quote(self, env: Environment):
        """Render quote block"""
        content = str(env.content)
        
        para = self.doc.add_paragraph()
        
        # Add quotation marks
        run = para.add_run('"')
        run = para.add_run(content)
        run = para.add_run('"')
        
        if env.reference:
            ref_para = self.doc.add_paragraph()
            run = ref_para.add_run(f"— {env.reference}")
            run.font.size = Pt(10)
            run.font.color.rgb = RGBColor(128, 128, 128)
            run.italic = True
            set_rtl(ref_para)
        
        set_rtl(para)
    
    def _render_definition(self, env: Environment):
        """Render definition block"""
        content = str(env.content)
        para = self.doc.add_paragraph(content)
        set_rtl(para)
    
    def _render_note(self, env: Environment):
        """Render note block"""
        content = str(env.content)
        para = self.doc.add_paragraph(content)
        set_rtl(para)
    
    def _render_table_env(self, env: Environment):
        """Render table environment"""
        table_data = env.content
        
        if isinstance(table_data, TableNode):
            headers = table_data.headers
            rows = table_data.rows
            
            # Create table
            num_cols = len(headers)
            table = self.doc.add_table(rows=1, cols=num_cols)
            table.style = 'Table Grid'
            
            # Header row
            header_row = table.rows[0].cells
            for i, header in enumerate(headers):
                cell = header_row[i]
                cell.text = header
                # Style header
                for paragraph in cell.paragraphs:
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    set_rtl(paragraph)
            
            # Data rows
            for row_data in rows:
                row = table.add_row().cells
                for i, cell_data in enumerate(row_data):
                    cell = row[i]
                    cell.text = cell_data
                    for paragraph in cell.paragraphs:
                        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        set_rtl(paragraph)
            
            # Add caption
            if table_data.caption:
                caption_para = self.doc.add_paragraph(f"جدول: {table_data.caption}")
                caption_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                set_rtl(caption_para)
    
    def _render_figure_env(self, env: Environment):
        """Render figure environment"""
        fig = env.content if isinstance(env.content, Figure) else Figure()
        
        path = fig.path
        caption = fig.caption or ''
        
        if path and os.path.exists(path):
            try:
                self.doc.add_picture(path, width=Cm(12))
            except Exception as e:
                # Image loading failed
                placeholder = self.doc.add_paragraph(f"[صورة: {path}]")
                set_rtl(placeholder)
        
        if caption:
            cap_para = self.doc.add_paragraph(f"شكل: {caption}")
            cap_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_rtl(cap_para)
    
    def _render_equation(self, env: Environment):
        """Render equation"""
        eq = env.content if isinstance(env.content, Equation) else Equation()
        
        content = str(eq.content)
        para = self.doc.add_paragraph(content)
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        if eq.caption:
            cap_para = self.doc.add_paragraph(f"معادلة: {eq.caption}")
            cap_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_rtl(cap_para)
    
    def _render_list_env(self, env: Environment):
        """Render list environment"""
        qlist = env.content if isinstance(env.content, QList) else QList()
        
        for i, item in enumerate(qlist.items):
            if qlist.ordered:
                para = self.doc.add_paragraph(f"{i+1}. {item}")
            else:
                para = self.doc.add_paragraph(f"• {item}")
            set_rtl(para)
    
    def _render_references(self, env: Environment):
        """Render references"""
        p = self.doc.add_heading("المراجع", level=2)
        set_rtl(p)
        
        content = str(env.content)
        ref_lines = content.split('\n')
        
        for line in ref_lines:
            if line.strip():
                para = self.doc.add_paragraph(line)
                set_rtl(para)
    
    def _render_paragraph(self, para: ParaNode):
        """Render paragraph"""
        content = para.content
        p = self.doc.add_paragraph(content)
        set_rtl(p)
    
    def _render_text(self, text: TextNode):
        """Render text node"""
        para = self.doc.add_paragraph()
        run = para.add_run(text.text)
        set_style_run(run, text.bold, text.italic, text.underline)
        set_rtl(para)


def render_docx(ast: Document, output_path: str):
    """Convenience function to render Word document"""
    renderer = DOCXRenderer(output_path, ast.metadata)
    renderer.render(ast)
