import { useEffect, useMemo, useState } from 'react';
import Footer from '@/components/Footer';
import Navbar from '@/components/Navbar';
import ProtectedPage from '@/components/ProtectedPage';
import { AdminBillingPayment, BillingPayment, billingAPI } from '@/lib/api';

const statuses: Array<{ value: '' | BillingPayment['status']; label: string }> = [
  { value: '', label: '전체' },
  { value: 'PAID', label: '결제 완료' },
  { value: 'READY', label: '결제 대기' },
  { value: 'FAILED', label: '결제 실패' },
  { value: 'CANCELED', label: '결제 취소' },
  { value: 'REFUNDED', label: '환불 완료' },
];

const statusLabel = Object.fromEntries(
  statuses.filter(({ value }) => value).map(({ value, label }) => [value, label]),
) as Record<BillingPayment['status'], string>;

export default function AdminBillingPage() {
  const [status, setStatus] = useState<'' | BillingPayment['status']>('');
  const [payments, setPayments] = useState<AdminBillingPayment[]>([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    setError('');
    billingAPI.adminPayments(status || undefined)
      .then(({ data }) => setPayments(data))
      .catch(() => setError('결제 현황을 불러오지 못했습니다.'))
      .finally(() => setLoading(false));
  }, [status]);

  const paidTotal = useMemo(
    () => payments.filter((payment) => payment.status === 'PAID').reduce((sum, payment) => sum + payment.amount, 0),
    [payments],
  );

  return (
    <ProtectedPage roles={['ADMIN']}>
      <div className="app-shell flex min-h-screen flex-col">
        <Navbar />
        <main className="page-container flex-1 py-10">
          <div className="flex flex-wrap items-end justify-between gap-4">
            <div>
              <p className="font-semibold text-[#8B5CF6]">ADMIN</p>
              <h1 className="text-3xl font-bold text-[#242C34]">결제 현황</h1>
              <p className="mt-2 text-[#6C757D]">최근 주문 최대 100건을 확인합니다.</p>
            </div>
            <select className="form-control w-40" value={status} onChange={(event) => setStatus(event.target.value as typeof status)}>
              {statuses.map((item) => <option key={item.value} value={item.value}>{item.label}</option>)}
            </select>
          </div>

          <div className="mt-6 grid gap-4 sm:grid-cols-2">
            <div className="surface-card p-5"><p className="text-sm text-[#6C757D]">조회 주문</p><p className="mt-1 text-2xl font-bold">{payments.length}건</p></div>
            <div className="surface-card p-5"><p className="text-sm text-[#6C757D]">조회 결과 결제액</p><p className="mt-1 text-2xl font-bold text-[#3B86D1]">{paidTotal.toLocaleString('ko-KR')}원</p></div>
          </div>

          {error && <div className="mt-6 rounded-xl border border-red-200 bg-red-50 p-4 text-red-700">{error}</div>}
          <section className="surface-card mt-6 overflow-x-auto p-6">
            {loading ? <p>불러오는 중...</p> : payments.length === 0 ? <p className="text-[#6C757D]">표시할 주문이 없습니다.</p> : (
              <table className="w-full min-w-[850px] text-left text-sm">
                <thead><tr className="border-b text-[#6C757D]"><th className="pb-3">주문시각</th><th className="pb-3">구매자</th><th className="pb-3">상품</th><th className="pb-3">주문번호</th><th className="pb-3 text-right">금액</th><th className="pb-3 text-right">상태</th></tr></thead>
                <tbody>{payments.map((payment) => (
                  <tr key={payment.order_id} className="border-b border-[#E9ECEF] last:border-0">
                    <td className="py-4">{new Date(payment.created_at).toLocaleString('ko-KR')}</td>
                    <td className="py-4"><p className="font-semibold">{payment.user_name}</p><p className="text-xs text-[#6C757D]">{payment.user_email} · {payment.user_role}</p></td>
                    <td className="py-4">{payment.plan_name}</td>
                    <td className="py-4 font-mono text-xs">{payment.order_id}</td>
                    <td className="py-4 text-right font-semibold">{payment.amount.toLocaleString('ko-KR')}원</td>
                    <td className="py-4 text-right">{statusLabel[payment.status]}</td>
                  </tr>
                ))}</tbody>
              </table>
            )}
          </section>
        </main>
        <Footer />
      </div>
    </ProtectedPage>
  );
}
