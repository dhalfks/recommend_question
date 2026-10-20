import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import ProtectedPage from '@/components/ProtectedPage';
import { ExamPaper, ExamPaperItem, examPapersAPI } from '@/lib/api';

function answerText(item: ExamPaperItem) {
  if (item.answer_type === 'MULTIPLE_CHOICE') {
    if (item.correct_option) return `${item.correct_option}번`;
    const legacyIndex = Number(item.correct_answer);
    if (item.correct_answer != null && Number.isInteger(legacyIndex) && legacyIndex >= 0 && legacyIndex < (item.options?.length ?? 0)) return `${legacyIndex + 1}번`;
    return item.correct_answer || '정답 미등록';
  }
  return item.correct_answer || '정답 미등록';
}

export default function PrintExamPaperPage() {
  const router = useRouter();
  const [paper, setPaper] = useState<ExamPaper | null>(null);
  const [showAnswers, setShowAnswers] = useState(false);
  const [error, setError] = useState('');
  const raw = router.query.paperId;
  const paperId = typeof raw === 'string' ? Number(raw) : NaN;
  useEffect(() => {
    if (!router.isReady || !Number.isInteger(paperId) || paperId <= 0) return;
    examPapersAPI.get(paperId).then((response) => setPaper(response.data)).catch(() => setError('시험지를 불러오지 못했습니다.'));
  }, [paperId, router.isReady]);
  return <ProtectedPage roles={['PROFESSOR']}><div className="min-h-screen bg-[#E9ECEF] print:bg-white">
    <div className="print-toolbar sticky top-0 z-10 flex flex-wrap items-center justify-center gap-3 bg-[#242C34] p-4 text-white"><button type="button" className="rounded-lg bg-white px-4 py-2 font-bold text-[#242C34]" onClick={() => router.back()}>편집으로</button><label className="flex items-center gap-2"><input type="checkbox" checked={showAnswers} onChange={(event) => setShowAnswers(event.target.checked)} />정답·해설지 포함</label><button type="button" className="rounded-lg bg-[#3B86D1] px-4 py-2 font-bold" onClick={() => window.print()} disabled={!paper}>인쇄 / PDF 저장</button></div>
    {error ? <main className="mx-auto mt-8 max-w-3xl bg-white p-8 text-red-700">{error}</main> : !paper ? <main className="p-10 text-center">불러오는 중...</main> : <>
      <main className="print-sheet mx-auto my-8 min-h-[297mm] w-[210mm] bg-white px-[18mm] py-[16mm] text-black shadow print:m-0 print:shadow-none"><header className="mb-8 border-b-2 border-black pb-5 text-center"><h1 className="text-3xl font-bold">{paper.title}</h1>{paper.description && <p className="mt-3 whitespace-pre-wrap">{paper.description}</p>}<div className="mt-5 flex justify-end gap-8 text-sm"><span>학번: __________________</span><span>이름: __________________</span></div></header><section>{[...paper.items].sort((a, b) => a.display_order - b.display_order).map((item) => <article key={item.id} className="question-block mb-8 break-inside-avoid"><p className="mb-2 text-xs font-semibold text-gray-500">{item.subject_name}</p><h2 className="text-lg font-bold">{item.display_order}. {item.title}</h2><p className="mt-3 whitespace-pre-wrap leading-7">{item.content}</p>{item.code_snippet && <pre className="mt-3 overflow-hidden whitespace-pre-wrap border border-gray-400 bg-gray-50 p-3 font-mono text-sm"><code>{item.code_snippet}</code></pre>}{item.options?.length ? <ol className="mt-4 space-y-2">{item.options.map((option, index) => <li key={index}>{index + 1}) {option}</li>)}</ol> : <div className="mt-5 h-20 border-b border-gray-400" />}</article>)}</section></main>
      {showAnswers && <main className="print-sheet answer-sheet mx-auto my-8 min-h-[297mm] w-[210mm] bg-white px-[18mm] py-[16mm] text-black shadow print:m-0 print:shadow-none"><h1 className="mb-8 border-b-2 border-black pb-4 text-2xl font-bold">{paper.title} — 정답 및 해설</h1>{[...paper.items].sort((a, b) => a.display_order - b.display_order).map((item) => <article key={item.id} className="mb-6 break-inside-avoid"><h2 className="font-bold">{item.display_order}. {answerText(item)}</h2>{item.explanation && <p className="mt-2 whitespace-pre-wrap leading-7">{item.explanation}</p>}</article>)}</main>}
    </>}
    <style>{`@media print { @page { size: A4; margin: 0; } .print-toolbar { display: none !important; } .print-sheet { width: 210mm !important; min-height: 297mm !important; page-break-after: always; } .print-sheet:last-child { page-break-after: auto; } .question-block { break-inside: avoid; page-break-inside: avoid; } }`}</style>
  </div></ProtectedPage>;
}
