// src/lib/api.ts
import axios from "axios";
import { getAuth, setAccess } from "@/context/AuthStore"; // mała pomocnicza “klasa” – patrz niżej

const api = axios.create({ baseURL: "/api" });

// ↳ 1)  dodaj token do żądań
api.interceptors.request.use(cfg => {
  const tok = localStorage.getItem("access_token");
  if (tok) cfg.headers.Authorization = `Bearer ${tok}`;
  return cfg;
});

// ↳ 2)  gdy backend zwróci 401 + "Token expired" spróbuj odświeżyć
api.interceptors.response.use(
  res => res,
  async err => {
    if (
      err.response?.status === 401 &&
      err.response.data?.detail === "Token expired"
    ) {
      try {
        const refresh = localStorage.getItem("refresh_token");
        if (!refresh) throw new Error("brak refresh‑tokenu");

        // pobierz nowy access‑token
        const { data } = await axios.post(
          "/api/auth/refresh",
          {},
          { headers: { Authorization: `Bearer ${refresh}` } }
        );

        setAccess(data.access_token);                 // zapisz w LS + wstrzyknij do api
        err.config.headers.Authorization = `Bearer ${data.access_token}`;
        return api.request(err.config);               // powtórz oryginalne żądanie
      } catch (e) {
        // refresh też się nie udał → wyloguj
        getAuth()?.logout();
      }
    }
    return Promise.reject(err);
  }
);

export default api;
