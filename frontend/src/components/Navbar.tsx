import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';

const roleLabel = {
  STUDENT: '학생',
  PROFESSOR: '교수자',
  ADMIN: '관리자',
};

export default function Navbar() {
  const { user, loading, logout } = useAuth();
  const canAuthor = user?.role === 'PROFESSOR' || user?.role === 'ADMIN';

  return (
    <header className="app-header sticky top-0 z-50">
      <div className="page-container flex min-h-16 flex-wrap items-center justify-between gap-3 py-2">
        <Link href="/" className="flex items-center gap-2 text-xl font-bold">
          <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-[#3B86D1]">Q</span>
          문제은행
        </Link>
        <nav className="flex flex-wrap items-center justify-end gap-1 text-sm font-medium sm:gap-3">
          {canAuthor && (
            <>
              <Link href="/analytics" className="rounded-lg px-3 py-2 hover:bg-white/10">문항 분석</Link>
              <Link href="/create-question" className="rounded-lg px-3 py-2 hover:bg-white/10">문제 출제</Link>
              <Link href="/manage-questions" className="rounded-lg px-3 py-2 hover:bg-white/10">문제 관리</Link>
              {user?.role === 'PROFESSOR' && <Link href="/exam-papers" className="rounded-lg px-3 py-2 hover:bg-white/10">시험지 출력</Link>}
              <Link href="/upload" className="rounded-lg px-3 py-2 hover:bg-white/10">파일 등록</Link>
            </>
          )}
          {user?.role === 'ADMIN' && (
            <>
              <Link href="/admin/billing" className="rounded-lg px-3 py-2 hover:bg-white/10">결제 관리</Link>
              <Link href="/admin/public-exams" className="rounded-lg px-3 py-2 hover:bg-white/10">공통 기출 관리</Link>
            </>
          )}
          {!loading && !user && (
            <>
              <Link href="/login" className="rounded-lg px-3 py-2 hover:bg-white/10">로그인</Link>
              <Link href="/register" className="rounded-lg bg-[#3B86D1] px-3 py-2">회원가입</Link>
            </>
          )}
          {user && (
            <>
              {user.role !== 'ADMIN' && (
                <Link href="/pricing" className="rounded-lg px-3 py-2 hover:bg-white/10">요금제</Link>
              )}
              <Link href="/profile" className="hidden rounded-lg px-3 py-2 text-slate-300 hover:bg-white/10 sm:inline">
                {user.name} · {roleLabel[user.role]}
              </Link>
              <button type="button" onClick={logout} className="rounded-lg px-3 py-2 hover:bg-white/10">로그아웃</button>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}
