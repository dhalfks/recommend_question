import { useEffect, useState } from 'react';
import Footer from '@/components/Footer';
import Navbar from '@/components/Navbar';
import ProtectedPage from '@/components/ProtectedPage';
import { AdminAIUsage, AIUsageMetric, billingAPI } from '@/lib/api';

const number = (value: number) => value.toLocaleString('ko-KR');

function MetricsTable({ rows, firstColumn }: { rows: AIUsageMetric[]; firstColumn: string }) {
  return <div className="overflow-x-auto"><table className="mt-4 w-full min-w-[720px] text-left text-sm">
    <thead><tr className="border-b text-[#6C757D]"><th className="pb-3">{firstColumn}</th><th className="pb-3 text-right">요청</th><th className="pb-3 text-right">성공</th><th className="pb-3 text-right">실패</th><th className="pb-3 text-right">입력 토큰</th><th className="pb-3 text-right">출력 토큰</th><th className="pb-3 text-right">예상 원가</th></tr></thead>
    <tbody>{rows.map((row) => <tr key={row.key} className="border-b border-[#E9ECEF] last:border-0"><td className="py-3 font-semibold">{row.label}</td><td className="py-3 text-right">{number(row.total_requests)}</td><td className="py-3 text-right text-green-700">{number(row.succeeded_requests)}</td><td className="py-3 text-right text-red-700">{number(row.failed_requests)}</td><td className="py-3 text-right">{number(row.input_tokens)}</td><td className="py-3 text-right">{number(row.output_tokens)}</td><td className="py-3 text-right font-semibold">{number(row.estimated_cost_krw)}원</td></tr>)}</tbody>
  </table></div>;
}

export default function AdminAIUsagePage() {
  const [days, setDays] = useState(30);
  const [report, setReport] = useState<AdminAIUsage | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    setError('');
    billingAPI.adminAIUsage(days).then(({ data }) => setReport(data)).catch(() => setError('AI 사용량을 불러오지 못했습니다.'));
  }, [days]);

  const successRate = report?.summary.total_requests
    ? Math.round((report.summary.succeeded_requests / report.summary.total_requests) * 100)
    : 0;

  return <ProtectedPage roles={['ADMIN']}><div className="app-shell flex min-h-screen flex-col"><Navbar />
    <main className="page-container flex-1 py-10">
      <div className="flex flex-wrap items-end justify-between gap-4"><div><p className="font-semibold text-[#8B5CF6]">ADMIN</p><h1 className="text-3xl font-bold text-[#242C34]">AI 사용 분석</h1><p className="mt-2 text-[#6C757D]">기능별 사용량과 토큰 기반 예상 원가를 확인합니다.</p></div>
        <select className="form-control w-36" value={days} onChange={(event) => setDays(Number(event.target.value))}><option value={7}>최근 7일</option><option value={30}>최근 30일</option><option value={90}>최근 90일</option></select>
      </div>
      {error && <div className="mt-6 rounded-xl border border-red-200 bg-red-50 p-4 text-red-700">{error}</div>}
      {report && <>
        {!report.cost_configured && <div className="mt-6 rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">토큰 단가가 설정되지 않아 예상 원가는 0원으로 표시됩니다. 배포 환경변수에 모델별 원화 단가를 설정해 주세요.</div>}
        <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <div className="surface-card p-5"><p className="text-sm text-[#6C757D]">전체 요청</p><p className="mt-1 text-2xl font-bold">{number(report.summary.total_requests)}건</p></div>
          <div className="surface-card p-5"><p className="text-sm text-[#6C757D]">성공률</p><p className="mt-1 text-2xl font-bold text-green-700">{successRate}%</p></div>
          <div className="surface-card p-5"><p className="text-sm text-[#6C757D]">전체 토큰</p><p className="mt-1 text-2xl font-bold">{number(report.summary.input_tokens + report.summary.output_tokens)}</p></div>
          <div className="surface-card p-5"><p className="text-sm text-[#6C757D]">예상 원가</p><p className="mt-1 text-2xl font-bold text-[#3B86D1]">{number(report.summary.estimated_cost_krw)}원</p></div>
        </div>
        <section className="surface-card mt-6 p-6"><h2 className="text-xl font-bold">기능별 사용량</h2>{report.by_feature.length ? <MetricsTable rows={report.by_feature} firstColumn="기능" /> : <p className="mt-4 text-[#6C757D]">선택 기간의 AI 사용 기록이 없습니다.</p>}</section>
        <section className="surface-card mt-6 p-6"><h2 className="text-xl font-bold">사용자별 상위 20명</h2>{report.by_user.length ? <MetricsTable rows={report.by_user} firstColumn="사용자" /> : <p className="mt-4 text-[#6C757D]">선택 기간의 사용자 기록이 없습니다.</p>}</section>
      </>}
    </main><Footer /></div></ProtectedPage>;
}
