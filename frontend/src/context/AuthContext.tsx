import React, { createContext, useContext, useState, useEffect } from "react";
import api from "@/lib/api";
import { setAuth, setAccess } from "./AuthStore";

interface AuthCtx {
  user: { id: number } | null;
  error: string | null;
  login: (e: string, p: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthCtx>({} as AuthCtx);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user,  setUser]  = useState<AuthCtx["user"]>(null);
  const [error, setError] = useState<string | null>(null);

  /* --- 1) token w localStorage -> interceptor --- */
  useEffect(() => {
    const tok = localStorage.getItem("access_token");
    if (tok) {
      api.defaults.headers.common.Authorization = `Bearer ${tok}`;
      setUser({ id: 0 });   // uproszczone – możesz dociągnąć /me
    }
  }, []);

  /* --- 2) login --- */
  const login = async (email: string, password: string) => {
    try {
      const { data } = await api.post("/auth/login", { email, password });
      setAccess(data.access_token);                    // zapis + nagłówek
      localStorage.setItem("refresh_token", data.refresh_token);
      setUser({ id: 0 });
      setError(null);
    } catch (err) {
      console.error(err);
      setError("Invalid credentials");
      setUser(null);
    }
  };

  /* --- 3) logout --- */
  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    delete api.defaults.headers.common.Authorization;
    setUser(null);
  };

  /* --- 4) zarejestruj kontekst w store, żeby interceptor mógł wołać logout() --- */
  useEffect(() => { setAuth({ logout }); }, []);

  return (
    <AuthContext.Provider value={{ user, error, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
