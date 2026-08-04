import { FormEvent, useEffect, useState } from 'react';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import ProtectedPage from '@/components/ProtectedPage';
import { useAuth } from '@/contexts/AuthContext';
import { authAPI } from '@/lib/api';

const roleLabels = {
  STUDENT: '학생',
  PROFESSOR: '교수자',
  ADMIN: '관리자',
};

export default function ProfilePage() {
  const { user, setUser } = useAuth();
  const [form, setForm] = useState({
    name: '',
    phone: '',
    email: '',
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  });
  const [message, setMessage] = useState('');
  const [isError, setIsError] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!user) return;
    setForm((current) => ({
      ...current,
      name: user.name,
      phone: user.phone,
      email: user.email,
    }));
  }, [user]);

  const update = (field: keyof typeof form, value: string) =>
    setForm((current) => ({ ...current, [field]: value }));

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    setMessage('');
    setIsError(false);

    if (form.newPassword && form.newPassword !== form.confirmPassword) {
      setMessage('새 비밀번호가 서로 일치하지 않습니다.');
      setIsError(true);
      return;
    }

    setLoading(true);
    try {
      const payload = {
        name: form.name,
        phone: form.phone,
        email: form.email,
        ...(form.newPassword
          ? {
              current_password: form.currentPassword,
              new_password: form.newPassword,
            }
          : {}),
      };
      const { data } = await authAPI.updateMe(payload);
      setUser(data);
      setForm((current) => ({
        ...current,
        currentPassword: '',
        newPassword: '',
        confirmPassword: '',
      }));
      setMessage('회원정보가 수정되었습니다.');
    } catch (error: any) {
      const detail = error.response?.data?.detail;
      setMessage(Array.isArray(detail) ? detail[0]?.msg : detail ?? '회원정보 수정에 실패했습니다.');
      setIsError(true);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ProtectedPage>
      <div className="app-shell flex flex-col">
        <Navbar />
        <main className="mx-auto w-full max-w-2xl flex-1 px-4 py-12">
          <h1 className="text-4xl font-bold text-[#242C34]">회원정보 수정</h1>
          <p className="mt-3 text-[#6C757D]">내 기본 정보와 비밀번호를 관리합니다.</p>

          <form onSubmit={submit} className="surface-card mt-8 space-y-6 p-8">
            <div className="rounded-xl bg-[#F8F9FA] p-4">
              <span className="text-sm text-[#6C757D]">현재 권한</span>
              <p className="mt-1 font-bold text-[#242C34]">
                {user ? roleLabels[user.role] : ''}
              </p>
              <p className="mt-1 text-xs text-[#6C757D]">
                권한은 본인이 직접 변경할 수 없습니다.
              </p>
            </div>

            <label className="block text-sm font-semibold">이름
              <input required minLength={2} value={form.name}
                onChange={(e) => update('name', e.target.value)}
                className="form-control mt-2" autoComplete="name" />
            </label>
            <label className="block text-sm font-semibold">전화번호
              <input required type="tel" value={form.phone}
                onChange={(e) => update('phone', e.target.value)}
                className="form-control mt-2" autoComplete="tel" />
            </label>
            <label className="block text-sm font-semibold">이메일
              <input required type="email" value={form.email}
                onChange={(e) => update('email', e.target.value)}
                className="form-control mt-2" autoComplete="email" />
            </label>

            <div className="border-t border-[#E9ECEF] pt-6">
              <h2 className="text-lg font-bold text-[#242C34]">비밀번호 변경</h2>
              <p className="mt-1 text-sm text-[#6C757D]">
                변경하지 않으려면 아래 항목을 비워두세요.
              </p>
              <div className="mt-4 space-y-4">
                <label className="block text-sm font-semibold">현재 비밀번호
                  <input type="password" value={form.currentPassword}
                    onChange={(e) => update('currentPassword', e.target.value)}
                    className="form-control mt-2" autoComplete="current-password" />
                </label>
                <label className="block text-sm font-semibold">새 비밀번호
                  <input type="password" minLength={8} value={form.newPassword}
                    onChange={(e) => update('newPassword', e.target.value)}
                    className="form-control mt-2" autoComplete="new-password" />
                </label>
                <label className="block text-sm font-semibold">새 비밀번호 확인
                  <input type="password" minLength={8} value={form.confirmPassword}
                    onChange={(e) => update('confirmPassword', e.target.value)}
                    className="form-control mt-2" autoComplete="new-password" />
                </label>
              </div>
            </div>

            {message && (
              <p className={`rounded-lg p-3 text-sm ${isError ? 'bg-red-50 text-red-700' : 'bg-green-50 text-green-700'}`}>
                {message}
              </p>
            )}
            <button disabled={loading} className="primary-button w-full">
              {loading ? '저장 중...' : '변경사항 저장'}
            </button>
          </form>
        </main>
        <Footer />
      </div>
    </ProtectedPage>
  );
}
