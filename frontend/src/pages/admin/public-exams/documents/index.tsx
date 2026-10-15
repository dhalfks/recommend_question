import { FormEvent, useEffect, useState } from 'react';
import Link from 'next/link';
import Footer from '@/components/Footer';
import Navbar from '@/components/Navbar';
import ProtectedPage from '@/components/ProtectedPage';
import { PublicExam, PublicExamRound, PublicExamSourceDocument, PublicExamSubject, publicExamsAPI } from '@/lib/api';

function message(error: unknown) {
  return (error as { response?: { data?: { detail?: string } } }).response?.data?.detail ?? '요청을 처리하지 못했습니다.';
}

export default function PublicExamDocumentsPage() {
  const [exams, setExams] = useState<PublicExam[]>([]);
  const [rounds, setRounds] = useState<PublicExamRound[]>([]);
  const [subjects, setSubjects] = useState<PublicExamSubject[]>([]);
  const [documents, setDocuments] = useState<PublicExamSourceDocument[]>([]);
  const [examId, setExamId] = useState(0); const [roundId, setRoundId] = useState(0); const [subjectId, setSubjectId] = useState(0);
  const [file, setFile] = useState<File | null>(null); const [busy, setBusy] = useState(false);
  const [error, setError] = useState(''); const [notice, setNotice] = useState('');

  useEffect(() => { publicExamsAPI.adminGetExams().then(({ data }) => { setExams(data); setExamId(data[0]?.id ?? 0); }).catch((caught) => setError(message(caught))); }, []);
  useEffect(() => { if (!examId) return; publicExamsAPI.adminGetRounds(examId).then(({ data }) => { setRounds(data); setRoundId(data[0]?.id ?? 0); }).catch((caught) => setError(message(caught))); }, [examId]);
  useEffect(() => {
    if (!roundId) { setSubjects([]); setDocuments([]); return; }
    Promise.all([publicExamsAPI.adminGetSubjects(roundId), publicExamsAPI.adminGetDocuments(roundId)])
      .then(([subjectResponse, documentResponse]) => { setSubjects(subjectResponse.data); setSubjectId(subjectResponse.data[0]?.id ?? 0); setDocuments(documentResponse.data); })
      .catch((caught) => setError(message(caught)));
  }, [roundId]);

  const upload = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault(); if (!file || !subjectId || busy) return;
    setBusy(true); setError(''); setNotice('PDF 저장 및 텍스트 추출 중입니다...');
    const values = new FormData(event.currentTarget); values.set('file', file);
    try {
      const response = await publicExamsAPI.adminUploadDocument(subjectId, values);
      setNotice(response.data.extraction_message || 'PDF를 등록했습니다. 문항을 반드시 원문과 대조해 주세요.');
      setFile(null); event.currentTarget.reset();
      const list = await publicExamsAPI.adminGetDocuments(roundId); setDocuments(list.data);
    } catch (caught) { setNotice(''); setError(message(caught)); } finally { setBusy(false); }
  };

  return <ProtectedPage roles={['ADMIN']}><div className="app-shell flex min-h-screen flex-col"><Navbar />
    <main className="page-container flex-1 py-10"><div className="mb-7 flex flex-wrap items-end justify-between gap-3"><div><p className="font-semibold text-[#8B5CF6]">ADMIN</p><h1 className="text-3xl font-bold">PDF 등록 문서</h1></div><Link href="/admin/public-exams" className="secondary-button">시험 구조 관리</Link></div>
      {error && <div className="mb-5 rounded-xl border border-red-200 bg-red-50 p-4 text-red-700">{error}</div>}{notice && <div className="mb-5 rounded-xl border border-blue-200 bg-blue-50 p-4 text-blue-800">{notice}</div>}
      <section className="surface-card mb-7 p-6"><h2 className="text-xl font-bold">PDF 업로드 및 자동 추출</h2><p className="mt-2 text-sm text-[#6C757D]">자동 추출은 후보 생성 단계입니다. 정답을 추측하지 않으며 모든 문항은 DRAFT·정답 미확인 상태로 등록됩니다.</p>
        <form className="mt-5 grid gap-4 md:grid-cols-2" onSubmit={upload}>
          <select className="form-control" value={examId} onChange={(e) => setExamId(Number(e.target.value))} required><option value={0}>시험 선택</option>{exams.map((exam) => <option key={exam.id} value={exam.id}>{exam.name}</option>)}</select>
          <select className="form-control" value={roundId} onChange={(e) => setRoundId(Number(e.target.value))} required><option value={0}>회차 선택</option>{rounds.map((round) => <option key={round.id} value={round.id}>{round.exam_year}년 {round.round_identifier}</option>)}</select>
          <select className="form-control" value={subjectId} onChange={(e) => setSubjectId(Number(e.target.value))} required><option value={0}>과목 선택</option>{subjects.map((subject) => <option key={subject.id} value={subject.id}>{subject.name}</option>)}</select>
          <input className="form-control" type="file" accept="application/pdf,.pdf" required onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
          <input className="form-control" name="source_organization" placeholder="출처 기관" /><input className="form-control" name="source_url" type="url" placeholder="출처 URL" />
          <textarea className="form-control md:col-span-2" name="source_notes" placeholder="출처 및 검수 메모" />
          <label className="flex items-center gap-2 text-sm"><input type="checkbox" name="is_test_data" value="true" /> 테스트용 문서로 명확히 표시</label>
          <button className="primary-button" disabled={busy || !file || !subjectId}>{busy ? '처리 중...' : 'PDF 등록 및 후보 추출'}</button>
        </form>
      </section>
      <section className="space-y-3"><h2 className="text-xl font-bold">등록 문서</h2>{documents.length ? documents.map((document) => <Link key={document.id} href={`/admin/public-exams/documents/${document.id}`} className="surface-card block p-5 transition hover:border-[#3B86D1]"><div className="flex flex-wrap justify-between gap-3"><div><strong>{document.original_file_name}</strong><p className="mt-1 text-sm text-[#6C757D]">{document.source_organization || '출처 기관 미입력'} · {new Date(document.uploaded_at).toLocaleString()}</p>{document.source_notes?.startsWith('[TEST DATA]') && <span className="mt-2 inline-block rounded bg-amber-100 px-2 py-1 text-xs font-bold text-amber-800">TEST DATA</span>}</div><div className="text-right text-sm"><p>추출 {document.question_count}문항</p><p>검수 {document.verified_count} · 게시 {document.published_count}</p></div></div></Link>) : <div className="surface-card p-10 text-center text-[#6C757D]">선택한 회차에 등록된 PDF가 없습니다.</div>}</section>
    </main><Footer /></div></ProtectedPage>;
}
