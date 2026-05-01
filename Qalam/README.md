# 🖊️ Qalam - لغة الكتابة الأكاديمية

<div align="center">

![Qalam Logo](https://img.shields.io/badge/Qalam-v1.0.0-gold)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![Next.js](https://img.shields.io/badge/next.js-14.2-black)

**لغة برمجة أكاديمية ثورية لكتابة المذكرات والبحوث العلمية**

[التوثيق](#) • [المحرر الأونلاين](#) • [الأمثلة](#) • [الأسعار](#)

</div>

---

## ✨ لماذا Qalam؟

| الميزة | LaTeX | Typst | **Qalam** |
|--------|-------|-------|-----------|
| دعم العربية الأصلي | ❌ (معقد) | ⚠️ (محدود) | ✅ **كامل** |
| منحنى التعلم | 📈 صعب | 📕 متوسط | 📗 **سهل** |
| وقت البناء | 🐢 بطيء | 🐇 سريع | 🚀 **فوري** |
| مساعد ذكي | ❌ | ❌ | ✅ **مدمج** |
| تصدير Word | ❌ | ❌ | ✅ **أصلي** |
| صيغة بديهية | ❌ | ⚠️ | ✅ **عربية** |

---

## 🚀 البدء السريع

### التثبيت

```bash
# تثبيت المحرك
pip install qalam-lang

# أو استنساخ المشروع
git clone https://github.com/qalam-lang/qalam.git
cd qalam/engine
pip install -r requirements.txt
```

### مثال سريع

أنشئ ملف `memoire.qlm`:

```qlm
@@ مذكرة
  عنوان   >> "اللسانيات الجنائية وتطبيقاتها"
  طالب    >> "واهيبة بلقاسم"
  مشرف    >> "أ.د. محمد الأمين بوزيد"
  جامعة   >> "جامعة 8 ماي 1945 — قالمة"
  سنة     >> "2025-2026"
  درجة    >> ماستر
  لغة     >> ar
@@

{{ ملخص }}
  تتناول هذه الدراسة علم اللسانيات الجنائية...
{{ /ملخص }}

=== فصل 1: الإطار النظري ===

--- قسم: مفهوم اللسانيات الجنائية ---

اللسانيات الجنائية هي العلم الذي يوظّف المعرفة اللغوية
في خدمة الإجراءات القانونية والقضائية.

{{ تعريف }}
  اللسانيات الجنائية هي الفرع التطبيقي من اللسانيات
  الذي يُعنى بتحليل اللغة في السياقات القضائية.
{{ /تعريف }}

{{ جدول >> فروع اللسانيات الجنائية }}
  | الفرع             | التعريف              |
  | الصوتيات الجنائية | تحليل الأصوات        |
  | تحليل الخطاب      | دراسة بنية النصوص    |
{{ /جدول }}

{{ مراجع }}
  {{ كتاب >> Coulthard2010 }}
    مؤلف  >> "Malcolm Coulthard"
    عنوان >> "Introduction to Forensic Linguistics"
    سنة   >> 2010
  {{ /كتاب }}
{{ /مراجع }}
```

ثم شغّل:

```bash
qalam build memoire.qlm
# سيتم توليد memoire.pdf و memoire.docx
```

---

## 📖 الصيغة (Syntax)

### البيانات الوصفية (Metadata)

```qlm
@@ نوع المستند
  مفتاح >> "قيمة"
@@
```

### الهيكلة

| العنصر | الصيغة |
|--------|--------|
| فصل | `=== عنوان الفصل ===` |
| قسم | `--- عنوان القسم ---` |
| فرع | `~~~ عنوان الفرع ~~~` |

### البيئات (Environments)

```qlm
{{ نوع البيئة }}
  المحتوى هنا...
{{ /نوع البيئة }}
```

**البيئات المتاحة:**
- `ملخص` / `abstract` / `résumé`
- `مقدمة` / `introduction`
- `خاتمة` / `conclusion`
- `إهداء` / `dedication`
- `اقتباس` / `quote`
- `تعريف` / `definition`
- `ملاحظة` / `note`
- `مثال` / `example`
- `جدول` / `table`
- `شكل` / `figure`
- `قائمة` / `list`
- `معادلة` / `equation`
- `مراجع` / `references`

### التنسيق المضمن

```qlm
**نص غامق**
*نص مائل*
__نص مسطر__
[ref: المرجع]  # إحالة مرجعية
```

---

## 🛠️ الأدوات

### واجهة سطر الأوامر (CLI)

```bash
# بناء PDF + Word
qalam build file.qlm

# بناء PDF فقط
qalam build file.qlm --output pdf

# فحص الصيغة
qalam check file.qlm

# إنشاء ملف جديد
qalam new --lang ar --name مذكرتي

# معلومات النظام
qalam info
```

### الواجهة الرسومية (GUI)

```bash
qalam gui
```

يوفر:
- محرر كود مع تلوين بناء الجملة
- شجرة هيكل المستند
- بناء بنقرة واحدة
- قوالب جاهزة

### المحرر الأونلاين

زر المحرر على: **[qalam-lang.com/editor](#)**

---

## 🤖 المساعد الذكي (AI Agent)

يمكنك استخدام المساعد الذكي لـ:

1. **توليد مذكرة كاملة**
   ```
   "اكتب لي هيكل مذكرة ماستر عن اللسانيات"
   ```

2. **إضافة فصل**
   ```
   "أضف فصلاً نظرياً عن phonetics"
   ```

3. **تنسيق مراجع**
   ```
   "أضف هذا المرجع بصيغة APA"
   ```

4. **ترجمة محتوى**
   ```
   "ترجم الملخص للفرنسية"
   ```

### عبر API

```typescript
const response = await fetch('/api/ai/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'أنشئ مذكرة عن الذكاء الاصطناعي',
    action: 'generate'
  })
});
```

---

## 📁 بنية المشروع

```
Qalam/
├── engine/                 # محرك اللغة (Python)
│   ├── qalam/
│   │   ├── lexer.py       # التحليل المعجمي
│   │   ├── parser.py      # التحليل النحوي
│   │   ├── ast_nodes.py   # عقد الشجرة
│   │   ├── keywords.py    # قاموس ثلاثي اللغات
│   │   ├── renderer_pdf.py    # محرك PDF
│   │   ├── renderer_docx.py   # محرك Word
│   │   └── renderer_html.py   # محرك HTML
│   ├── qalam_cli.py       # واجهة سطر الأوامر
│   ├── qalam_gui.py       # واجهة رسومية
│   └── tests/
│
├── website/                # الموقع (Next.js)
│   ├── src/app/
│   │   ├── page.tsx       # الصفحة الرئيسية
│   │   ├── editor/        # المحرر الأونلاين
│   │   └── api/           # واجهات API
│   └── package.json
│
└── README.md
```

---

## 🎨 التصاميم والمخرجات

### PDF
- صفحة غلاف بتصميم Navy + Gold
- ترقيم صفحات تلقائي
- فهرس محتويات تلقائي
- جداول احترافية
- اقتباسات مؤطرة
- دعم RTL كامل للعربية

### Word
- أنماط Heading حقيقية
- جدول محتويات قابل للتحديث
- تنسيق احترافي كامل

### HTML
- معاينة مباشرة
- تصميم متجاوب
- مشاركة سهلة

---

## 🧪 الاختبار

```bash
cd engine
python -m pytest tests/

# أو تشغيل العينة
python -c "
from qalam.lexer import QalamLexer
from qalam.parser import QalamParser
from qalam.renderer_pdf import PDFRenderer

with open('tests/samples/memoire_ar.qlm') as f:
    content = f.read()

lexer = QalamLexer(content)
tokens = lexer.tokenize()

parser = QalamParser(tokens)
ast = parser.parse()

renderer = PDFRenderer()
renderer.render(ast, 'output.pdf')
"
```

---

## 📚 القوالب الجاهزة

متوفرة قوالب لـ:
- 🇩🇿 مذكرة ماستر جزائرية
- 🇫🇷 Mémoire de Master français
- 🇬🇧 MSc Thesis (UK)
- 📄 مقال IEEE
- 📄 مقال APA
- 📊 تقرير تقني

---

## 🗺️ خارطة الطريق

- [x] المحرك الأساسي (Lexer, Parser, AST)
- [x] مولّد PDF
- [x] مولّد Word
- [x] مولّد HTML
- [x] واجهة سطر الأوامر
- [x] واجهة رسومية
- [x] موقع الويب
- [x] المحرر الأونلاين
- [x] API المساعد الذكي
- [ ] تكامل حقيقي مع OpenAI
- [ ] دعم المعادلات LaTeX
- [ ] إضافات VS Code
- [ ] تطبيق سطح مكتب (Electron)

---

## 👥 المساهمة

نرحب بالمساهمات! يرجى قراءة [دليل المساهمة](CONTRIBUTING.md).

```bash
# Fork ثم
git clone https://github.com/YOUR_USERNAME/qalam.git
git checkout -b feature/amazing-feature
git commit -m "Add amazing feature"
git push origin feature/amazing-feature
```

---

## 📝 الترخيص

مرخص تحت [MIT License](LICENSE).

---

## 🙏 شكر خاص

- جامعة 8 ماي 1945 - قالمة
- مجتمع المطورين العرب
- كل من ساهم في تطوير اللغة

---

<div align="center">

**🖊️ كتب بـ Qalam، بُني بحب ❤️**

[الموقع الرسمي](#) • [التوثيق](#) • [GitHub](#) • [Discord](#)

</div>
