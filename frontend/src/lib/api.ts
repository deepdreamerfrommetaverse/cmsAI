// frontend/src/lib/api.ts
import axios from "axios";

export const api = axios.create({
  baseURL: '/api',        // nginx proxy kieruje /api → backend:8000
  withCredentials: false  // używamy nagłówka, nie ciasteczek
});

// ► interceptor – za każdym żądaniem dorzuca JWT z localStorage
api.interceptors.request.use(cfg => {
  const tok = localStorage.getItem('access_token');
  if (tok) cfg.headers.Authorization = `Bearer ${tok}`;
  return cfg;
});

export default api;
