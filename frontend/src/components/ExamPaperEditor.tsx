import { DragEvent, useEffect, useMemo, useState } from 'react';
import { useRouter } from 'next/router';
import Footer from '@/components/Footer';
import Navbar from '@/components/Navbar';
import ProtectedPage from '@/components/ProtectedPage';
import { ExamPaper, QuestionBankQuestion, examPapersAPI, questionsAPI, subjectsAPI } from '@/lib/api';

type Subject = { id: number; name: string };

function errorMessage(error: unknown, fallback: string) {
  if (typeof error === 'object' && error && 'response' in error) {
    const response = (error as { response?: { data?: { detail?: unknown } } }).response;
    if (typeof response?.data?.detail === 'string') return response.data.detail;
  }
  return fallback;
}

function setDragPayload(event: DragEvent, value: string) {
  event.dataTransfer.effectAllowed = 'move';
  event.dataTransfer.setData('text/plain', value);
}

export default function ExamPaperEditor({ paperId }: { paperId?: number }) {
  const router = useRouter();
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [questions, setQuestions] = useState<QuestionBankQuestion[]>([]);
  const [selectedIds, setSelectedIds] = useState<number[]>([]);
  const [subjectId, setSubjectId] = useState('');
  const [search, setSearch] = useState('');
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    let active = true;
    const load = async () => {
      setLoading(true); setError('');
      try {
        const paperRequest: Promise<{ data: ExamPaper | null }> = paperId
          ? examPapersAPI.get(paperId)
          : Promise.resolve({ data: null });
        const [subjectResponse, questionResponse, paperResponse] = await Promise.all([
          subjectsAPI.getAll(), questionsAPI.getAll({ limit: 1000 }), paperRequest,
        ]);
        if (!active) return;
        setSubjects(subjectResponse.data);
        setQuestions(questionResponse.data);
        if (paperResponse.data) {
          setTitle(paperResponse.data.title);
          setDescription(paperResponse.data.description ?? '');
          setSelectedIds([...paperResponse.data.items]
            .sort((a, b) => a.display_order - b.display_order)
            .map((item) => item.question_id));
        }
      } catch (caught) {
        if (active) setError(errorMessage(caught, '시험지 편집 정보를 불러오지 못했습니다.'));
      } finally {
        if (active) setLoading(false);
      }
    };
    load();
    return () => { active = false; };
  }, [paperId]);

  const subjectNames = useMemo(() => new Map(subjects.map((subject) => [subject.id, subject.name])), [subjects]);
  const questionById = useMemo(() => new Map(questions.map((question) => [question.id, question])), [questions]);
  const selectedQuestions = selectedIds.map((id) => questionById.get(id)).filter((question): question is QuestionBankQuestion => Boolean(question));
  const availableQuestions = useMemo(() => {
    const keyword = search.trim().toLocaleLowerCase();
    const selected = new Set(selectedIds);
    return questions.filter((question) => !selected.has(question.id)
      && (!subjectId || question.subject_id === Number(subjectId))
      && (!keyword || `${question.title} ${question.content} ${question.subject_unit ?? ''}`.toLocaleLowerCase().includes(keyword)));
  }, [questions, search, selectedIds, subjectId]);

  const addQuestion = (questionId: number, at = selectedIds.length) => {
    setSelectedIds((current) => {
      if (current.includes(questionId)) return current;
      const next = [...current]; next.splice(at, 0, questionId); return next;
    });
  };
  const moveQuestion = (from: number, to: number) => setSelectedIds((current) => {
    if (from === to || from < 0 || from >= current.length) return current;
    const next = [...current]; const [item] = next.splice(from, 1);
    next.splice(Math.max(0, Math.min(to, next.length)), 0, item); return next;
  });
  const dropAt = (event: DragEvent, index: number) => {
    event.preventDefault();
    const [kind, raw] = event.dataTransfer.getData('text/plain').split(':');
    const value = Number(raw);
    if (!Number.isInteger(value)) return;
    if (kind === 'source') addQuestion(value, index);
    if (kind === 'paper') moveQuestion(value, index);
  };

  const save = async () => {
    if (!title.trim()) { setError('시험지 제목을 입력해 주세요.'); return; }
    if (!selectedIds.length) { setError('시험지에 문항을 한 개 이상 추가해 주세요.'); return; }
    setSaving(true); setError('');
    try {
      const payload = { title: title.trim(), description: description.trim() || null, question_ids: selectedIds };
      const response = paperId ? await examPapersAPI.update(paperId, payload) : await examPapersAPI.create(payload);
      await router.push(`/exam-papers/${response.data.id}`);
    } catch (caught) {
      setError(errorMessage(caught, '시험지를 저장하지 못했습니다.'));
    } finally { setSaving(false); }
  };

  return <ProtectedPage roles={['PROFESSOR']}><div className="app-shell flex min-h-screen flex-col"><Navbar />
    <main className="page-container flex-1 py-8">
      <div className="mb-6 flex flex-wrap items-end justify-between gap-3"><div><p className="font-semibold text-[#3B86D1]">EXAM PAPER</p><h1 className="text-3xl font-bold">{paperId ? '시험지 편집' : '새 시험지 만들기'}</h1></div><button type="button" className="secondary-button" onClick={() => router.push('/exam-papers')}>시험지 목록</button></div>
      {error && <div role="alert" className="mb-5 rounded-xl bg-red-50 p-4 text-red-700">{error}</div>}
      {loading ? <div className="surface-card p-10 text-center text-[#6C757D]">불러오는 중...</div> : <>
        <section className="surface-card mb-6 grid gap-4 p-5 md:grid-cols-2"><label className="text-sm font-semibold">시험지 제목<input className="form-control mt-2" value={title} maxLength={255} onChange={(event) => setTitle(event.target.value)} /></label><label className="text-sm font-semibold">설명<input className="form-control mt-2" value={description} maxLength={2000} onChange={(event) => setDescription(event.target.value)} placeholder="선택 사항" /></label></section>
        <div className="grid gap-6 lg:grid-cols-2">
          <section className="surface-card min-w-0 overflow-hidden"><div className="border-b border-[#E9ECEF] p-5"><h2 className="text-xl font-bold">문제 목록</h2><div className="mt-4 grid gap-3 sm:grid-cols-2"><select className="form-control" value={subjectId} onChange={(event) => setSubjectId(event.target.value)}><option value="">전체 과목</option>{subjects.map((subject) => <option key={subject.id} value={subject.id}>{subject.name}</option>)}</select><input className="form-control" value={search} onChange={(event) => setSearch(event.target.value)} placeholder="제목·본문·단원 검색" /></div></div>
            <div className="max-h-[65vh] space-y-3 overflow-y-auto p-4">{!availableQuestions.length && <p className="p-6 text-center text-[#6C757D]">조건에 맞는 추가 가능한 문제가 없습니다.</p>}{availableQuestions.map((question) => <article key={question.id} draggable onDragStart={(event) => setDragPayload(event, `source:${question.id}`)} className="cursor-grab rounded-xl border border-[#DCE3EA] bg-white p-4 active:cursor-grabbing"><div className="flex items-start justify-between gap-3"><div><span className="text-xs font-bold text-[#3B86D1]">{subjectNames.get(question.subject_id) ?? '과목 미확인'}</span><h3 className="mt-1 font-bold">{question.title}</h3></div><button type="button" className="shrink-0 rounded-lg bg-[#EAF3FC] px-3 py-2 text-sm font-bold text-[#245E96]" onClick={() => addQuestion(question.id)}>추가</button></div><p className="mt-2 line-clamp-3 whitespace-pre-wrap text-sm text-[#6C757D]">{question.content}</p></article>)}</div>
          </section>
          <section className="surface-card min-w-0 overflow-hidden"><div className="flex items-center justify-between border-b border-[#E9ECEF] p-5"><div><h2 className="text-xl font-bold">시험지</h2><p className="mt-1 text-sm text-[#6C757D]">{selectedIds.length}문항 · 끌어서 순서 변경</p></div><button type="button" className="primary-button" disabled={saving} onClick={save}>{saving ? '저장 중...' : '저장'}</button></div>
            <div className="min-h-72 max-h-[65vh] space-y-3 overflow-y-auto p-4" onDragOver={(event) => event.preventDefault()} onDrop={(event) => dropAt(event, selectedIds.length)}>{!selectedQuestions.length && <div className="flex min-h-56 items-center justify-center rounded-xl border-2 border-dashed border-[#CCD5DE] p-8 text-center text-[#6C757D]">왼쪽 문제를 이곳으로 끌거나<br />추가 버튼을 눌러 주세요.</div>}{selectedQuestions.map((question, index) => <article key={question.id} draggable onDragStart={(event) => setDragPayload(event, `paper:${index}`)} onDragOver={(event) => event.preventDefault()} onDrop={(event) => { event.stopPropagation(); dropAt(event, index); }} className="cursor-grab rounded-xl border border-[#DCE3EA] bg-[#F8F9FA] p-4 active:cursor-grabbing"><div className="flex items-start gap-3"><span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-[#3B86D1] font-bold text-white">{index + 1}</span><div className="min-w-0 flex-1"><span className="text-xs font-bold text-[#3B86D1]">{subjectNames.get(question.subject_id) ?? '과목 미확인'}</span><h3 className="font-bold">{question.title}</h3><p className="mt-1 line-clamp-2 whitespace-pre-wrap text-sm text-[#6C757D]">{question.content}</p></div><div className="flex shrink-0 gap-1"><button type="button" aria-label="위로 이동" disabled={index === 0} className="rounded bg-white px-2 py-1 disabled:opacity-30" onClick={() => moveQuestion(index, index - 1)}>↑</button><button type="button" aria-label="아래로 이동" disabled={index === selectedIds.length - 1} className="rounded bg-white px-2 py-1 disabled:opacity-30" onClick={() => moveQuestion(index, index + 1)}>↓</button><button type="button" aria-label="시험지에서 제거" className="rounded bg-red-50 px-2 py-1 text-red-700" onClick={() => setSelectedIds((current) => current.filter((id) => id !== question.id))}>×</button></div></div></article>)}</div>
          </section>
        </div>
      </>}
    </main><Footer /></div></ProtectedPage>;
}
