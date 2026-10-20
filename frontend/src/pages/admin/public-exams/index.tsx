import { FormEvent, useEffect, useState } from 'react';
import Link from 'next/link';
import Footer from '@/components/Footer';
import Navbar from '@/components/Navbar';
import ProtectedPage from '@/components/ProtectedPage';
import { PublicExam, PublicExamRound, PublicExamSubject, publicExamsAPI } from '@/lib/api';

function message(error: unknown) {
  return (error as { response?: { data?: { detail?: string } } }).response?.data?.detail ?? '요청을 처리하지 못했습니다.';
}

export default function PublicExamAdminPage() {
  const [exams, setExams] = useState<PublicExam[]>([]);
  const [rounds, setRounds] = useState<PublicExamRound[]>([]);
  const [subjects, setSubjects] = useState<PublicExamSubject[]>([]);
  const [examId, setExamId] = useState<number | null>(null);
  const [roundId, setRoundId] = useState<number | null>(null);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  const loadExams = async () => {
    const response = await publicExamsAPI.adminGetExams();
    setExams(response.data);
    setExamId((current) => current ?? response.data[0]?.id ?? null);
  };
  const loadRounds = async (selectedExamId: number) => {
    const response = await publicExamsAPI.adminGetRounds(selectedExamId);
    setRounds(response.data);
    setRoundId(response.data[0]?.id ?? null);
  };
  const loadSubjects = async (selectedRoundId: number) => {
    const response = await publicExamsAPI.adminGetSubjects(selectedRoundId);
    setSubjects(response.data);
  };

  useEffect(() => { loadExams().catch((caught) => setError(message(caught))); }, []);
  useEffect(() => {
    if (!examId) { setRounds([]); setRoundId(null); return; }
    loadRounds(examId).catch((caught) => setError(message(caught)));
  }, [examId]);
  useEffect(() => {
    if (!roundId) { setSubjects([]); return; }
    loadSubjects(roundId).catch((caught) => setError(message(caught)));
  }, [roundId]);

  const createExam = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault(); setBusy(true); setError('');
    const form = new FormData(event.currentTarget);
    try {
      await publicExamsAPI.adminCreateExam({ code: String(form.get('code')), name: String(form.get('name')), description: String(form.get('description') || ''), is_active: true });
      event.currentTarget.reset(); await loadExams();
    } catch (caught) { setError(message(caught)); } finally { setBusy(false); }
  };
  const createRound = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault(); if (!examId) return; setBusy(true); setError('');
    const form = new FormData(event.currentTarget);
    try {
      await publicExamsAPI.adminCreateRound(examId, { exam_year: Number(form.get('year')), round_identifier: String(form.get('identifier')), display_name: String(form.get('display_name') || ''), is_published: false });
      event.currentTarget.reset(); await loadRounds(examId);
    } catch (caught) { setError(message(caught)); } finally { setBusy(false); }
  };
  const createSubject = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault(); if (!roundId) return; setBusy(true); setError('');
    const form = new FormData(event.currentTarget);
    try {
      await publicExamsAPI.adminCreateSubject(roundId, { code: String(form.get('code') || ''), name: String(form.get('name')), display_order: Number(form.get('order')) });
      event.currentTarget.reset(); await loadSubjects(roundId);
    } catch (caught) { setError(message(caught)); } finally { setBusy(false); }
  };

  return <ProtectedPage roles={['ADMIN']}><div className="app-shell flex min-h-screen flex-col"><Navbar />
    <main className="page-container flex-1 py-10">
      <div className="mb-7 flex flex-wrap items-end justify-between gap-4"><div><p className="font-semibold text-[#8B5CF6]">ADMIN</p><h1 className="text-3xl font-bold">공통 기출 콘텐츠 관리</h1></div>
        <Link className="primary-button" href="/admin/public-exams/documents">PDF 문서 관리</Link></div>
      {error && <div className="mb-6 rounded-xl border border-red-200 bg-red-50 p-4 text-red-700">{error}</div>}
      <div className="grid gap-6 lg:grid-cols-3">
        <section className="surface-card p-6 lg:col-span-2"><h2 className="text-xl font-bold">1. 시험·연도·회차</h2>
          <p className="mt-2 text-sm text-[#6C757D]">시험을 선택한 뒤 해당 시험의 연도·회차를 한 화면에서 관리합니다.</p>
          <div className="mt-4 grid gap-4 md:grid-cols-2">
            <label className="text-sm font-semibold">시험<select className="form-control mt-2" value={examId ?? ''} onChange={(e) => setExamId(Number(e.target.value))}><option value="">시험 선택</option>{exams.map((exam) => <option key={exam.id} value={exam.id}>{exam.name}{exam.is_active ? '' : ' (비활성)'}</option>)}</select></label>
            <label className="text-sm font-semibold">연도·회차<select className="form-control mt-2" value={roundId ?? ''} onChange={(e) => setRoundId(Number(e.target.value))}><option value="">연도·회차 선택</option>{rounds.map((round) => <option key={round.id} value={round.id}>{round.exam_year}년 {round.round_identifier}{round.is_published ? ' · 공개' : ' · 비공개'}</option>)}</select></label>
          </div>
          {roundId && <button className="secondary-button mt-4 w-full" disabled={busy} onClick={async () => { const round = rounds.find((item) => item.id === roundId); if (!round) return; setBusy(true); setError(''); try { await publicExamsAPI.adminUpdateRound(round.id, { is_published: !round.is_published }); await loadRounds(examId!); } catch (caught) { setError(message(caught)); } finally { setBusy(false); } }}>{rounds.find((item) => item.id === roundId)?.is_published ? '선택 회차 비공개 전환' : '선택 회차 검수 후 공개'}</button>}
          <div className="mt-5 grid gap-5 border-t pt-5 md:grid-cols-2">
            <form className="space-y-3" onSubmit={createExam}><h3 className="font-bold">새 시험 추가</h3><input className="form-control" name="code" placeholder="시험 코드 (예: SQLD)" required /><input className="form-control" name="name" placeholder="시험명" required /><textarea className="form-control" name="description" placeholder="설명" /><button className="success-button w-full" disabled={busy}>시험 추가</button></form>
            <form className="space-y-3" onSubmit={createRound}><h3 className="font-bold">선택 시험에 연도·회차 추가</h3><input className="form-control" name="year" type="number" min="1900" max="2200" placeholder="연도" required /><input className="form-control" name="identifier" placeholder="회차 식별자" required /><input className="form-control" name="display_name" placeholder="표시명 (선택)" /><button className="success-button w-full" disabled={busy || !examId}>연도·회차 추가</button></form>
          </div>
        </section>
        <section className="surface-card p-6"><h2 className="text-xl font-bold">2. 과목</h2>
          <div className="my-4 space-y-2">{subjects.length ? subjects.map((subject) => <div key={subject.id} className="rounded-lg border p-3"><strong>{subject.display_order}. {subject.name}</strong><p className="text-sm text-[#6C757D]">{subject.code || '코드 없음'}</p></div>) : <p className="text-sm text-[#6C757D]">등록된 과목이 없습니다.</p>}</div>
          <form className="space-y-3 border-t pt-4" onSubmit={createSubject}><input className="form-control" name="name" placeholder="과목명" required /><input className="form-control" name="code" placeholder="과목 코드 (선택)" /><input className="form-control" name="order" type="number" min="1" defaultValue={subjects.length + 1} required /><button className="success-button w-full" disabled={busy || !roundId}>과목 추가</button></form>
        </section>
      </div>
    </main><Footer /></div></ProtectedPage>;
}
