// ═══════════════════════════════════════════════════════════
// DentAI Mobile — Auth Context
// ═══════════════════════════════════════════════════════════
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface User {
  id: number;
  name: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  login: (user: User, token: string) => Promise<void>;
  logout: () => Promise<void>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType>({
  user: null, token: null, isLoading: true,
  login: async () => {}, logout: async () => {},
  isAuthenticated: false,
});

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const restoreSession = async () => {
      try {
        const [storedToken, storedUser] = await AsyncStorage.multiGet(['access_token', 'user']);
        const t = storedToken[1];
        const u = storedUser[1] ? JSON.parse(storedUser[1]) : null;
        if (t && u) { setToken(t); setUser(u); }
      } catch {}
      finally { setIsLoading(false); }
    };
    restoreSession();
  }, []);

  const login = async (userData: User, accessToken: string) => {
    setUser(userData);
    setToken(accessToken);
    await AsyncStorage.multiSet([
      ['access_token', accessToken],
      ['user', JSON.stringify(userData)],
    ]);
  };

  const logout = async () => {
    setUser(null);
    setToken(null);
    await AsyncStorage.multiRemove(['access_token', 'user']);
  };

  return (
    <AuthContext.Provider value={{
      user, token, isLoading,
      login, logout,
      isAuthenticated: !!token && !!user,
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
