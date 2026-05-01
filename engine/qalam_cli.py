#!/usr/bin/env python3
"""
Qalam CLI - Command Line Interface
واجهة سطر الأوامر للغة قلم
"""

import argparse
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from qalam.lexer import Lexer
from qalam.parser import Parser
from qalam.renderer_pdf import QalamPDFRenderer
from qalam.renderer_docx import QalamWordRenderer


def read_file(filepath: str) -> str:
    """Read file content"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def build_document(source: str, output_format: str = 'both', output_dir: str = '.'):
    """Build document from source"""
    # Lexical analysis
    print("🔍 التحليل المعجمي...")
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    print(f"   ✓ تم إنتاج {len(tokens)} رمز")
    
    # Parsing
    print("📊 التحليل النحوي...")
    parser = Parser(tokens)
    document = parser.parse()
    print(f"   ✓ تم تحليل المستند بنجاح")
    print(f"   📝 العنوان: {document.metadata.get('title', 'غير محدد')}")
    print(f"   👤 الطالب: {document.metadata.get('student', 'غير محدد')}")
    
    # Rendering
    base_name = Path(output_dir).stem
    
    if output_format in ['pdf', 'both']:
        pdf_path = os.path.join(output_dir, f"{base_name}.pdf")
        print(f"\n📄 توليد PDF...")
        renderer_pdf = QalamPDFRenderer(pdf_path)
        renderer_pdf.render(document)
        print(f"   ✓ تم حفظ PDF: {pdf_path}")
    
    if output_format in ['word', 'both']:
        word_path = os.path.join(output_dir, f"{base_name}.docx")
        print(f"\n📝 توليد Word...")
        renderer_word = QalamWordRenderer(word_path)
        renderer_word.render(document)
        print(f"   ✓ تم حفظ Word: {word_path}")
    
    print("\n✅ اكتمل البناء بنجاح!")


def check_document(source: str):
    """Check document without building"""
    print("🔍 فحص المستند...")
    
    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        print(f"✓ التحليل المعجمي: OK ({len(tokens)} token)")
        
        parser = Parser(tokens)
        document = parser.parse()
        print(f"✓ التحليل النحوي: OK")
        print(f"✓ عدد الفصول: {len([c for c in document.children if hasattr(c, 'title')])}")
        
        print("\n✅ المستند صحيح!")
        return True
    except Exception as e:
        print(f"\n❌ خطأ: {e}")
        return False


def create_template(lang: str = 'ar', name: str = 'memoir'):
    """Create a new template file"""
    templates = {
        'ar': '''@@ مذكرة
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

{{ ملخص }}
  اكتب الملخص هنا...
{{ /ملخص }}

{{ مقدمة }}
  اكتب المقدمة هنا...
{{ /مقدمة }}

=== فصل 1: الإطار النظري ===

--- قسم: المفاهيم الأساسية ---

اكتب النص هنا...

{{ تعريف }}
  اكتب التعريف هنا...
{{ /تعريف }}

{{ اقتباس >> المرجع }}
  نص الاقتباس...
{{ /اقتباس }}

{{ خاتمة }}
  اكتب الخاتمة هنا...
{{ /خاتمة }}

{{ مراجع }}
  {{ كتاب >> Ref1 }}
    مؤلف  >> "اسم المؤلف"
    عنوان >> "عنوان الكتاب"
    سنة   >> 2020
    ناشر  >> "دار النشر"
  {{ /كتاب }}
{{ /مراجع }}
''',
        'en': '''@@ thesis
  title      >> "Thesis Title Here"
  student    >> "Student Name"
  supervisor >> "Supervisor Name"
  university >> "University Name"
  faculty    >> "Faculty Name"
  year       >> "2025-2026"
  degree     >> master
  language   >> en
  output     >> pdf, word
@@

{{ abstract }}
  Write your abstract here...
{{ /abstract }}

{{ introduction }}
  Write your introduction here...
{{ /introduction }}

=== Chapter 1: Theoretical Framework ===

--- Section: Basic Concepts ---

Write your text here...

{{ definition }}
  Write your definition here...
{{ /definition }}

{{ quote >> Reference }}
  Quote text here...
{{ /quote }}

{{ conclusion }}
  Write your conclusion here...
{{ /conclusion }}

{{ references }}
  {{ book >> Ref1 }}
    author  >> "Author Name"
    title   >> "Book Title"
    year    >> 2020
    publisher >> "Publisher"
  {{ /book }}
{{ /references }}
'''
    }
    
    template = templates.get(lang, templates['ar'])
    filename = f"{name}.{lang}.qlm"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(template)
    
    print(f"✅ تم إنشاء القالب: {filename}")
    return filename


def show_info():
    """Show system information"""
    print("""
╔═══════════════════════════════════════╗
║         🖊️  QALAM Language            ║
║         لغة قلم الأكاديمية            ║
╠═══════════════════════════════════════╣
║  Version: 1.0.0                       ║
║  Author: Qalam Team                   ║
║                                       ║
║  A modern academic writing language   ║
║  designed for Arabic, English &       ║
║  French documents.                    ║
║                                       ║
║  Features:                            ║
║  ✓ Multi-language support             ║
║  ✓ PDF & Word export                  ║
║  ✓ Professional academic formatting   ║
║  ✓ Navy & Gold theme                  ║
║  ✓ RTL support for Arabic             ║
╚═══════════════════════════════════════╝
    """)


def main():
    parser = argparse.ArgumentParser(
        description='🖊️ Qalam Language CLI - لغة قلم الأكاديمية',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Build command
    build_parser = subparsers.add_parser('build', help='Build document')
    build_parser.add_argument('file', help='Input .qlm file')
    build_parser.add_argument('--output', '-o', choices=['pdf', 'word', 'both'], 
                             default='both', help='Output format')
    build_parser.add_argument('--dir', '-d', default='.', help='Output directory')
    
    # Check command
    check_parser = subparsers.add_parser('check', help='Check document syntax')
    check_parser.add_argument('file', help='Input .qlm file')
    
    # New command
    new_parser = subparsers.add_parser('new', help='Create new template')
    new_parser.add_argument('--lang', '-l', choices=['ar', 'en', 'fr'], 
                           default='ar', help='Language')
    new_parser.add_argument('--name', '-n', default='memoir', help='File name')
    
    # Info command
    subparsers.add_parser('info', help='Show system info')
    
    args = parser.parse_args()
    
    if args.command == 'build':
        if not os.path.exists(args.file):
            print(f"❌ الملف غير موجود: {args.file}")
            sys.exit(1)
        
        source = read_file(args.file)
        build_document(source, args.output, args.dir)
    
    elif args.command == 'check':
        if not os.path.exists(args.file):
            print(f"❌ الملف غير موجود: {args.file}")
            sys.exit(1)
        
        source = read_file(args.file)
        success = check_document(source)
        sys.exit(0 if success else 1)
    
    elif args.command == 'new':
        create_template(args.lang, args.name)
    
    elif args.command == 'info':
        show_info()
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
