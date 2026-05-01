import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Qalam - لغة الكتابة الأكاديمية",
  description: "لغة برمجة أكاديمية ثورية لكتابة المذكرات والبحوث العلمية تتفوق على LaTeX و Typst",
  keywords: ["Qalam", "أكاديمي", "LaTeX", "PDF", "بحث علمي", "مذكرة"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ar" dir="rtl">
      <body className="bg-dark-navy text-white min-h-screen">
        {/* Navigation */}
        <nav className="fixed top-0 w-full z-50 glass border-b border-white/10">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16">
              <div className="flex items-center gap-3">
                <span className="text-3xl">🖊️</span>
                <span className="text-2xl font-bold gradient-text">Qalam</span>
              </div>
              
              <div className="hidden md:flex items-center gap-8">
                <a href="/#features" className="hover:text-gold transition-colors">المميزات</a>
                <a href="/docs" className="hover:text-gold transition-colors">التوثيق</a>
                <a href="/editor" className="hover:text-gold transition-colors">المحرر</a>
                <a href="/templates" className="hover:text-gold transition-colors">القوالب</a>
                <a href="/pricing" className="hover:text-gold transition-colors">الأسعار</a>
              </div>
              
              <div className="flex items-center gap-4">
                <button className="px-4 py-2 rounded-lg border border-gold/50 hover:bg-gold/20 transition-all">
                  تسجيل الدخول
                </button>
                <button className="px-6 py-2 bg-gold hover:bg-yellow-500 text-dark-navy font-bold rounded-lg transition-all transform hover:scale-105">
                  ابدأ مجاناً
                </button>
              </div>
            </div>
          </div>
        </nav>

        {children}

        {/* Footer */}
        <footer className="border-t border-white/10 mt-20 py-12">
          <div className="max-w-7xl mx-auto px-4 grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center gap-2 mb-4">
                <span className="text-2xl">🖊️</span>
                <span className="text-xl font-bold">Qalam</span>
              </div>
              <p className="text-gray-400 text-sm">
                لغة برمجة أكاديمية ثورية لكتابة المذكرات والبحوث العلمية
              </p>
            </div>
            
            <div>
              <h4 className="font-bold mb-4">روابط سريعة</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="/docs" className="hover:text-gold">التوثيق</a></li>
                <li><a href="/editor" className="hover:text-gold">المحرر</a></li>
                <li><a href="/blog" className="hover:text-gold">المدونة</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-bold mb-4">المجتمع</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="https://github.com/qalam-lang" target="_blank" rel="noopener noreferrer" className="hover:text-gold">GitHub</a></li>
                <li><a href="#" className="hover:text-gold">Discord</a></li>
                <li><a href="#" className="hover:text-gold">Twitter</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-bold mb-4">تواصل معنا</h4>
              <ul className="space-y-2 text-gray-400">
                <li>support@qalam-lang.com</li>
                <li>متابعة على وسائل التواصل</li>
              </ul>
            </div>
          </div>
          
          <div className="max-w-7xl mx-auto px-4 mt-8 pt-8 border-t border-white/10 text-center text-gray-500">
            © 2025 Qalam. جميع الحقوق محفوظة.
          </div>
        </footer>
      </body>
    </html>
  );
}
