import { useCallback, useEffect, useMemo, useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import Footer from '@/components/Footer';
import Navbar from '@/components/Navbar';
import ProtectedPage from '@/components/ProtectedPage';
import { PublicExamQuestionAdmin, PublicExamSourceDocumentDetail, publicExamsAPI } from '@/lib/api';

type QuestionDraft = Pick<PublicExamQuestionAdmin, 'content' | 'question_type' | 'correct_option' | 'correct_answer' | 'explanation' | 'answer_verification_status' | 'review_notes'> & { optionsText: string };

function message(error: unknown) {
  return (error as { response?: { data?: { detail?: string | Array<{ msg?: string }> } } }).response?.data?.detail instanceof Array
    ? (error as { response: { data: { detail: Array<{ msg?: string }> } } }).response.data.detail.map((item) => item.msg).join(', ')
    : String((error as { response?: { data?: { detail?: string } } }).response?.data?.detail ?? '요청을 처리하지 못했습니다.');
}

function toDraft(question: PublicExamQuestionAdmin): QuestionDraft {
  return { content: question.content, question_type: question.question_type, optionsText: (question.options ?? []).join('\n'), correct_option: question.correct_option, correct_answer: question.correct_answer, explanation: question.explanation, answer_verification_status: question.answer_verification_status, review_notes: question.review_notes };
}

export default function PublicExamDocumentReviewPage() {
  const router = useRouter(); const documentId = typeof router.query.documentId === 'string' ? Number(router.query.documentId) : 0;
  const [document, setDocument] = useState<PublicExamSourceDocumentDetail | null>(null);
  const [drafts, setDrafts] = useState<Record<number, QuestionDraft>>({});
  const [saving, setSaving] = useState<Record<number, boolean>>({}); const [publishing, setPublishing] = useState(false);
  const [error, setError] = useState(''); const [notice, setNotice] = useState('');

  const load = useCallback(async () => {
    const response = await publicExamsAPI.adminGetDocument(documentId); setDocument(response.data);
    setDrafts(Object.fromEntries(response.data.questions.map((question) => [question.id, toDraft(question)])));
  }, [documentId]);
  useEffect(() => { if (documentId) load().catch((caught) => setError(message(caught))); }, [documentId, load]);

  const allPublishable = useMemo(() => Boolean(document?.questions.length) && document!.questions.every((question) => question.answer_verification_status === 'VERIFIED' && (question.question_type === 'MULTIPLE_CHOICE' ? question.correct_option != null : Boolean(question.correct_answer?.trim()))), [document]);
  const change = <K extends keyof QuestionDraft>(id: number, key: K, value: QuestionDraft[K]) => setDrafts((current) => ({ ...current, [id]: { ...current[id], [key]: value } }));

  const save = async (question: PublicExamQuestionAdmin) => {
    const draft = drafts[question.id]; if (!draft) return; setSaving((current) => ({ ...current, [question.id]: true })); setError(''); setNotice('');
    const options = draft.question_type === 'MULTIPLE_CHOICE' ? draft.optionsText.split('\n').map((item) => item.trim()).filter(Boolean) : null;
    const verified = draft.answer_verification_status === 'VERIFIED';
    try {
      await publicExamsAPI.adminUpdateQuestion(question.id, {
        content: draft.content, question_type: draft.question_type, options,
        correct_option: draft.question_type === 'MULTIPLE_CHOICE' && draft.answer_verification_status !== 'MISSING' ? draft.correct_option || null : null,
        correct_answer: draft.question_type === 'SHORT_ANSWER' && draft.answer_verification_status !== 'MISSING' ? draft.correct_answer?.trim() || null : null,
        explanation: draft.explanation?.trim() || null, answer_verification_status: draft.answer_verification_status,
        publication_status: verified ? 'READY' : 'DRAFT', review_notes: draft.review_notes?.trim() || null,
      });
      setNotice(`${question.question_number}번 문항을 저장했습니다.`); await load();
    } catch (caught) { setError(message(caught)); } finally { setSaving((current) => ({ ...current, [question.id]: false })); }
  };

  const openPdf = async () => {
    setError(''); try { const response = await publicExamsAPI.adminOpenDocument(documentId); const url = URL.createObjectURL(response.data); window.open(url, '_blank', 'noopener,noreferrer'); window.setTimeout(() => URL.revokeObjectURL(url), 60000); } catch (caught) { setError(message(caught)); }
  };
  const publish = async () => {
    if (!allPublishable || publishing || !window.confirm('검수 완료된 문항을 학생에게 게시 가능한 상태로 전환할까요?')) return;
    setPublishing(true); setError(''); try { const response = await publicExamsAPI.adminPublishDocument(documentId); setNotice(`${response.data.published_count}개 문항을 게시했습니다. 회차가 공개 상태인지도 확인하세요.`); await load(); } catch (caught) { setError(message(caught)); } finally { setPublishing(false); }
  };

  return <ProtectedPage roles={['ADMIN']}><div className="app-shell flex min-h-screen flex-col"><Navbar />
    <main className="page-container flex-1 py-10"><div className="mb-7 flex flex-wrap items-end justify-between gap-3"><div><p className="font-semibold text-[#8B5CF6]">PDF REVIEW</p><h1 className="text-3xl font-bold">{document?.original_file_name || '문서 불러오는 중...'}</h1></div><div className="flex gap-2"><Link className="secondary-button" href="/admin/public-exams/documents">문서 목록</Link><button className="primary-button" onClick={openPdf} disabled={!document}>원본 PDF 열기</button></div></div>
      {document?.source_notes?.startsWith('[TEST DATA]') && <div className="mb-5 rounded-xl border border-amber-300 bg-amber-50 p-4 font-bold text-amber-800">이 문서는 테스트 데이터로 표시되어 있습니다.</div>}
      {error && <div className="mb-5 rounded-xl border border-red-200 bg-red-50 p-4 text-red-700">{error}</div>}{notice && <div className="mb-5 rounded-xl border border-green-200 bg-green-50 p-4 text-green-800">{notice}</div>}
      {document && <div className="mb-6 flex flex-wrap items-center justify-between gap-4 rounded-xl bg-[#242C34] p-5 text-white"><div>추출 {document.question_count} · 검수 {document.verified_count} · 게시 {document.published_count}</div><button className="success-button" disabled={!allPublishable || publishing} onClick={publish}>{publishing ? '게시 중...' : allPublishable ? '검수 완료 문항 전체 게시' : '모든 정답 검수 후 게시 가능'}</button></div>}
      <section className="space-y-6">{document?.questions.map((question) => { const draft = drafts[question.id]; if (!draft) return null; return <article key={question.id} className="surface-card p-6"><div className="mb-4 flex flex-wrap justify-between gap-2"><h2 className="text-xl font-bold">문항 {question.question_number}</h2><span className="text-sm text-[#6C757D]">PDF {question.source_page ? `${question.source_page}쪽` : '쪽 미확인'} · {question.publication_status}</span></div>
        <label className="block text-sm font-semibold">문제 본문<textarea className="form-control mt-2" rows={6} value={draft.content} onChange={(e) => change(question.id, 'content', e.target.value)} /></label>
        <div className="mt-4 grid gap-4 md:grid-cols-2"><label className="text-sm font-semibold">유형<select className="form-control mt-2" value={draft.question_type} onChange={(e) => change(question.id, 'question_type', e.target.value as QuestionDraft['question_type'])}><option value="MULTIPLE_CHOICE">객관식</option><option value="SHORT_ANSWER">단답형</option></select></label><label className="text-sm font-semibold">검수 상태<select className="form-control mt-2" value={draft.answer_verification_status} onChange={(e) => change(question.id, 'answer_verification_status', e.target.value as QuestionDraft['answer_verification_status'])}><option value="MISSING">정답 없음</option><option value="UNVERIFIED">정답 미검수</option><option value="VERIFIED">검수 완료</option></select></label></div>
        {draft.question_type === 'MULTIPLE_CHOICE' ? <div className="mt-4 grid gap-4 md:grid-cols-[1fr_180px]"><label className="text-sm font-semibold">보기 (한 줄에 하나)<textarea className="form-control mt-2" rows={6} value={draft.optionsText} onChange={(e) => change(question.id, 'optionsText', e.target.value)} /></label><label className="text-sm font-semibold">정답 보기 번호<input className="form-control mt-2" type="number" min="1" value={draft.correct_option ?? ''} onChange={(e) => change(question.id, 'correct_option', e.target.value ? Number(e.target.value) : null)} disabled={draft.answer_verification_status === 'MISSING'} /></label></div> : <label className="mt-4 block text-sm font-semibold">정답<input className="form-control mt-2" value={draft.correct_answer ?? ''} onChange={(e) => change(question.id, 'correct_answer', e.target.value)} disabled={draft.answer_verification_status === 'MISSING'} /></label>}
        <label className="mt-4 block text-sm font-semibold">해설<textarea className="form-control mt-2" rows={4} value={draft.explanation ?? ''} onChange={(e) => change(question.id, 'explanation', e.target.value)} /></label><label className="mt-4 block text-sm font-semibold">검수 메모<textarea className="form-control mt-2" rows={2} value={draft.review_notes ?? ''} onChange={(e) => change(question.id, 'review_notes', e.target.value)} /></label>
        <div className="mt-5 flex justify-end"><button className="primary-button" disabled={saving[question.id]} onClick={() => save(question)}>{saving[question.id] ? '저장 중...' : '문항 저장'}</button></div>
      </article>; })}</section>
    </main><Footer /></div></ProtectedPage>;
}
