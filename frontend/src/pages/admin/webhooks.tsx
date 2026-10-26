import { useEffect, useMemo, useState } from 'react';
import Footer from '@/components/Footer';
import Navbar from '@/components/Navbar';
import ProtectedPage from '@/components/ProtectedPage';
import { AdminWebhookEvent, billingAPI } from '@/lib/api';

const filters: Array<{ value: '' | AdminWebhookEvent['status']; label: string }> = [
  { value: '', label: '전체' },
  { value: 'PROCESSED', label: '처리 완료' },
  { value: 'FAILED', label: '처리 실패' },
  { value: 'RECEIVED', label: '처리 중' },
];
const statusLabels: Record<AdminWebhookEvent['status'], string> = {
  PROCESSED: '처리 완료', FAILED: '처리 실패', RECEIVED: '처리 중',
};

export default function AdminWebhooksPage() {
  const [status, setStatus] = useState<'' | AdminWebhookEvent['status']>('');
  const [events, setEvents] = useState<AdminWebhookEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [processingEventId, setProcessingEventId] = useState<number | null>(null);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');

  const load = () => {
    setLoading(true); setError('');
    return billingAPI.adminWebhooks(status || undefined)
      .then(({ data }) => setEvents(data))
      .catch(() => setError('웹훅 처리 이력을 불러오지 못했습니다.'))
      .finally(() => setLoading(false));
  };
  useEffect(() => { void load(); }, [status]);

  const retry = async (event: AdminWebhookEvent) => {
    if (!window.confirm('토스 결제 상태를 다시 확인하고 이 웹훅을 재처리할까요?')) return;
    setProcessingEventId(event.id); setError(''); setNotice('');
    try {
      await billingAPI.retryAdminWebhook(event.id);
      setNotice('웹훅을 다시 검증하고 정상 처리했습니다.');
      await load();
    } catch (caught: any) {
      const detail = caught.response?.data?.detail;
      setError(typeof detail === 'string' ? detail : detail?.message ?? '웹훅을 재처리하지 못했습니다.');
    } finally { setProcessingEventId(null); }
  };

  const failedCount = useMemo(() => events.filter((event) => event.status === 'FAILED').length, [events]);
  return <ProtectedPage roles={['ADMIN']}><div className="app-shell flex min-h-screen flex-col"><Navbar />
    <main className="page-container flex-1 py-10">
      <div className="flex flex-wrap items-end justify-between gap-4"><div><p className="font-semibold text-[#8B5CF6]">ADMIN</p><h1 className="text-3xl font-bold text-[#242C34]">결제 웹훅 이력</h1><p className="mt-2 text-[#6C757D]">토스가 전송한 결제 상태 알림의 처리 결과와 오류를 확인합니다.</p></div>
        <div className="flex gap-2"><select className="form-control w-36" value={status} onChange={(event) => setStatus(event.target.value as typeof status)}>{filters.map((filter) => <option key={filter.value} value={filter.value}>{filter.label}</option>)}</select><button type="button" className="secondary-button" disabled={loading} onClick={() => void load()}>새로고침</button></div>
      </div>
      <div className="mt-6 grid gap-4 sm:grid-cols-2"><div className="surface-card p-5"><p className="text-sm text-[#6C757D]">조회 이벤트</p><p className="mt-1 text-2xl font-bold">{events.length}건</p></div><div className="surface-card p-5"><p className="text-sm text-[#6C757D]">조회 결과 중 실패</p><p className="mt-1 text-2xl font-bold text-red-700">{failedCount}건</p></div></div>
      {error && <div className="mt-6 rounded-xl border border-red-200 bg-red-50 p-4 text-red-700">{error}</div>}
      {notice && <div className="mt-6 rounded-xl border border-green-200 bg-green-50 p-4 text-green-800">{notice}</div>}
      <section className="surface-card mt-6 overflow-x-auto p-6">{loading ? <p>불러오는 중...</p> : events.length === 0 ? <p className="text-[#6C757D]">수신된 웹훅 기록이 없습니다.</p> : <table className="w-full min-w-[960px] text-left text-sm">
        <thead><tr className="border-b text-[#6C757D]"><th className="pb-3">수신 시각</th><th className="pb-3">주문번호</th><th className="pb-3">결제 상태</th><th className="pb-3">처리 상태</th><th className="pb-3">이벤트</th><th className="pb-3">오류</th><th className="pb-3 text-right">관리</th></tr></thead>
        <tbody>{events.map((event) => <tr key={event.id} className="border-b border-[#E9ECEF] align-top last:border-0"><td className="py-4 whitespace-nowrap">{new Date(event.received_at).toLocaleString('ko-KR')}</td><td className="max-w-[220px] break-all py-4 font-mono text-xs">{event.order_id ?? '-'}</td><td className="py-4">{event.payment_status ?? '-'}</td><td className={`py-4 font-semibold ${event.status === 'FAILED' ? 'text-red-700' : event.status === 'PROCESSED' ? 'text-green-700' : 'text-amber-700'}`}>{statusLabels[event.status]}</td><td className="py-4">{event.event_type}</td><td className="max-w-[300px] break-words py-4 text-xs text-red-700">{event.error_message ?? '-'}</td><td className="py-4 text-right">{event.status === 'FAILED' ? <button type="button" className="secondary-button whitespace-nowrap" disabled={processingEventId === event.id} onClick={() => void retry(event)}>{processingEventId === event.id ? '처리 중...' : '다시 검증'}</button> : '-'}</td></tr>)}</tbody>
      </table>}</section>
    </main><Footer /></div></ProtectedPage>;
}
