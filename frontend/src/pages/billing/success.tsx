import { useEffect, useRef, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import ProtectedPage from '@/components/ProtectedPage';
import { billingAPI } from '@/lib/api';

export default function BillingSuccessPage() {
  const router = useRouter();
  const requested = useRef(false);
  const [state, setState] = useState<'confirming' | 'success' | 'error'>('confirming');
  const [message, setMessage] = useState('결제를 확인하고 있습니다. 창을 닫지 마세요.');

  useEffect(() => {
    if (!router.isReady || requested.current) return;
    const paymentKey = typeof router.query.paymentKey === 'string' ? router.query.paymentKey : '';
    const orderId = typeof router.query.orderId === 'string' ? router.query.orderId : '';
    const amountText = typeof router.query.amount === 'string' ? router.query.amount : '';
    const amount = Number(amountText);
    if (!paymentKey || !orderId || !Number.isSafeInteger(amount) || amount <= 0) {
      setState('error');
      setMessage('결제 승인 정보가 올바르지 않습니다.');
      return;
    }
    requested.current = true;

    const confirmWithRetry = async () => {
      let lastError: any;
      for (let attempt = 0; attempt < 3; attempt += 1) {
        try {
          await billingAPI.confirm({ payment_key: paymentKey, order_id: orderId, amount });
          return;
        } catch (error: any) {
          lastError = error;
          const retryable = !error.response || error.response.status >= 500;
          if (!retryable || attempt === 2) break;
          setMessage(`토스페이먼츠 응답을 다시 확인하고 있습니다. (${attempt + 2}/3)`);
          await new Promise((resolve) => window.setTimeout(resolve, 1000 * (attempt + 1)));
        }
      }

      // Toss 승인은 끝났지만 첫 응답만 유실될 수 있으므로 저장 상태를 마지막에 확인한다.
      try {
        const { data } = await billingAPI.payments();
        if (data.some((payment) => payment.order_id === orderId && payment.status === 'PAID')) return;
      } catch {
        // 상태 조회도 실패하면 원래 승인 오류를 사용자에게 안내한다.
      }
      throw lastError;
    };

    void confirmWithRetry()
      .then(() => {
        sessionStorage.removeItem(`billing-order:${orderId}`);
        setState('success');
        setMessage('결제가 완료되고 이용권이 활성화되었습니다.');
      })
      .catch((error: any) => {
        const detail = error?.response?.data?.detail;
        setState('error');
        setMessage(detail?.message ?? (typeof detail === 'string' ? detail : '결제 확인이 지연되고 있습니다. 잠시 후 다시 확인해 주세요.'));
      });
  }, [router.isReady, router.query]);

  return <ProtectedPage roles={['STUDENT', 'PROFESSOR']}>
    <div className="app-shell flex min-h-screen flex-col"><Navbar />
      <main className="flex flex-1 items-center justify-center px-4 py-12">
        <section className="surface-card w-full max-w-xl p-10 text-center">
          <h1 className={`text-3xl font-bold ${state === 'error' ? 'text-amber-700' : 'text-[#242C34]'}`}>
            {state === 'confirming' ? '결제 확인 중' : state === 'success' ? '결제 완료' : '결제 확인 지연'}
          </h1>
          <p className="mt-4 text-[#6C757D]">{message}</p>
          {state !== 'confirming' && <div className="mt-8 flex justify-center gap-3">
            <Link href="/profile" className="primary-button">내 이용권 확인</Link>
            {state === 'error' && <button type="button" className="secondary-button" onClick={() => window.location.reload()}>결제 다시 확인</button>}
          </div>}
        </section>
      </main><Footer />
    </div>
  </ProtectedPage>;
}
