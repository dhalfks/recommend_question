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
    billingAPI.confirm({ payment_key: paymentKey, order_id: orderId, amount })
      .then(() => {
        sessionStorage.removeItem(`billing-order:${orderId}`);
        setState('success');
        setMessage('결제가 완료되고 이용권이 활성화되었습니다.');
      })
      .catch((error: any) => {
        const detail = error.response?.data?.detail;
        setState('error');
        setMessage(detail?.message ?? (typeof detail === 'string' ? detail : '결제 승인에 실패했습니다. 고객센터에 문의해 주세요.'));
      });
  }, [router.isReady, router.query]);

  return (
    <ProtectedPage roles={['STUDENT', 'PROFESSOR']}>
      <div className="app-shell flex min-h-screen flex-col">
        <Navbar />
        <main className="flex flex-1 items-center justify-center px-4 py-12">
          <section className="surface-card w-full max-w-xl p-10 text-center">
            <h1 className={`text-3xl font-bold ${state === 'error' ? 'text-red-700' : 'text-[#242C34]'}`}>
              {state === 'confirming' ? '결제 확인 중' : state === 'success' ? '결제 완료' : '결제 확인 실패'}
            </h1>
            <p className="mt-4 text-[#6C757D]">{message}</p>
            {state !== 'confirming' && (
              <div className="mt-8 flex justify-center gap-3">
                <Link href="/profile" className="primary-button">내 이용권 확인</Link>
                {state === 'error' && <Link href="/pricing" className="secondary-button">다시 시도</Link>}
              </div>
            )}
          </section>
        </main>
        <Footer />
      </div>
    </ProtectedPage>
  );
}
