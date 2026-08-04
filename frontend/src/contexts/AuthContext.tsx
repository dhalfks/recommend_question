import { createContext, useContext, useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { authAPI, AuthUser } from '@/lib/api';

type AuthContextValue = {
  user: AuthUser | null;
  loading: boolean;
  setSession: (token: string, user: AuthUser) => void;
  setUser: (user: AuthUser) => void;
  logout: () => void;
};

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = window.localStorage.getItem('access_token');
    if (!token) {
      setLoading(false);
      return;
    }
    authAPI
      .me()
      .then(({ data }) => setUser(data))
      .catch(() => window.localStorage.removeItem('access_token'))
      .finally(() => setLoading(false));
  }, []);

  const setSession = (token: string, nextUser: AuthUser) => {
    window.localStorage.setItem('access_token', token);
    setUser(nextUser);
  };

  const logout = () => {
    window.localStorage.removeItem('access_token');
    setUser(null);
    router.push('/login');
  };

  return (
    <AuthContext.Provider value={{ user, loading, setSession, setUser, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used inside AuthProvider');
  return context;
}
