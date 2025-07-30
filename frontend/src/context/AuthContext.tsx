import React, { createContext, useContext, useState, useEffect } from "react";
import api from "@/lib/api";

interface AuthCtx {
  user: { id: number } | null;
  error: string | null;
  login: (e: string, p: string) => Promise<void>;
  logout: () => void;
}
const AuthContext = createContext<AuthCtx>({} as AuthCtx);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<AuthCtx["user"]>(null);
  const [error, setError] = useState<string | null>(null);

  // 1) token w localStorage → ustaw interceptor od razu
  useEffect(() => {
    const tok = localStorage.getItem("access_token");
    if (tok) {
      api.defaults.headers.common.Authorization = `Bearer ${tok}`;
      setUser({ id: 0 });              // (opcjonalnie: /me endpoint)
    }
  }, []);

  // 2) login
  const login = async (email: string, password: string) => {
    try {
      const { data } = await api.post("/auth/login", { email, password });
      localStorage.setItem("access_token",  data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);
      api.defaults.headers.common.Authorization = `Bearer ${data.access_token}`;
      setUser({ id: 0 });
      setError(null);
    } catch (err) {
      console.error(err);
      setError("Invalid credentials");
      setUser(null);
    }
  };

  // 3) logout
  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    delete api.defaults.headers.common.Authorization;
    setUser(null);
  };

  return <AuthContext.Provider value={{ user, error, login, logout }}>
           {children}
         </AuthContext.Provider>;
};

export const useAuth = () => useContext(AuthContext);
