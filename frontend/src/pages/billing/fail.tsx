import Link from 'next/link';
import { useRouter } from 'next/router';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import ProtectedPage from '@/components/ProtectedPage';


export default function BillingFailPage() {
  const router = useRouter();
  const code = typeof router.query.code === 'string' ? router.query.code : 'PAYMENT_FAILED';
  const rawMessage = typeof router.query.message === 'string' ? router.query.message : '';
  const message = code === 'PAY_PROCESS_CANCELED'
    ? '결제를 취소했습니다.'
    : rawMessage || '결제를 완료하지 못했습니다.';

  return (
    <ProtectedPage roles={['STUDENT', 'PROFESSOR']}>
      <div className="app-shell flex min-h-screen flex-col">
        <Navbar />
        <main className="flex flex-1 items-center justify-center px-4 py-12">
          <section className="surface-card w-full max-w-xl p-10 text-center">
            <h1 className="text-3xl font-bold text-red-700">결제 실패</h1>
            <p className="mt-4 text-[#6C757D]">{message}</p>
            <p className="mt-2 text-xs text-[#ADB5BD]">오류 코드: {code}</p>
            <Link href="/pricing" className="primary-button mt-8 inline-block">요금제로 돌아가기</Link>
          </section>
        </main>
        <Footer />
      </div>
    </ProtectedPage>
  );
}
