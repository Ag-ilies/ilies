'use client';

import { motion } from 'framer-motion';
import { BookOpen, PenTool, GraduationCap } from 'lucide-react';

const articles = [
  {
    id: 1,
    title: 'كيف تكتب مذكرة ماستر ناجحة؟',
    excerpt: 'دليل شامل لكتابة مذكرة ماستر من البداية حتى التسليم...',
    category: 'نصائح أكاديمية',
    date: '2025-01-15',
    readTime: '8 دقائق'
  },
  {
    id: 2,
    title: 'مقارنة بين LaTeX و Qalam',
    excerpt: 'لماذا تعتبر Qalam الخيار الأفضل للباحثين العرب...',
    category: 'مقارنات',
    date: '2025-01-10',
    readTime: '6 دقائق'
  },
  {
    id: 3,
    title: 'التنسيق الأكاديمي حسب المعايير الجزائرية',
    excerpt: 'كل ما تحتاج معرفته حول معايير تنسيق المذكرات في الجامعات الجزائرية...',
    category: 'معايير',
    date: '2025-01-05',
    readTime: '10 دقائق'
  },
  {
    id: 4,
    title: 'كيفية استخدام الذكاء الاصطناعي في البحث العلمي',
    excerpt: 'أفضل الممارسات لاستخدام AI في كتابة البحوث مع الحفاظ على النزاهة الأكاديمية...',
    category: 'ذكاء اصطناعي',
    date: '2024-12-28',
    readTime: '7 دقائق'
  },
  {
    id: 5,
    title: 'تنسيق المراجع بصيغة APA',
    excerpt: 'دليل عملي لتنسيق المراجع والمصادر حسب أسلوب APA...',
    category: 'توثيق',
    date: '2024-12-20',
    readTime: '5 دقائق'
  },
  {
    id: 6,
    title: 'أخطاء شائعة في الكتابة الأكاديمية',
    excerpt: 'تعرف على الأخطاء الأكثر شيوعاً وكيفية تجنبها...',
    category: 'نصائح',
    date: '2024-12-15',
    readTime: '6 دقائق'
  }
];

export default function BlogPage() {
  return (
    <main className="pt-24 pb-20 px-4">
      <div className="max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-16"
        >
          <h1 className="text-5xl font-bold mb-6 gradient-text">المدونة</h1>
          <p className="text-xl text-gray-300">مقالات ونصائح للباحثين والطلاب</p>
        </motion.div>

        {/* Featured Article */}
        <motion.div
          className="glass p-8 rounded-2xl mb-12 border border-gold/30"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
        >
          <div className="flex flex-col md:flex-row gap-8 items-center">
            <div className="flex-1">
              <span className="px-3 py-1 bg-gold/20 text-gold rounded-full text-sm">
                مميز
              </span>
              <h2 className="text-3xl font-bold mt-4 mb-4">
                كيف تكتب مذكرة ماستر ناجحة؟
              </h2>
              <p className="text-gray-300 mb-6">
                دليل شامل يغطي جميع مراحل كتابة مذكرة الماستر، من اختيار الموضوع حتى المناقشة النهائية...
              </p>
              <div className="flex items-center gap-6 text-gray-400 text-sm">
                <span className="flex items-center gap-2">
                  <BookOpen size={16} />
                  نصائح أكاديمية
                </span>
                <span>2025-01-15</span>
                <span className="flex items-center gap-2">
                  <PenTool size={16} />
                  8 دقائق قراءة
                </span>
              </div>
              <button className="mt-6 px-6 py-3 bg-gold hover:bg-yellow-500 text-dark-navy font-bold rounded-xl transition-all">
                اقرأ المقال
              </button>
            </div>
            <div className="w-full md:w-64 h-40 bg-gradient-to-br from-gold/30 to-gold/10 rounded-xl flex items-center justify-center">
              <GraduationCap size={64} className="text-gold" />
            </div>
          </div>
        </motion.div>

        {/* Articles Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {articles.map((article, idx) => (
            <motion.article
              key={article.id}
              className="glass p-6 rounded-xl hover:bg-white/5 transition-all cursor-pointer group"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.1 }}
            >
              <span className="px-3 py-1 bg-white/10 text-gray-300 rounded-full text-xs">
                {article.category}
              </span>
              <h3 className="text-xl font-bold mt-4 mb-3 group-hover:text-gold transition-colors">
                {article.title}
              </h3>
              <p className="text-gray-400 text-sm mb-4 line-clamp-2">
                {article.excerpt}
              </p>
              <div className="flex items-center justify-between text-gray-500 text-xs">
                <span>{article.date}</span>
                <span>{article.readTime}</span>
              </div>
            </motion.article>
          ))}
        </div>

        {/* Newsletter */}
        <motion.div
          className="mt-16 glass p-8 rounded-2xl text-center border border-gold/30"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
        >
          <h2 className="text-2xl font-bold mb-4">اشترك في نشرتنا البريدية</h2>
          <p className="text-gray-400 mb-6 max-w-md mx-auto">
            احصل على أحدث المقالات والنصائح الأكاديمية مباشرة في بريدك الإلكتروني
          </p>
          <div className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
            <input
              type="email"
              placeholder="بريدك الإلكتروني"
              className="flex-1 px-4 py-3 bg-black/30 border border-white/20 rounded-xl focus:outline-none focus:border-gold"
            />
            <button className="px-6 py-3 bg-gold hover:bg-yellow-500 text-dark-navy font-bold rounded-xl transition-all">
              اشترك
            </button>
          </div>
        </motion.div>
      </div>
    </main>
  );
}
