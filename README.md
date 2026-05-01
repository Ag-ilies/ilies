# 🖊️ QALAM Language - لغة قلم الأكاديمية

A modern academic writing language designed for Arabic, English, and French documents.

## Features

- ✅ Multi-language support (Arabic, English, French)
- ✅ PDF & Word export
- ✅ Professional academic formatting
- ✅ Navy & Gold theme
- ✅ RTL support for Arabic
- ✅ No LaTeX dependency

## Installation

```bash
cd engine
pip install -r requirements.txt
```

## Usage

### CLI Commands

```bash
# Build document
python qalam_cli.py build file.qlm

# Build PDF only
python qalam_cli.py build file.qlm --output pdf

# Build Word only  
python qalam_cli.py build file.qlm --output word

# Check syntax
python qalam_cli.py check file.qlm

# Create new template
python qalam_cli.py new --lang ar --name memoir

# Show info
python qalam_cli.py info
```

## Syntax Example

```qlm
@@ مذكرة
  عنوان   >> "عنوان المذكرة"
  طالب    >> "اسم الطالب"
  مشرف    >> "اسم المشرف"
  جامعة   >> "اسم الجامعة"
  سنة     >> "2025-2026"
  درجة    >> ماستر
@@

{{ ملخص }}
  نص الملخص هنا...
{{ /ملخص }}

=== فصل 1: الإطار النظري ===

--- قسم: المفاهيم الأساسية ---

نص القسم...

{{ تعريف }}
  نص التعريف...
{{ /تعريف }}

{{ اقتباس >> المرجع }}
  نص الاقتباس...
{{ /اقتباس }}
```

## Project Structure

```
Qalam/
├── engine/                 # Python engine
│   ├── qalam/             # Core library
│   │   ├── lexer.py       # Tokenizer
│   │   ├── parser.py      # Parser
│   │   ├── ast_nodes.py   # AST definitions
│   │   ├── keywords.py    # Multi-language keywords
│   │   ├── renderer_pdf.py    # PDF generator
│   │   └── renderer_docx.py   # Word generator
│   ├── qalam_cli.py       # Command-line interface
│   └── tests/             # Test files
└── website/               # Next.js website (coming soon)
```

## License

MIT License - Qalam Team 2025