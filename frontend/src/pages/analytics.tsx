import { useEffect, useMemo, useState } from 'react';
import { useRouter } from 'next/router';
import Footer from '@/components/Footer';
import Navbar from '@/components/Navbar';
import ProtectedPage from '@/components/ProtectedPage';
import { progressAPI, subjectsAPI } from '@/lib/api';

type Item = { question_id: number; question_number: number; title: string; content: string; subject_name: string; difficulty: string; responses: number; correct: number; wrong: number; skipped: number; correct_rate: number; wrong_rate: number; average_seconds: number; most_common_wrong: { answer: string; count: number } | null };
type Summary = { questions: number; responses: number; correct_rate: number; average_seconds: number; highest_wrong: Item | null; slowest: Item | null };
type Student = { id: number | string; name: string; answer: string | null; elapsed_seconds: number };
type Detail = { question: { id: number; number: number; title: string; content: string; explanation?: string; correct_option: number | null }; options: Array<{ index: number; text: string; count: number }>; students: Record<'correct' | 'incorrect' | 'skipped', Student[]> };
type StudentSummary = { id: number; name: string; email: string; affiliation?: string | null; academic_year?: number | null; course_name?: string | null; attempted: number; correct: number; score_percent: number; achievement_score: number; average_seconds: number; last_attempted: string | null };
type StudentGroup = { subject_id: number; subject_name: string; difficulty: string; attempted: number; correct: number; score_percent: number; achievement_score: number; average_seconds: number };
type StudentDetail = { student: { id: number; name: string; email: string; affiliation?: string | null; academic_year?: number | null; course_name?: string | null }; total_attempted: number; total_correct: number; score_percent: number; achievement_score: number; average_seconds: number; total_sessions: number; groups: StudentGroup[] };

const difficultyLabels: Record<string, string> = { EASY: '초급', MEDIUM: '중급', HARD: '고급', EXPERT: '전문가' };
const difficultyColors: Record<string, string> = { EASY: '#3B86D1', MEDIUM: '#21BF06', HARD: '#F59E0B', EXPERT: '#8B5CF6' };
const emptySummary: Summary = { questions: 0, responses: 0, correct_rate: 0, average_seconds: 0, highest_wrong: null, slowest: null };

function AnalyticsPage() {
  const router = useRouter();
  const [items, setItems] = useState<Item[]>([]);
  const [summary, setSummary] = useState<Summary>(emptySummary);
  const [subjects, setSubjects] = useState<Array<{ id: number; name: string }>>([]);
  const [filters, setFilters] = useState({ subject_id: '', difficulty: '', search: '', min_wrong_rate: '0' });
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<number | null>(null);
  const [detail, setDetail] = useState<Detail | null>(null);
  const [studentTab, setStudentTab] = useState<'correct' | 'incorrect' | 'skipped'>('correct');
  const [studentItems, setStudentItems] = useState<StudentSummary[]>([]);
  const [studentPage, setStudentPage] = useState(1);
  const [studentTotal, setStudentTotal] = useState(0);
  const [studentLoading, setStudentLoading] = useState(true);
  const [selectedStudent, setSelectedStudent] = useState<number | null>(null);
  const [studentDetail, setStudentDetail] = useState<StudentDetail | null>(null);
  const pageSize = 5;

  useEffect(() => { subjectsAPI.getAll().then(({ data }) => setSubjects(data)); }, []);
  useEffect(() => {
    const timer = window.setTimeout(() => {
      setLoading(true);
      const params: Record<string, string | number> = { page, page_size: pageSize, sort: 'responses_desc', min_wrong_rate: filters.min_wrong_rate };
      if (filters.subject_id) params.subject_id = filters.subject_id;
      if (filters.difficulty) params.difficulty = filters.difficulty;
      if (filters.search.trim()) params.search = filters.search.trim();
      progressAPI.questionAnalytics(params).then(({ data }) => {
        setItems((current) => page === 1 ? data.items : [...current, ...data.items]);
        setSummary(data.summary); setTotal(data.total);
      }).catch((error) => { if (error.response?.status === 403) router.replace('/'); }).finally(() => setLoading(false));
    }, 250);
    return () => window.clearTimeout(timer);
  }, [filters, page, router]);

  useEffect(() => {
    setStudentLoading(true);
    progressAPI.studentAnalytics({ page: studentPage, page_size: 5 }).then(({ data }) => {
      setStudentItems((current) => {
        const combined: StudentSummary[] = studentPage === 1 ? data.items : [...current, ...data.items];
        return combined.sort((left, right) =>
          right.attempted - left.attempted
          || right.achievement_score - left.achievement_score
          || left.name.localeCompare(right.name, 'ko')
        );
      });
      setStudentTotal(data.total);
    }).catch((error) => { if (error.response?.status === 403) router.replace('/'); }).finally(() => setStudentLoading(false));
  }, [studentPage, router]);

  const setFilter = (name: keyof typeof filters, value: string) => { setFilters((current) => ({ ...current, [name]: value })); setPage(1); };
  const openDetail = (id: number) => { setSelectedStudent(null); setSelected(id); setDetail(null); setStudentTab('correct'); progressAPI.questionAnalyticsDetail(id).then(({ data }) => setDetail(data)); };
  const openStudentDetail = (id: number) => { setSelected(null); setSelectedStudent(id); setStudentDetail(null); progressAPI.studentAnalyticsDetail(id).then(({ data }) => setStudentDetail(data)); };
  const hasMore = items.length < total;
  const hasMoreStudents = studentItems.length < studentTotal;
  const maxOptionCount = useMemo(() => Math.max(1, ...(detail?.options.map((option) => option.count) ?? [1])), [detail]);

  return <div className="app-shell flex flex-col"><Navbar /><main className="page-container flex-1 py-10">
    <div className="mb-8 flex flex-col justify-between gap-4 sm:flex-row sm:items-end"><div><p className="font-semibold text-[#3B86D1]">교수자 분석</p><h1 className="mt-1 text-3xl font-bold text-[#242C34]">문항별 대시보드</h1><p className="mt-2 text-[#6C757D]">오답이 많거나 오래 걸린 문항을 먼저 확인해 보세요.</p></div><div className="rounded-xl bg-[#EAF3FC] px-4 py-3 text-sm text-[#245E96]">행을 누르면 학생과 보기별 응답을 확인할 수 있습니다.</div></div>
    <section className="mb-7 grid gap-4 sm:grid-cols-2 xl:grid-cols-4"><Metric label="분석 문항" value={`${summary.questions}문항`} color="#3B86D1" note={`${summary.responses}회 응답`} /><Metric label="전체 정답률" value={`${summary.correct_rate}%`} color="#21A608" note={`오답률 ${(100 - summary.correct_rate).toFixed(1)}%`} /><Metric label="평균 풀이시간" value={`${summary.average_seconds}초`} color="#7C3AED" note={summary.slowest ? `최장 ${summary.slowest.question_number}번` : '응답 없음'} /><Metric label="최고 오답 문항" value={summary.highest_wrong ? `${summary.highest_wrong.question_number}번` : '-'} color="#E25241" note={summary.highest_wrong ? `오답률 ${summary.highest_wrong.wrong_rate}%` : '응답 없음'} /></section>
    <section className="surface-card mb-6 grid gap-3 p-4 md:grid-cols-[1.4fr_1fr_1fr_1fr]"><input className="form-control" placeholder="문항 제목·내용 검색" value={filters.search} onChange={(e) => setFilter('search', e.target.value)} /><select className="form-control" value={filters.subject_id} onChange={(e) => setFilter('subject_id', e.target.value)}><option value="">전체 과목</option>{subjects.map((subject) => <option key={subject.id} value={subject.id}>{subject.name}</option>)}</select><select className="form-control" value={filters.difficulty} onChange={(e) => setFilter('difficulty', e.target.value)}><option value="">전체 난이도</option>{Object.entries(difficultyLabels).map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select><select className="form-control" value={filters.min_wrong_rate} onChange={(e) => setFilter('min_wrong_rate', e.target.value)}><option value="0">전체 오답률</option><option value="30">오답률 30% 이상</option><option value="50">오답률 50% 이상</option><option value="70">오답률 70% 이상</option></select></section>
    <section className="surface-card overflow-hidden"><div className="overflow-x-auto"><table className="w-full min-w-[960px] text-left text-sm"><thead className="bg-[#F2F5F7] text-[#5E6872]"><tr><th className="px-5 py-4">문항</th><th className="px-4 py-4">과목·난이도</th><th className="px-4 py-4 text-right">응답</th><th className="px-4 py-4">정답률</th><th className="px-4 py-4">오답률</th><th className="px-4 py-4">최다 오답</th><th className="px-5 py-4 text-right">평균 시간</th></tr></thead><tbody>
      {loading && page === 1 ? <tr><td colSpan={7} className="p-14 text-center text-[#6C757D]">문항 통계를 불러오는 중...</td></tr> : !items.length ? <tr><td colSpan={7} className="p-14 text-center text-[#6C757D]">조건에 맞는 문항이 없습니다.</td></tr> : items.map((item) => <tr key={item.question_id} onClick={() => openDetail(item.question_id)} className="cursor-pointer border-t border-[#E9ECEF] hover:bg-[#F8FBFE]"><td className="max-w-[320px] px-5 py-4"><div className="font-bold text-[#242C34]">{item.question_number}번 · {item.title}</div><div className="mt-1 truncate text-[#6C757D]">{item.content}</div></td><td className="px-4 py-4"><div>{item.subject_name}</div><span className="mt-1 inline-block rounded-full bg-[#EEF1F4] px-2 py-1 text-xs">{difficultyLabels[item.difficulty] ?? item.difficulty}</span></td><td className="px-4 py-4 text-right font-semibold">{item.responses}</td><td className="px-4 py-4"><Rate value={item.correct_rate} color="#21A608" /></td><td className="px-4 py-4"><Rate value={item.wrong_rate} color={item.wrong_rate >= 50 ? '#E25241' : '#F59E0B'} /></td><td className="max-w-[190px] px-4 py-4"><div className="truncate font-semibold">{item.most_common_wrong?.answer ?? '-'}</div>{item.most_common_wrong && <div className="text-xs text-[#6C757D]">{item.most_common_wrong.count}회 선택</div>}</td><td className="px-5 py-4 text-right font-bold">{item.average_seconds}초</td></tr>)}</tbody></table></div>
      <div className="flex flex-col items-center gap-3 border-t border-[#E9ECEF] px-5 py-5 text-sm"><span className="text-[#6C757D]">전체 {total}문항 중 {items.length}문항 표시 · 응답이 많은 순</span>{hasMore && <button className="primary-button min-w-44" disabled={loading} onClick={() => setPage((value) => value + 1)}>{loading ? '불러오는 중...' : '5개 더보기'}</button>}</div></section>

    <section className="mt-10">
      <div className="mb-4"><p className="font-semibold text-[#3B86D1]">학생별 분석</p><h2 className="mt-1 text-2xl font-bold text-[#242C34]">학생 성취도 현황</h2><p className="mt-2 text-sm text-[#6C757D]">학생을 선택하면 개인별 성취도와 과목·난이도 분석을 확인할 수 있습니다.</p></div>
      <div className="surface-card overflow-hidden"><div className="overflow-x-auto"><table className="w-full min-w-[760px] text-left text-sm"><thead className="bg-[#F2F5F7] text-[#5E6872]"><tr><th className="px-5 py-4">학생</th><th className="px-4 py-4 text-right">풀이 문항</th><th className="px-4 py-4 text-right">정답</th><th className="px-4 py-4">정답률</th><th className="px-4 py-4 text-right">성취도</th><th className="px-5 py-4 text-right">평균 시간</th></tr></thead><tbody>
        {studentLoading && studentPage === 1 ? <tr><td colSpan={6} className="p-12 text-center text-[#6C757D]">학생 분석을 불러오는 중...</td></tr> : !studentItems.length ? <tr><td colSpan={6} className="p-12 text-center text-[#6C757D]">등록된 학생이 없습니다.</td></tr> : studentItems.map((student) => <tr key={student.id} onClick={() => openStudentDetail(student.id)} className="cursor-pointer border-t border-[#E9ECEF] hover:bg-[#F8FBFE]"><td className="px-5 py-4"><strong className="text-[#242C34]">{student.name}</strong><div className="mt-1 text-xs text-[#6C757D]">{student.email}</div></td><td className="px-4 py-4 text-right font-semibold">{student.attempted}</td><td className="px-4 py-4 text-right">{student.correct}</td><td className="px-4 py-4"><Rate value={student.score_percent} color={student.score_percent >= 70 ? '#21A608' : '#F59E0B'} /></td><td className="px-4 py-4 text-right font-bold text-[#7C3AED]">{student.achievement_score}</td><td className="px-5 py-4 text-right">{student.average_seconds}초</td></tr>)}</tbody></table></div>
        <div className="flex flex-col items-center gap-3 border-t border-[#E9ECEF] px-5 py-5 text-sm"><span className="text-[#6C757D]">전체 {studentTotal}명 중 {studentItems.length}명 표시</span>{hasMoreStudents && <button className="primary-button min-w-44" disabled={studentLoading} onClick={() => setStudentPage((value) => value + 1)}>{studentLoading ? '불러오는 중...' : '5명 더보기'}</button>}</div>
      </div>
    </section>
  </main><Footer />
  {selected !== null && <div className="fixed inset-0 z-[60] flex justify-end bg-black/35" onClick={() => setSelected(null)}><aside className="h-full w-full max-w-2xl overflow-y-auto bg-white p-6 shadow-2xl sm:p-8" onClick={(event) => event.stopPropagation()}><div className="flex items-start justify-between gap-4"><div><p className="text-sm font-semibold text-[#3B86D1]">문항 상세 분석</p><h2 className="mt-1 text-2xl font-bold">{detail ? `${detail.question.number}번 · ${detail.question.title}` : '불러오는 중...'}</h2></div><button className="rounded-lg bg-[#EEF1F4] px-3 py-2" onClick={() => setSelected(null)}>닫기</button></div>{detail && <DetailPanel detail={detail} studentTab={studentTab} setStudentTab={setStudentTab} maxOptionCount={maxOptionCount} />}</aside></div>}
  {selectedStudent !== null && <div className="fixed inset-0 z-[60] flex justify-end bg-black/35" onClick={() => setSelectedStudent(null)}><aside className="h-full w-full max-w-3xl overflow-y-auto bg-white p-6 shadow-2xl sm:p-8" onClick={(event) => event.stopPropagation()}><div className="flex items-start justify-between gap-4"><div><p className="text-sm font-semibold text-[#3B86D1]">학생 상세 분석</p><h2 className="mt-1 text-2xl font-bold">{studentDetail ? studentDetail.student.name : '불러오는 중...'}</h2>{studentDetail && <p className="mt-1 text-sm text-[#6C757D]">{studentDetail.student.email}</p>}</div><button className="rounded-lg bg-[#EEF1F4] px-3 py-2" onClick={() => setSelectedStudent(null)}>닫기</button></div>{studentDetail && <StudentDetailPanel detail={studentDetail} />}</aside></div>}
  </div>;
}

function DetailPanel({ detail, studentTab, setStudentTab, maxOptionCount }: { detail: Detail; studentTab: 'correct' | 'incorrect' | 'skipped'; setStudentTab: (tab: 'correct' | 'incorrect' | 'skipped') => void; maxOptionCount: number }) {
  return <><p className="mt-5 whitespace-pre-wrap rounded-xl bg-[#F8F9FA] p-4 text-sm leading-6">{detail.question.content}</p><section className="mt-7"><h3 className="font-bold">보기별 선택</h3><div className="mt-4 space-y-3">{detail.options.length ? detail.options.map((option) => <div key={option.index}><div className="mb-1 flex justify-between gap-3 text-sm"><span className={option.index === detail.question.correct_option ? 'font-bold text-[#168A04]' : ''}>{option.index + 1}. {option.text} {option.index === detail.question.correct_option && '✓ 정답'}</span><strong>{option.count}회</strong></div><div className="h-3 overflow-hidden rounded-full bg-[#E9ECEF]"><div className={`h-full rounded-full ${option.index === detail.question.correct_option ? 'bg-[#21BF06]' : 'bg-[#E25241]'}`} style={{ width: `${option.count / maxOptionCount * 100}%` }} /></div></div>) : <p className="text-sm text-[#6C757D]">주관식 문항은 보기 분포가 없습니다.</p>}</div></section><section className="mt-8"><div className="flex gap-2 border-b">{(['correct', 'incorrect', 'skipped'] as const).map((tab) => <button key={tab} onClick={() => setStudentTab(tab)} className={`border-b-2 px-3 py-3 text-sm font-semibold ${studentTab === tab ? 'border-[#3B86D1] text-[#3B86D1]' : 'border-transparent text-[#6C757D]'}`}>{tab === 'correct' ? '맞힌 학생' : tab === 'incorrect' ? '틀린 학생' : '미응답'} ({detail.students[tab].length})</button>)}</div><div className="divide-y">{detail.students[studentTab].length ? detail.students[studentTab].map((student) => <div key={student.id} className="flex items-center justify-between py-3 text-sm"><strong>{student.name}</strong><span className="text-[#6C757D]">{student.elapsed_seconds}초</span></div>) : <p className="py-8 text-center text-sm text-[#6C757D]">해당 학생이 없습니다.</p>}</div></section>{detail.question.explanation && <section className="mt-7 rounded-xl border border-[#DDE9D8] bg-[#F5FBF2] p-4"><h3 className="font-bold text-[#168A04]">해설</h3><p className="mt-2 whitespace-pre-wrap text-sm leading-6">{detail.question.explanation}</p></section>}</>;
}

function StudentDetailPanel({ detail }: { detail: StudentDetail }) {
  const subjectStats = useMemo(() => {
    const totals = new Map<number, { name: string; attempted: number; correct: number }>();
    detail.groups.forEach((group) => {
      const current = totals.get(group.subject_id) ?? { name: group.subject_name, attempted: 0, correct: 0 };
      current.attempted += group.attempted;
      current.correct += group.correct;
      totals.set(group.subject_id, current);
    });
    return Array.from(totals.entries()).map(([id, value]) => ({
      id, ...value, score: value.attempted ? Math.round(value.correct / value.attempted * 100) : 0,
    }));
  }, [detail.groups]);

  const difficultyStats = useMemo(() => {
    const totals = new Map<string, number>();
    detail.groups.forEach((group) => totals.set(group.difficulty, (totals.get(group.difficulty) ?? 0) + group.attempted));
    return ['EASY', 'MEDIUM', 'HARD', 'EXPERT'].map((difficulty) => ({ difficulty, count: totals.get(difficulty) ?? 0 })).filter((item) => item.count > 0);
  }, [detail.groups]);
  const gradient = useMemo(() => {
    let current = 0;
    const parts = difficultyStats.map((item) => {
      const start = current;
      current += detail.total_attempted ? item.count / detail.total_attempted * 100 : 0;
      return `${difficultyColors[item.difficulty]} ${start}% ${current}%`;
    });
    return parts.length ? `conic-gradient(${parts.join(', ')})` : '#E9ECEF';
  }, [difficultyStats, detail.total_attempted]);

  return <div className="mt-7">
    <section className="mb-5 rounded-xl bg-[#F8F9FA] p-4 text-sm text-[#5E6872]">
      {[detail.student.affiliation, detail.student.academic_year ? `${detail.student.academic_year}년` : null, detail.student.course_name].filter(Boolean).join(' · ') || '소속 정보 없음'}
    </section>
    <section className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
      <Metric label="풀이 문항" value={`${detail.total_attempted}`} color="#3B86D1" note={`정답 ${detail.total_correct}개`} />
      <Metric label="정답률" value={`${detail.score_percent}%`} color="#21A608" note="전체 풀이 기준" />
      <Metric label="성취도" value={`${detail.achievement_score}`} color="#7C3AED" note="문항별 성취도 평균" />
      <Metric label="평균 풀이시간" value={`${detail.average_seconds}초`} color="#F59E0B" note={`${detail.total_sessions}회 응시`} />
    </section>

    {!detail.groups.length ? <div className="mt-8 rounded-xl bg-[#F8F9FA] p-10 text-center text-[#6C757D]">아직 풀이 기록이 없습니다.</div> : <div className="mt-8 grid gap-6 lg:grid-cols-[1.25fr_1fr]">
      <section className="rounded-2xl border border-[#E9ECEF] p-5"><h3 className="font-bold">과목별 점수</h3><p className="mt-1 text-xs text-[#6C757D]">과목별 전체 응시 결과입니다.</p><div className="mt-5 space-y-5">{subjectStats.map((subject) => <div key={subject.id}><div className="mb-2 flex justify-between text-sm"><strong>{subject.name}</strong><span>{subject.correct}/{subject.attempted} · {subject.score}%</span></div><div className="h-6 overflow-hidden rounded-lg bg-[#E9ECEF]"><div className="h-full rounded-lg bg-gradient-to-r from-[#3B86D1] to-[#63A7E8]" style={{ width: `${subject.score}%` }} /></div></div>)}</div></section>
      <section className="rounded-2xl border border-[#E9ECEF] p-5"><h3 className="font-bold">난이도별 풀이 비율</h3><p className="mt-1 text-xs text-[#6C757D]">푼 문제를 난이도별로 구분했습니다.</p><div className="mt-6 flex flex-col items-center gap-6"><div className="relative h-44 w-44 rounded-full" style={{ background: gradient }}><div className="absolute inset-9 flex flex-col items-center justify-center rounded-full bg-white shadow-inner"><strong className="text-3xl">{detail.total_attempted}</strong><span className="text-xs text-[#6C757D]">총 풀이</span></div></div><div className="w-full space-y-2">{difficultyStats.map((item) => <div key={item.difficulty} className="flex items-center gap-3 text-sm"><span className="h-3 w-3 rounded-full" style={{ backgroundColor: difficultyColors[item.difficulty] }} /><span className="flex-1 font-semibold">{difficultyLabels[item.difficulty] ?? item.difficulty}</span><strong>{item.count}문항</strong><span className="w-10 text-right text-[#6C757D]">{Math.round(item.count / detail.total_attempted * 100)}%</span></div>)}</div></div></section>
    </div>}
  </div>;
}

function Metric({ label, value, color, note }: { label: string; value: string; color: string; note: string }) { return <div className="surface-card p-5" style={{ borderTop: `4px solid ${color}` }}><p className="text-sm font-semibold text-[#6C757D]">{label}</p><strong className="mt-2 block text-3xl" style={{ color }}>{value}</strong><p className="mt-2 text-xs text-[#6C757D]">{note}</p></div>; }
function Rate({ value, color }: { value: number; color: string }) { return <div className="min-w-[110px]"><strong style={{ color }}>{value}%</strong><div className="mt-1 h-2 overflow-hidden rounded-full bg-[#E9ECEF]"><div className="h-full rounded-full" style={{ width: `${value}%`, backgroundColor: color }} /></div></div>; }
export default function Analytics() { return <ProtectedPage><AnalyticsPage /></ProtectedPage>; }
