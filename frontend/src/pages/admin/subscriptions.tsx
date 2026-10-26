import { useCallback, useEffect, useMemo, useState } from 'react';
import Footer from '@/components/Footer';
import Navbar from '@/components/Navbar';
import ProtectedPage from '@/components/ProtectedPage';
import { AdminSubscription, billingAPI } from '@/lib/api';

const statuses: Array<{ value: '' | AdminSubscription['status']; label: string }> = [
  { value: '', label: '전체' }, { value: 'ACTIVE', label: '이용 중' },
  { value: 'EXPIRED', label: '기간 만료' }, { value: 'CANCELED', label: '취소' },
  { value: 'PENDING', label: '대기' }, { value: 'PAST_DUE', label: '결제 연체' },
];
const statusLabel = Object.fromEntries(statuses.filter(({ value }) => value).map(({ value, label }) => [value, label])) as Record<AdminSubscription['status'], string>;

export default function AdminSubscriptionsPage() {
  const [status, setStatus] = useState<'' | AdminSubscription['status']>('');
  const [subscriptions, setSubscriptions] = useState<AdminSubscription[]>([]);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');

  const load = useCallback(() => {
    setLoading(true); setError('');
    return billingAPI.adminSubscriptions(status || undefined).then(({ data }) => setSubscriptions(data))
      .catch(() => setError('이용권 현황을 불러오지 못했습니다.')).finally(() => setLoading(false));
  }, [status]);
  useEffect(() => { void load(); }, [load]);

  const expireDue = async () => {
    if (!window.confirm('종료 시각이 지난 ACTIVE 이용권을 EXPIRED 상태로 정리할까요?')) return;
    setProcessing(true); setError(''); setNotice('');
    try {
      const { data } = await billingAPI.expireSubscriptions();
      setNotice(data.message);
      await load();
    } catch (caught: any) {
      const detail = caught.response?.data?.detail;
      setError(typeof detail === 'string' ? detail : '만료 상태를 정리하지 못했습니다.');
    } finally { setProcessing(false); }
  };

  const activeCount = useMemo(() => subscriptions.filter((item) => item.status === 'ACTIVE').length, [subscriptions]);
  return <ProtectedPage roles={['ADMIN']}><div className="app-shell flex min-h-screen flex-col"><Navbar />
    <main className="page-container flex-1 py-10">
      <div className="flex flex-wrap items-end justify-between gap-4"><div><p className="font-semibold text-[#8B5CF6]">ADMIN</p><h1 className="text-3xl font-bold text-[#242C34]">이용권 관리</h1><p className="mt-2 text-[#6C757D]">사용자별 이용권 기간과 상태를 확인합니다.</p></div>
        <div className="flex gap-2"><select className="form-control w-36" value={status} onChange={(event) => setStatus(event.target.value as typeof status)}>{statuses.map((item) => <option key={item.value} value={item.value}>{item.label}</option>)}</select>
          <button type="button" className="secondary-button" disabled={processing} onClick={() => void expireDue()}>만료 상태 정리</button></div>
      </div>
      <div className="mt-6 grid gap-4 sm:grid-cols-2"><div className="surface-card p-5"><p className="text-sm text-[#6C757D]">조회 이용권</p><p className="mt-1 text-2xl font-bold">{subscriptions.length}건</p></div><div className="surface-card p-5"><p className="text-sm text-[#6C757D]">조회 결과 중 ACTIVE</p><p className="mt-1 text-2xl font-bold text-green-700">{activeCount}건</p></div></div>
      {error && <div className="mt-6 rounded-xl border border-red-200 bg-red-50 p-4 text-red-700">{error}</div>}
      {notice && <div className="mt-6 rounded-xl border border-green-200 bg-green-50 p-4 text-green-800">{notice}</div>}
      <section className="surface-card mt-6 overflow-x-auto p-6">{loading ? <p>불러오는 중...</p> : subscriptions.length === 0 ? <p className="text-[#6C757D]">표시할 이용권이 없습니다.</p> : <table className="w-full min-w-[850px] text-left text-sm">
        <thead><tr className="border-b text-[#6C757D]"><th className="pb-3">사용자</th><th className="pb-3">이용권</th><th className="pb-3">상태</th><th className="pb-3">시작</th><th className="pb-3">종료</th><th className="pb-3 text-right">남은 기간</th></tr></thead>
        <tbody>{subscriptions.map((item) => <tr key={item.id} className="border-b border-[#E9ECEF] last:border-0"><td className="py-4"><p className="font-semibold">{item.user_name}</p><p className="text-xs text-[#6C757D]">{item.user_email} · {item.user_role}</p></td><td className="py-4">{item.plan_name}</td><td className="py-4 font-semibold">{statusLabel[item.status]}</td><td className="py-4">{item.current_period_start ? new Date(item.current_period_start).toLocaleString('ko-KR') : '-'}</td><td className="py-4">{item.current_period_end ? new Date(item.current_period_end).toLocaleString('ko-KR') : '-'}</td><td className="py-4 text-right">{item.status === 'ACTIVE' ? `${item.remaining_days}일` : '-'}</td></tr>)}</tbody>
      </table>}</section>
    </main><Footer /></div></ProtectedPage>;
}
