import { useEffect, useMemo, useState } from 'react';
import Footer from '@/components/Footer';
import Navbar from '@/components/Navbar';
import ProtectedPage from '@/components/ProtectedPage';
import { AdminBillingPayment, BillingPayment, RefundRequest, billingAPI } from '@/lib/api';

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
  const [refundRequests, setRefundRequests] = useState<RefundRequest[]>([]);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const [loading, setLoading] = useState(true);
  const [processingOrderId, setProcessingOrderId] = useState('');

  const loadPayments = () => {
    setLoading(true);
    setError('');
    return billingAPI.adminPayments(status || undefined)
      .then(({ data }) => setPayments(data))
      .catch(() => setError('결제 현황을 불러오지 못했습니다.'))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    void loadPayments();
  }, [status]);

  const loadRefundRequests = () => billingAPI.adminRefundRequests()
    .then(({ data }) => setRefundRequests(data))
    .catch(() => setError('환불 신청 목록을 불러오지 못했습니다.'));

  useEffect(() => { void loadRefundRequests(); }, []);

  const decideRefund = async (request: RefundRequest, approved: boolean) => {
    const reason = window.prompt(approved ? '승인 사유를 입력해 주세요.' : '반려 사유를 입력해 주세요.');
    if (!reason?.trim() || reason.trim().length < 2) return;
    if (approved && !window.confirm(`${request.amount.toLocaleString('ko-KR')}원을 토스에서 전액 환불할까요?`)) return;
    setProcessingOrderId(request.order_id); setError(''); setNotice('');
    try {
      if (approved) await billingAPI.approveRefundRequest(request.id, reason.trim());
      else await billingAPI.rejectRefundRequest(request.id, reason.trim());
      setNotice(approved ? '환불을 승인하고 결제를 취소했습니다.' : '환불 신청을 반려했습니다.');
      await Promise.all([loadPayments(), loadRefundRequests()]);
    } catch (caught: any) {
      const detail = caught.response?.data?.detail;
      setError(typeof detail === 'string' ? detail : detail?.message ?? '환불 신청을 처리하지 못했습니다.');
    } finally { setProcessingOrderId(''); }
  };

  const closeUnpaidOrder = async (payment: AdminBillingPayment) => {
    if (!window.confirm('PG 결제키가 없는 장시간 미완료 주문을 종료할까요? 종료 후에는 결제할 수 없습니다.')) return;
    setProcessingOrderId(payment.order_id);
    setError('');
    setNotice('');
    try {
      const { data } = await billingAPI.closeAdminPayment(payment.order_id);
      setNotice(data.message ?? '미결제 주문을 종료했습니다.');
      await loadPayments();
    } catch (caught: any) {
      const detail = caught.response?.data?.detail;
      setError(typeof detail === 'string' ? detail : detail?.message ?? '미결제 주문을 종료하지 못했습니다.');
    } finally {
      setProcessingOrderId('');
    }
  };

  const recoverPayment = async (payment: AdminBillingPayment) => {
    if (!window.confirm('저장된 결제키로 Toss 승인을 다시 확인하고 복구할까요?')) return;
    setProcessingOrderId(payment.order_id);
    setError('');
    setNotice('');
    try {
      const { data } = await billingAPI.recoverAdminPayment(payment.order_id);
      setNotice(data.message ?? '결제를 확인하고 복구했습니다.');
      await loadPayments();
    } catch (caught: any) {
      const detail = caught.response?.data?.detail;
      setError(typeof detail === 'string' ? detail : detail?.message ?? '결제를 복구하지 못했습니다.');
    } finally {
      setProcessingOrderId('');
    }
  };

  const refundPayment = async (payment: AdminBillingPayment) => {
    const reason = window.prompt('전액 환불 사유를 입력해 주세요. 이용 기간에서 해당 주문의 기간이 차감됩니다.');
    if (!reason?.trim()) return;
    if (!window.confirm(`${payment.amount.toLocaleString('ko-KR')}원을 전액 환불할까요? 이 작업은 되돌릴 수 없습니다.`)) return;
    setProcessingOrderId(payment.order_id);
    setError('');
    setNotice('');
    try {
      const { data } = await billingAPI.refundAdminPayment(payment.order_id, reason.trim());
      setNotice(data.message ?? '전액 환불을 완료했습니다.');
      await loadPayments();
    } catch (caught: any) {
      const detail = caught.response?.data?.detail;
      setError(typeof detail === 'string' ? detail : detail?.message ?? '환불을 처리하지 못했습니다.');
    } finally {
      setProcessingOrderId('');
    }
  };

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
          {notice && <div className="mt-6 rounded-xl border border-green-200 bg-green-50 p-4 text-green-800">{notice}</div>}
          <section className="surface-card mt-6 p-6">
            <div className="flex items-center justify-between gap-4"><h2 className="text-xl font-bold text-[#242C34]">환불 신청 관리</h2><span className="text-sm text-[#6C757D]">대기 {refundRequests.filter((item) => item.status === 'PENDING').length}건</span></div>
            {refundRequests.length === 0 ? <p className="mt-4 text-[#6C757D]">환불 신청이 없습니다.</p> : <div className="mt-4 divide-y divide-[#E9ECEF]">{refundRequests.map((request) => (
              <div key={request.id} className="grid gap-3 py-4 lg:grid-cols-[1.2fr_1fr_2fr_auto] lg:items-center">
                <div><p className="font-semibold">{request.user_name} · {request.plan_name}</p><p className="text-xs text-[#6C757D]">{request.user_email}</p></div>
                <div><p className="font-semibold">{request.amount.toLocaleString('ko-KR')}원</p><p className="text-xs text-[#6C757D]">{new Date(request.requested_at).toLocaleString('ko-KR')}</p></div>
                <div><p className="text-sm">{request.reason}</p><p className={`mt-1 text-xs ${request.standard_full_refund ? 'text-green-700' : 'text-amber-700'}`}>{request.policy_message}</p>{request.decision_reason && <p className="mt-1 text-xs text-[#6C757D]">처리 사유: {request.decision_reason}</p>}</div>
                <div className="flex gap-2 lg:justify-end">{request.status === 'PENDING' ? <><button type="button" className="text-sm font-semibold text-[#3B86D1] underline disabled:opacity-40" disabled={processingOrderId === request.order_id} onClick={() => void decideRefund(request, true)}>승인</button><button type="button" className="text-sm font-semibold text-red-700 underline disabled:opacity-40" disabled={processingOrderId === request.order_id} onClick={() => void decideRefund(request, false)}>반려</button></> : <span className="text-sm font-semibold">{request.status === 'APPROVED' ? '승인 완료' : '반려 완료'}</span>}</div>
              </div>
            ))}</div>}
          </section>
          <section className="surface-card mt-6 overflow-x-auto p-6">
            {loading ? <p>불러오는 중...</p> : payments.length === 0 ? <p className="text-[#6C757D]">표시할 주문이 없습니다.</p> : (
              <table className="w-full min-w-[850px] text-left text-sm">
                <thead><tr className="border-b text-[#6C757D]"><th className="pb-3">주문시각</th><th className="pb-3">구매자</th><th className="pb-3">상품</th><th className="pb-3">주문번호</th><th className="pb-3 text-right">금액</th><th className="pb-3 text-right">상태·처리</th></tr></thead>
                <tbody>{payments.map((payment) => (
                  <tr key={payment.order_id} className="border-b border-[#E9ECEF] last:border-0">
                    <td className="py-4">{new Date(payment.created_at).toLocaleString('ko-KR')}</td>
                    <td className="py-4"><p className="font-semibold">{payment.user_name}</p><p className="text-xs text-[#6C757D]">{payment.user_email} · {payment.user_role}</p></td>
                    <td className="py-4">{payment.plan_name}</td>
                    <td className="py-4 font-mono text-xs">{payment.order_id}</td>
                    <td className="py-4 text-right font-semibold">{payment.amount.toLocaleString('ko-KR')}원</td>
                    <td className="py-4 text-right">
                      <p>{statusLabel[payment.status]}</p>
                      {payment.status === 'READY' && (
                        <div className="mt-2 flex flex-col items-end gap-1">
                          <button
                            type="button"
                            className="text-xs font-semibold text-red-700 underline disabled:cursor-not-allowed disabled:opacity-40"
                            disabled={!payment.can_close || processingOrderId === payment.order_id}
                            title={payment.can_close ? '장시간 미완료 주문을 종료합니다.' : '결제키가 없어야 하며 생성 후 30분이 지나야 합니다.'}
                            onClick={() => void closeUnpaidOrder(payment)}
                          >미결제 주문 종료</button>
                          <button
                            type="button"
                            className="text-xs font-semibold text-[#3B86D1] underline disabled:cursor-not-allowed disabled:opacity-40"
                            disabled={!payment.can_recover || processingOrderId === payment.order_id}
                            title={payment.can_recover ? '저장된 결제키로 승인을 안전하게 재시도합니다.' : '결제키가 저장된 네트워크 실패 주문만 복구할 수 있습니다.'}
                            onClick={() => void recoverPayment(payment)}
                          >결제 상태 확인 및 복구</button>
                        </div>
                      )}
                      {payment.status === 'PAID' && (
                        <div className="mt-2 flex flex-col items-end gap-1">
                          <span className={`text-xs ${payment.standard_full_refund ? 'text-green-700' : 'text-amber-700'}`} title={payment.refund_policy_message}>
                            {payment.standard_full_refund ? '기본 전액 환불 대상' : '관리자 검토 필요'}
                          </span>
                          <button
                            type="button"
                            className="text-xs font-semibold text-red-700 underline disabled:cursor-not-allowed disabled:opacity-40"
                            disabled={processingOrderId === payment.order_id}
                            title={payment.refund_policy_message}
                            onClick={() => void refundPayment(payment)}
                          >전액 환불</button>
                        </div>
                      )}
                    </td>
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
