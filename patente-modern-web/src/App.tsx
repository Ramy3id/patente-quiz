import { useState, useEffect, useCallback, useMemo } from 'react';
import { 
  Car, 
  CheckCircle2, 
  XCircle, 
  Clock, 
  Sparkles, 
  BookOpen, 
  RotateCcw, 
  ShieldCheck, 
  Volume2, 
  VolumeX, 
  Languages, 
  Layers, 
  TrendingUp, 
  Play, 
  Search, 
  Eye, 
  EyeOff, 
  Check, 
  X,
  FileText
} from 'lucide-react';
import confetti from 'canvas-confetti';
import { sound } from './lib/sound.ts';

// Question Type definition
export interface QuizQuestion {
  img?: string;
  q: string;
  a: boolean;
  topic?: string;
  subtopic?: string;
}

// Chapter metadata definition
interface ChapterMeta {
  id: string;
  num: number;
  title_it: string;
  title_ar: string;
}

const CHAPTERS: ChapterMeta[] = [
  { id: 'definizioni-generali-doveri-strada', num: 1, title_it: 'Definizioni generali e doveri della strada', title_ar: 'المفاهيم العامة واستخدام الطريق' },
  { id: 'segnali-pericolo', num: 2, title_it: 'Segnali di pericolo', title_ar: 'إشارات الخطر' },
  { id: 'segnali-divieto', num: 3, title_it: 'Segnali di divieto', title_ar: 'إشارات المنع' },
  { id: 'segnali-obbligo', num: 4, title_it: 'Segnali di obbligo', title_ar: 'إشارات الإلزام' },
  { id: 'segnali-precedenza', num: 5, title_it: 'Segnali di precedenza', title_ar: 'إشارات الأسبقية' },
  { id: 'segnaletica-orizzontale-ostacoli', num: 6, title_it: 'Segnaletica orizzontale e ostacoli', title_ar: 'العلامات الأرضية والحواجز' },
  { id: 'semafori-vigili', num: 7, title_it: 'Semafori e vigili', title_ar: 'إشارات المرور الضوئية ورجال الشرطة' },
  { id: 'segnali-indicazione', num: 8, title_it: 'Segnali di indicazione', title_ar: 'إشارات الإرشاد والمعلومات' },
  { id: 'segnali-complementari-cantiere', num: 9, title_it: 'Segnali complementari e cantiere', title_ar: 'الإشارات التكميلية وأعمال الطرق' },
  { id: 'pannelli-integrativi', num: 10, title_it: 'Pannelli integrativi', title_ar: 'اللوحات الإضافية الملحقة' },
  { id: 'limiti-di-velocita', num: 11, title_it: 'Limiti di velocità', title_ar: 'حدود السرعة' },
  { id: 'distanza-di-sicurezza', num: 12, title_it: 'Distanza di sicurezza', title_ar: 'مسافة الأمان' },
  { id: 'norme-di-circolazione', num: 13, title_it: 'Norme di circolazione', title_ar: 'قواعد السير والمرور' },
  { id: 'precedenza-incroci', num: 14, title_it: 'Precedenza agli incroci', title_ar: 'حق الأسبقية في التقاطعات' },
  { id: 'sorpasso', num: 15, title_it: 'Manovra di sorpasso', title_ar: 'مناورة التجاوز' },
  { id: 'fermata-sosta-arresto', num: 16, title_it: 'Fermata, sosta e arresto', title_ar: 'الوقوف والتوقف والانتظار' },
  { id: 'norme-varie-autostrade-pannelli', num: 17, title_it: 'Autostrade e strade extraurbane', title_ar: 'الطرق السريعة وقواعد خاصة' },
  { id: 'luci-dispositivi-acustici', num: 18, title_it: 'Luci e dispositivi acustici', title_ar: 'أضواء المركبة والإشارات الصوتية' },
  { id: 'cinture-casco-sicurezza', num: 19, title_it: 'Cinture, casco e sicurezza', title_ar: 'أحزمة الأمان والخوذة' },
  { id: 'patente-punti-documenti', num: 20, title_it: 'Patente a punti e documenti', title_ar: 'رخصة القيادة بالنقاط والمستندات' },
  { id: 'incidenti-stradali-comportamenti', num: 21, title_it: 'Incidenti stradali e comportamenti', title_ar: 'حوادث السير والتصرفات السليمة' },
  { id: 'alcool-droga-primo-soccorso', num: 22, title_it: 'Alcool, droghe e primo soccorso', title_ar: 'الكحول والمخدرات والإسعافات الأولية' },
  { id: 'responsabilita-civile-penale-e-assicurazione', num: 23, title_it: 'Responsabilità e assicurazione R.C.A.', title_ar: 'المسؤولية القانونية والتأمين الإجباري' },
  { id: 'consumi-ambiente-inquinamento', num: 24, title_it: 'Consumi e tutela ambientale', title_ar: 'استهلاك الوقود وحماية البيئة' },
  { id: 'elementi-veicolo-manutenzione-comportamenti', num: 25, title_it: 'Manutenzione del veicolo', title_ar: 'مكونات المركبة وصيانتها' },
];

export default function App() {
  const [activeTab, setActiveTab] = useState<'dashboard' | 'study' | 'exam'>('dashboard');
  const [soundEnabled, setSoundEnabled] = useState(true);
  const [arabicMode, setArabicMode] = useState(false);

  // Full Raw Database
  const [fullDb, setFullDb] = useState<Record<string, Record<string, QuizQuestion[]>>>({});
  const [allQuestionsPool, setAllQuestionsPool] = useState<QuizQuestion[]>([]);

  // Interactive Speed Calculator state
  const [speed, setSpeed] = useState<number>(90);
  const [cardFlipped, setCardFlipped] = useState(false);

  // Study Mode State
  const [selectedChapterId, setSelectedChapterId] = useState<string>(CHAPTERS[0].id);
  const [studyFilter, setStudyFilter] = useState<'all' | 'true' | 'false'>('all');
  const [studySearch, setStudySearch] = useState('');
  const [memorizeMode, setMemorizeMode] = useState(false);
  const [studyAnswers, setStudyAnswers] = useState<Record<string, boolean>>({});

  // Exam state
  const [examQuestions, setExamQuestions] = useState<QuizQuestion[]>([]);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [userAnswers, setUserAnswers] = useState<Record<number, boolean>>({});
  const [examSubmitted, setExamSubmitted] = useState(false);
  const [timeLeft, setTimeLeft] = useState(20 * 60);
  const [isTimerRunning, setIsTimerRunning] = useState(false);

  // Audio helper
  const triggerSound = useCallback((type: 'click' | 'correct' | 'wrong') => {
    if (!soundEnabled) return;
    if (type === 'click') sound.click();
    if (type === 'correct') sound.correct();
    if (type === 'wrong') sound.wrong();
  }, [soundEnabled]);

  // Load database once
  useEffect(() => {
    fetch('/quizPatenteB2023.json')
      .then(res => res.json())
      .then((data: Record<string, Record<string, QuizQuestion[]>>) => {
        setFullDb(data);
        const pool: QuizQuestion[] = [];
        Object.keys(data).forEach(cat => {
          const sub = data[cat];
          if (typeof sub === 'object' && sub !== null) {
            Object.keys(sub).forEach(subCat => {
              const list = sub[subCat];
              if (Array.isArray(list)) {
                list.forEach(item => {
                  pool.push({
                    q: item.q,
                    a: item.a,
                    img: item.img,
                    topic: cat,
                    subtopic: subCat.replace(/-/g, ' ')
                  });
                });
              }
            });
          }
        });
        setAllQuestionsPool(pool);
        // Prepare initial exam sample
        if (pool.length > 0) {
          const shuffled = [...pool].sort(() => 0.5 - Math.random()).slice(0, 30);
          setExamQuestions(shuffled);
        }
      })
      .catch(err => {
        console.warn('Fallback: could not load full database', err);
      });
  }, []);

  // Timer countdown
  useEffect(() => {
    let interval: ReturnType<typeof setInterval>;
    if (isTimerRunning && timeLeft > 0 && !examSubmitted) {
      interval = setInterval(() => {
        setTimeLeft(prev => {
          if (prev <= 1) {
            setExamSubmitted(true);
            setIsTimerRunning(false);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isTimerRunning, timeLeft, examSubmitted]);

  // Exam keyboard shortcuts (V, F, Arrows)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (activeTab !== 'exam' || examSubmitted) return;
      if (e.key.toLowerCase() === 'v') {
        handleExamAnswer(true);
      } else if (e.key.toLowerCase() === 'f') {
        handleExamAnswer(false);
      } else if (e.key === 'ArrowRight') {
        if (currentIdx < examQuestions.length - 1) setCurrentIdx(c => c + 1);
      } else if (e.key === 'ArrowLeft') {
        if (currentIdx > 0) setCurrentIdx(c => c - 1);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [activeTab, examSubmitted, currentIdx, examQuestions.length]);

  const handleExamAnswer = (ans: boolean) => {
    triggerSound('click');
    setUserAnswers(prev => ({ ...prev, [currentIdx]: ans }));
    if (currentIdx < examQuestions.length - 1) {
      setCurrentIdx(prev => prev + 1);
    }
  };

  const startExam = () => {
    triggerSound('click');
    if (allQuestionsPool.length > 0) {
      const shuffled = [...allQuestionsPool].sort(() => 0.5 - Math.random()).slice(0, 30);
      setExamQuestions(shuffled);
    }
    setUserAnswers({});
    setCurrentIdx(0);
    setTimeLeft(20 * 60);
    setExamSubmitted(false);
    setIsTimerRunning(true);
    setActiveTab('exam');
  };

  const submitExam = () => {
    triggerSound('click');
    setExamSubmitted(true);
    setIsTimerRunning(false);
    
    let errors = 0;
    examQuestions.forEach((q, idx) => {
      const userAns = userAnswers[idx];
      if (userAns !== q.a) errors++;
    });

    if (errors <= 3) {
      triggerSound('correct');
      confetti({
        particleCount: 120,
        spread: 80,
        origin: { y: 0.6 }
      });
    } else {
      triggerSound('wrong');
    }
  };

  // Speed calculation
  const reactionDist = Math.round((speed / 10) * 3);
  const brakingDist = Math.round(Math.pow(speed / 10, 2) * 0.6);
  const totalStoppingDist = reactionDist + brakingDist;

  // Selected Chapter Questions
  const currentChapterQuestions = useMemo(() => {
    const chapterData = fullDb[selectedChapterId];
    if (!chapterData) return [];
    const list: QuizQuestion[] = [];
    Object.keys(chapterData).forEach(subCat => {
      const subList = chapterData[subCat];
      if (Array.isArray(subList)) {
        subList.forEach(item => {
          list.push({
            q: item.q,
            a: item.a,
            img: item.img,
            subtopic: subCat.replace(/-/g, ' ')
          });
        });
      }
    });
    return list;
  }, [fullDb, selectedChapterId]);

  // Filtered Chapter Questions
  const filteredChapterQuestions = useMemo(() => {
    return currentChapterQuestions.filter(q => {
      if (studyFilter === 'true' && !q.a) return false;
      if (studyFilter === 'false' && q.a) return false;
      if (studySearch.trim()) {
        const query = studySearch.toLowerCase();
        return q.q.toLowerCase().includes(query) || (q.subtopic && q.subtopic.toLowerCase().includes(query));
      }
      return true;
    });
  }, [currentChapterQuestions, studyFilter, studySearch]);

  const activeChapterInfo = CHAPTERS.find(c => c.id === selectedChapterId) || CHAPTERS[0];

  // Exam stats computation
  const answeredCount = Object.keys(userAnswers).length;
  const errorCount = useMemo(() => {
    if (!examSubmitted) return 0;
    return examQuestions.reduce((acc, q, idx) => {
      return userAnswers[idx] !== q.a ? acc + 1 : acc;
    }, 0);
  }, [examSubmitted, examQuestions, userAnswers]);
  const isPassed = examSubmitted && errorCount <= 3;

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 bg-grain selection:bg-emerald-500/20 selection:text-emerald-300 flex flex-col font-sans">
      
      {/* Top Navbar */}
      <header className="sticky top-0 z-40 border-b border-white/[0.07] bg-zinc-950/85 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-700 flex items-center justify-center shadow-lg shadow-emerald-950/40 border border-emerald-400/30">
              <Car className="h-5 w-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-extrabold tracking-tight text-lg text-white">PATENTE B</span>
                <span className="text-[11px] font-mono tracking-wider px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-semibold">
                  PRO SUITE
                </span>
              </div>
              <p className="text-xs text-zinc-400 hidden sm:block">
                Standard Ministeriali 2024/2026 • Design Engineering Architecture
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            {/* Audio Toggle */}
            <button 
              onClick={() => { triggerSound('click'); setSoundEnabled(!soundEnabled); }}
              className="p-2 rounded-lg text-zinc-400 hover:text-white hover:bg-zinc-900 border border-transparent hover:border-zinc-800 interactive-tactile"
              title={soundEnabled ? "Mute audio" : "Enable sound"}
            >
              {soundEnabled ? <Volume2 className="h-4 w-4" /> : <VolumeX className="h-4 w-4 text-zinc-600" />}
            </button>

            {/* Arabic / Italian translation toggle */}
            <button 
              onClick={() => { triggerSound('click'); setArabicMode(!arabicMode); }}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1.5 border interactive-tactile ${
                arabicMode 
                  ? 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30' 
                  : 'bg-zinc-900 text-zinc-400 border-zinc-800 hover:text-white'
              }`}
            >
              <Languages className="h-3.5 w-3.5" />
              <span>{arabicMode ? 'عربي / IT' : 'Italiano'}</span>
            </button>

            {/* Main Navigation Tabs */}
            <div className="hidden md:flex items-center p-1 bg-zinc-900/90 rounded-xl border border-white/[0.08]">
              <button 
                onClick={() => { triggerSound('click'); setActiveTab('dashboard'); }}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                  activeTab === 'dashboard' ? 'bg-zinc-800 text-white shadow-sm' : 'text-zinc-400 hover:text-zinc-200'
                }`}
              >
                {arabicMode ? 'لوحة القيادة' : 'Panoramica'}
              </button>
              <button 
                onClick={() => { triggerSound('click'); setActiveTab('study'); }}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-all ${
                  activeTab === 'study' ? 'bg-zinc-800 text-white shadow-sm' : 'text-zinc-400 hover:text-zinc-200'
                }`}
              >
                <BookOpen className="h-3.5 w-3.5" />
                <span>{arabicMode ? 'مذاكرة الأبواب (25 باب)' : 'Studio Capitoli'}</span>
              </button>
              <button 
                onClick={startExam}
                className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all ${
                  activeTab === 'exam' 
                    ? 'bg-emerald-600 text-white shadow-md shadow-emerald-950/40' 
                    : 'bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20'
                }`}
              >
                <Play className="h-3 w-3 fill-current" />
                <span>{arabicMode ? 'محاكاة الامتحان' : 'Simulatore'}</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content View Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* ======================================================== */}
        {/* VIEW 1: DASHBOARD & BENTO LAB */}
        {/* ======================================================== */}
        {activeTab === 'dashboard' && (
          <div className="space-y-10 animate-fadeIn">
            {/* Hero Section */}
            <div className="relative rounded-3xl overflow-hidden border border-white/[0.08] card-surface p-8 sm:p-12">
              <div className="absolute top-0 right-0 -mr-20 -mt-20 w-96 h-96 rounded-full bg-emerald-500/[0.05] blur-3xl pointer-events-none" />
              <div className="max-w-2xl relative z-10 space-y-5">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-zinc-800/80 border border-white/10 text-xs text-zinc-300">
                  <Sparkles className="h-3.5 w-3.5 text-emerald-400" />
                  <span>{arabicMode ? 'المنظومة الشاملة لرخصة القيادة الإيطالية' : 'Suite Ministeriale Ufficiale 2024/2026'}</span>
                </div>

                <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-white leading-tight">
                  {arabicMode ? (
                    <>استعد لاجتياز رخصة القيادة <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-300">بدقة واحترافية</span></>
                  ) : (
                    <>Supera la Patente B con la precisione di un <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-300">Design Engineer</span></>
                  )}
                </h1>

                <p className="text-zinc-400 text-sm sm:text-base leading-relaxed">
                  {arabicMode ? (
                    'واجهة موحدة تجمع بين المذاكرة الشاملة لكافة الأبواب الـ 25 (7,140 سؤالاً)، ومحاكاة الامتحان الوزاري الحقيقي في 20 دقيقة، مع استجابة فيزيائية وردود فعل صوتية واقعية.'
                  ) : (
                    'Architettura ad alta fedeltà con i 25 capitoli completi, simulatore d\'esame ufficiale in 20 minuti, calcolatore dinamico di arresto e zero template generici AI.'
                  )}
                </p>

                <div className="pt-2 flex flex-wrap items-center gap-4">
                  <button 
                    onClick={startExam}
                    className="px-6 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-zinc-950 font-bold text-sm flex items-center gap-2.5 shadow-lg shadow-emerald-500/20 interactive-tactile"
                  >
                    <Play className="h-4 w-4 fill-current" />
                    <span>{arabicMode ? 'بدء محاكاة الاختبار الرسمي' : 'Inizia Simulazione Ministeriale'}</span>
                    <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-zinc-950/20 text-zinc-950 font-bold ml-1">30 Quiz</span>
                  </button>

                  <button 
                    onClick={() => { triggerSound('click'); setActiveTab('study'); }}
                    className="px-5 py-3 rounded-xl bg-zinc-900 hover:bg-zinc-800 text-zinc-200 border border-zinc-800 hover:border-zinc-700 text-sm font-medium flex items-center gap-2 interactive-tactile"
                  >
                    <BookOpen className="h-4 w-4 text-emerald-400" />
                    <span>{arabicMode ? 'مذاكرة الأبواب الـ 25' : 'Studio per Capitolo'}</span>
                  </button>
                </div>
              </div>
            </div>

            {/* Quick Metrics Strip */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="card-surface p-5 rounded-2xl border border-white/[0.08]">
                <div className="flex items-center justify-between text-zinc-400 text-xs mb-2">
                  <span>{arabicMode ? 'قاعدة الأسئلة' : 'Database Ufficiale'}</span>
                  <BookOpen className="h-4 w-4 text-emerald-400" />
                </div>
                <div className="text-2xl font-bold font-mono tracking-tight text-white">7,140+</div>
                <div className="text-xs text-zinc-500 mt-1">{arabicMode ? 'سؤال وزاري مقسم' : 'Tutti i 25 capitoli'}</div>
              </div>

              <div className="card-surface p-5 rounded-2xl border border-white/[0.08]">
                <div className="flex items-center justify-between text-zinc-400 text-xs mb-2">
                  <span>{arabicMode ? 'الأبواب التعليمية' : 'Capitoli di Teoria'}</span>
                  <Layers className="h-4 w-4 text-teal-400" />
                </div>
                <div className="text-2xl font-bold font-mono tracking-tight text-white">25</div>
                <div className="text-xs text-zinc-500 mt-1">{arabicMode ? 'باباً شاملاً مترجماً' : 'Argomenti ministeriali'}</div>
              </div>

              <div className="card-surface p-5 rounded-2xl border border-white/[0.08]">
                <div className="flex items-center justify-between text-zinc-400 text-xs mb-2">
                  <span>{arabicMode ? 'وقت الامتحان' : 'Tempo Ufficiale'}</span>
                  <Clock className="h-4 w-4 text-indigo-400" />
                </div>
                <div className="text-2xl font-bold font-mono tracking-tight text-white">20:00</div>
                <div className="text-xs text-zinc-500 mt-1">{arabicMode ? '30 سؤالاً • Max 3 أخطاء' : 'Idoneo con ≤ 3 errori'}</div>
              </div>

              <div className="card-surface p-5 rounded-2xl border border-white/[0.08]">
                <div className="flex items-center justify-between text-zinc-400 text-xs mb-2">
                  <span>{arabicMode ? 'الإشارات المرورية' : 'Cartelli e Segnali'}</span>
                  <FileText className="h-4 w-4 text-amber-400" />
                </div>
                <div className="text-2xl font-bold font-mono tracking-tight text-white">413</div>
                <div className="text-xs text-zinc-500 mt-1">{arabicMode ? 'صورة إشارة ملحقة' : 'Segnali ad alta risoluzione'}</div>
              </div>
            </div>

            {/* Bento Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
              {/* 2-col card: Braking distance */}
              <div className="md:col-span-2 card-surface p-6 rounded-2xl border border-white/[0.08] space-y-5">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                      <TrendingUp className="h-4 w-4" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-white text-sm">
                        {arabicMode ? 'حاسبة مسافة التوقف الحقيقية (Spazio di Frenata)' : 'Calcolatore Spazio Totale di Arresto'}
                      </h3>
                      <p className="text-xs text-zinc-400">{arabicMode ? 'معادلة فيزيائية تحسب زمن رد الفعل ومسافة الفرملة' : 'Reazione + Frenata su asfalto asciutto'}</p>
                    </div>
                  </div>
                  <span className="text-lg font-mono font-bold text-emerald-400 px-3 py-1 bg-zinc-900 rounded-lg border border-zinc-800">
                    {speed} km/h
                  </span>
                </div>

                <div className="space-y-2">
                  <input 
                    type="range" 
                    min="30" 
                    max="150" 
                    step="10"
                    value={speed}
                    onChange={(e) => {
                      triggerSound('click');
                      setSpeed(Number(e.target.value));
                    }}
                    className="w-full h-2 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-emerald-500"
                  />
                  <div className="flex justify-between text-[11px] font-mono text-zinc-500">
                    <span>30 km/h</span>
                    <span>50 km/h (Città)</span>
                    <span>90 km/h (Extraurbana)</span>
                    <span>130 km/h (Autostrada)</span>
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-3 pt-2">
                  <div className="bg-zinc-900/80 p-3.5 rounded-xl border border-white/[0.05]">
                    <div className="text-[11px] text-zinc-400">{arabicMode ? 'مسافة رد الفعل' : 'Spazio Reazione (1s)'}</div>
                    <div className="text-xl font-bold font-mono text-zinc-200 mt-1">{reactionDist} m</div>
                  </div>
                  <div className="bg-zinc-900/80 p-3.5 rounded-xl border border-white/[0.05]">
                    <div className="text-[11px] text-zinc-400">{arabicMode ? 'مسافة الفرملة' : 'Spazio Frenata'}</div>
                    <div className="text-xl font-bold font-mono text-zinc-200 mt-1">{brakingDist} m</div>
                  </div>
                  <div className="bg-emerald-500/10 p-3.5 rounded-xl border border-emerald-500/20">
                    <div className="text-[11px] text-emerald-400 font-medium">{arabicMode ? 'المجموع الكلي' : 'Arresto Totale'}</div>
                    <div className="text-xl font-bold font-mono text-emerald-300 mt-1">{totalStoppingDist} m</div>
                  </div>
                </div>
              </div>

              {/* 1-col card: 3D Flip Card */}
              <div 
                onClick={() => {
                  triggerSound('click');
                  setCardFlipped(!cardFlipped);
                }}
                className="card-surface p-6 rounded-2xl border border-white/[0.08] flex flex-col justify-between cursor-pointer interactive-tactile group relative"
              >
                <div className="flex items-center justify-between text-xs text-zinc-400">
                  <span className="font-mono text-emerald-400">#Segnale Ministeriale</span>
                  <RotateCcw className="h-3.5 w-3.5 text-zinc-500 group-hover:rotate-180 transition-transform duration-300" />
                </div>

                <div className="py-4 flex flex-col items-center justify-center text-center">
                  {!cardFlipped ? (
                    <>
                      <div className="h-28 w-28 bg-white/5 rounded-2xl p-2 flex items-center justify-center border border-white/10 mb-3 shadow-inner">
                        <img 
                          src="/img_sign/2.png" 
                          alt="Segnale" 
                          className="max-h-full max-w-full object-contain"
                          onError={(e) => { (e.target as HTMLElement).style.display = 'none'; }}
                        />
                      </div>
                      <h4 className="font-bold text-white text-sm">Strada Deformata</h4>
                      <p className="text-xs text-zinc-400 mt-1">{arabicMode ? 'انقر لقلب البطاقة وكشف الفخاخ الامتحانية' : 'Clicca per vedere la regola del quiz'}</p>
                    </>
                  ) : (
                    <div className="space-y-2">
                      <div className="inline-block px-2 py-0.5 rounded text-[10px] font-mono bg-amber-500/20 text-amber-300 border border-amber-500/30">
                        ATTENZIONE TRABOCCHETTO
                      </div>
                      <p className="text-xs text-zinc-200 leading-relaxed">
                        {arabicMode ? (
                          'الخطأ الشائع: Segnale di pericolo يوضع قبل 150 متراً، ولا يعني طريقاً زلقاً بالمطر بل طريقاً به هبوط وتلف في السطح.'
                        ) : (
                          'Preannuncia un tratto di strada con fondo irregolare o dissestato. Non confondere con strada scivolosa.'
                        )}
                      </p>
                    </div>
                  )}
                </div>

                <div className="pt-2 border-t border-white/[0.06] text-[11px] text-zinc-500 flex justify-between">
                  <span>{cardFlipped ? 'Regola esame' : 'Tocca per girare'}</span>
                  <span className="font-mono text-zinc-400">Art. 85 CdS</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ======================================================== */}
        {/* VIEW 2: STUDY MODE BY TOPIC / CHAPTER (25 CHAPTERS) */}
        {/* ======================================================== */}
        {activeTab === 'study' && (
          <div className="flex flex-col lg:flex-row gap-6 animate-fadeIn">
            {/* Left Sidebar: 25 Chapters */}
            <div className="lg:w-80 flex-shrink-0 card-surface rounded-2xl border border-white/[0.08] p-4 flex flex-col h-[750px]">
              <div className="pb-3 border-b border-white/[0.07] mb-3">
                <h3 className="font-bold text-white text-sm flex items-center gap-2">
                  <BookOpen className="h-4 w-4 text-emerald-400" />
                  <span>{arabicMode ? 'أبواب المذاكرة (25 باب)' : 'Capitoli Ufficiali (25)'}</span>
                </h3>
                <p className="text-[11px] text-zinc-400 mt-0.5">
                  {arabicMode ? 'اختر الباب لدراسة أسئلته كاملة' : 'Seleziona un argomento ministeriale'}
                </p>
              </div>

              {/* Scrollable Chapter list */}
              <div className="flex-1 overflow-y-auto space-y-1.5 pr-1">
                {CHAPTERS.map(ch => {
                  const isSelected = ch.id === selectedChapterId;
                  return (
                    <button
                      key={ch.id}
                      onClick={() => {
                        triggerSound('click');
                        setSelectedChapterId(ch.id);
                      }}
                      className={`w-full text-left p-2.5 rounded-xl border text-xs transition-all interactive-tactile ${
                        isSelected 
                          ? 'bg-emerald-500/15 border-emerald-500/40 text-emerald-200 font-semibold' 
                          : 'bg-zinc-900/60 border-zinc-800/80 text-zinc-400 hover:text-white hover:bg-zinc-800/60'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-mono text-[10px] text-zinc-500">Cap. {ch.num.toString().padStart(2, '0')}</span>
                        {isSelected && <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />}
                      </div>
                      <div className="font-medium text-zinc-200 mt-1 line-clamp-1">{ch.title_it}</div>
                      {arabicMode && (
                        <div className="text-[11px] text-zinc-400 mt-0.5 text-right font-sans">{ch.title_ar}</div>
                      )}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Right Area: Questions in Selected Chapter */}
            <div className="flex-1 card-surface rounded-2xl border border-white/[0.08] p-6 flex flex-col h-[750px]">
              {/* Header & Controls */}
              <div className="pb-4 border-b border-white/[0.07] space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div>
                    <div className="text-xs font-mono text-emerald-400 font-medium">
                      CAPITOLO {activeChapterInfo.num} DI 25
                    </div>
                    <h2 className="text-lg font-bold text-white mt-0.5">
                      {activeChapterInfo.title_it}
                    </h2>
                    {arabicMode && (
                      <p className="text-xs text-zinc-400 mt-0.5 text-right">
                        {activeChapterInfo.title_ar}
                      </p>
                    )}
                  </div>

                  {/* Memorize Mode Toggle */}
                  <button 
                    onClick={() => {
                      triggerSound('click');
                      setMemorizeMode(!memorizeMode);
                    }}
                    className={`px-3 py-1.5 rounded-xl text-xs font-medium flex items-center gap-2 border interactive-tactile ${
                      memorizeMode 
                        ? 'bg-amber-500/15 text-amber-300 border-amber-500/30' 
                        : 'bg-zinc-900 text-zinc-400 border-zinc-800 hover:text-white'
                    }`}
                  >
                    {memorizeMode ? <Eye className="h-3.5 w-3.5" /> : <EyeOff className="h-3.5 w-3.5" />}
                    <span>{arabicMode ? 'وضع الحفظ (كشف الإجابات)' : 'Modalità Studio'}</span>
                  </button>
                </div>

                {/* Filter & Search Bar */}
                <div className="flex flex-wrap items-center gap-3">
                  <div className="relative flex-1 min-w-[200px]">
                    <Search className="h-4 w-4 absolute left-3 top-2.5 text-zinc-500" />
                    <input 
                      type="text" 
                      placeholder={arabicMode ? 'بحث في أسئلة هذا الباب...' : 'Cerca tra le domande del capitolo...'}
                      value={studySearch}
                      onChange={(e) => setStudySearch(e.target.value)}
                      className="w-full bg-zinc-900 border border-zinc-800 rounded-xl pl-9 pr-3 py-1.5 text-xs text-white placeholder-zinc-500 focus:outline-none focus:border-emerald-500/50"
                    />
                  </div>

                  <div className="flex items-center p-1 bg-zinc-900 rounded-xl border border-zinc-800">
                    <button 
                      onClick={() => { triggerSound('click'); setStudyFilter('all'); }}
                      className={`px-3 py-1 rounded-lg text-xs font-medium ${studyFilter === 'all' ? 'bg-zinc-800 text-white' : 'text-zinc-400'}`}
                    >
                      {arabicMode ? 'الكل' : 'Tutti'} ({currentChapterQuestions.length})
                    </button>
                    <button 
                      onClick={() => { triggerSound('click'); setStudyFilter('true'); }}
                      className={`px-3 py-1 rounded-lg text-xs font-medium ${studyFilter === 'true' ? 'bg-emerald-500/20 text-emerald-300' : 'text-zinc-400'}`}
                    >
                      VERO
                    </button>
                    <button 
                      onClick={() => { triggerSound('click'); setStudyFilter('false'); }}
                      className={`px-3 py-1 rounded-lg text-xs font-medium ${studyFilter === 'false' ? 'bg-rose-500/20 text-rose-300' : 'text-zinc-400'}`}
                    >
                      FALSO
                    </button>
                  </div>
                </div>
              </div>

              {/* Scrollable Questions list */}
              <div className="flex-1 overflow-y-auto py-4 space-y-4 pr-2">
                {filteredChapterQuestions.length === 0 ? (
                  <div className="text-center py-20 text-zinc-500 text-xs">
                    {arabicMode ? 'لا توجد أسئلة تطابق بحثك في هذا الباب.' : 'Nessuna domanda trovata per questo filtro.'}
                  </div>
                ) : (
                  filteredChapterQuestions.map((q, idx) => {
                    const qKey = `${selectedChapterId}-${idx}`;
                    const answered = studyAnswers[qKey];
                    const isAnswered = answered !== undefined;
                    const isCorrectAnswer = isAnswered && answered === q.a;

                    return (
                      <div 
                        key={idx}
                        className="bg-zinc-900/60 border border-white/[0.06] rounded-2xl p-4 flex flex-col sm:flex-row gap-4 items-start interactive-tactile"
                      >
                        {/* Traffic Sign Image if present */}
                        {q.img && (
                          <div className="h-20 w-20 flex-shrink-0 bg-zinc-950/80 rounded-xl p-2 border border-white/10 flex items-center justify-center">
                            <img 
                              src={q.img} 
                              alt="Segnale" 
                              className="max-h-full max-w-full object-contain"
                              onError={(e) => { (e.target as HTMLElement).style.display = 'none'; }}
                            />
                          </div>
                        )}

                        <div className="flex-1 space-y-3">
                          <div className="flex items-center justify-between text-[11px] text-zinc-500">
                            <span className="font-mono text-zinc-400">#Quesito {idx + 1}</span>
                            {q.subtopic && (
                              <span className="px-2 py-0.5 rounded bg-zinc-800 text-zinc-300 font-medium">
                                {q.subtopic}
                              </span>
                            )}
                          </div>

                          <p className="text-sm font-medium text-zinc-100 leading-relaxed">
                            "{q.q}"
                          </p>

                          {/* Action Buttons or Memorize Badge */}
                          {memorizeMode ? (
                            <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-mono font-bold border" style={{
                              backgroundColor: q.a ? 'rgba(16, 185, 129, 0.15)' : 'rgba(244, 63, 94, 0.15)',
                              borderColor: q.a ? 'rgba(16, 185, 129, 0.3)' : 'rgba(244, 63, 94, 0.3)',
                              color: q.a ? '#34d399' : '#fb7185'
                            }}>
                              {q.a ? <Check className="h-3.5 w-3.5" /> : <X className="h-3.5 w-3.5" />}
                              <span>RISPOSTA: {q.a ? 'VERO' : 'FALSO'}</span>
                            </div>
                          ) : (
                            <div className="flex items-center gap-3">
                              <button
                                disabled={isAnswered}
                                onClick={() => {
                                  triggerSound(q.a === true ? 'correct' : 'wrong');
                                  setStudyAnswers(prev => ({ ...prev, [qKey]: true }));
                                }}
                                className={`px-4 py-1.5 rounded-xl text-xs font-bold font-mono border interactive-tactile ${
                                  isAnswered
                                    ? q.a === true
                                      ? 'bg-emerald-500 text-zinc-950 border-emerald-400'
                                      : answered === true
                                        ? 'bg-rose-500 text-white border-rose-400'
                                        : 'bg-zinc-800 text-zinc-500 border-zinc-700'
                                    : 'bg-zinc-800 hover:bg-emerald-500/20 text-zinc-200 hover:text-emerald-300 border-zinc-700'
                                }`}
                              >
                                VERO
                              </button>

                              <button
                                disabled={isAnswered}
                                onClick={() => {
                                  triggerSound(q.a === false ? 'correct' : 'wrong');
                                  setStudyAnswers(prev => ({ ...prev, [qKey]: false }));
                                }}
                                className={`px-4 py-1.5 rounded-xl text-xs font-bold font-mono border interactive-tactile ${
                                  isAnswered
                                    ? q.a === false
                                      ? 'bg-emerald-500 text-zinc-950 border-emerald-400'
                                      : answered === false
                                        ? 'bg-rose-500 text-white border-rose-400'
                                        : 'bg-zinc-800 text-zinc-500 border-zinc-700'
                                    : 'bg-zinc-800 hover:bg-rose-500/20 text-zinc-200 hover:text-rose-300 border-zinc-700'
                                }`}
                              >
                                FALSO
                              </button>

                              {isAnswered && (
                                <span className={`text-xs font-bold flex items-center gap-1 ${
                                  isCorrectAnswer ? 'text-emerald-400' : 'text-rose-400'
                                }`}>
                                  {isCorrectAnswer ? (
                                    <>
                                      <CheckCircle2 className="h-3.5 w-3.5" />
                                      <span>Esatto!</span>
                                    </>
                                  ) : (
                                    <>
                                      <XCircle className="h-3.5 w-3.5" />
                                      <span>Errato! Era {q.a ? 'VERO' : 'FALSO'}</span>
                                    </>
                                  )}
                                </span>
                              )}
                            </div>
                          )}
                        </div>
                      </div>
                    );
                  })
                )}
              </div>
            </div>
          </div>
        )}

        {/* ======================================================== */}
        {/* VIEW 3: OFFICIAL EXAM SIMULATION ENGINE */}
        {/* ======================================================== */}
        {activeTab === 'exam' && (
          <div className="space-y-6 max-w-4xl mx-auto animate-fadeIn">
            {/* Exam Header Strip */}
            <div className="card-surface p-4 sm:p-5 rounded-2xl border border-white/[0.08] flex items-center justify-between flex-wrap gap-4">
              <div className="flex items-center gap-3">
                <div className="h-10 w-10 rounded-xl bg-zinc-900 border border-zinc-800 flex items-center justify-center">
                  <ShieldCheck className="h-5 w-5 text-emerald-400" />
                </div>
                <div>
                  <div className="font-bold text-white text-sm flex items-center gap-2">
                    <span>{arabicMode ? 'بطاقة الامتحان الوزاري' : 'Scheda Esame Ufficiale'}</span>
                    <span className="text-xs font-mono text-zinc-400">
                      ({answeredCount}/{examQuestions.length} {arabicMode ? 'إجابات' : 'risposte'})
                    </span>
                  </div>
                  <div className="text-xs text-zinc-400 flex items-center gap-2 mt-0.5">
                    <span>{arabicMode ? 'اختصارات: اضغط [V] للصحيح و [F] للخطأ' : 'Tasti rapidi: [V] Vero • [F] Falso'}</span>
                  </div>
                </div>
              </div>

              {/* Countdown Timer */}
              <div className="flex items-center gap-3">
                <div className={`flex items-center gap-2 px-3 py-1.5 rounded-xl font-mono text-sm font-bold border ${
                  timeLeft < 300 
                    ? 'bg-rose-500/15 text-rose-400 border-rose-500/30 animate-pulse' 
                    : 'bg-zinc-900 text-zinc-200 border-zinc-800'
                }`}>
                  <Clock className="h-4 w-4 text-zinc-400" />
                  <span>
                    {Math.floor(timeLeft / 60).toString().padStart(2, '0')}:
                    {(timeLeft % 60).toString().padStart(2, '0')}
                  </span>
                </div>

                {!examSubmitted ? (
                  <button 
                    onClick={submitExam}
                    className="px-4 py-1.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-zinc-950 font-bold text-xs interactive-tactile"
                  >
                    {arabicMode ? 'تسليم الورقة' : 'Consegna Scheda'}
                  </button>
                ) : (
                  <button 
                    onClick={startExam}
                    className="px-4 py-1.5 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-zinc-200 font-medium text-xs flex items-center gap-1.5 interactive-tactile"
                  >
                    <RotateCcw className="h-3.5 w-3.5" />
                    <span>{arabicMode ? 'إعادة الاختبار' : 'Ricomincia'}</span>
                  </button>
                )}
              </div>
            </div>

            {/* Results Banner if submitted */}
            {examSubmitted && (
              <div className={`p-6 rounded-2xl border ${
                isPassed 
                  ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-200' 
                  : 'bg-rose-500/10 border-rose-500/30 text-rose-200'
              } card-surface space-y-3`}>
                <div className="flex items-center gap-3">
                  {isPassed ? (
                    <CheckCircle2 className="h-7 w-7 text-emerald-400" />
                  ) : (
                    <XCircle className="h-7 w-7 text-rose-400" />
                  )}
                  <div>
                    <h3 className="text-xl font-bold tracking-tight text-white">
                      {isPassed 
                        ? (arabicMode ? 'مبروك! لقد اجتزت الاختبار بنجاح' : 'PROMOSSO! Esame Superato') 
                        : (arabicMode ? 'للأسف! لم تجتز الاختبار هذه المرة' : 'RESPINTO! Troppi Errori')}
                    </h3>
                    <p className="text-xs text-zinc-300 mt-0.5">
                      {arabicMode 
                        ? `لقد ارتكبت ${errorCount} أخطاء (الحد الأقصى المسموح به 3 أخطاء).`
                        : `Hai totalizzato ${errorCount} errori su 30 quiz (massimo consentito: 3).`}
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Question Card */}
            {examQuestions.length > 0 && (
              <div className="card-surface p-6 sm:p-8 rounded-3xl border border-white/[0.08] space-y-6">
                <div className="flex items-center justify-between text-xs text-zinc-400 border-b border-white/[0.06] pb-4">
                  <span className="font-mono text-emerald-400 font-semibold">
                    DOMANDA {currentIdx + 1} / {examQuestions.length}
                  </span>
                  <span className="px-2 py-0.5 rounded bg-zinc-900 border border-zinc-800 text-zinc-300">
                    {examQuestions[currentIdx]?.topic || 'Codice della Strada'}
                  </span>
                </div>

                {/* Road Sign Image */}
                {examQuestions[currentIdx]?.img && (
                  <div className="flex justify-center py-2">
                    <div className="h-36 w-36 bg-zinc-900/90 rounded-2xl p-3 border border-white/10 flex items-center justify-center shadow-lg">
                      <img 
                        src={examQuestions[currentIdx].img} 
                        alt="Segnale Stradale" 
                        className="max-h-full max-w-full object-contain"
                        onError={(e) => { (e.target as HTMLElement).style.display = 'none'; }}
                      />
                    </div>
                  </div>
                )}

                {/* Question Statement */}
                <div className="py-2">
                  <p className="text-lg sm:text-xl font-medium text-white leading-relaxed text-center">
                    "{examQuestions[currentIdx]?.q}"
                  </p>
                </div>

                {/* VERO / FALSO Big Tactile Buttons */}
                <div className="grid grid-cols-2 gap-4 pt-4">
                  <button 
                    onClick={() => handleExamAnswer(true)}
                    className={`py-4 rounded-2xl font-bold text-lg flex flex-col items-center justify-center gap-1 border interactive-tactile ${
                      userAnswers[currentIdx] === true 
                        ? 'bg-emerald-500 text-zinc-950 border-emerald-400 shadow-lg shadow-emerald-500/20' 
                        : 'bg-zinc-900/90 text-emerald-400 border-zinc-800 hover:border-emerald-500/50 hover:bg-emerald-500/10'
                    }`}
                  >
                    <span>VERO</span>
                    <span className="text-[11px] font-mono opacity-70">[V]</span>
                  </button>

                  <button 
                    onClick={() => handleExamAnswer(false)}
                    className={`py-4 rounded-2xl font-bold text-lg flex flex-col items-center justify-center gap-1 border interactive-tactile ${
                      userAnswers[currentIdx] === false 
                        ? 'bg-rose-500 text-white border-rose-400 shadow-lg shadow-rose-500/20' 
                        : 'bg-zinc-900/90 text-rose-400 border-zinc-800 hover:border-rose-500/50 hover:bg-rose-500/10'
                    }`}
                  >
                    <span>FALSO</span>
                    <span className="text-[11px] font-mono opacity-70">[F]</span>
                  </button>
                </div>

                {/* Navigation Pills (1 to 30) */}
                <div className="pt-4 border-t border-white/[0.06] space-y-2">
                  <div className="text-[11px] text-zinc-500 flex justify-between">
                    <span>Mappa rapida quesiti</span>
                    <span>Tocca un numero per saltare</span>
                  </div>
                  <div className="grid grid-cols-10 sm:grid-cols-15 gap-1.5">
                    {examQuestions.map((q, idx) => {
                      const isAnswered = userAnswers[idx] !== undefined;
                      const isCurrent = idx === currentIdx;
                      let badgeColor = 'bg-zinc-900 text-zinc-500 border-zinc-800';
                      
                      if (examSubmitted) {
                        const correct = userAnswers[idx] === q.a;
                        badgeColor = correct 
                          ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40' 
                          : 'bg-rose-500/20 text-rose-300 border-rose-500/40';
                      } else if (isAnswered) {
                        badgeColor = 'bg-zinc-800 text-zinc-200 border-zinc-700';
                      }

                      if (isCurrent) {
                        badgeColor += ' ring-2 ring-emerald-400 ring-offset-2 ring-offset-zinc-950';
                      }

                      return (
                        <button
                          key={idx}
                          onClick={() => {
                            triggerSound('click');
                            setCurrentIdx(idx);
                          }}
                          className={`h-7 rounded-lg text-xs font-mono font-medium border flex items-center justify-center interactive-tactile ${badgeColor}`}
                        >
                          {idx + 1}
                        </button>
                      );
                    })}
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

      </main>

      {/* Footer */}
      <footer className="border-t border-white/[0.06] bg-zinc-950 py-6 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-zinc-500">
          <div>
            Patente B Pro • Design Engineer Architecture • Zero AI Slop.
          </div>
          <div className="flex items-center gap-4">
            <span className="inline-flex items-center gap-1.5 text-zinc-400">
              <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
              <span>Sistema Operativo Locale</span>
            </span>
          </div>
        </div>
      </footer>

    </div>
  );
}
