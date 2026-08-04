'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { subjectsAPI, questionsAPI } from '@/lib/api';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import StudentDashboard from '@/components/StudentDashboard';
import { useAuth } from '@/contexts/AuthContext';

export default function Home() {
  const router = useRouter();
  const { user, loading: authLoading } = useAuth();
  const [subjects, setSubjects] = useState<any[]>([]);
  const [selectedSubject, setSelectedSubject] = useState('');
  const [difficulty, setDifficulty] = useState('');
  const [questionCount, setQuestionCount] = useState(5);
  const [stats, setStats] = useState({
    totalQuestions: 0,
    totalSubjects: 0,
    difficultyStats: [] as any[],
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!authLoading && user && user.role !== 'STUDENT') {
      loadStats();
    } else if (!authLoading) {
      setLoading(false);
    }
  }, [authLoading, user]);

  const loadStats = async () => {
    try {
      const subjectsRes = await subjectsAPI.getAll();
      setSubjects(subjectsRes.data);

      setStats({
        totalSubjects: subjectsRes.data.length || 0,
        totalQuestions: 0,
        difficultyStats: [],
      });

      // 총 문제 수 조회
      try {
        const allQuestionsRes = await questionsAPI.getAll({ limit: 1000 });
        const total = allQuestionsRes.data.length || 0;
        setStats((prev) => ({
          ...prev,
          totalQuestions: total,
        }));
      } catch {
        console.log('전체 문제 조회 실패');
      }
    } catch (error) {
      console.error('통계 로드 실패:', error);
    } finally {
      setLoading(false);
    }
  };

  const startQuiz = (event: React.FormEvent) => {
    event.preventDefault();
    const query = new URLSearchParams({ count: String(questionCount) });
    if (selectedSubject) query.set('subjectId', selectedSubject);
    if (difficulty) query.set('difficulty', difficulty);
    router.push(`/quiz?${query.toString()}`);
  };

  if (authLoading) {
    return (
      <div className="app-shell flex min-h-screen items-center justify-center text-[#6C757D]">
        사용자 정보를 확인하는 중...
      </div>
    );
  }

  if (user?.role === 'STUDENT') {
    return <StudentDashboard />;
  }

  return (
    <div className="app-shell">
      <Navbar />

      {/* Main Content */}
      <main className="page-container py-12">
        <section className="mb-12 overflow-hidden rounded-3xl bg-[#242C34] text-white shadow-lg">
          <div className="grid lg:grid-cols-[1fr_1.1fr]">
            <div className="flex flex-col justify-center p-8 sm:p-12">
              <span className="mb-4 w-fit rounded-full bg-[#21BF06]/15 px-4 py-2 text-sm font-semibold text-[#63E64B]">250개 샘플 문제 등록 완료</span>
              <h1 className="text-3xl font-bold leading-tight sm:text-5xl">원하는 조건으로<br />바로 문제를 출제하세요.</h1>
              <p className="mt-5 max-w-xl text-slate-300">과목과 난이도, 문항 수를 선택하면 문제은행에서 무작위로 출제합니다.</p>
            </div>
            <form onSubmit={startQuiz} className="m-5 rounded-2xl bg-white p-6 text-[#212529] sm:m-8 sm:p-8">
              <h2 className="mb-6 text-2xl font-bold text-[#242C34]">문제 출제 설정</h2>
              <div className="space-y-5">
                <div>
                  <label htmlFor="home-subject" className="mb-2 block text-sm font-semibold">과목</label>
                  <select id="home-subject" className="form-control" value={selectedSubject} onChange={(event) => setSelectedSubject(event.target.value)}>
                    <option value="">전체 과목</option>
                    {subjects.map((subject) => <option key={subject.id} value={subject.id}>{subject.name}</option>)}
                  </select>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="home-difficulty" className="mb-2 block text-sm font-semibold">난이도</label>
                    <select id="home-difficulty" className="form-control" value={difficulty} onChange={(event) => setDifficulty(event.target.value)}>
                      <option value="">전체</option><option value="EASY">초급</option><option value="MEDIUM">중급</option><option value="HARD">고급</option>
                    </select>
                  </div>
                  <div>
                    <label htmlFor="home-count" className="mb-2 block text-sm font-semibold">문항 수</label>
                    <select id="home-count" className="form-control" value={questionCount} onChange={(event) => setQuestionCount(Number(event.target.value))}>
                      <option value={5}>5문항</option><option value={10}>10문항</option><option value={20}>20문항</option>
                    </select>
                  </div>
                </div>
                <button type="submit" className="success-button w-full">문제 출제 시작 →</button>
              </div>
            </form>
          </div>
        </section>
        {/* Stats Grid */}
        {!loading && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            <div className="surface-card border-t-4 border-t-[#3B86D1] p-6">
              <div className="text-4xl font-bold text-[#3B86D1]">
                {stats.totalQuestions}
              </div>
              <p className="mt-2 text-[#6C757D]">총 문제 수</p>
            </div>
            <div className="surface-card border-t-4 border-t-[#21BF06] p-6">
              <div className="text-4xl font-bold text-[#21BF06]">
                {stats.totalSubjects}
              </div>
              <p className="mt-2 text-[#6C757D]">과목</p>
            </div>
            <div className="surface-card border-t-4 border-t-[#242C34] p-6">
              <div className="text-4xl font-bold text-[#242C34]">
                {stats.difficultyStats.length || 0}
              </div>
              <p className="mt-2 text-[#6C757D]">난이도 종류</p>
            </div>
          </div>
        )}

        {/* Action Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Upload Card */}
          <div className="surface-card surface-card-hover p-8">
            <div className="text-3xl mb-4">📤</div>
            <h2 className="mb-4 text-2xl font-bold text-[#242C34]">
              문제 업로드
            </h2>
            <p className="mb-6 text-[#6C757D]">
              Excel 파일이나 코드 파일을 업로드하여 자동으로 문제를 생성하세요.
            </p>
            <Link
              href="/upload"
              className="primary-button"
            >
              파일 업로드 →
            </Link>
          </div>

          {/* Quiz Card */}
          <div className="surface-card surface-card-hover p-8">
            <div className="text-3xl mb-4">✏️</div>
            <h2 className="mb-4 text-2xl font-bold text-[#242C34]">
              문제 풀이
            </h2>
            <p className="mb-6 text-[#6C757D]">
              난이도별, 과목별로 랜덤 문제를 선택하여 풀어보세요.
            </p>
            <Link
              href="/quiz"
              className="success-button"
            >
              문제 풀이 →
            </Link>
          </div>

        </div>

        {/* Features Section */}
        <div className="surface-card mt-16 p-8">
          <h2 className="mb-8 text-2xl font-bold text-[#242C34]">주요 기능</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h3 className="mb-2 text-lg font-semibold text-[#242C34]">
                📊 Excel 기반 문제 관리
              </h3>
              <p className="text-[#6C757D]">
                Excel 파일에서 데이터를 직접 읽어와 문제를 생성하고 관리할 수 있습니다.
              </p>
            </div>
            <div>
              <h3 className="mb-2 text-lg font-semibold text-[#242C34]">
                🤖 AI 자동 문제 생성
              </h3>
              <p className="text-[#6C757D]">
                OpenAI API를 활용하여 코드 파일에서 자동으로 문제를 생성합니다.
              </p>
            </div>
            <div>
              <h3 className="mb-2 text-lg font-semibold text-[#242C34]">
                🎯 난이도별 출제
              </h3>
              <p className="text-[#6C757D]">
                EASY, MEDIUM, HARD, EXPERT 4단계로 난이도를 분류하고 출제합니다.
              </p>
            </div>
            <div>
              <h3 className="mb-2 text-lg font-semibold text-[#242C34]">
                📁 다양한 파일 지원
              </h3>
              <p className="text-[#6C757D]">
                Java, JavaScript, SQL, Markdown 등 다양한 파일 형식을 지원합니다.
              </p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
}
