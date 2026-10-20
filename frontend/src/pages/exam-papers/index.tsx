import { useEffect, useState } from 'react';
import Link from 'next/link';
import Footer from '@/components/Footer';
import Navbar from '@/components/Navbar';
import ProtectedPage from '@/components/ProtectedPage';
import { ExamPaperSummary, examPapersAPI } from '@/lib/api';

function errorMessage(error: unknown) {
  if (typeof error === 'object' && error && 'response' in error) {
    const detail = (error as { response?: { data?: { detail?: unknown } } }).response?.data?.detail;
    if (typeof detail === 'string') return detail;
  }
  return '시험지 목록을 불러오지 못했습니다.';
}

export default function ExamPapersPage() {
  const [papers, setPapers] = useState<ExamPaperSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  useEffect(() => {
    examPapersAPI.list().then((response) => setPapers(response.data)).catch((caught) => setError(errorMessage(caught))).finally(() => setLoading(false));
  }, []);
  const remove = async (paper: ExamPaperSummary) => {
    if (!window.confirm(`“${paper.title}” 시험지를 삭제할까요?`)) return;
    try { await examPapersAPI.delete(paper.id); setPapers((current) => current.filter((item) => item.id !== paper.id)); }
    catch (caught) { setError(errorMessage(caught)); }
  };
  return <ProtectedPage roles={['PROFESSOR']}><div className="app-shell flex min-h-screen flex-col"><Navbar /><main className="page-container flex-1 py-10">
    <div className="mb-7 flex flex-wrap items-end justify-between gap-3"><div><p className="font-semibold text-[#3B86D1]">EXAM PAPERS</p><h1 className="text-3xl font-bold">시험지 출력</h1><p className="mt-2 text-[#6C757D]">과목별 문제를 골라 시험지를 만들고 PDF로 저장할 수 있습니다.</p></div><Link className="primary-button" href="/exam-papers/new">새 시험지</Link></div>
    {error && <div role="alert" className="mb-5 rounded-xl bg-red-50 p-4 text-red-700">{error}</div>}
    {loading ? <div className="surface-card p-10 text-center">불러오는 중...</div> : !papers.length ? <div className="surface-card p-10 text-center text-[#6C757D]">저장된 시험지가 없습니다.</div> : <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">{papers.map((paper) => <article key={paper.id} className="surface-card p-5"><h2 className="text-xl font-bold">{paper.title}</h2><p className="mt-2 min-h-10 text-sm text-[#6C757D]">{paper.description || '설명 없음'}</p><p className="mt-4 text-sm font-semibold">{paper.item_count}문항 · {new Date(paper.updated_at).toLocaleDateString()}</p><div className="mt-5 flex flex-wrap gap-2"><Link className="primary-button" href={`/exam-papers/${paper.id}`}>편집</Link><Link className="secondary-button" href={`/exam-papers/${paper.id}/print`}>PDF 출력</Link><button type="button" className="rounded-xl bg-red-50 px-4 py-3 font-bold text-red-700" onClick={() => remove(paper)}>삭제</button></div></article>)}</section>}
  </main><Footer /></div></ProtectedPage>;
}
