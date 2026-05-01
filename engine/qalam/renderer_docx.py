"""
Word Renderer for Qalam Language using python-docx
محرك توليد Word للغة قلم
"""

import os
from typing import List, Dict, Any, Optional
from docx import Document as DocxDocument
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn

import arabic_reshaper
from bidi.algorithm import get_display

from .ast_nodes import (
    Document, Chapter, Section, Subsection, Environment,
    Paragraph as ParaNode, PageBreak, Comment
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


def set_rtl(paragraph):
    """Set paragraph to RTL direction"""
    try:
        pPr = paragraph._element.get_or_add_pPr()
        bidi = pPr.get_or_add_bidi()
        bidi.val = True
    except AttributeError:
        # Fallback for newer python-docx versions
        from docx.oxml import OxmlElement
        pPr = paragraph._element.get_or_add_pPr()
        bidi = OxmlElement('w:bidi')
        bidi.set(qn('w:val'), '1')
        pPr.append(bidi)
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT


class QalamWordRenderer:
    """
    Word Renderer for Qalam documents
    Generates professional academic Word documents with proper RTL support
    """
    
    # Theme colors
    NAVY = RGBColor(27, 42, 74)  # #1B2A4A
    GOLD = RGBColor(201, 168, 76)  # #C9A84C
    DARK_GRAY = RGBColor(51, 51, 51)
    
    def __init__(self, output_path: str):
        self.output_path = output_path
        self.doc = DocxDocument()
        self.metadata = {}
        
        # Setup styles
        self._setup_styles()
    
    def _setup_styles(self):
        """Setup document styles"""
        styles = self.doc.styles
        
        # Modify Normal style for Arabic
        if 'Normal' in styles:
            normal_style = styles['Normal']
            font = normal_style.font
            font.size = Pt(11)
            font.name = 'Arial'
            try:
                font._element.rFonts.set(qn('w:eastAsia'), 'Arial')
            except AttributeError:
                pass  # Skip if rFonts not available
        
        # Heading 1 (Chapters)
        if 'Heading 1' in styles:
            h1 = styles['Heading 1']
            h1.font.size = Pt(18)
            h1.font.bold = True
            h1.font.color.rgb = self.NAVY
    
    def render(self, document: Document) -> str:
        """Render document to Word"""
        self.metadata = document.metadata
        
        # Generate cover page
        self._generate_cover_page(document)
        
        # Add page break
        self.doc.add_page_break()
        
        # Generate content
        self._generate_content(document)
        
        # Save document
        self.doc.save(self.output_path)
        
        return self.output_path
    
    def _generate_cover_page(self, document: Document):
        """Generate cover page"""
        metadata = document.metadata
        
        # University
        university = metadata.get('university', '')
        faculty = metadata.get('faculty', '')
        
        if university:
            uni_para = self.doc.add_paragraph()
            run = uni_para.add_run(rtl_text(university))
            run.font.size = Pt(16)
            run.font.bold = True
            run.font.color.rgb = self.NAVY
            set_rtl(uni_para)
            uni_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        if faculty:
            fac_para = self.doc.add_paragraph()
            run = fac_para.add_run(rtl_text(faculty))
            run.font.size = Pt(12)
            set_rtl(fac_para)
            fac_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Title
        title = metadata.get('title', 'Untitled')
        self.doc.add_paragraph()  # Spacer
        
        title_para = self.doc.add_paragraph()
        run = title_para.add_run(rtl_text(title))
        run.font.size = Pt(20)
        run.font.bold = True
        run.font.color.rgb = self.NAVY
        set_rtl(title_para)
        title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Student info
        self.doc.add_paragraph()  # Spacer
        
        student = metadata.get('student', '')
        supervisor = metadata.get('supervisor', '')
        degree = metadata.get('degree', '')
        year = metadata.get('year', '')
        
        if student:
            stu_para = self.doc.add_paragraph()
            run = stu_para.add_run(rtl_text(f"إعداد الطالب: {student}"))
            run.font.size = Pt(12)
            run.font.color.rgb = self.NAVY
            set_rtl(stu_para)
            stu_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        if supervisor:
            sup_para = self.doc.add_paragraph()
            run = sup_para.add_run(rtl_text(f"إشراف الأستاذ: {supervisor}"))
            run.font.size = Pt(12)
            run.font.color.rgb = self.NAVY
            set_rtl(sup_para)
            sup_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        if degree:
            deg_para = self.doc.add_paragraph()
            run = deg_para.add_run(rtl_text(f"درجة: {degree}"))
            run.font.size = Pt(12)
            set_rtl(deg_para)
            deg_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        if year:
            year_para = self.doc.add_paragraph()
            run = year_para.add_run(rtl_text(f"السنة: {year}"))
            run.font.size = Pt(12)
            set_rtl(year_para)
            year_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
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
            self.doc.add_page_break()
    
    def _render_chapter(self, chapter: Chapter):
        """Render chapter"""
        chapter_title = rtl_text(chapter.title)
        
        # Use Heading 1 style
        heading = self.doc.add_heading(chapter_title, level=1)
        set_rtl(heading)
        
        # Render children
        for child in chapter.children:
            self._render_node(child)
    
    def _render_section(self, section: Section):
        """Render section"""
        section_title = rtl_text(section.title)
        
        # Use Heading 2 style
        heading = self.doc.add_heading(section_title, level=2)
        set_rtl(heading)
        
        for child in section.children:
            self._render_node(child)
    
    def _render_subsection(self, subsection: Subsection):
        """Render subsection"""
        subsec_title = rtl_text(subsection.title)
        
        # Use Heading 3 style
        heading = self.doc.add_heading(subsec_title, level=3)
        set_rtl(heading)
        
        for child in subsection.children:
            self._render_node(child)
    
    def _render_environment(self, env: Environment):
        """Render environment based on type"""
        env_type = env.env_type.lower()
        
        if env_type in ['abstract', 'introduction', 'conclusion']:
            self._render_section_like(env)
        elif env_type == 'quote':
            self._render_quote(env)
        elif env_type == 'definition':
            self._render_definition(env)
        elif env_type == 'note':
            self._render_note(env)
        elif env_type == 'list':
            self._render_list(env)
        else:
            content = rtl_text(env.content)
            para = self.doc.add_paragraph(content)
            set_rtl(para)
    
    def _render_section_like(self, env: Environment):
        """Render abstract/introduction/conclusion"""
        env_type = env.env_type.lower()
        
        titles = {
            'abstract': 'الملخص',
            'introduction': 'المقدمة',
            'conclusion': 'الخاتمة'
        }
        
        title = titles.get(env_type, env_type)
        heading = self.doc.add_heading(rtl_text(title), level=2)
        set_rtl(heading)
        
        content = rtl_text(env.content)
        para = self.doc.add_paragraph(content)
        set_rtl(para)
    
    def _render_quote(self, env: Environment):
        """Render quote"""
        content = rtl_text(env.content)
        ref = env.reference or ""
        
        quote_para = self.doc.add_paragraph()
        run = quote_para.add_run(f"«{content}»")
        run.italic = True
        
        if ref:
            quote_para.add_run(f"\n— {rtl_text(ref)}")
        
        quote_para.paragraph_format.left_indent = Cm(2)
        quote_para.paragraph_format.right_indent = Cm(2)
        set_rtl(quote_para)
    
    def _render_definition(self, env: Environment):
        """Render definition"""
        content = rtl_text(env.content)
        
        def_para = self.doc.add_paragraph(content)
        def_para.paragraph_format.left_indent = Cm(1)
        def_para.paragraph_format.right_indent = Cm(1)
        # Note: Background color requires shading which is complex in python-docx
        set_rtl(def_para)
    
    def _render_note(self, env: Environment):
        """Render note"""
        content = rtl_text(env.content)
        
        note_para = self.doc.add_paragraph(content)
        note_para.paragraph_format.left_indent = Cm(1)
        note_para.paragraph_format.right_indent = Cm(1)
        set_rtl(note_para)
    
    def _render_list(self, env: Environment):
        """Render list"""
        content = env.content
        
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('- '):
                item_text = rtl_text(line[2:])
                para = self.doc.add_paragraph(style='List Bullet')
                run = para.add_run(item_text)
                set_rtl(para)
    
    def _render_paragraph(self, para: ParaNode):
        """Render paragraph"""
        content = rtl_text(para.text)
        p = self.doc.add_paragraph(content)
        set_rtl(p)
