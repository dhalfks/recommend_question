import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { loadTossPayments, TossPaymentsWidgets } from '@tosspayments/tosspayments-sdk';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import ProtectedPage from '@/components/ProtectedPage';
import { useAuth } from '@/contexts/AuthContext';
import { BillingOrder } from '@/lib/api';


export default function BillingCheckoutPage() {
  const router = useRouter();
  const { user } = useAuth();
  const [order, setOrder] = useState<BillingOrder | null>(null);
  const [widgets, setWidgets] = useState<TossPaymentsWidgets | null>(null);
  const [error, setError] = useState('');
  const [paying, setPaying] = useState(false);

  useEffect(() => {
    if (!router.isReady) return;
    const orderId = typeof router.query.orderId === 'string' ? router.query.orderId : '';
    const raw = orderId ? sessionStorage.getItem(`billing-order:${orderId}`) : null;
    if (!raw) {
      setError('주문 정보를 찾을 수 없습니다. 요금제를 다시 선택해 주세요.');
      return;
    }
    try {
      const parsed = JSON.parse(raw) as BillingOrder;
      if (parsed.order_id !== orderId || !parsed.customer_key) throw new Error();
      setOrder(parsed);
    } catch {
      setError('유효하지 않은 주문 정보입니다.');
    }
  }, [router.isReady, router.query.orderId]);

  useEffect(() => {
    if (!order) return;
    const clientKey = process.env.NEXT_PUBLIC_TOSS_CLIENT_KEY;
    if (!clientKey) {
      setError('토스 클라이언트 키가 설정되지 않았습니다.');
      return;
    }
    let active = true;
    const initializeWidgets = async () => {
      try {
        const tossPayments = await loadTossPayments(clientKey);
        if (!active) return;

        const instance = tossPayments.widgets({ customerKey: order.customer_key! });
        await instance.setAmount({ currency: 'KRW', value: order.amount });
        if (!active) return;

        const paymentMethod = document.querySelector('#payment-method');
        const agreement = document.querySelector('#agreement');
        if (!paymentMethod || !agreement) return;

        await instance.renderPaymentMethods({ selector: '#payment-method', variantKey: 'DEFAULT' });
        if (!active) return;
        await instance.renderAgreement({ selector: '#agreement', variantKey: 'AGREEMENT' });
        if (active) setWidgets(instance);
      } catch (sdkError: any) {
        if (active) {
          setError(sdkError.message ?? '결제 UI를 불러오지 못했습니다.');
        }
      }
    };

    // React Strict Mode immediately mounts and cleans up effects once in development.
    // Defer SDK initialization so the discarded effect cannot render into removed nodes.
    const frameId = window.requestAnimationFrame(() => {
      void initializeWidgets();
    });

    return () => {
      active = false;
      window.cancelAnimationFrame(frameId);
    };
  }, [order]);

  const requestPayment = async () => {
    if (!order || !widgets || !user) return;
    setPaying(true);
    setError('');
    try {
      await widgets.requestPayment({
        orderId: order.order_id,
        orderName: order.order_name,
        successUrl: `${window.location.origin}/billing/success`,
        failUrl: `${window.location.origin}/billing/fail`,
        customerEmail: user.email,
        customerName: user.name,
      });
    } catch (requestError: any) {
      setError(requestError.message ?? '결제 요청을 시작하지 못했습니다.');
      setPaying(false);
    }
  };

  return (
    <ProtectedPage roles={['STUDENT', 'PROFESSOR']}>
      <div className="app-shell flex min-h-screen flex-col">
        <Navbar />
        <main className="mx-auto w-full max-w-3xl flex-1 px-4 py-10">
          <h1 className="text-3xl font-bold text-[#242C34]">결제하기</h1>
          {order && (
            <div className="mt-6 rounded-xl bg-[#F8F9FA] p-5">
              <p className="font-bold">{order.order_name}</p>
              <p className="mt-1 text-2xl font-bold text-[#3B86D1]">{order.amount.toLocaleString('ko-KR')}원</p>
            </div>
          )}
          {error && <p className="mt-6 rounded-xl bg-red-50 p-4 text-red-700">{error}</p>}
          <div id="payment-method" className="mt-6 min-h-40" />
          <div id="agreement" className="mt-4 min-h-20" />
          <button
            type="button"
            disabled={!widgets || !order || paying}
            onClick={requestPayment}
            className="primary-button mt-6 w-full disabled:opacity-50"
          >
            {paying ? '결제창 여는 중...' : order ? `${order.amount.toLocaleString('ko-KR')}원 결제하기` : '결제 준비 중...'}
          </button>
        </main>
        <Footer />
      </div>
    </ProtectedPage>
  );
}
