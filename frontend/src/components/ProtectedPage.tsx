import { useEffect } from 'react';
import { useRouter } from 'next/router';
import { UserRole } from '@/lib/api';
import { useAuth } from '@/contexts/AuthContext';

export default function ProtectedPage({
  children,
  roles,
}: {
  children: React.ReactNode;
  roles?: UserRole[];
}) {
  const router = useRouter();
  const { user, loading } = useAuth();

  useEffect(() => {
    if (loading) return;
    if (!user) {
      router.replace(`/login?next=${encodeURIComponent(router.asPath)}`);
    } else if (roles && !roles.includes(user.role)) {
      router.replace('/quiz');
    }
  }, [loading, roles, router, user]);

  if (loading || !user || (roles && !roles.includes(user.role))) {
    return (
      <main className="flex min-h-[60vh] items-center justify-center text-[#6C757D]">
        확인 중...
      </main>
    );
  }
  return <>{children}</>;
}
