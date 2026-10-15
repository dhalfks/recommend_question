import { useEffect, useMemo, useState } from 'react';
import { useRouter } from 'next/router';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import { useAuth } from '@/contexts/AuthContext';
import { progressAPI, questionsAPI, recommendationsAPI, subjectsAPI } from '@/lib/api';

type DashboardGroup = {
  subject_id: number;
  subject_name: string;
  difficulty: string;
  attempted: number;
  correct: number;
  score_percent: number;
  achievement_score: number;
  average_seconds: number;
};

type DashboardData = {
  total_attempted: number;
  total_correct: number;
  score_percent: number;
  achievement_score: number;
  groups: DashboardGroup[];
};

type PeerMissedUnit = {
  subject_id: number;
  subject_name: string;
  subject_unit: string;
  question_count: number;
  similar_learner_miss_count: number;
  similar_learner_attempt_count: number;
  miss_rate: number;
};

type MyWrongQuestion = {
  question_id: number;
  title: string;
  subject_name: string;
  subject_unit: string;
  difficulty: string;
};

type SnapQuestion = {
  id: number;
  title: string;
  content: string;
  options?: string | null;
  code_snippet?: string | null;
};

const difficultyLabels: Record<string, string> = {
  EASY: '초급',
  MEDIUM: '중급',
  HARD: '고급',
  EXPERT: '전문가',
};

const difficultyColors: Record<string, string> = {
  EASY: '#3B86D1',
  MEDIUM: '#21BF06',
  HARD: '#F59E0B',
  EXPERT: '#8B5CF6',
};

export default function StudentDashboard() {
  const router = useRouter();
  const { user } = useAuth();
  const [data, setData] = useState<DashboardData | null>(null);
  const [peerMissedUnits, setPeerMissedUnits] = useState<PeerMissedUnit[]>([]);
  const [myWrong, setMyWrong] = useState<MyWrongQuestion[]>([]);
  const [snapQuestion, setSnapQuestion] = useState<SnapQuestion | null>(null);
  const [snapAnswer, setSnapAnswer] = useState<number | string | null>(null);
  const [snapStartedAt, setSnapStartedAt] = useState(0);
  const [snapLoading, setSnapLoading] = useState(false);
  const [subjects, setSubjects] = useState<Array<{ id: number; name: string }>>([]);
  const [subjectId, setSubjectId] = useState('');
  const [subjectUnits, setSubjectUnits] = useState<string[]>([]);
  const [subjectUnit, setSubjectUnit] = useState('');
  const [difficulty, setDifficulty] = useState('');
  const [count, setCount] = useState(5);
  const [quizMode, setQuizMode] = useState<'STANDARD' | 'CODE'>('STANDARD');
  const [loading, setLoading] = useState(true);

  const subjectStats = useMemo(() => {
    const totals = new Map<number, {
      subject_id: number;
      subject_name: string;
      attempted: number;
      correct: number;
    }>();
    for (const group of data?.groups ?? []) {
      const current = totals.get(group.subject_id) ?? {
        subject_id: group.subject_id,
        subject_name: group.subject_name,
        attempted: 0,
        correct: 0,
      };
      current.attempted += group.attempted;
      current.correct += group.correct;
      totals.set(group.subject_id, current);
    }
    return Array.from(totals.values()).map((subject) => ({
      ...subject,
      score_percent: subject.attempted
        ? Math.round(subject.correct / subject.attempted * 100)
        : 0,
    }));
  }, [data]);

  const difficultyStats = useMemo(() => {
    const totals = new Map<string, number>();
    for (const group of data?.groups ?? []) {
      totals.set(group.difficulty, (totals.get(group.difficulty) ?? 0) + group.attempted);
    }
    const total = Array.from(totals.values()).reduce((sum, value) => sum + value, 0);
    return ['EASY', 'MEDIUM', 'HARD', 'EXPERT']
      .map((difficulty) => ({
        difficulty,
        attempted: totals.get(difficulty) ?? 0,
        percent: total ? (totals.get(difficulty) ?? 0) / total * 100 : 0,
      }))
      .filter((item) => item.attempted > 0);
  }, [data]);

  const difficultyGradient = useMemo(() => {
    let current = 0;
    const segments = difficultyStats.map((item) => {
      const start = current;
      current += item.percent;
      return `${difficultyColors[item.difficulty]} ${start}% ${current}%`;
    });
    return `conic-gradient(${segments.join(', ')})`;
  }, [difficultyStats]);

  useEffect(() => {
    let active = true;

    progressAPI.dashboard()
      .then((response) => {
        if (active) setData(response.data);
      })
      .catch((error) => console.error('대시보드 조회 실패:', error))
      .finally(() => {
        if (active) setLoading(false);
      });

    subjectsAPI.getAll()
      .then((response) => {
        if (active) setSubjects(response.data);
      })
      .catch((error) => console.error('과목 조회 실패:', error));

    recommendationsAPI.getPeerMissedUnits({ count: 5 })
      .then((response) => {
        if (active) setPeerMissedUnits(response.data.items);
      })
      .catch((error) => console.error('유사 학습자 추천 조회 실패:', error));

    recommendationsAPI.getMyWrong({ count: 5 })
      .then((response) => {
        if (active) setMyWrong(response.data.items);
      })
      .catch((error) => console.error('오답 추천 조회 실패:', error));

    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    setSubjectUnit('');
    if (!subjectId) {
      setSubjectUnits([]);
      return;
    }
    questionsAPI.getSubjectUnits(Number(subjectId))
      .then((response) => setSubjectUnits(response.data.subject_units ?? []))
      .catch(() => setSubjectUnits([]));
  }, [subjectId]);

  const startQuiz = (event: React.FormEvent) => {
    event.preventDefault();
    const query = new URLSearchParams({ count: String(quizMode === 'CODE' ? 1 : count) });
    query.set('mode', quizMode);
    if (subjectId) query.set('subjectId', subjectId);
    if (quizMode === 'STANDARD' && subjectUnit) query.set('subjectUnit', subjectUnit);
    if (difficulty) query.set('difficulty', difficulty);
    router.push(`/quiz?${query.toString()}`);
  };

  const retryUnit = (unit: PeerMissedUnit) => {
    const query = new URLSearchParams({
      subjectId: String(unit.subject_id),
      subjectUnit: unit.subject_unit,
      count: String(Math.max(1, Math.min(20, unit.question_count))),
    });
    router.push(`/quiz?${query.toString()}`);
  };

  const openSnapQuestion = async (questionId: number) => {
    setSnapLoading(true);
    try {
      const response = await questionsAPI.getById(questionId);
      setSnapQuestion(response.data);
      setSnapAnswer(null);
      setSnapStartedAt(Date.now());
    } finally {
      setSnapLoading(false);
    }
  };

  const snapOptions = useMemo(() => {
    if (!snapQuestion?.options) return [] as string[];
    try {
      const parsed = JSON.parse(snapQuestion.options);
      return Array.isArray(parsed) ? parsed.map(String) : [];
    } catch {
      return [] as string[];
    }
  }, [snapQuestion]);

  const submitSnapAnswer = async () => {
    if (!snapQuestion || snapAnswer === null || snapAnswer === '') return;
    setSnapLoading(true);
    try {
      const response = await progressAPI.submit({
        session_id: typeof crypto !== 'undefined' && crypto.randomUUID
          ? crypto.randomUUID()
          : `snap-${Date.now()}`,
        total_seconds: Math.max((Date.now() - snapStartedAt) / 1000, 1),
        answers: [{
          question_id: snapQuestion.id,
          answer: snapAnswer,
          sequence_number: 1,
          elapsed_seconds: Math.max((Date.now() - snapStartedAt) / 1000, 1),
        }],
      });
      const correct = response.data.results?.[0]?.is_correct === true;
      if (correct) {
        setMyWrong((current) => current.filter((item) => item.question_id !== snapQuestion.id));
        setSnapQuestion(null);
        const [wrongResult, dashboardResult] = await Promise.allSettled([
          recommendationsAPI.getMyWrong({ count: 5 }),
          progressAPI.dashboard(),
        ]);
        if (wrongResult.status === 'fulfilled') {
          setMyWrong(wrongResult.value.data.items);
        }
        if (dashboardResult.status === 'fulfilled') {
          setData(dashboardResult.value.data);
        }
        alert('정답입니다. 내 오답 문제 목록에서 제거했습니다.');
      } else {
        setSnapStartedAt(Date.now());
        alert('정답이 아닙니다. 다시 풀어보세요.');
      }
    } finally {
      setSnapLoading(false);
    }
  };

  return (
    <div className="app-shell flex flex-col">
      <Navbar />
      <main className="page-container flex-1 py-12">
        <section className="flex flex-col justify-between gap-6 rounded-3xl bg-[#242C34] p-8 text-white shadow-lg sm:flex-row sm:items-center sm:p-10">
          <div>
            <p className="font-semibold text-[#63E64B]">{user?.name} 학생의 학습 현황</p>
            <h1 className="mt-2 text-3xl font-bold sm:text-4xl">학습 대시보드</h1>
            <p className="mt-3 text-slate-300">과목과 난이도별 누적 점수를 확인하고 학습을 이어가세요.</p>
          </div>
          <div className="w-full shrink-0 sm:w-auto sm:min-w-64">
            <button
              type="button"
              onClick={() => router.push('/quiz?adaptive=1&count=10')}
              className="w-full rounded-xl bg-[#21BF06] px-6 py-4 text-base font-bold text-white shadow-lg transition hover:bg-[#1AA005]"
            >
              맞춤 추천 10문제 시작
            </button>
            <p className="mt-2 text-center text-xs text-slate-300">학습 기록과 취약 영역을 분석해 추천합니다.</p>
          </div>
        </section>

        <section className="surface-card my-8 overflow-hidden border-l-4 border-l-[#8B5CF6]">
          <div className="flex flex-col justify-between gap-5 p-6 sm:flex-row sm:items-center">
            <div>
              <p className="text-sm font-semibold text-[#8B5CF6]">모든 학생 공통</p>
              <h2 className="mt-1 text-2xl font-bold text-[#242C34]">자격증 기출문제</h2>
              <p className="mt-2 text-[#6C757D]">정보처리기사와 SQLD의 등록된 연도·회차·과목을 선택해 풀어보세요.</p>
            </div>
            <button type="button" onClick={() => router.push('/public-exams')}
              className="shrink-0 rounded-xl bg-[#8B5CF6] px-6 py-4 font-bold text-white transition hover:bg-[#7448D1]">
              공통 기출 시작 →
            </button>
          </div>
        </section>

        {loading ? (
          <div className="py-20 text-center text-[#6C757D]">학습 기록을 불러오는 중...</div>
        ) : (
          <>
            <section className="surface-card my-8 overflow-hidden">
              <div className="flex border-b border-[#DCE3EA]">
                <button type="button" onClick={() => setQuizMode('STANDARD')} className={`flex-1 px-5 py-4 font-bold ${quizMode === 'STANDARD' ? 'bg-blue-50 text-[#2F70B5]' : 'text-[#6C757D]'}`}>랜덤 풀기</button>
                <button type="button" onClick={() => { setQuizMode('CODE'); if (difficulty === 'EXPERT') setDifficulty(''); }} className={`flex-1 px-5 py-4 font-bold ${quizMode === 'CODE' ? 'bg-[#F3FBF1] text-[#168A04]' : 'text-[#6C757D]'}`}>코드만 풀기</button>
              </div>
              <div className="px-6 pt-5 text-sm text-[#6C757D]">{quizMode === 'CODE' ? '코딩 테스트처럼 코드 입력 문제만 풀고 GPT 채점과 리팩토링 해설을 받습니다.' : '객관식과 주관식 문제만 무작위로 출제합니다.'}</div>
            <form onSubmit={startQuiz} className={`grid items-end gap-4 p-6 ${quizMode === 'CODE' ? 'md:grid-cols-[1fr_1fr_auto]' : 'lg:grid-cols-[1fr_1fr_1fr_140px_auto]'}`}>
              <label className="text-sm font-semibold">과목
                <select className="form-control mt-2" value={subjectId} onChange={(e) => setSubjectId(e.target.value)}>
                  <option value="">전체 과목</option>
                  {subjects.map((subject) => <option key={subject.id} value={subject.id}>{subject.name}</option>)}
                </select>
              </label>
              {quizMode === 'STANDARD' && <label className="text-sm font-semibold">소제목
                <select
                  className="form-control mt-2"
                  value={subjectUnit}
                  onChange={(e) => setSubjectUnit(e.target.value)}
                  disabled={!subjectId}
                >
                  <option value="">{subjectId ? '전체 소제목' : '과목을 먼저 선택하세요'}</option>
                  {subjectUnits.map((unit) => <option key={unit} value={unit}>{unit}</option>)}
                </select>
              </label>}
              <label className="text-sm font-semibold">난이도
                <select className="form-control mt-2" value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>
                  <option value="">전체 난이도</option>
                  <option value="EASY">초급</option>
                  <option value="MEDIUM">중급</option>
                  <option value="HARD">고급</option>
                  {quizMode === 'STANDARD' && <option value="EXPERT">전문가</option>}
                </select>
              </label>
              {quizMode === 'STANDARD' && <label className="text-sm font-semibold">문항 수
                <select className="form-control mt-2" value={count} onChange={(e) => setCount(Number(e.target.value))}>
                  <option value={5}>5문항</option>
                  <option value={10}>10문항</option>
                  <option value={20}>20문항</option>
                </select>
              </label>}
              <button className="success-button h-[50px]">{quizMode === 'CODE' ? '코딩 테스트 시작' : '랜덤 문제'}</button>
            </form>
            </section>

            <section className="my-8 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
              <div className="surface-card border-t-4 border-t-[#3B86D1] p-6">
                <p className="text-sm font-semibold text-[#6C757D]">푼 문제 합계</p>
                <p className="mt-2 text-4xl font-bold text-[#3B86D1]">{data?.total_attempted ?? 0}</p>
              </div>
              <div className="surface-card border-t-4 border-t-[#21BF06] p-6">
                <p className="text-sm font-semibold text-[#6C757D]">정답 합계</p>
                <p className="mt-2 text-4xl font-bold text-[#21BF06]">{data?.total_correct ?? 0}</p>
              </div>
              <div className="surface-card border-t-4 border-t-[#242C34] p-6">
                <p className="text-sm font-semibold text-[#6C757D]">누적 점수</p>
                <p className="mt-2 text-4xl font-bold text-[#242C34]">{data?.score_percent ?? 0}점</p>
              </div>
              <div className="surface-card border-t-4 border-t-[#8B5CF6] p-6">
                <p className="text-sm font-semibold text-[#6C757D]">나의 성취도</p>
                <p className="mt-2 text-4xl font-bold text-[#8B5CF6]">{data?.achievement_score ?? 0}</p>
              </div>
            </section>

            <section className="mb-8 grid gap-6 lg:grid-cols-2">
              <div className="surface-card overflow-hidden">
                <div className="border-b border-[#E9ECEF] p-6"><h2 className="text-xl font-bold text-[#242C34]">유사 학습자가 많이 틀린 단원 Top 5</h2><p className="mt-1 text-sm text-[#6C757D]">비슷한 학습 패턴을 가진 학생들의 오답을 단원별로 묶었습니다.</p></div>
                {!peerMissedUnits.length ? <div className="p-8 text-center text-[#6C757D]">유사 학습자를 찾기 위한 풀이 기록이 아직 충분하지 않습니다.</div> : <ol className="divide-y divide-[#E9ECEF]">{peerMissedUnits.map((unit, index) => <li key={`${unit.subject_id}-${unit.subject_unit}`} className="p-5"><div className="flex items-center gap-3"><span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-[#EEF5FC] font-bold text-[#3B86D1]">{index + 1}</span><div className="min-w-0 flex-1"><p className="truncate font-semibold text-[#242C34]">{unit.subject_unit}</p><p className="mt-1 truncate text-sm text-[#6C757D]">{unit.subject_name} · 관련 문제 {unit.question_count}개</p></div><div className="shrink-0 text-right"><strong className="text-lg text-[#DC3545]">{unit.miss_rate}%</strong><p className="text-xs text-[#6C757D]">단원 오답률</p></div><button type="button" onClick={() => retryUnit(unit)} className="shrink-0 whitespace-nowrap rounded-lg bg-[#3B86D1] px-3 py-2 text-xs font-bold text-white hover:bg-[#2F70B5]">다시 풀기</button></div></li>)}</ol>}
              </div>

              <div className="surface-card overflow-hidden">
                <div className="border-b border-[#E9ECEF] p-6"><h2 className="text-xl font-bold text-[#242C34]">내가 틀린 문제 Top 5</h2><p className="mt-1 text-sm text-[#6C757D]">최근 결과가 오답인 문제입니다. 정답을 맞히면 목록에서 사라집니다.</p></div>
                {!myWrong.length ? <div className="p-8 text-center text-[#6C757D]">다시 풀 오답 문제가 없습니다.</div> : <ol className="divide-y divide-[#E9ECEF]">{myWrong.map((question, index) => <li key={question.question_id} className="flex items-center gap-4 p-5"><span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-red-50 font-bold text-[#DC3545]">{index + 1}</span><div className="min-w-0 flex-1"><p className="truncate font-semibold text-[#242C34]">{question.title}</p><p className="mt-1 text-sm text-[#6C757D]">{question.subject_name} · {question.subject_unit} · {difficultyLabels[question.difficulty] ?? question.difficulty}</p></div><button type="button" disabled={snapLoading} onClick={() => openSnapQuestion(question.question_id)} className="shrink-0 rounded-lg bg-[#EAF3FC] px-3 py-2 text-sm font-bold text-[#245E96]">바로 풀기</button></li>)}</ol>}
              </div>
            </section>

            {!!data?.groups.length && (
              <section className="mb-8 grid gap-6 lg:grid-cols-[1.35fr_1fr]">
                <div className="surface-card p-6">
                  <h2 className="text-xl font-bold text-[#242C34]">과목별 평균 점수</h2>
                  <p className="mt-1 text-sm text-[#6C757D]">과목별 전체 응시 결과를 합산했습니다.</p>
                  <div className="mt-6 space-y-5">
                    {subjectStats.map((subject) => (
                      <div key={`subject-chart-${subject.subject_id}`}>
                        <div className="mb-2 flex justify-between gap-4 text-sm">
                          <span className="font-semibold">{subject.subject_name}</span>
                          <span>{subject.correct}/{subject.attempted} · {subject.score_percent}점</span>
                        </div>
                        <div className="h-7 overflow-hidden rounded-lg bg-[#E9ECEF]">
                          <div
                            className="flex h-full items-center justify-end rounded-lg bg-gradient-to-r from-[#3B86D1] to-[#63A7E8] pr-2 text-xs font-bold text-white transition-all duration-500"
                            style={{ width: `${subject.score_percent}%` }}
                            role="img"
                            aria-label={`${subject.subject_name} 평균 ${subject.score_percent}점`}
                          >
                            {subject.score_percent >= 15 ? `${subject.score_percent}` : ''}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="surface-card p-6">
                  <h2 className="text-xl font-bold text-[#242C34]">난이도별 풀이 비율</h2>
                  <p className="mt-1 text-sm text-[#6C757D]">푼 문제 수를 난이도별로 구분했습니다.</p>
                  <div className="mt-8 flex flex-col items-center gap-7 sm:flex-row sm:justify-center lg:flex-col xl:flex-row">
                    <div
                      className="relative h-48 w-48 shrink-0 rounded-full"
                      style={{ background: difficultyGradient }}
                      role="img"
                      aria-label={difficultyStats.map((item) => (
                        `${difficultyLabels[item.difficulty]} ${Math.round(item.percent)}%`
                      )).join(', ')}
                    >
                      <div className="absolute inset-10 flex flex-col items-center justify-center rounded-full bg-white shadow-inner">
                        <strong className="text-3xl text-[#242C34]">{data.total_attempted}</strong>
                        <span className="text-xs font-semibold text-[#6C757D]">총 풀이</span>
                      </div>
                    </div>
                    <div className="w-full space-y-3">
                      {difficultyStats.map((item) => (
                        <div key={item.difficulty} className="flex items-center gap-3 text-sm">
                          <span className="h-3 w-3 rounded-full"
                            style={{ backgroundColor: difficultyColors[item.difficulty] }} />
                          <span className="flex-1 font-semibold">
                            {difficultyLabels[item.difficulty] ?? item.difficulty}
                          </span>
                          <span className="text-[#6C757D]">{item.attempted}문항</span>
                          <strong className="w-10 text-right">{Math.round(item.percent)}%</strong>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </section>
            )}

            <section className="surface-card overflow-hidden">
              <div className="border-b border-[#E9ECEF] p-6">
                <h2 className="text-xl font-bold text-[#242C34]">과목별·난이도별 점수</h2>
              </div>
              {!data?.groups.length ? (
                <div className="p-10 text-center text-[#6C757D]">
                  아직 저장된 풀이 기록이 없습니다. 문제를 풀고 제출하면 여기에 점수가 표시됩니다.
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full min-w-[620px] text-left">
                    <thead className="bg-[#F8F9FA] text-sm text-[#6C757D]">
                      <tr>
                        <th className="px-6 py-4">과목</th>
                        <th className="px-6 py-4">난이도</th>
                        <th className="px-6 py-4 text-right">푼 문제</th>
                        <th className="px-6 py-4 text-right">정답</th>
                        <th className="px-6 py-4 text-right">점수</th>
                        <th className="px-6 py-4 text-right">평균 시간</th>
                        <th className="px-6 py-4 text-right">성취도</th>
                      </tr>
                    </thead>
                    <tbody>
                      {data.groups.map((group) => (
                        <tr key={`${group.subject_id}-${group.difficulty}`} className="border-t border-[#E9ECEF]">
                          <td className="px-6 py-4 font-semibold">{group.subject_name}</td>
                          <td className="px-6 py-4">{difficultyLabels[group.difficulty] ?? group.difficulty}</td>
                          <td className="px-6 py-4 text-right">{group.attempted}</td>
                          <td className="px-6 py-4 text-right text-[#168A04]">{group.correct}</td>
                          <td className="px-6 py-4 text-right font-bold">{group.score_percent}점</td>
                          <td className="px-6 py-4 text-right">{group.average_seconds}초</td>
                          <td className="px-6 py-4 text-right font-bold text-[#8B5CF6]">{group.achievement_score}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </section>
          </>
        )}
      </main>
      <Footer />
      {snapQuestion && <div className="fixed inset-0 z-[70] flex justify-end bg-black/40" onClick={() => setSnapQuestion(null)}><aside className="h-full w-full max-w-xl overflow-y-auto bg-white p-6 shadow-2xl sm:p-8" onClick={(event) => event.stopPropagation()}><div className="flex items-start justify-between gap-4"><div><p className="text-sm font-semibold text-[#DC3545]">오답 스냅 풀이</p><h2 className="mt-1 text-2xl font-bold text-[#242C34]">{snapQuestion.title}</h2></div><button type="button" className="rounded-lg bg-[#EEF1F4] px-3 py-2" onClick={() => setSnapQuestion(null)}>닫기</button></div><p className="mt-6 whitespace-pre-wrap rounded-xl bg-[#F8F9FA] p-4 leading-7">{snapQuestion.content}</p>{snapQuestion.code_snippet && <pre className="mt-4 overflow-x-auto rounded-xl bg-[#1F2937] p-4 text-sm text-white"><code>{snapQuestion.code_snippet}</code></pre>}{snapOptions.length ? <div className="mt-6 space-y-3">{snapOptions.map((option, index) => <label key={index} className={`flex cursor-pointer items-center gap-3 rounded-xl border p-4 ${snapAnswer === index ? 'border-[#3B86D1] bg-blue-50' : 'border-[#E9ECEF]'}`}><input type="radio" name="snap-answer" checked={snapAnswer === index} onChange={() => setSnapAnswer(index)} /><span><strong>{index + 1}.</strong> {option}</span></label>)}</div> : <textarea className="form-control mt-6" rows={6} value={typeof snapAnswer === 'string' ? snapAnswer : ''} onChange={(event) => setSnapAnswer(event.target.value)} placeholder="답안을 입력하세요." />}<button type="button" onClick={submitSnapAnswer} disabled={snapLoading || snapAnswer === null || snapAnswer === ''} className="success-button mt-6 w-full">{snapLoading ? '채점 중...' : '정답 제출'}</button></aside></div>}
    </div>
  );
}
