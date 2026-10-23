import Link from 'next/link';
import { useEffect, useState } from 'react';
import { BillingMe, BillingPayment, billingAPI } from '@/lib/api';


const featureLabels: Record<string, string> = {
  AI_EXPLANATION: 'AI 해설',
  CODE_REVIEW: 'AI 코드 채점',
  QUESTION_GENERATION: 'AI 문제 생성',
};

const paymentStatusLabels: Record<BillingPayment['status'], string> = {
  READY: '결제 대기',
  PAID: '결제 완료',
  FAILED: '결제 실패',
  CANCELED: '결제 취소',
  REFUNDED: '환불 완료',
};


export default function BillingSummary() {
  const [billing, setBilling] = useState<BillingMe | null>(null);
  const [payments, setPayments] = useState<BillingPayment[]>([]);
  const [error, setError] = useState('');

  useEffect(() => {
    Promise.all([billingAPI.me(), billingAPI.payments()])
      .then(([billingResponse, paymentsResponse]) => {
        setBilling(billingResponse.data);
        setPayments(paymentsResponse.data);
      })
      .catch(() => setError('이용권 정보를 불러오지 못했습니다.'));
  }, []);

  return (
    <section className="surface-card mt-8 p-8">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="text-sm font-semibold text-[#3B86D1]">현재 이용권</p>
          <h2 className="mt-1 text-2xl font-bold text-[#242C34]">
            {billing?.plan_name ?? (error || '불러오는 중...')}
          </h2>
          {billing?.subscription && (
            <p className="mt-2 text-sm text-[#6C757D]">
              {new Date(billing.subscription.current_period_end).toLocaleString('ko-KR')}까지 이용 가능
            </p>
          )}
        </div>
        <Link href="/pricing" className="primary-button">
          요금제 보기
        </Link>
      </div>

      {billing && (
        <div className="mt-6 grid gap-3 sm:grid-cols-3">
          {Object.entries(billing.features).map(([code, feature]) => (
            <div key={code} className="rounded-xl bg-[#F8F9FA] p-4">
              <p className="text-sm font-semibold text-[#242C34]">{featureLabels[code] ?? code}</p>
              <p className="mt-2 text-sm text-[#6C757D]">
                {feature.daily_limit === null
                  ? '무제한'
                  : feature.daily_limit === 0
                    ? '현재 플랜에서 제공되지 않음'
                    : `오늘 ${feature.used_today}회 사용 · ${feature.remaining_today}회 남음`}
              </p>
            </div>
          ))}
        </div>
      )}

      {payments.length > 0 && (
        <div className="mt-8 border-t border-[#E9ECEF] pt-6">
          <h3 className="text-lg font-bold text-[#242C34]">결제 이력</h3>
          <div className="mt-3 divide-y divide-[#E9ECEF]">
            {payments.map((payment) => (
              <div key={payment.order_id} className="flex flex-wrap items-center justify-between gap-3 py-4">
                <div>
                  <p className="font-semibold text-[#242C34]">{payment.plan_name}</p>
                  <p className="mt-1 text-xs text-[#6C757D]">
                    {new Date(payment.paid_at ?? payment.created_at).toLocaleString('ko-KR')}
                  </p>
                </div>
                <div className="text-right">
                  <p className="font-bold text-[#242C34]">{payment.amount.toLocaleString('ko-KR')}원</p>
                  <p className="mt-1 text-xs text-[#6C757D]">{paymentStatusLabels[payment.status]}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </section>
  );
}
