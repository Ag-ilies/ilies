#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qalam HTML Renderer - محرك توليد HTML للمعاينة
"""

from .ast_nodes import Document, Chapter, Section, Subsection, Environment, TextNode, Table, List as NodeList, Equation, Figure, ReferenceEntry, Paragraph
import re


class HTMLRenderer:
    """محول AST إلى HTML مع دعم RTL"""
    
    def __init__(self):
        self.html_parts = []
        self.toc = []  # جدول المحتويات
        self.figures_list = []  # قائمة الأشكال
        self.tables_list = []  # قائمة الجداول
        
    def render(self, ast: Document, output_path: str = None) -> str:
        """توليد HTML من المستند"""
        self.html_parts = []
        self.toc = []
        self.figures_list = []
        self.tables_list = []
        
        # رأس HTML
        self.html_parts.append('''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>''')
        
        title = "مستند Qalam"
        if ast.metadata and 'title' in ast.metadata:
            title = ast.metadata['title']
            
        self.html_parts.append(f'{title}</title>')
        
        # التنسيقات
        self.html_parts.append('''
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Cairo:wght@400;600;700&display=swap');
        
        :root {
            --navy: #1B2A4A;
            --gold: #C9A84C;
            --light-gold: #E8D59E;
            --bg: #f8f9fa;
            --text: #2c3e50;
            --border: #dee2e6;
            --blue-bg: #e3f2fd;
            --yellow-bg: #fff9c4;
            --green-bg: #e8f5e9;
        }
        
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        body {
            font-family: 'Amiri', 'Cairo', serif;
            line-height: 1.8;
            background: var(--bg);
            color: var(--text);
            direction: rtl;
            text-align: right;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }
        
        /* صفحة الغلاف */
        .cover-page {
            background: linear-gradient(135deg, var(--navy) 0%, #2c3e50 100%);
            color: white;
            padding: 60px 40px;
            text-align: center;
            border-radius: 10px;
            margin-bottom: 40px;
            border: 3px solid var(--gold);
        }
        
        .cover-page h1 {
            font-size: 2em;
            margin-bottom: 30px;
            color: var(--gold);
        }
        
        .cover-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 30px;
        }
        
        .cover-info-item {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 8px;
            border-right: 3px solid var(--gold);
        }
        
        /* الفصول */
        .chapter {
            margin: 40px 0;
            page-break-before: always;
        }
        
        .chapter-title {
            background: linear-gradient(90deg, var(--navy), #2c3e50);
            color: white;
            padding: 15px 25px;
            border-radius: 8px;
            border-right: 5px solid var(--gold);
            margin-bottom: 25px;
        }
        
        .chapter-title h2 {
            font-size: 1.6em;
        }
        
        /* الأقسام */
        .section {
            margin: 30px 0;
        }
        
        .section-title {
            color: var(--navy);
            border-bottom: 2px solid var(--gold);
            padding-bottom: 10px;
            margin-bottom: 20px;
            font-size: 1.3em;
        }
        
        /* الفروع */
        .subsection {
            margin: 25px 0;
            padding-right: 20px;
            border-right: 3px solid var(--light-gold);
        }
        
        .subsection-title {
            color: var(--navy);
            font-weight: bold;
            font-size: 1.1em;
            margin-bottom: 15px;
        }
        
        /* البيئات */
        .environment {
            margin: 20px 0;
            padding: 20px;
            border-radius: 8px;
        }
        
        .env-quote {
            background: var(--yellow-bg);
            border: 2px solid var(--gold);
            border-right: 5px solid var(--gold);
            font-style: italic;
        }
        
        .env-definition {
            background: var(--blue-bg);
            border: 2px solid #2196F3;
            border-right: 5px solid #2196F3;
        }
        
        .env-note {
            background: var(--yellow-bg);
            border: 2px solid #FFC107;
            border-right: 5px solid #FFC107;
        }
        
        .env-example {
            background: var(--green-bg);
            border: 2px solid #4CAF50;
            border-right: 5px solid #4CAF50;
        }
        
        .env-label {
            font-weight: bold;
            color: var(--navy);
            margin-bottom: 10px;
            display: block;
        }
        
        /* الجداول */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
        }
        
        th {
            background: var(--navy);
            color: white;
            padding: 12px;
            text-align: right;
        }
        
        td {
            padding: 10px;
            border: 1px solid var(--border);
        }
        
        tr:nth-child(even) {
            background: #f8f9fa;
        }
        
        tr:hover {
            background: var(--light-gold);
        }
        
        /* القوائم */
        ul, ol {
            margin: 15px 0;
            padding-right: 30px;
        }
        
        li {
            margin: 8px 0;
        }
        
        /* المعادلات */
        .equation {
            background: #f8f9fa;
            border: 1px solid var(--border);
            padding: 15px;
            text-align: center;
            font-family: 'Courier New', monospace;
            margin: 20px 0;
            border-radius: 8px;
        }
        
        /* الأشكال */
        .figure {
            text-align: center;
            margin: 25px 0;
        }
        
        .figure img {
            max-width: 100%;
            height: auto;
            border: 2px solid var(--border);
            border-radius: 8px;
        }
        
        .figure-caption {
            margin-top: 10px;
            font-size: 0.9em;
            color: #666;
        }
        
        /* المراجع */
        .references {
            margin-top: 40px;
            padding-top: 30px;
            border-top: 3px solid var(--gold);
        }
        
        .ref-entry {
            margin: 15px 0;
            padding-right: 20px;
            border-right: 2px solid var(--border);
        }
        
        /* التنسيق المضمن */
        strong { color: var(--navy); }
        em { color: #666; }
        u { text-decoration: underline; }
        
        /* فهرس المحتويات */
        .toc {
            background: white;
            padding: 25px;
            border-radius: 8px;
            border: 2px solid var(--gold);
            margin: 30px 0;
        }
        
        .toc h3 {
            color: var(--navy);
            margin-bottom: 15px;
            border-bottom: 2px solid var(--gold);
            padding-bottom: 10px;
        }
        
        .toc ul {
            list-style: none;
            padding-right: 0;
        }
        
        .toc li {
            margin: 8px 0;
        }
        
        .toc a {
            color: var(--navy);
            text-decoration: none;
        }
        
        .toc a:hover {
            color: var(--gold);
            text-decoration: underline;
        }
        
        /* فاصل الصفحة */
        .page-break {
            page-break-before: always;
            margin: 50px 0;
            border-top: 2px dashed var(--gold);
        }
    </style>
</head>
<body>
''')
        
        # معالجة العناصر
        if hasattr(ast, 'elements'):
            for elem in ast.elements:
                self.process_element(elem)
                
        # ذيل HTML
        self.html_parts.append('</body></html>')
        
        html_content = ''.join(self.html_parts)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
                
        return html_content
        
    def process_element(self, elem, level=0):
        """معالجة عنصر AST"""
        
        if elem.type == 'metadata':
            self.render_metadata(elem.data)
            
        elif elem.type == 'chapter':
            self.render_chapter(elem)
            
        elif elem.type == 'section':
            self.render_section(elem)
            
        elif elem.type == 'subsection':
            self.render_subsection(elem)
            
        elif elem.type == 'environment':
            self.render_environment(elem)
            
        elif elem.type == 'text':
            self.html_parts.append(f'<p>{self.format_text(elem.content)}</p>')
            
        elif elem.type == 'pagebreak':
            self.html_parts.append('<div class="page-break"></div>')
            
    def render_metadata(self, data):
        """توليد صفحة الغلاف"""
        self.html_parts.append('<div class="cover-page">')
        self.html_parts.append(f'<h1>{data.get("title", "عنوان المستند")}</h1>')
        
        self.html_parts.append('<div class="cover-info">')
        
        labels = {
            'student': 'الطالب',
            'supervisor': 'المشرف',
            'university': 'الجامعة',
            'faculty': 'الكلية',
            'year': 'السنة',
            'degree': 'الدرجة',
            'language': 'اللغة'
        }
        
        for key, label in labels.items():
            if key in data:
                self.html_parts.append(f'''
                <div class="cover-info-item">
                    <strong>{label}:</strong><br>
                    {data[key]}
                </div>
                ''')
                
        self.html_parts.append('</div></div>')
        
        # إضافة جدول المحتويات
        self.html_parts.append('<div class="toc"><h3>فهرس المحتويات</h3><ul id="toc-list"></ul></div>')
        
    def render_chapter(self, elem):
        """توليد فصل"""
        chapter_id = f"chap-{elem.title.replace(' ', '-').replace(':', '')}"
        self.toc.append((chapter_id, elem.title, 'chapter'))
        
        self.html_parts.append(f'<div class="chapter" id="{chapter_id}">')
        self.html_parts.append(f'<div class="chapter-title"><h2>{elem.title}</h2></div>')
        
        if hasattr(elem, 'elements'):
            for sub_elem in elem.elements:
                self.process_element(sub_elem, level=1)
                
        self.html_parts.append('</div>')
        
    def render_section(self, elem):
        """توليد قسم"""
        section_id = f"sec-{elem.title.replace(' ', '-').replace(':', '')}"
        self.toc.append((section_id, elem.title, 'section'))
        
        self.html_parts.append(f'<div class="section" id="{section_id}">')
        self.html_parts.append(f'<h3 class="section-title">{elem.title}</h3>')
        
        if hasattr(elem, 'content'):
            for content in elem.content:
                if isinstance(content, str):
                    self.html_parts.append(f'<p>{self.format_text(content)}</p>')
                else:
                    self.process_element(content, level=2)
                    
        self.html_parts.append('</div>')
        
    def render_subsection(self, elem):
        """توليد فرع"""
        self.html_parts.append(f'<div class="subsection">')
        self.html_parts.append(f'<h4 class="subsection-title">{elem.title}</h4>')
        
        if hasattr(elem, 'content'):
            for content in elem.content:
                if isinstance(content, str):
                    self.html_parts.append(f'<p>{self.format_text(content)}</p>')
                else:
                    self.process_element(content, level=3)
                    
        self.html_parts.append('</div>')
        
    def render_environment(self, elem):
        """توليد بيئة"""
        env_classes = {
            'quote': 'env-quote',
            'اقتباس': 'env-quote',
            'definition': 'env-definition',
            'تعريف': 'env-definition',
            'note': 'env-note',
            'ملاحظة': 'env-note',
            'example': 'env-example',
            'مثال': 'env-example'
        }
        
        env_class = env_classes.get(elem.env_type, 'environment')
        
        self.html_parts.append(f'<div class="environment {env_class}">')
        
        if elem.reference:
            self.html_parts.append(f'<span class="env-label">{elem.env_type} ({elem.reference})</span>')
        else:
            self.html_parts.append(f'<span class="env-label">{elem.env_type}</span>')
            
        # معالجة محتوى البيئة
        if hasattr(elem, 'content'):
            content = elem.content
            if isinstance(content, str):
                self.html_parts.append(f'<p>{self.format_text(content)}</p>')
            elif isinstance(content, list):
                for item in content:
                    if isinstance(item, Table):
                        self.render_table(item)
                    elif isinstance(item, NodeList):
                        self.render_list_node(item)
                    elif isinstance(item, str):
                        self.html_parts.append(f'<p>{self.format_text(item)}</p>')
                    else:
                        self.process_element(item)
                    
        self.html_parts.append('</div>')
        
    def render_list_node(self, list_node: NodeList):
        """توليد قائمة من NodeList"""
        tag = 'ol' if list_node.ordered else 'ul'
        self.html_parts.append(f'<{tag}>')
        
        for item in list_node.items:
            self.html_parts.append(f'<li>{self.format_text(str(item))}</li>')
            
        self.html_parts.append(f'</{tag}>')
        
    def render_table(self, table: Table):
        """توليد جدول"""
        table_id = f"table-{len(self.tables_list) + 1}"
        self.tables_list.append((table_id, table.caption))
        
        self.html_parts.append(f'<table id="{table_id}">')
        
        if table.caption:
            self.html_parts.append(f'<caption>{table.caption}</caption>')
            
        # الترويسة
        if table.headers:
            self.html_parts.append('<thead><tr>')
            for header in table.headers:
                self.html_parts.append(f'<th>{header}</th>')
            self.html_parts.append('</tr></thead>')
            
        # الصفوف
        self.html_parts.append('<tbody>')
        for row in table.rows:
            self.html_parts.append('<tr>')
            for cell in row:
                self.html_parts.append(f'<td>{self.format_text(str(cell))}</td>')
            self.html_parts.append('</tr>')
        self.html_parts.append('</tbody>')
        
        self.html_parts.append('</table>')
        
    def render_list(self, items, ordered=False):
        """توليد قائمة"""
        tag = 'ol' if ordered else 'ul'
        self.html_parts.append(f'<{tag}>')
        
        for item in items:
            content = item.content if isinstance(item, ListItem) else item
            self.html_parts.append(f'<li>{self.format_text(str(content))}</li>')
            
        self.html_parts.append(f'</{tag}>')
        
    def format_text(self, text):
        """تنسيق النص المضمن"""
        if not isinstance(text, str):
            return str(text)
            
        # Bold
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        # Italic
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        # Underline
        text = re.sub(r'__(.+?)__', r'<u>\1</u>', text)
        
        return text


import re
