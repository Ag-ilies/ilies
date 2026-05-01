'use client';

import { motion } from 'framer-motion';
import { FileText, Download, Eye } from 'lucide-react';

const templates = [
  {
    id: 'algeria-master',
    title: 'مذكرة ماستر جزائرية',
    description: 'قالب مطابق للمعايير الجزائرية للمذكرات',
    lang: 'ar',
    preview: '@@ مذكرة\n  عنوان >> "عنوان المذكرة"\n  طالب >> "اسم الطالب"\n...'
  },
  {
    id: 'ieee-paper',
    title: 'ورقة بحثية IEEE',
    description: 'قالب بصيغة IEEE الدولية',
    lang: 'en',
    preview: '@@ Paper\n  Title >> "Research Paper"\n  Author >> "Author Name"\n...'
  },
  {
    id: 'apa-thesis',
    title: 'أطروحة APA',
    description: 'قالب بصيغة APA الأكاديمية',
    lang: 'en',
    preview: '@@ Thesis\n  Title >> "Thesis Title"\n  Student >> "Student"\n...'
  },
  {
    id: 'french-memoire',
    title: 'Mémoire Français',
    description: 'Template pour mémoire en français',
    lang: 'fr',
    preview: '@@ Mémoire\n  Titre >> "Titre du mémoire"\n  Étudiant >> "Nom"\n...'
  }
];

export default function TemplatesPage() {
  return (
    <main className="pt-24 pb-20 px-4">
      <div className="max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-16"
        >
          <h1 className="text-5xl font-bold mb-6 gradient-text">معرض القوالب</h1>
          <p className="text-xl text-gray-300">اختر قالباً جاهزاً وابدأ الكتابة فوراً</p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {templates.map((template, idx) => (
            <motion.div
              key={template.id}
              className="glass p-6 rounded-2xl hover:bg-white/5 transition-all group"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.1 }}
            >
              <div className="flex items-center justify-between mb-4">
                <FileText className="text-gold" size={32} />
                <span className="px-3 py-1 bg-gold/20 text-gold rounded-full text-sm">
                  {template.lang === 'ar' ? 'عربي' : template.lang === 'fr' ? 'Français' : 'English'}
                </span>
              </div>
              
              <h3 className="text-xl font-bold mb-2">{template.title}</h3>
              <p className="text-gray-400 mb-4">{template.description}</p>
              
              <div className="bg-[#1e1e1e] rounded-lg p-3 mb-4 overflow-x-auto" dir="ltr">
                <pre className="text-xs text-gray-400">{template.preview}</pre>
              </div>
              
              <div className="flex gap-2">
                <button className="flex-1 px-4 py-2 bg-gold hover:bg-yellow-500 text-dark-navy font-bold rounded-lg transition-all flex items-center justify-center gap-2">
                  <Eye size={18} />
                  معاينة
                </button>
                <button className="flex-1 px-4 py-2 border border-gold/50 hover:bg-gold/20 text-gold font-bold rounded-lg transition-all flex items-center justify-center gap-2">
                  <Download size={18} />
                  استخدام
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </main>
  );
}
