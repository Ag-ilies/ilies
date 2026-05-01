#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qalam GUI - واجهة رسومية احترافية لمحرر قلم
Dark Theme مع Syntax Highlighting وشجرة المستند
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys
import json
import re
from pathlib import Path
import threading
import subprocess

# إضافة مسار المحرك
sys.path.insert(0, str(Path(__file__).parent))

from qalam.lexer import QalamLexer
from qalam.parser import QalamParser
from qalam.renderer_pdf import PDFRenderer
from qalam.renderer_docx import WordRenderer

class SyntaxHighlighter:
    """تلوين بناء الجمجة للعربية والإنجليزية"""
    
    def __init__(self, text_widget):
        self.text = text_widget
        self.patterns = {
            # Metadata
            'metadata': (r'@@[^@]*@@', '#C9A84C'),  # Gold
            # Chapters
            'chapter': (r'===.*?===', '#FF6B6B'),  # Red
            # Sections
            'section': (r'---.*?---', '#4ECDC4'),  # Teal
            # Subsections
            'subsection': (r'~~~.*?~~~', '#95E1D3'),  # Light Teal
            # Environments
            'env_start': (r'\{\{[^}]*\}\}', '#DDA0DD'),  # Plum
            'env_end': (r'\{\{/[^\}]*\}\}', '#DDA0DD'),
            # Properties
            'property': (r'[a-zA-Z\u0600-\u06FF]+\s*>>', '#87CEEB'),  # Sky Blue
            # Strings
            'string': (r'"[^"]*"', '#98FB98'),  # Pale Green
            # Comments
            'comment': (r'#.*$', '#808080'),  # Gray
            # Bold/Italic
            'bold': (r'\*\*[^*]*\*\*', '#FFB6C1'),  # Light Pink
            'italic': (r'\*[^*]*\*', '#FFB6C1'),
            # Page break
            'pagebreak': (r'<<<', '#FF4500'),  # Orange Red
        }
        
    def highlight(self):
        """تطبيق التلوين على كل النص"""
        content = self.text.get("1.0", tk.END)
        
        # إزالة كل التلوين السابق
        for tag in self.patterns.keys():
            self.text.tag_delete(tag)
            
        # تطبيق الأنماط
        for tag_name, (pattern, color) in self.patterns.items():
            self.text.tag_configure(tag_name, foreground=color)
            for match in re.finditer(pattern, content, re.MULTILINE | re.DOTALL):
                start = f"1.0 + {match.start()} chars"
                end = f"1.0 + {match.end()} chars"
                try:
                    self.text.tag_add(tag_name, start, end)
                except:
                    pass


class DocumentTree(ttk.Frame):
    """شجرة هيكل المستند"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.tree = ttk.Treeview(self, show='tree')
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def update_tree(self, ast):
        """تحديث الشجرة من AST"""
        # مسح المحتوى القديم
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        if not ast:
            return
            
        # إضافة العقدة الجذرية
        root_id = self.tree.insert("", "end", text="المستند", open=True)
        
        # إضافة الفصول والأقسام
        if hasattr(ast, 'elements'):
            for elem in ast.elements:
                if elem.type == 'chapter':
                    chapter_id = self.tree.insert(root_id, "end", text=f"فصل: {elem.title}", open=True)
                    if hasattr(elem, 'elements'):
                        for sub_elem in elem.elements:
                            if sub_elem.type == 'section':
                                self.tree.insert(chapter_id, "end", text=f"قسم: {sub_elem.title}")
                            elif sub_elem.type == 'subsection':
                                self.tree.insert(chapter_id, "end", text=f"فرع: {sub_elem.title}")
                elif elem.type == 'section':
                    self.tree.insert(root_id, "end", text=f"قسم: {elem.title}")
                elif elem.type == 'environment':
                    self.tree.insert(root_id, "end", text=f"{{{{{elem.env_type}}}}}")


class BuildLog(ttk.Frame):
    """سجل العمليات"""
    
    def __init__(self, parent):
        super().__init__(parent, height=150)
        self.pack_propagate(False)
        
        label = ttk.Label(self, text="📋 سجل العمليات", font=("Segoe UI", 10, "bold"))
        label.pack(anchor="w", padx=5, pady=2)
        
        self.log_text = scrolledtext.ScrolledText(self, height=8, font=("Consolas", 9), 
                                                   bg="#1e1e1e", fg="#d4d4d4", insertbackground="white")
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)
        
    def log(self, message, level="INFO"):
        """إضافة رسالة للسجل"""
        timestamp = threading.current_thread().name
        colors = {
            "INFO": "#4ECDC4",
            "SUCCESS": "#98FB98",
            "WARNING": "#FFD700",
            "ERROR": "#FF6B6B"
        }
        color = colors.get(level, "#d4d4d4")
        
        self.log_text.insert(tk.END, f"[{level}] ", ('color',))
        self.log_text.tag_configure('color', foreground=color)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        
    def clear(self):
        """مسح السجل"""
        self.log_text.delete("1.0", tk.END)


class QalamGUI:
    """الواجهة الرسومية الرئيسية"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🖊️ Qalam - محرر قلم الأكاديمي")
        self.root.geometry("1400x900")
        
        # الألوان
        self.colors = {
            'bg': '#1e1e1e',
            'fg': '#d4d4d4',
            'accent': '#C9A84C',
            'secondary': '#2d2d2d',
            'border': '#3d3d3d'
        }
        
        self.current_file = None
        self.ast = None
        
        self.setup_ui()
        self.setup_bindings()
        
    def setup_ui(self):
        """إنشاء الواجهة"""
        self.root.configure(bg=self.colors['bg'])
        
        # الشريط العلوي
        self.create_toolbar()
        
        # الحاوية الرئيسية
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # الشريط الجانبي (شجرة المستند)
        sidebar = ttk.LabelFrame(main_frame, text="🌳 هيكل المستند", padding=5)
        sidebar.pack(side="left", fill="y", padx=(0, 5))
        self.doc_tree = DocumentTree(sidebar)
        self.doc_tree.pack(fill="both", expand=True)
        
        # منطقة المحرر
        editor_frame = ttk.LabelFrame(main_frame, text="✏️ المحرر", padding=5)
        editor_frame.pack(side="left", fill="both", expand=True)
        
        self.editor = scrolledtext.ScrolledText(editor_frame, font=("Consolas", 11),
                                                 bg="#1e1e1e", fg="#d4d4d4",
                                                 insertbackground="white",
                                                 undo=True, autoseparators=True)
        self.editor.pack(fill="both", expand=True)
        
        self.highlighter = SyntaxHighlighter(self.editor)
        
        # ربط حدث التغيير بالتلوين
        self.editor.bind('<KeyRelease>', lambda e: self.root.after(100, self.highlighter.highlight))
        
        # شريط الحالة السفلي
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill="x", side="bottom")
        
        self.status_label = ttk.Label(status_frame, text="جاهز", relief="sunken", anchor="w")
        self.status_label.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        # سجل العمليات
        self.build_log = BuildLog(self.root)
        self.build_log.pack(fill="x", side="bottom", padx=5, pady=(0, 5))
        
        # تحميل قالب افتراضي
        self.load_template('arabic_master')
        
    def create_toolbar(self):
        """إنشاء شريط الأدوات"""
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill="x", padx=5, pady=5)
        
        buttons = [
            ("📄 جديد", self.new_file),
            ("📂 فتح", self.open_file),
            ("💾 حفظ", self.save_file),
            ("💾 حفظ باسم", self.save_file_as),
            (None, None),  # فاصل
            ("▶️ بناء PDF", lambda: self.build('pdf')),
            ("📝 بناء Word", lambda: self.build('docx')),
            ("📦 بناء الكل", lambda: self.build('all')),
            (None, None),
            ("🔍 فحص", self.check_syntax),
            ("🌐 معاينة HTML", self.preview_html),
            (None, None),
            ("🎨 قوالب", self.show_templates),
            ("⚙️ إعدادات", self.show_settings),
            ("❓ مساعدة", self.show_help),
        ]
        
        for text, command in buttons:
            if text is None:
                ttk.Separator(toolbar, orient="vertical").pack(side="left", padx=10, fill="y")
            else:
                btn = ttk.Button(toolbar, text=text, command=command, width=12)
                btn.pack(side="left", padx=2)
                
    def setup_bindings(self):
        """ربط اختصارات لوحة المفاتيح"""
        bindings = {
            '<Control-n>': lambda e: self.new_file(),
            '<Control-o>': lambda e: self.open_file(),
            '<Control-s>': lambda e: self.save_file(),
            '<Control-Shift-S>': lambda e: self.save_file_as(),
            '<F5>': lambda e: self.build('all'),
            '<F6>': lambda e: self.build('pdf'),
            '<F7>': lambda e: self.build('docx'),
            '<F9>': lambda e: self.check_syntax(),
            '<Control-q>': lambda e: self.root.quit(),
        }
        
        for key, handler in bindings.items():
            self.root.bind(key, handler)
            
    def new_file(self):
        """إنشاء ملف جديد"""
        if self.maybe_save():
            self.editor.delete("1.0", tk.END)
            self.current_file = None
            self.ast = None
            self.status_label.config(text="ملف جديد")
            self.build_log.clear()
            
    def open_file(self):
        """فتح ملف .qlm"""
        if not self.maybe_save():
            return
            
        filepath = filedialog.askopenfilename(
            title="فتح ملف Qalam",
            filetypes=[("Qalam Files", "*.qlm"), ("All Files", "*.*")]
        )
        
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                self.editor.delete("1.0", tk.END)
                self.editor.insert("1.0", content)
                self.current_file = filepath
                self.status_label.config(text=f"مفتوح: {filepath}")
                self.build_log.log(f"تم فتح الملف: {filepath}", "INFO")
                self.highlighter.highlight()
                
            except Exception as e:
                messagebox.showerror("خطأ", f"فشل فتح الملف:\n{str(e)}")
                
    def save_file(self):
        """حفظ الملف الحالي"""
        if self.current_file:
            self.save_file_as(filepath=self.current_file)
        else:
            self.save_file_as()
            
    def save_file_as(self, filepath=None):
        """حفظ الملف باسم"""
        if not filepath:
            filepath = filedialog.asksaveasfilename(
                title="حفظ ملف Qalam",
                defaultextension=".qlm",
                filetypes=[("Qalam Files", "*.qlm"), ("All Files", "*.*")]
            )
            
        if filepath:
            try:
                content = self.editor.get("1.0", tk.END).rstrip()
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                self.current_file = filepath
                self.status_label.config(text=f"محفوظ: {filepath}")
                self.build_log.log(f"تم الحفظ: {filepath}", "SUCCESS")
                
            except Exception as e:
                messagebox.showerror("خطأ", f"فشل الحفظ:\n{str(e)}")
                
    def maybe_save(self):
        """السؤال عن الحفظ إذا كانت هناك تغييرات"""
        # تبسيط: لا نتحقق من التغييرات في هذه النسخة
        return True
        
    def check_syntax(self):
        """فحص الصيغة النحوية"""
        content = self.editor.get("1.0", tk.END)
        
        try:
            lexer = QalamLexer()
            tokens = lexer.tokenize(content)
            self.build_log.log(f"✓ تم التحليل المعجمي: {len(tokens)} رمز", "SUCCESS")
            
            parser = QalamParser()
            self.ast = parser.parse(tokens)
            self.build_log.log(f"✓ تم التحليل النحوي بنجاح", "SUCCESS")
            
            # تحديث شجرة المستند
            self.doc_tree.update_tree(self.ast)
            
            self.status_label.config(text="✓ الصيغة صحيحة")
            messagebox.showinfo("فحص ناجح", "✓ لا توجد أخطاء في الصيغة!")
            
        except Exception as e:
            self.build_log.log(f"✗ خطأ: {str(e)}", "ERROR")
            self.status_label.config(text="✗ خطأ في الصيغة")
            messagebox.showerror("خطأ في الصيغة", str(e))
            
    def build(self, output_format='all'):
        """بناء المستند"""
        if not self.current_file:
            messagebox.showwarning("تحذير", "يرجى حفظ الملف أولاً!")
            return
            
        self.build_log.clear()
        self.status_label.config(text="جاري البناء...")
        
        def build_thread():
            try:
                content = self.editor.get("1.0", tk.END)
                
                # التحليل
                lexer = QalamLexer()
                tokens = lexer.tokenize(content)
                self.build_log.log(f"✓ تم التحليل المعجمي: {len(tokens)} رمز", "SUCCESS")
                
                parser = QalamParser()
                ast = parser.parse(tokens)
                self.build_log.log(f"✓ تم التحليل النحوي", "SUCCESS")
                
                # التحديث
                self.doc_tree.update_tree(ast)
                
                # البناء
                output_dir = os.path.dirname(self.current_file)
                base_name = os.path.splitext(os.path.basename(self.current_file))[0]
                
                if output_format in ['pdf', 'all']:
                    pdf_renderer = PDFRenderer()
                    pdf_path = os.path.join(output_dir, f"{base_name}.pdf")
                    pdf_renderer.render(ast, pdf_path)
                    self.build_log.log(f"✓ تم توليد PDF: {pdf_path}", "SUCCESS")
                    
                if output_format in ['docx', 'all']:
                    docx_renderer = WordRenderer()
                    docx_path = os.path.join(output_dir, f"{base_name}.docx")
                    docx_renderer.render(ast, docx_path)
                    self.build_log.log(f"✓ تم توليد Word: {docx_path}", "SUCCESS")
                    
                self.status_label.config(text="✓ اكتمل البناء بنجاح!")
                self.build_log.log("✓ اكتمل البناء بنجاح!", "SUCCESS")
                
                # فتح الملف المولد
                if output_format == 'pdf':
                    os.startfile(os.path.join(output_dir, f"{base_name}.pdf"))
                elif output_format == 'docx':
                    os.startfile(os.path.join(output_dir, f"{base_name}.docx"))
                    
            except Exception as e:
                self.build_log.log(f"✗ فشل البناء: {str(e)}", "ERROR")
                self.status_label.config(text="✗ فشل البناء")
                messagebox.showerror("فشل البناء", str(e))
                
        thread = threading.Thread(target=build_thread, daemon=True)
        thread.start()
        
    def preview_html(self):
        """معاينة HTML"""
        messagebox.showinfo("قريباً", "ميزة معاينة HTML قيد التطوير")
        
    def load_template(self, template_name):
        """تحميل قالب جاهز"""
        templates = {
            'arabic_master': '''@@ مذكرة
  عنوان   >> "عنوان المذكرة هنا"
  طالب    >> "اسم الطالب"
  مشرف    >> "اسم المشرف"
  جامعة   >> "اسم الجامعة"
  كلية    >> "اسم الكلية"
  سنة     >> "2025-2026"
  درجة    >> ماستر
  لغة     >> ar
  مخرج    >> pdf, word
@@

{{ إهداء }}
  إلى من كان لي سنداً وعوناً...
{{ /إهداء }}

{{ ملخص }}
  ملخص البحث هنا...
{{ /ملخص }}

=== فصل 1: الإطار النظري ===

--- قسم: المفاهيم الأساسية ---

نص القسم هنا...

{{ تعريف }}
  تعريف المفهوم...
{{ /تعريف }}

{{ مثال }}
  مثال توضيحي...
{{ /مثال }}

~~~ فرع: التفاصيل ~~~

نص الفرع...

{{ قائمة }}
  - النقطة الأولى
  - النقطة الثانية
  - النقطة الثالثة
{{ /قائمة }}

=== فصل 2: الدراسة الميدانية ===

--- قسم: المنهجية ---

وصف المنهجية...

{{ جدول >> نتائج الدراسة }}
  | المتغير | القيمة | النسبة |
  | الأول   | 100    | 50%    |
  | الثاني  | 200    | 50%    |
{{ /جدول }}

{{ خاتمة }}
  خاتمة البحث...
{{ /خاتمة }}

{{ مراجع }}
  {{ كتاب >> Ref1 }}
    مؤلف  >> "اسم المؤلف"
    عنوان >> "عنوان الكتاب"
    سنة   >> 2024
    ناشر  >> "دار النشر"
  {{ /كتاب }}
{{ /مراجع }}
'''
        }
        
        if template_name in templates:
            self.editor.delete("1.0", tk.END)
            self.editor.insert("1.0", templates[template_name])
            self.highlighter.highlight()
            self.build_log.log("✓ تم تحميل القالب", "INFO")
            
    def show_templates(self):
        """عرض القوالب المتاحة"""
        template_win = tk.Toplevel(self.root)
        template_win.title("🎨 قوالب Qalam")
        template_win.geometry("600x400")
        
        ttk.Label(template_win, text="اختر قالباً:", font=("Segoe UI", 12, "bold")).pack(pady=10)
        
        templates_list = [
            "مذكرة ماستر عربية",
            "رسالة دكتوراه",
            "مقال علمي IEEE",
            "مقال علمي APA",
            "تقرير تقني",
            "عرض تقديمي"
        ]
        
        for tpl in templates_list:
            btn = ttk.Button(template_win, text=tpl, 
                           command=lambda t=tpl: self.select_template(t, template_win))
            btn.pack(fill="x", padx=20, pady=5)
            
    def select_template(self, template_name, window):
        """اختيار قالب"""
        # تبسيط: تحميل القالب العربي فقط
        self.load_template('arabic_master')
        window.destroy()
        
    def show_settings(self):
        """عرض الإعدادات"""
        messagebox.showinfo("الإعدادات", "نافذة الإعدادات قيد التطوير")
        
    def show_help(self):
        """عرض المساعدة"""
        help_text = """
🖊️ مساعدة Qalam

اختصارات لوحة المفاتيح:
  F5       - بناء PDF + Word
  F6       - بناء PDF فقط
  F7       - بناء Word فقط
  F9       - فحص الصيغة
  Ctrl+S   - حفظ
  Ctrl+O   - فتح
  Ctrl+N   - ملف جديد
  
الصيغة:
  @@ ... @@      - البيانات الوصفية
  === عنوان ===  - فصل
  --- عنوان ---  - قسم
  ~~~ عنوان ~~~  - فرع
  {{ نوع }}      - بيئة
  مفتاح >> قيمة  - خاصية
  
للمزيد من المعلومات، راجع التوثيق.
        """
        messagebox.showinfo("مساعدة Qalam", help_text)
        
    def run(self):
        """تشغيل التطبيق"""
        self.root.mainloop()


if __name__ == "__main__":
    app = QalamGUI()
    app.run()
