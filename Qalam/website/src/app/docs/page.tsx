'use client';

import { motion } from 'framer-motion';
import { Book, Code, FileText, CheckCircle } from 'lucide-react';

export default function DocsPage() {
  return (
    <main className="pt-24 pb-20 px-4">
      <div className="max-w-5xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-16"
        >
          <h1 className="text-5xl font-bold mb-6 gradient-text">التوثيق</h1>
          <p className="text-xl text-gray-300">دليلك الشامل لاستخدام لغة Qalam</p>
        </motion.div>

        {/* Quick Start */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
            <Book className="text-gold" />
            البداية السريعة
          </h2>
          <div className="glass p-8 rounded-2xl">
            <p className="text-gray-300 mb-4">
              لغة Qalam هي لغة برمجة أكاديمية بسيطة وقوية لكتابة المذكرات والبحوث العلمية.
            </p>
            <div className="bg-[#1e1e1e] rounded-xl p-6 overflow-x-auto" dir="ltr">
              <pre className="text-sm text-gray-300">{`@@ مذكرة
  عنوان >> "عنوان البحث"
  طالب >> "اسم الطالب"
  جامعة >> "اسم الجامعة"
@@

{{ ملخص }}
  اكتب الملخص هنا...
{{ /ملخص }}

=== فصل 1: المقدمة ===

--- قسم: الخلفية ---

نص القسم هنا...

{{ تعريف }}
  التعريف هنا...
{{ /تعريف }}`}</pre>
            </div>
          </div>
        </section>

        {/* Syntax Guide */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
            <Code className="text-gold" />
            دليل الصيغة
          </h2>
          
          <div className="space-y-6">
            <div className="glass p-6 rounded-xl">
              <h3 className="text-xl font-bold mb-3 text-gold">البيانات الوصفية @@</h3>
              <p className="text-gray-400 mb-3">تستخدم لتحديد معلومات المستند الأساسية</p>
              <div className="bg-[#1e1e1e] rounded-lg p-4" dir="ltr">
                <pre className="text-sm text-gray-300">{`@@ مذكرة
  عنوان >> "العنوان"
  طالب >> "الطالب"
@@`}</pre>
              </div>
            </div>

            <div className="glass p-6 rounded-xl">
              <h3 className="text-xl font-bold mb-3 text-gold">الفصول والأقسام</h3>
              <p className="text-gray-400 mb-3">هيكلة المستند باستخدام الفصول والأقسام</p>
              <div className="bg-[#1e1e1e] rounded-lg p-4" dir="ltr">
                <pre className="text-sm text-gray-300">{`=== فصل 1: العنوان ===

--- قسم: العنوان ---

~~~ فرع: العنوان ~~~`}</pre>
              </div>
            </div>

            <div className="glass p-6 rounded-xl">
              <h3 className="text-xl font-bold mb-3 text-gold">البيئات {{ }}</h3>
              <p className="text-gray-400 mb-3">أنواع البيئات المتاحة:</p>
              <ul className="grid md:grid-cols-2 gap-3 text-gray-300">
                <li><CheckCircle size={16} className="inline text-green-500 ml-2" />ملخص، مقدمة، خاتمة</li>
                <li><CheckCircle size={16} className="inline text-green-500 ml-2" />إهداء، شكر</li>
                <li><CheckCircle size={16} className="inline text-green-500 ml-2" />اقتباس، تعريف، ملاحظة</li>
                <li><CheckCircle size={16} className="inline text-green-500 ml-2" />جدول، قائمة، معادلة</li>
                <li><CheckCircle size={16} className="inline text-green-500 ml-2" />شكل، مراجع، كتاب، مقال</li>
              </ul>
            </div>
          </div>
        </section>

        {/* Examples */}
        <section>
          <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
            <FileText className="text-gold" />
            أمثلة
          </h2>
          <div className="grid md:grid-cols-2 gap-6">
            <a href="/editor" className="glass p-6 rounded-xl hover:bg-white/5 transition-all block">
              <h3 className="text-xl font-bold mb-2">مذكرة ماستر جزائرية</h3>
              <p className="text-gray-400">قالب جاهز للمذكرات الجزائرية</p>
            </a>
            <a href="/editor" className="glass p-6 rounded-xl hover:bg-white/5 transition-all block">
              <h3 className="text-xl font-bold mb-2">بحث IEEE</h3>
              <p className="text-gray-400">قالب بصيغة IEEE الدولية</p>
            </a>
          </div>
        </section>
      </div>
    </main>
  );
}
