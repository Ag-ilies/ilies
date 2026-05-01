'use client';

import { useState, useRef } from 'react';
import Editor from '@monaco-editor/react';
import { Play, Download, FileText, Code2, MessageSquare, Copy, Check, Loader2 } from 'lucide-react';

export default function EditorPage() {
  const [code, setCode] = useState<string>('@@ مذكرة\n  عنوان   >> "عنوان المذكرة"\n  طالب    >> "اسم الطالب"\n  جامعة   >> "اسم الجامعة"\n@@\n\n{{ ملخص }}\n  اكتب الملخص هنا...\n{{ /ملخص }}\n\n=== فصل 1: الإطار النظري ===\n\n--- قسم: المفاهيم ---\n\nاكتب المحتوى هنا...\n');
  const [output, setOutput] = useState<string | null>(null);
  const [isBuilding, setIsBuilding] = useState(false);
  const [copied, setCopied] = useState(false);
  const [showAI, setShowAI] = useState(false);
  const editorRef = useRef<any>(null);

  const handleBuild = async (format: 'pdf' | 'word' | 'all' = 'all') => {
    setIsBuilding(true);
    try {
      const response = await fetch('/api/build', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, format })
      });
      const data = await response.json();
      if (data.success) {
        setOutput(`✓ تم البناء بنجاح!\n⏱️ وقت البناء: ${data.stats.buildTime}\n📊 الإحصائيات:\n  - الرموز: ${data.stats.tokens}\n  - الفصول: ${data.stats.chapters}\n  - الأقسام: ${data.stats.sections}\n  - الجداول: ${data.stats.tables}`);
      } else {
        setOutput(`✗ فشل البناء:\n${data.error}`);
      }
    } catch (error) {
      setOutput(`✗ خطأ:\n${String(error)}`);
    } finally {
      setIsBuilding(false);
    }
  };

  const handleAIGenerate = async () => {
    try {
      const response = await fetch('/api/ai', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message: 'أنشئ هيكل مذكرة ماستر عن اللسانيات الجنائية',
          action: 'generate'
        })
      });
      const data = await response.json();
      if (data.success && data.code) {
        setCode(data.code);
      }
    } catch (error) {
      console.error('AI error:', error);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="min-h-screen pt-16 flex flex-col">
      {/* Toolbar */}
      <div className="border-b border-white/10 bg-dark-navy/50 backdrop-blur p-4">
        <div className="max-w-[1800px] mx-auto flex items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <h1 className="text-xl font-bold gradient-text">🖊️ محرر Qalam</h1>
          </div>
          
          <div className="flex items-center gap-2">
            <button
              onClick={handleAIGenerate}
              className="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg flex items-center gap-2 transition-all"
            >
              <MessageSquare size={18} />
              <span className="hidden sm:inline">توليد بالذكاء الاصطناعي</span>
            </button>
            
            <button
              onClick={handleCopy}
              className="px-4 py-2 border border-white/20 hover:bg-white/10 rounded-lg flex items-center gap-2 transition-all"
            >
              {copied ? <Check size={18} className="text-green-500" /> : <Copy size={18} />}
              <span className="hidden sm:inline">نسخ</span>
            </button>
            
            <div className="h-6 w-px bg-white/20"></div>
            
            <button
              onClick={() => handleBuild('pdf')}
              disabled={isBuilding}
              className="px-4 py-2 bg-red-600 hover:bg-red-700 disabled:opacity-50 rounded-lg flex items-center gap-2 transition-all"
            >
              <FileText size={18} />
              <span className="hidden sm:inline">PDF</span>
            </button>
            
            <button
              onClick={() => handleBuild('word')}
              disabled={isBuilding}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 rounded-lg flex items-center gap-2 transition-all"
            >
              <Code2 size={18} />
              <span className="hidden sm:inline">Word</span>
            </button>
            
            <button
              onClick={() => handleBuild('all')}
              disabled={isBuilding}
              className="px-6 py-2 bg-gold hover:bg-yellow-500 text-dark-navy font-bold rounded-lg flex items-center gap-2 transition-all"
            >
              {isBuilding ? <Loader2 className="animate-spin" size={18} /> : <Play size={18} />}
              <span>بناء الكل</span>
            </button>
          </div>
        </div>
      </div>

      {/* Main Editor Area */}
      <div className="flex-1 grid md:grid-cols-2 gap-0 overflow-hidden">
        {/* Code Editor */}
        <div className="border-l border-white/10 flex flex-col">
          <div className="p-2 bg-[#2d2d2d] flex items-center justify-between">
            <span className="text-sm text-gray-400">memoire.qlm</span>
            <span className="text-xs text-gray-500">Qalam Language</span>
          </div>
          <Editor
            height="calc(100vh - 200px)"
            language="yaml"
            theme="vs-dark"
            value={code}
            onChange={(value) => setCode(value || '')}
            onMount={(editor) => {
              editorRef.current = editor;
            }}
            options={{
              fontSize: 14,
              minimap: { enabled: false },
              scrollBeyondLastLine: false,
              automaticLayout: true,
              wordWrap: 'on',
              padding: { top: 16, bottom: 16 },
              fontFamily: 'Consolas, Monaco, monospace',
              direction: 'ltr'
            }}
          />
        </div>

        {/* Preview/Output Panel */}
        <div className="bg-[#1e1e1e] flex flex-col">
          <div className="p-2 bg-[#2d2d2d] border-b border-white/10">
            <span className="text-sm text-gray-400">📋 سجل العمليات</span>
          </div>
          <div className="flex-1 p-4 overflow-auto font-mono text-sm">
            {output ? (
              <pre className="whitespace-pre-wrap text-gray-300">{output}</pre>
            ) : (
              <div className="text-gray-500 text-center mt-20">
                <Play size={48} className="mx-auto mb-4 opacity-50" />
                <p>اضغط على &quot;بناء الكل&quot; لبدء البناء</p>
                <p className="text-xs mt-2">أو استخدم الذكاء الاصطناعي لتوليد محتوى تلقائياً</p>
              </div>
            )}
          </div>
          
          {/* Quick Tips */}
          <div className="p-4 bg-dark-navy/50 border-t border-white/10">
            <h4 className="font-bold text-gold mb-2">💡 نصائح سريعة:</h4>
            <ul className="text-xs text-gray-400 space-y-1 arabic-text">
              <li>• @@ ... @@ للبيانات الوصفية</li>
              <li>• === عنوان === للفصول</li>
              <li>• --- عنوان --- للأقسام</li>
              <li>• {{ نوع }} ... {{ /نوع }} للبيئات</li>
              <li>• F5 للبناء السريع</li>
            </ul>
          </div>
        </div>
      </div>

      {/* AI Chat Panel (Collapsible) */}
      {showAI && (
        <div className="fixed bottom-0 right-0 w-96 h-[500px] bg-dark-navy border-t border-l border-white/20 shadow-2xl rounded-tl-2xl z-50">
          <div className="p-4 border-b border-white/10 flex items-center justify-between">
            <h3 className="font-bold flex items-center gap-2">
              <MessageSquare size={20} className="text-gold" />
              مساعد قلم الذكي
            </h3>
            <button onClick={() => setShowAI(false)} className="text-gray-400 hover:text-white">×</button>
          </div>
          <div className="p-4 h-[calc(100%-120px)] overflow-auto">
            <p className="text-gray-400 text-sm">اكتب طلبك وسأقوم بإنشاء ملف .qlm كامل...</p>
          </div>
          <div className="p-4 border-t border-white/10">
            <input
              type="text"
              placeholder="مثال: أنشئ مذكرة عن الذكاء الاصطناعي..."
              className="w-full px-4 py-2 bg-white/5 border border-white/20 rounded-lg focus:outline-none focus:border-gold text-white"
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  handleAIGenerate();
                }
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
}
