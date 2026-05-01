"""
Qalam CLI - Command Line Interface
"""

import argparse
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from qalam.lexer import lex
from qalam.parser import parse, parse_source
from qalam.renderer_pdf import render_pdf
from qalam.renderer_docx import render_docx


def cmd_build(args):
    """Build command: compile .qlm to PDF/Word"""
    input_file = args.input
    
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    
    # Read source
    with open(input_file, 'r', encoding='utf-8') as f:
        source = f.read()
    
    # Parse
    try:
        ast = parse_source(source)
        print(f"✓ Parsed successfully: {len(ast.children)} elements")
    except Exception as e:
        print(f"✗ Parse error: {e}")
        sys.exit(1)
    
    # Determine output format
    output_format = args.output or 'both'
    base_name = os.path.splitext(input_file)[0]
    
    # Build PDF
    if output_format in ['pdf', 'both']:
        pdf_path = f"{base_name}.pdf"
        try:
            render_pdf(ast, pdf_path)
            print(f"✓ PDF generated: {pdf_path}")
        except Exception as e:
            print(f"✗ PDF error: {e}")
            if output_format == 'pdf':
                sys.exit(1)
    
    # Build Word
    if output_format in ['word', 'docx', 'both']:
        docx_path = f"{base_name}.docx"
        try:
            render_docx(ast, docx_path)
            print(f"✓ Word document generated: {docx_path}")
        except Exception as e:
            print(f"✗ Word error: {e}")
            if output_format in ['word', 'docx']:
                sys.exit(1)
    
    print("\n✓ Build completed successfully!")


def cmd_check(args):
    """Check command: validate .qlm syntax without building"""
    input_file = args.input
    
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    
    # Read source
    with open(input_file, 'r', encoding='utf-8') as f:
        source = f.read()
    
    # Lex
    try:
        tokens = lex(source)
        print(f"✓ Lexical analysis: {len(tokens)} tokens")
    except Exception as e:
        print(f"✗ Lexer error: {e}")
        sys.exit(1)
    
    # Parse
    try:
        ast = parse(tokens)
        print(f"✓ Syntax validation passed")
        print(f"  - Document type: {ast.metadata.get('doc_type', 'N/A')}")
        print(f"  - Title: {ast.metadata.get('title', 'N/A')}")
        print(f"  - Elements: {len(ast.children)}")
    except Exception as e:
        print(f"✗ Parse error: {e}")
        sys.exit(1)
    
    print("\n✓ File is valid!")


def cmd_new(args):
    """New command: create a new .qlm file from template"""
    lang = args.lang or 'ar'
    name = args.name or 'document'
    
    # Ensure .qlm extension
    if not name.endswith('.qlm'):
        name += '.qlm'
    
    # Generate template based on language
    if lang == 'ar':
        template = generate_arabic_template()
    elif lang == 'fr':
        template = generate_french_template()
    else:
        template = generate_english_template()
    
    # Write file
    with open(name, 'w', encoding='utf-8') as f:
        f.write(template)
    
    print(f"✓ Created new file: {name}")
    print("  Edit this file and run: qalam build " + name)


def cmd_info(args):
    """Info command: show system information"""
    print("🖊️  Qalam Language Engine")
    print("=" * 40)
    print(f"Version: 1.0.0")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Platform: {sys.platform}")
    print()
    print("Supported formats:")
    print("  - PDF (ReportLab)")
    print("  - Word (.docx)")
    print()
    print("Supported languages:")
    print("  - العربية (Arabic)")
    print("  - English")
    print("  - Français")
    print()
    print("Usage:")
    print("  qalam build <file.qlm> [--output pdf|word]")
    print("  qalam check <file.qlm>")
    print("  qalam new --lang ar|en|fr --name <filename>")
    print("  qalam info")


def generate_arabic_template():
    """Generate Arabic memoire template"""
    return '''@@ مذكرة
  عنوان   >> "عنوان البحث العلمي هنا"
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
  اكتب هنا ملخص البحث باللغة العربية...
{{ /ملخص }}

{{ مقدمة }}
  مقدمة البحث تمهد للموضوع وتوضح أهمية الدراسة...
{{ /مقدمة }}

=== فصل 1: الإطار النظري ===

--- قسم: المفاهيم الأساسية ---

نص القسم يتحدث عن المفاهيم الأساسية للموضوع...

{{ تعريف }}
  التعريف الأول للمفهوم الرئيسي في الدراسة...
{{ /تعريف }}

{{ اقتباس >> المرجع، 2020 }}
  "نص الاقتباس من المصدر الموثوق..."
{{ /اقتباس }}

--- قسم: الدراسات السابقة ---

استعراض الدراسات السابقة ذات الصلة بالموضوع...

{{ ملاحظة }}
  ملاحظة مهمة حول الدراسات السابقة...
{{ /ملاحظة }}

=== فصل 2: الدراسة الميدانية ===

~~~ فرع: منهجية البحث ~~~

وصف منهجية البحث المستخدمة في الدراسة...

{{ قائمة }}
  - العنصر الأول في القائمة
  - العنصر الثاني مع **تنسيق غامق**
  - العنصر الثالث مع *مائل*
{{ /قائمة }}

~~~ فرع: النتائج والمناقشة ~~~

عرض ومناقشة نتائج الدراسة الميدانية...

{{ جدول >> نتائج الدراسة }}
  | المتغير | القيمة | النسبة |
  | المتغير الأول | 150 | 75% |
  | المتغير الثاني | 50 | 25% |
{{ /جدول }}

{{ خاتمة }}
  خاتمة البحث تلخص أهم النتائج والتوصيات...
{{ /خاتمة }}

{{ مراجع }}
  {{ كتاب >> المرجع1 }}
    مؤلف  >> "اسم المؤلف"
    عنوان >> "عنوان الكتاب"
    سنة   >> 2020
    ناشر  >> "دار النشر"
  {{ /كتاب }}

  {{ مقال >> المرجع2 }}
    مؤلف  >> "اسم الباحث"
    عنوان >> "عنوان المقال"
    مجلة  >> "اسم المجلة"
    سنة   >> 2021
  {{ /مقال }}
{{ /مراجع }}
'''


def generate_english_template():
    """Generate English thesis template"""
    return '''@@ Thesis
  Title     >> "Research Title Here"
  Student   >> "Student Name"
  Supervisor>> "Supervisor Name"
  University>> "University Name"
  Faculty   >> "Faculty Name"
  Year      >> "2025-2026"
  Degree    >> Master
  Language  >> en
  Output    >> pdf, word
@@

{{ Abstract }}
  Write the abstract of your research here...
{{ /Abstract }}

{{ Introduction }}
  Introduction that outlines the research problem and significance...
{{ /Introduction }}

=== Chapter 1: Theoretical Framework ===

--- Section: Key Concepts ---

Text discussing the key concepts of the topic...

{{ Definition }}
  Definition of the main concept in the study...
{{ /Definition }}

{{ Quote >> Author, 2020 }}
  "Direct quote from a reliable source..."
{{ /Quote }}

--- Section: Literature Review ---

Review of previous studies related to the topic...

{{ Note }}
  Important note about previous studies...
{{ /Note }}

=== Chapter 2: Field Study ===

~~~ Subsection: Research Methodology ~~~

Description of the research methodology used...

{{ List }}
  - First item in the list
  - Second item with **bold** formatting
  - Third item with *italic*
{{ /List }}

~~~ Subsection: Results and Discussion ~~~

Presentation and discussion of field study results...

{{ Table >> Study Results }}
  | Variable | Value | Percentage |
  | Variable 1 | 150 | 75% |
  | Variable 2 | 50 | 25% |
{{ /Table }}

{{ Conclusion }}
  Conclusion summarizing key findings and recommendations...
{{ /Conclusion }}

{{ References }}
  {{ Book >> ref1 }}
    Author >> "Author Name"
    Title  >> "Book Title"
    Year   >> 2020
    Publisher >> "Publisher"
  {{ /Book }}

  {{ Article >> ref2 }}
    Author >> "Researcher Name"
    Title  >> "Article Title"
    Journal>> "Journal Name"
    Year   >> 2021
  {{ /Article }}
{{ /References }}
'''


def generate_french_template():
    """Generate French mémoire template"""
    return '''@@ Mémoire
  Titre      >> "Titre du mémoire ici"
  Étudiant   >> "Nom de l'étudiant"
  Directeur  >> "Nom du directeur"
  Université >> "Nom de l'université"
  Faculté    >> "Nom de la faculté"
  Année      >> "2025-2026"
  Diplôme    >> Master
  Langue     >> fr
  Sortie     >> pdf, word
@@

{{ Résumé }}
  Écrivez le résumé de votre recherche ici...
{{ /Résumé }}

{{ Introduction }}
  Introduction présentant le problème de recherche...
{{ /Introduction }}

=== Chapitre 1: Cadre Théorique ===

--- Section: Concepts Clés ---

Texte discutant des concepts clés du sujet...

{{ Définition }}
  Définition du concept principal de l'étude...
{{ /Définition }}

{{ Citation >> Auteur, 2020 }}
  "Citation directe d'une source fiable..."
{{ /Citation }}

--- Section: Revue de Littérature ---

Revue des études antérieures sur le sujet...

{{ Note }}
  Note importante sur les études antérieures...
{{ /Note }}

=== Chapitre 2: Étude de Terrain ===

~~~ Sous-section: Méthodologie de Recherche ~~~

Description de la méthodologie de recherche utilisée...

{{ Liste }}
  - Premier élément de la liste
  - Deuxième élément avec **gras**
  - Troisième élément avec *italique*
{{ /Liste }}

~~~ Sous-section: Résultats et Discussion ~~~

Présentation et discussion des résultats...

{{ Tableau >> Résultats de l'étude }}
  | Variable | Valeur | Pourcentage |
  | Variable 1 | 150 | 75% |
  | Variable 2 | 50 | 25% |
{{ /Tableau }}

{{ Conclusion }}
  Conclusion résumant les principaux résultats...
{{ /Conclusion }}

{{ Bibliographie }}
  {{ Livre >> ref1 }}
    Auteur >> "Nom de l'auteur"
    Titre  >> "Titre du livre"
    Année  >> 2020
    Éditeur>> "Maison d'édition"
  {{ /Livre }}

  {{ Article >> ref2 }}
    Auteur >> "Nom du chercheur"
    Titre  >> "Titre de l'article"
    Revue  >> "Nom de la revue"
    Année  >> 2021
  {{ /Article }}
{{ /Bibliographie }}
'''


def main():
    """Main entry point for CLI"""
    parser = argparse.ArgumentParser(
        prog='qalam',
        description='🖊️ Qalam Language Compiler - Academic Writing Made Easy'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Build command
    build_parser = subparsers.add_parser('build', help='Build PDF/Word from .qlm file')
    build_parser.add_argument('input', help='Input .qlm file')
    build_parser.add_argument('--output', '-o', choices=['pdf', 'word', 'both'], 
                             default='both', help='Output format (default: both)')
    build_parser.set_defaults(func=cmd_build)
    
    # Check command
    check_parser = subparsers.add_parser('check', help='Validate .qlm syntax')
    check_parser.add_argument('input', help='Input .qlm file')
    check_parser.set_defaults(func=cmd_check)
    
    # New command
    new_parser = subparsers.add_parser('new', help='Create new .qlm file')
    new_parser.add_argument('--lang', '-l', choices=['ar', 'en', 'fr'],
                           default='ar', help='Language (default: ar)')
    new_parser.add_argument('--name', '-n', help='Output filename')
    new_parser.set_defaults(func=cmd_new)
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show system information')
    info_parser.set_defaults(func=cmd_info)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(0)
    
    args.func(args)


if __name__ == '__main__':
    main()
