import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

interface AuthContextType {
  user: any;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType>({} as AuthContextType);

export const AuthProvider: React.FC<{children: React.ReactNode}> = ({ children }) => {
  const [user, setUser] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  // Check for token in localStorage on load
  useEffect(() => {
    const storedToken = localStorage.getItem('access_token');
    if (storedToken) {
      // (Optional) We could verify token or fetch user info here.
      setUser({ token: storedToken });
    }
  }, []);

  const login = async (email: string, password: string) => {
    try {
      setError(null);
      const res = await axios.post('/api/auth/login', { email, password });
      const { access_token, refresh_token } = res.data;
      // Save tokens
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('refresh_token', refresh_token);
      setUser({ token: access_token });
      // Set auth header for future requests
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
    } catch (err: any) {
      console.error('Login failed', err);
      setError('Invalid credentials');
      setUser(null);
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
    delete axios.defaults.headers.common['Authorization'];
  };

  const value = { user, error, login, logout };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => useContext(AuthContext);
