import { FormEvent, useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import { useAuth } from '@/contexts/AuthContext';
import { authAPI } from '@/lib/api';

export default function LoginPage() {
  const router = useRouter();
  const { setSession } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    setLoading(true);
    setError('');
    try {
      const { data } = await authAPI.login({ email, password });
      setSession(data.access_token, data.user);
      const next = typeof router.query.next === 'string' && router.query.next.startsWith('/')
        ? router.query.next
        : data.user.role === 'STUDENT' ? '/' : '/create-question';
      await router.replace(next);
    } catch (requestError: any) {
      setError(requestError.response?.data?.detail ?? '로그인에 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell flex flex-col">
      <Navbar />
      <main className="mx-auto flex w-full max-w-md flex-1 items-center px-4 py-12">
        <section className="surface-card w-full p-8">
          <h1 className="text-3xl font-bold text-[#242C34]">로그인</h1>
          <p className="mt-2 text-[#6C757D]">계정에 로그인해 학습을 시작하세요.</p>
          <form onSubmit={submit} className="mt-8 space-y-5">
            <label className="block text-sm font-semibold">
              이메일
              <input type="email" required value={email} onChange={(e) => setEmail(e.target.value)}
                className="form-control mt-2" autoComplete="email" />
            </label>
            <label className="block text-sm font-semibold">
              비밀번호
              <input type="password" required value={password} onChange={(e) => setPassword(e.target.value)}
                className="form-control mt-2" autoComplete="current-password" />
            </label>
            {error && <p className="rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</p>}
            <button className="primary-button w-full" disabled={loading}>
              {loading ? '로그인 중...' : '로그인'}
            </button>
          </form>
          <p className="mt-6 text-center text-sm text-[#6C757D]">
            계정이 없나요? <Link href="/register" className="font-semibold text-[#3B86D1]">회원가입</Link>
          </p>
        </section>
      </main>
      <Footer />
    </div>
  );
}
