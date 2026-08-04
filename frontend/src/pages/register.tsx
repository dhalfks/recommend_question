import { FormEvent, useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import { useAuth } from '@/contexts/AuthContext';
import { authAPI, UserRole } from '@/lib/api';

export default function RegisterPage() {
  const router = useRouter();
  const { setSession } = useAuth();
  const [form, setForm] = useState({
    name: '', phone: '', email: '', password: '', role: 'STUDENT' as UserRole,
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    setLoading(true);
    setError('');
    try {
      const { data } = await authAPI.register(form);
      setSession(data.access_token, data.user);
      await router.replace(data.user.role === 'STUDENT' ? '/' : '/create-question');
    } catch (requestError: any) {
      const detail = requestError.response?.data?.detail;
      setError(Array.isArray(detail) ? detail[0]?.msg : detail ?? '회원가입에 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const update = (field: keyof typeof form, value: string) =>
    setForm((current) => ({ ...current, [field]: value }));

  return (
    <div className="app-shell flex flex-col">
      <Navbar />
      <main className="mx-auto w-full max-w-lg flex-1 px-4 py-12">
        <section className="surface-card p-8">
          <h1 className="text-3xl font-bold text-[#242C34]">회원가입</h1>
          <p className="mt-2 text-[#6C757D]">학생 또는 교수자 계정을 선택해 가입하세요.</p>
          <form onSubmit={submit} className="mt-8 space-y-5">
            <div className="grid grid-cols-2 gap-3">
              {(['STUDENT', 'PROFESSOR'] as UserRole[]).map((role) => (
                <button key={role} type="button" onClick={() => update('role', role)}
                  className={`rounded-xl border p-4 font-semibold ${form.role === role ? 'border-[#3B86D1] bg-blue-50 text-[#2F70B5]' : 'border-[#CED4DA]'}`}>
                  {role === 'STUDENT' ? '학생' : '교수자'}
                </button>
              ))}
            </div>
            <label className="block text-sm font-semibold">이름
              <input required minLength={2} value={form.name} onChange={(e) => update('name', e.target.value)}
                className="form-control mt-2" autoComplete="name" />
            </label>
            <label className="block text-sm font-semibold">전화번호
              <input required type="tel" value={form.phone} onChange={(e) => update('phone', e.target.value)}
                className="form-control mt-2" autoComplete="tel" placeholder="010-1234-5678" />
            </label>
            <label className="block text-sm font-semibold">이메일
              <input required type="email" value={form.email} onChange={(e) => update('email', e.target.value)}
                className="form-control mt-2" autoComplete="email" />
            </label>
            <label className="block text-sm font-semibold">비밀번호
              <input required minLength={8} type="password" value={form.password}
                onChange={(e) => update('password', e.target.value)}
                className="form-control mt-2" autoComplete="new-password" />
              <span className="mt-1 block font-normal text-[#6C757D]">8자 이상 입력하세요.</span>
            </label>
            {error && <p className="rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</p>}
            <button className="primary-button w-full" disabled={loading}>
              {loading ? '가입 중...' : '회원가입'}
            </button>
          </form>
          <p className="mt-6 text-center text-sm text-[#6C757D]">
            이미 계정이 있나요? <Link href="/login" className="font-semibold text-[#3B86D1]">로그인</Link>
          </p>
        </section>
      </main>
      <Footer />
    </div>
  );
}
