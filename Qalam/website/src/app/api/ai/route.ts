import { NextRequest, NextResponse } from 'next/server';

// System Prompt للمساعد الذكي
const SYSTEM_PROMPT = `أنت "مساعد قلم" — خبير أكاديمي ذكي متخصص في لغة Qalam (.qlm).

مهامك:
1. كتابة ملفات .qlm صحيحة نحوياً
2. استخدام الصيغة الصحيحة: @@ للمعلومات، === للفصول،
   --- للأقسام، {{ }} للبيئات، >> للخصائص
3. الالتزام بالمعايير الأكاديمية الجزائرية
4. دعم العربية والفرنسية والإنجليزية
5. اقتراح مراجع حقيقية ومحتوى أكاديمي

دائماً أخرج كود .qlm كامل وصالح للبناء مباشرة.

الصيغة:
- @@ ... @@ للبيانات الوصفية
- === عنوان === للفصول
- --- عنوان --- للأقسام
- ~~~ عنوان ~~~ للفروع
- {{ نوع }} ... {{ /نوع }} للبيئات
- مفتاح >> "قيمة" للخصائص
- **نص** للغامق
- *نص* للمائل
- | خلية | لجدول`;

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { message, context = '', action = 'generate' } = body;

    if (!message) {
      return NextResponse.json(
        { error: 'الرسالة مطلوبة' },
        { status: 400 }
      );
    }

    // محاكاة استجابة AI - في الإنتاج سيتم استخدام OpenAI API
    const mockResponses: Record<string, any> = {
      generate: {
        success: true,
        code: `@@ مذكرة
  عنوان   >> "${message.substring(0, 50)}..."
  طالب    >> "اسم الطالب"
  مشرف    >> "اسم المشرف"
  جامعة   >> "اسم الجامعة"
  كلية    >> "كلية الآداب والعلوم الإنسانية"
  سنة     >> "2025-2026"
  درجة    >> ماستر
  لغة     >> ar
  مخرج    >> pdf, word
@@

{{ إهداء }}
  إلى من كان لي سنداً وعوناً...
{{ /إهداء }}

{{ ملخص }}
  ${message}
{{ /ملخص }}

=== فصل 1: الإطار النظري ===

--- قسم: المفاهيم الأساسية ---

${message}

{{ تعريف }}
  التعريف الأكاديمي للمفهوم...
{{ /تعريف }}

{{ مثال }}
  مثال توضيحي من الواقع...
{{ /مثال }}

~~~ فرع: التفاصيل الدقيقة ~~~

شرح تفصيلي للموضوع...

{{ قائمة }}
  - النقطة الأولى
  - النقطة الثانية
  - النقطة الثالثة
{{ /قائمة }}

=== فصل 2: الدراسة الميدانية ===

--- قسم: المنهجية ---

وصف منهجية البحث...

{{ جدول >> نتائج العينة }}
  | المجموعة | العدد | النسبة |
  | الضابطة  | 50    | 50%    |
  | التجريبية| 50    | 50%    |
{{ /جدول }}

{{ خاتمة }}
  خاتمة البحث والاستنتاجات...
{{ /خاتمة }}

{{ مراجع }}
  {{ كتاب >> Ref1 }}
    مؤلف  >> "اسم المؤلف"
    عنوان >> "عنوان الكتاب المرجعي"
    سنة   >> 2024
    ناشر  >> "دار النشر"
  {{ /كتاب }}
  
  {{ مقال >> Ref2 }}
    مؤلف  >> "باحث آخر"
    عنوان >> "عنوان المقال العلمي"
    مجلة  >> "مجلة محكمة"
    سنة   >> 2023
    صفحات >> "1-20"
  {{ /مقال }}
{{ /مراجع }}`,
        explanation: 'تم إنشاء هيكل مذكرة كامل يتضمن:\n- صفحة غلاف مع البيانات الوصفية\n- إهداء وملخص\n- فصلين رئيسيين مع أقسام وفروع\n- بيئات متنوعة (تعريف، مثال، قائمة، جدول)\n- خاتمة ومراجع',
        suggestions: [
          'يمكنك إضافة المزيد من الفصول حسب الحاجة',
          'استخدم {{ معادلة }} لإضافة معادلات رياضية',
          'أضف {{ شكل }} لتضمين الصور والرسوم البيانية',
          'استخدم [ref: Ref1] للإحالة على المراجع في النص'
        ]
      },
      
      edit: {
        success: true,
        code: '// الكود المعدل سيظهر هنا',
        changes: ['تم تحسين التنسيق', 'أضيفت مراجع إضافية']
      },
      
      translate: {
        success: true,
        originalLang: 'ar',
        targetLang: 'fr',
        code: '// الترجمة الفرنسية'
      },
      
      references: {
        success: true,
        references: [
          { type: 'book', key: 'Coulthard2010', formatted: 'Coulthard, M. & Johnson, A. (2010). Introduction to Forensic Linguistics. Routledge.' },
          { type: 'article', key: 'Smith2022', formatted: 'Smith, J. (2022). Language in Court. Applied Linguistics, 43(1), 1-20.' }
        ]
      }
    };

    const response = mockResponses[action] || mockResponses.generate;

    // في الإنتاج: استدعاء OpenAI API
    /*
    const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
    const completion = await openai.chat.completions.create({
      model: 'gpt-4-turbo-preview',
      messages: [
        { role: 'system', content: SYSTEM_PROMPT },
        { role: 'user', content: `${context}\n\n${message}` }
      ],
      temperature: 0.7,
      max_tokens: 2000
    });
    */

    return NextResponse.json(response);

  } catch (error) {
    console.error('AI error:', error);
    return NextResponse.json(
      { error: 'فشل المعالجة', details: String(error) },
      { status: 500 }
    );
  }
}

export async function GET() {
  return NextResponse.json({
    message: 'Qalam AI Assistant API',
    version: '1.0.0',
    actions: ['generate', 'edit', 'translate', 'references', 'chat'],
    languages: ['ar', 'en', 'fr']
  });
}
