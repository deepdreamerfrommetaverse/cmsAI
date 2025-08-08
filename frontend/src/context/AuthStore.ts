import api from "../lib/api";
// src/context/AuthStore.ts


let auth: ReturnType<typeof import("./AuthContext").useAuth> | null = null;
export const setAuth   = (v: any) => (auth = v);
export const getAuth   = () => auth;
export const setAccess = (tok: string) => {
  localStorage.setItem("access_token", tok);
  api.defaults.headers.common.Authorization = `Bearer ${tok}`;
};
