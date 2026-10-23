import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import ProtectedPage from '@/components/ProtectedPage';
import { useAuth } from '@/contexts/AuthContext';
import { BillingMe, BillingPlan, billingAPI } from '@/lib/api';


const featureLabels: Record<string, string> = {
  AI_EXPLANATION: 'AI 해설',
  CODE_REVIEW: 'AI 코드 채점',
  QUESTION_GENERATION: 'AI 문제 생성',
};


export default function PricingPage() {
  const router = useRouter();
  const { user } = useAuth();
  const [plans, setPlans] = useState<BillingPlan[]>([]);
  const [billing, setBilling] = useState<BillingMe | null>(null);
  const [loadingCode, setLoadingCode] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    Promise.all([billingAPI.plans(), billingAPI.me()])
      .then(([plansResult, billingResult]) => {
        setPlans(plansResult.data);
        setBilling(billingResult.data);
      })
      .catch(() => setError('요금제 정보를 불러오지 못했습니다.'));
  }, []);

  const startCheckout = async (plan: BillingPlan) => {
    setError('');
    setLoadingCode(plan.code);
    try {
      const { data: order } = await billingAPI.createOrder(plan.code);
      if (!order.customer_key) throw new Error('결제 고객 키가 없습니다.');
      sessionStorage.setItem(`billing-order:${order.order_id}`, JSON.stringify(order));
      await router.push(`/billing/checkout?orderId=${encodeURIComponent(order.order_id)}`);
    } catch (requestError: any) {
      setError(requestError.response?.data?.detail ?? requestError.message ?? '주문 생성에 실패했습니다.');
      setLoadingCode('');
    }
  };

  return (
    <ProtectedPage roles={['STUDENT', 'PROFESSOR']}>
      <div className="app-shell flex min-h-screen flex-col">
        <Navbar />
        <main className="page-container flex-1 py-12">
          <div className="text-center">
            <p className="font-semibold text-[#3B86D1]">30일 단건 이용권</p>
            <h1 className="mt-2 text-4xl font-bold text-[#242C34]">필요할 때만 Pro로 업그레이드하세요</h1>
            <p className="mt-3 text-[#6C757D]">자동 갱신 없이 결제일부터 30일 동안 이용합니다.</p>
          </div>

          {billing && (
            <div className="mx-auto mt-8 max-w-2xl rounded-xl bg-blue-50 p-4 text-center text-sm text-blue-800">
              현재 플랜: <strong>{billing.plan_name}</strong>
              {billing.subscription && ` · ${new Date(billing.subscription.current_period_end).toLocaleDateString('ko-KR')}까지`}
            </div>
          )}
          {error && <p className="mx-auto mt-6 max-w-2xl rounded-xl bg-red-50 p-4 text-red-700">{String(error)}</p>}

          <div className="mx-auto mt-10 grid max-w-3xl gap-6">
            {plans.map((plan) => (
              <section key={plan.code} className="surface-card p-8">
                <div className="flex flex-col justify-between gap-6 sm:flex-row sm:items-start">
                  <div>
                    <h2 className="text-2xl font-bold text-[#242C34]">{plan.name}</h2>
                    <p className="mt-2 text-3xl font-bold text-[#3B86D1]">
                      {plan.price.toLocaleString('ko-KR')}원
                    </p>
                    <ul className="mt-5 space-y-2 text-[#495057]">
                      {Object.entries(plan.features).map(([code, policy]) => (
                        <li key={code}>✓ {featureLabels[code] ?? code} 하루 {policy.daily_limit}회</li>
                      ))}
                      <li>✓ 결제일부터 {plan.entitlement_days}일 이용</li>
                      <li>✓ 자동 갱신 없음</li>
                    </ul>
                  </div>
                  <button
                    type="button"
                    disabled={Boolean(loadingCode) || !user}
                    onClick={() => startCheckout(plan)}
                    className="primary-button min-w-40 disabled:opacity-50"
                  >
                    {loadingCode === plan.code ? '주문 생성 중...' : '결제하기'}
                  </button>
                </div>
              </section>
            ))}
          </div>
          <p className="mx-auto mt-6 max-w-3xl text-center text-sm text-[#6C757D]">
            결제 전 <Link href="/refund-policy" className="font-semibold text-[#3B86D1] underline">환불 정책</Link>을 확인해 주세요.
          </p>
        </main>
        <Footer />
      </div>
    </ProtectedPage>
  );
}
