'use client';

import { motion } from 'framer-motion';
import { Zap, Globe, Brain, Layers, Shield, Rocket } from 'lucide-react';

const features = [
  {
    icon: Zap,
    title: 'سرعة فائقة',
    description: 'بناء فوري للمستندات بدون انتظار، أسرع 10 مرات من LaTeX',
    color: 'from-yellow-500 to-orange-500'
  },
  {
    icon: Globe,
    title: 'دعم عربي كامل',
    description: 'تنسيق أصلي للغة العربية مع RTL صحيح وتشكيل كامل',
    color: 'from-green-500 to-emerald-500'
  },
  {
    icon: Brain,
    title: 'ذكاء اصطناعي مدمج',
    description: 'مساعد ذكي يكتب ويصحح ويترجم المحتوى تلقائياً',
    color: 'from-blue-500 to-purple-500'
  },
  {
    icon: Layers,
    title: 'صيغة بسيطة',
    description: 'تعلم الأساسيات في 5 دقائق وابدأ الكتابة بلا حدود',
    color: 'from-pink-500 to-rose-500'
  },
  {
    icon: Shield,
    title: 'جودة أكاديمية',
    description: 'تنسيق احترافي يلبي معايير الجامعات الجزائرية والدولية',
    color: 'from-cyan-500 to-blue-500'
  },
  {
    icon: Rocket,
    title: 'مخرجات متعددة',
    description: 'صدّر مستندك إلى PDF و Word و HTML من ملف واحد',
    color: 'from-amber-500 to-yellow-500'
  }
];

export default function FeaturesPage() {
  return (
    <main className="pt-24 pb-20 px-4">
      <div className="max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-16"
        >
          <h1 className="text-5xl font-bold mb-6 gradient-text">المميزات</h1>
          <p className="text-xl text-gray-300">لماذا يختار الباحثون Qalam؟</p>
        </motion.div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-20">
          {features.map((feature, idx) => (
            <motion.div
              key={feature.title}
              className="glass p-8 rounded-2xl hover:bg-white/5 transition-all group"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.1 }}
            >
              <div
                className={`w-16 h-16 rounded-xl bg-gradient-to-br ${feature.color} flex items-center justify-center mb-6 group-hover:scale-110 transition-transform`}
              >
                <feature.icon size={32} className="text-white" />
              </div>
              <h3 className="text-2xl font-bold mb-4">{feature.title}</h3>
              <p className="text-gray-400">{feature.description}</p>
            </motion.div>
          ))}
        </div>

        {/* Detailed Sections */}
        <div className="space-y-20">
          {/* Arabic Support */}
          <motion.section
            className="grid md:grid-cols-2 gap-12 items-center"
            initial={{ opacity: 0, x: -50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
          >
            <div>
              <h2 className="text-4xl font-bold mb-6">
                دعم <span className="gradient-text">العربية</span> بشكل أصلي
              </h2>
              <p className="text-gray-300 mb-6 text-lg">
                Qalam صُممت من الصفر لدعم اللغة العربية بشكل كامل. لا حاجة لإعدادات معقدة
                أو حزم إضافية - كل شيء يعمل بشكل طبيعي.
              </p>
              <ul className="space-y-4 text-gray-400">
                <li className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-gold rounded-full"></div>
                  اتجاه RTL تلقائي
                </li>
                <li className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-gold rounded-full"></div>
                  دعم التشكيل والحركات
                </li>
                <li className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-gold rounded-full"></div>
                  خطوط عربية احترافية مدمجة
                </li>
                <li className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-gold rounded-full"></div>
                  ترقيم الصفحات بالعربية
                </li>
              </ul>
            </div>
            <div className="glass p-6 rounded-2xl" dir="rtl">
              <pre className="text-sm text-gray-300 overflow-x-auto">{`@@ مذكرة
  عنوان >> "اللسانيات الجنائية"
  طالب >> "واهيبة بلقاسم"
  جامعة >> "جامعة قالمة"
@@

{{ ملخص }}
  تتناول هذه الدراسة علم اللسانيات
  الجنائية وتطبيقاته في السياق الجزائري...
{{ /ملخص }}`}</pre>
            </div>
          </motion.section>

          {/* AI Assistant */}
          <motion.section
            className="grid md:grid-cols-2 gap-12 items-center"
            initial={{ opacity: 0, x: 50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
          >
            <div className="order-2 md:order-1 glass p-6 rounded-2xl" dir="ltr">
              <pre className="text-sm text-gray-300 overflow-x-auto">{`> اكتب لي فصلاً نظرياً
  عن اللسانيات الجنائية

✓ تم إنشاء الفصل:
=== فصل 1: الإطار النظري ===
--- قسم: مفهوم اللسانيات ---
اللسانيات الجنائية هي العلم الذي...
{{ تعريف }}
  التعريف الكامل...
{{ /تعريف }}`}</pre>
            </div>
            <div className="order-1 md:order-2">
              <h2 className="text-4xl font-bold mb-6">
                مساعد <span className="gradient-text">ذكاء اصطناعي</span> متطور
              </h2>
              <p className="text-gray-300 mb-6 text-lg">
                اطلب من المساعد كتابة أي جزء من بحثك وسيتولى المهمة. يمكنه أيضاً
                تصحيح الأخطاء، ترجمة المحتوى، واقتراح المراجع.
              </p>
              <ul className="space-y-4 text-gray-400">
                <li className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-gold rounded-full"></div>
                  كتابة تلقائية للفصول والأقسام
                </li>
                <li className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-gold rounded-full"></div>
                  تصحيح إملائي ونحوي
                </li>
                <li className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-gold rounded-full"></div>
                  ترجمة بين العربية والفرنسية والإنجليزية
                </li>
                <li className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-gold rounded-full"></div>
                  اقتراح مراجع حقيقية
                </li>
              </ul>
            </div>
          </motion.section>
        </div>

        {/* CTA */}
        <motion.div
          className="mt-20 glass p-12 rounded-3xl text-center border border-gold/30"
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
        >
          <h2 className="text-4xl font-bold mb-6">
            جاهز لتجربة <span className="gradient-text">المستقبل</span>؟
          </h2>
          <p className="text-xl text-gray-300 mb-8">
            انضم إلى آلاف الباحثين الذين يستخدمون Qalam لكتابة مذكراتهم
          </p>
          <button className="px-8 py-4 bg-gold hover:bg-yellow-500 text-dark-navy font-bold text-lg rounded-xl transition-all transform hover:scale-105">
            ابدأ مجاناً الآن
          </button>
        </motion.div>
      </div>
    </main>
  );
}
