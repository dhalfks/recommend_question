import Link from 'next/link';
import { useEffect, useState } from 'react';
import { BillingMe, billingAPI } from '@/lib/api';


const featureLabels: Record<string, string> = {
  AI_EXPLANATION: 'AI 해설',
  CODE_REVIEW: 'AI 코드 채점',
  QUESTION_GENERATION: 'AI 문제 생성',
};


export default function BillingSummary() {
  const [billing, setBilling] = useState<BillingMe | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    billingAPI.me()
      .then(({ data }) => setBilling(data))
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
    </section>
  );
}
