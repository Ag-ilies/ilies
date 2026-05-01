'use client';

import { motion } from 'framer-motion';
import { Code, FileText, Zap, Globe, Brain, Layers, CheckCircle, ArrowLeft } from 'lucide-react';

export default function Home() {
  return (
    <main className="pt-16">
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
        {/* Background Effects */}
        <div className="absolute inset-0 bg-gradient-to-br from-navy via-dark-navy to-black"></div>
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-gold/20 rounded-full blur-3xl animate-float"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-float" style={{ animationDelay: '1s' }}></div>
        
        <div className="relative z-10 max-w-6xl mx-auto px-4 text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <span className="text-8xl mb-6 block animate-float">🖊️</span>
            <h1 className="text-6xl md:text-8xl font-bold mb-6">
              <span className="gradient-text">Qalam</span>
            </h1>
            <p className="text-2xl md:text-3xl text-gray-300 mb-8 arabic-text">
              لغة الكتابة الأكاديمية للمستقبل
            </p>
            <p className="text-lg text-gray-400 mb-12 max-w-3xl mx-auto">
              اكتب مذكراتك وبحوثك العلمية بصيغة عربية أنيقة، وحوّلها إلى PDF و Word احترافيين بنقرة واحدة. 
              أفضل من LaTeX، أسهل من Typst، مصممة للباحثين العرب.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="px-8 py-4 bg-gold hover:bg-yellow-500 text-dark-navy font-bold text-lg rounded-xl transition-all transform hover:scale-105 flex items-center justify-center gap-2">
                <Code size={24} />
                جرب المحرر الآن
              </button>
              <button className="px-8 py-4 border-2 border-gold/50 hover:bg-gold/20 text-gold font-bold text-lg rounded-xl transition-all flex items-center justify-center gap-2">
                <FileText size={24} />
                اقرأ التوثيق
              </button>
            </div>
            
            {/* Stats */}
            <div className="grid grid-cols-3 gap-8 mt-16 max-w-3xl mx-auto">
              <div className="glass p-6 rounded-xl">
                <div className="text-4xl font-bold gradient-text">+2,500</div>
                <div className="text-gray-400 mt-2">مستخدم نشط</div>
              </div>
              <div className="glass p-6 rounded-xl">
                <div className="text-4xl font-bold gradient-text">+10,000</div>
                <div className="text-gray-400 mt-2">مذكرة مولّدة</div>
              </div>
              <div className="glass p-6 rounded-xl">
                <div className="text-4xl font-bold gradient-text">99.9%</div>
                <div className="text-gray-400 mt-2">رضا المستخدمين</div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Comparison Section */}
      <section className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <motion.h2 
            className="text-4xl md:text-5xl font-bold text-center mb-16"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
          >
            لماذا <span className="gradient-text">Qalam</span>؟
          </motion.h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: Zap,
                title: "أسرع 10 مرات",
                desc: "بناء فوري بدون تعقيدات LaTeX الطويلة",
                color: "from-yellow-500 to-orange-500"
              },
              {
                icon: Globe,
                title: "عربي بالكامل",
                desc: "دعم أصلي للغة العربية مع RTL صحيح",
                color: "from-green-500 to-emerald-500"
              },
              {
                icon: Brain,
                title: "ذكاء اصطناعي",
                desc: "مساعد ذكي يكتب ويصحح ويترجم تلقائياً",
                color: "from-blue-500 to-purple-500"
              },
              {
                icon: Layers,
                title: "صيغة بسيطة",
                desc: "تعلم الصيغة في 5 دقائق، اكتب بلا حدود",
                color: "from-pink-500 to-rose-500"
              },
              {
                icon: FileText,
                title: "مخرجات متعددة",
                desc: "PDF، Word، HTML من ملف واحد",
                color: "from-cyan-500 to-blue-500"
              },
              {
                icon: CheckCircle,
                title: "جودة أكاديمية",
                desc: "تنسيق احترافي يلبي معايير الجامعات",
                color: "from-amber-500 to-yellow-500"
              }
            ].map((feature, idx) => (
              <motion.div
                key={idx}
                className="glass p-8 rounded-2xl hover:bg-white/5 transition-all group"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.1 }}
              >
                <div className={`w-16 h-16 rounded-xl bg-gradient-to-br ${feature.color} flex items-center justify-center mb-6 group-hover:scale-110 transition-transform`}>
                  <feature.icon size={32} className="text-white" />
                </div>
                <h3 className="text-2xl font-bold mb-4">{feature.title}</h3>
                <p className="text-gray-400">{feature.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Code Example */}
      <section className="py-20 px-4 bg-black/30">
        <div className="max-w-6xl mx-auto">
          <motion.h2 
            className="text-4xl md:text-5xl font-bold text-center mb-8"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
          >
            صيغة <span className="gradient-text">بسيطة وقوية</span>
          </motion.h2>
          
          <div className="grid md:grid-cols-2 gap-8 items-center">
            <motion.div
              className="bg-[#1e1e1e] rounded-xl overflow-hidden shadow-2xl"
              initial={{ opacity: 0, x: -50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
            >
              <div className="flex items-center gap-2 px-4 py-3 bg-[#2d2d2d]">
                <div className="w-3 h-3 rounded-full bg-red-500"></div>
                <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                <div className="w-3 h-3 rounded-full bg-green-500"></div>
                <span className="ml-4 text-gray-400 text-sm">memoire.qlm</span>
              </div>
              <pre className="p-6 text-sm overflow-x-auto text-gray-300" dir="ltr">
{`@@ مذكرة
  عنوان >> "اللسانيات الجنائية"
  طالب >> "واهيبة بلقاسم"
  جامعة >> "جامعة قالمة"
@@

{{ ملخص }}
  تتناول هذه الدراسة...
{{ /ملخص }}

=== فصل 1: الإطار النظري ===

--- قسم: المفاهيم ---

اللسانيات الجنائية هي...

{{ تعريف }}
  التعريف هنا...
{{ /تعريف }}

{{ جدول >> النتائج }}
  | العينة | النسبة |
  | أ      | 50%    |
  | ب      | 50%    |
{{ /جدول }}`}
              </pre>
            </motion.div>
            
            <motion.div
              className="space-y-6"
              initial={{ opacity: 0, x: 50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
            >
              <div className="flex items-start gap-4">
                <div className="w-10 h-10 rounded-lg bg-gold/20 flex items-center justify-center flex-shrink-0">
                  <span className="text-gold text-xl">@@</span>
                </div>
                <div>
                  <h4 className="text-xl font-bold mb-2">بيانات وصفية واضحة</h4>
                  <p className="text-gray-400">حدد معلومات المذكرة كاملة بصيغة سهلة القراءة</p>
                </div>
              </div>
              
              <div className="flex items-start gap-4">
                <div className="w-10 h-10 rounded-lg bg-gold/20 flex items-center justify-center flex-shrink-0">
                  <span className="text-gold text-xl">===</span>
                </div>
                <div>
                  <h4 className="text-xl font-bold mb-2">هيكلة هرمية بديهية</h4>
                  <p className="text-gray-400">فصول، أقسام، وفروع بتنظيم طبيعي</p>
                </div>
              </div>
              
              <div className="flex items-start gap-4">
                <div className="w-10 h-10 rounded-lg bg-gold/20 flex items-center justify-center flex-shrink-0">
                  <span className="text-gold text-xl">{{`{{}}`}}</span>
                </div>
                <div>
                  <h4 className="text-xl font-bold mb-2">بيئات غنية</h4>
                  <p className="text-gray-400">جداول، اقتباسات، تعريفات، ملاحظات، معادلات</p>
                </div>
              </div>
              
              <div className="flex items-start gap-4">
                <div className="w-10 h-10 rounded-lg bg-gold/20 flex items-center justify-center flex-shrink-0">
                  <span className="text-gold text-xl">&gt;&gt;</span>
                </div>
                <div>
                  <h4 className="text-xl font-bold mb-2">خصائص مرنة</h4>
                  <p className="text-gray-400">أضف تفاصيل إضافية لكل عنصر بسهولة</p>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            className="glass p-12 rounded-3xl border border-gold/30"
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              جاهز لبدء كتابة <span className="gradient-text">احترافية</span>؟
            </h2>
            <p className="text-xl text-gray-300 mb-8 arabic-text">
              انضم إلى آلاف الباحثين الذين يستخدمون Qalam لكتابة مذكراتهم
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="px-8 py-4 bg-gold hover:bg-yellow-500 text-dark-navy font-bold text-lg rounded-xl transition-all transform hover:scale-105 flex items-center justify-center gap-2">
                ابدأ مجاناً الآن
                <ArrowLeft size={24} className="rotate-180" />
              </button>
              <button className="px-8 py-4 border-2 border-white/30 hover:bg-white/10 font-bold text-lg rounded-xl transition-all">
                تحميل التطبيق
              </button>
            </div>
          </motion.div>
        </div>
      </section>
    </main>
  );
}
