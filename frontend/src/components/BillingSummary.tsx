import Link from 'next/link';
import { useEffect, useState } from 'react';
import { BillingMe, BillingPayment, RefundRequest, billingAPI } from '@/lib/api';

const featureLabels: Record<string, string> = { AI_EXPLANATION: 'AI 해설', CODE_REVIEW: 'AI 코드 채점', QUESTION_GENERATION: 'AI 문제 생성' };
const paymentStatusLabels: Record<BillingPayment['status'], string> = { READY: '결제 대기', PAID: '결제 완료', FAILED: '결제 실패', CANCELED: '결제 취소', REFUNDED: '환불 완료' };

export default function BillingSummary() {
  const [billing, setBilling] = useState<BillingMe | null>(null);
  const [payments, setPayments] = useState<BillingPayment[]>([]);
  const [refundRequests, setRefundRequests] = useState<RefundRequest[]>([]);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const [processingOrderId, setProcessingOrderId] = useState('');

  const loadBilling = async () => {
    const [billingResult, paymentsResult, refundResult] = await Promise.allSettled([
      billingAPI.me(), billingAPI.payments(), billingAPI.refundRequests(),
    ]);
    if (billingResult.status === 'fulfilled') setBilling(billingResult.value.data);
    if (paymentsResult.status === 'fulfilled') setPayments(paymentsResult.value.data);
    if (refundResult.status === 'fulfilled') setRefundRequests(refundResult.value.data);
    else setRefundRequests([]);
    if (billingResult.status === 'rejected' || paymentsResult.status === 'rejected') {
      setError('이용권 또는 결제내역을 불러오지 못했습니다.');
    } else {
      setError('');
    }
  };

  useEffect(() => { void loadBilling(); }, []);

  const requestRefund = async (payment: BillingPayment) => {
    const reason = window.prompt('환불 신청 사유를 입력해 주세요.');
    if (!reason?.trim() || reason.trim().length < 2) return;
    setProcessingOrderId(payment.order_id); setError(''); setNotice('');
    try {
      await billingAPI.requestRefund(payment.order_id, reason.trim());
      setNotice('환불 신청이 접수되었습니다. 관리자가 확인한 뒤 처리합니다.');
      await loadBilling();
    } catch (caught: any) {
      const detail = caught.response?.data?.detail;
      setError(typeof detail === 'string' ? detail : detail?.message ?? '환불 신청을 접수하지 못했습니다.');
    } finally { setProcessingOrderId(''); }
  };

  return <section className="surface-card mt-8 p-8">
    <div className="flex flex-wrap items-start justify-between gap-4"><div><p className="text-sm font-semibold text-[#3B86D1]">현재 이용권</p>
      <h2 className="mt-1 text-2xl font-bold text-[#242C34]">{billing?.plan_name ?? (error || '불러오는 중...')}</h2>
      {billing?.subscription && <p className="mt-2 text-sm text-[#6C757D]">{new Date(billing.subscription.current_period_end).toLocaleString('ko-KR')}까지 이용 가능</p>}
    </div><Link href="/pricing" className="primary-button">요금제 보기</Link></div>
    {billing && <div className="mt-6 grid gap-3 sm:grid-cols-3">{Object.entries(billing.features).map(([code, feature]) => <div key={code} className="rounded-xl bg-[#F8F9FA] p-4">
      <p className="text-sm font-semibold text-[#242C34]">{featureLabels[code] ?? code}</p><p className="mt-2 text-sm text-[#6C757D]">{feature.daily_limit === null ? '무제한' : feature.daily_limit === 0 ? '현재 플랜에서 제공하지 않음' : `오늘 ${feature.used_today}회 사용 · ${feature.remaining_today}회 남음`}</p>
    </div>)}</div>}
    {notice && <div className="mt-6 rounded-xl border border-green-200 bg-green-50 p-4 text-sm text-green-800">{notice}</div>}
    {error && <div className="mt-6 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div>}
    {payments.length > 0 && <div className="mt-8 border-t border-[#E9ECEF] pt-6"><h3 className="text-lg font-bold text-[#242C34]">결제 내역</h3><div className="mt-3 divide-y divide-[#E9ECEF]">{payments.map((payment) => {
      const request = refundRequests.find((item) => item.order_id === payment.order_id);
      return <div key={payment.order_id} className="flex flex-wrap items-center justify-between gap-3 py-4"><div><p className="font-semibold text-[#242C34]">{payment.plan_name}</p><p className="mt-1 text-xs text-[#6C757D]">{new Date(payment.paid_at ?? payment.created_at).toLocaleString('ko-KR')}</p></div>
        <div className="text-right"><p className="font-bold text-[#242C34]">{payment.amount.toLocaleString('ko-KR')}원</p><p className="mt-1 text-xs text-[#6C757D]">{paymentStatusLabels[payment.status]}</p>
          {request && <p className="mt-1 text-xs font-semibold text-[#8B5CF6]">환불 신청: {request.status === 'PENDING' ? '검토 중' : request.status === 'APPROVED' ? '승인' : '반려'}</p>}
          {payment.status === 'PAID' && (!request || request.status === 'REJECTED') && <button type="button" className="mt-2 text-xs font-semibold text-red-700 underline disabled:opacity-40" disabled={processingOrderId === payment.order_id} onClick={() => void requestRefund(payment)}>{request?.status === 'REJECTED' ? '환불 재신청' : '환불 신청'}</button>}
        </div></div>;
    })}</div></div>}
  </section>;
}
