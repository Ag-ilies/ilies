'use client';

import { motion } from 'framer-motion';
import { CheckCircle, Star, Zap } from 'lucide-react';

const plans = [
  {
    name: 'مجاني',
    price: '0',
    period: 'دائماً',
    features: [
      'محرر أونلاين أساسي',
      'بناء PDF و Word',
      '5 قوالب جاهزة',
      'مساحة تخزين 100MB',
      'دعم المجتمع'
    ],
    cta: 'ابدأ مجاناً',
    popular: false
  },
  {
    name: 'محترف',
    price: '9.99',
    period: '/ شهر',
    features: [
      'كل ميزات الخطة المجانية',
      'قوالب غير محدودة',
      'مساعد AI ذكي',
      'مساحة تخزين 10GB',
      'أولوية في الدعم',
      'إحصائيات متقدمة',
      'تصدير HTML'
    ],
    cta: 'اشترك الآن',
    popular: true
  },
  {
    name: 'مؤسسات',
    price: '49.99',
    period: '/ شهر',
    features: [
      'كل ميزات خطة محترف',
      'حسابات غير محدودة',
      'API كامل',
      'مساحة تخزين غير محدودة',
      'دعم فني 24/7',
      'تدريب مخصص',
      'SLA 99.9%'
    ],
    cta: 'تواصل معنا',
    popular: false
  }
];

export default function PricingPage() {
  return (
    <main className="pt-24 pb-20 px-4">
      <div className="max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-16"
        >
          <h1 className="text-5xl font-bold mb-6 gradient-text">الأسعار</h1>
          <p className="text-xl text-gray-300">اختر الخطة المناسبة لاحتياجاتك الأكاديمية</p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-8">
          {plans.map((plan, idx) => (
            <motion.div
              key={plan.name}
              className={`glass p-8 rounded-2xl relative ${
                plan.popular ? 'border-2 border-gold scale-105' : ''
              }`}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.1 }}
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                  <span className="bg-gold text-dark-navy px-4 py-1 rounded-full text-sm font-bold flex items-center gap-1">
                    <Star size={16} />
                    الأكثر شعبية
                  </span>
                </div>
              )}
              
              <div className="text-center mb-8">
                <h3 className="text-2xl font-bold mb-2">{plan.name}</h3>
                <div className="flex items-baseline justify-center gap-1">
                  <span className="text-4xl font-bold gradient-text">${plan.price}</span>
                  <span className="text-gray-400">{plan.period}</span>
                </div>
              </div>
              
              <ul className="space-y-4 mb-8">
                {plan.features.map((feature, i) => (
                  <li key={i} className="flex items-start gap-3 text-gray-300">
                    <CheckCircle size={20} className="text-green-500 flex-shrink-0 mt-0.5" />
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>
              
              <button
                className={`w-full py-3 rounded-xl font-bold transition-all ${
                  plan.popular
                    ? 'bg-gold hover:bg-yellow-500 text-dark-navy'
                    : 'border border-gold/50 hover:bg-gold/20 text-gold'
                }`}
              >
                {plan.cta}
              </button>
            </motion.div>
          ))}
        </div>

        {/* FAQ */}
        <motion.div
          className="mt-20"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
        >
          <h2 className="text-3xl font-bold text-center mb-8">الأسئلة الشائعة</h2>
          <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
            {[
              { q: 'هل يمكنني إلغاء اشتراكي في أي وقت؟', a: 'نعم، يمكنك إلغاء اشتراكك في أي وقت دون أي التزامات.' },
              { q: 'هل توجد فترة تجريبية؟', a: 'نعم، نوفر فترة تجريبية مجانية لمدة 14 يوماً للخطة الاحترافية.' },
              { q: 'هل يمكنني التبديل بين الخطط؟', a: 'بالطبع، يمكنك الترقية أو التخفيض في أي وقت من لوحة التحكم.' },
              { q: 'ما طرق الدفع المتاحة؟', a: 'نقبل البطاقات الائتمانية، PayPal، والتحويل البنكي.' }
            ].map((faq, idx) => (
              <div key={idx} className="glass p-6 rounded-xl">
                <h4 className="font-bold mb-2 flex items-center gap-2">
                  <Zap size={18} className="text-gold" />
                  {faq.q}
                </h4>
                <p className="text-gray-400">{faq.a}</p>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </main>
  );
}
