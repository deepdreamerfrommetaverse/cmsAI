import React from 'react';
import ReactDOM from 'react-dom/client';
import api from "@/lib/api";
import App from './App';
import { AuthProvider } from './context/AuthContext';
import { ThemeConfigProvider } from './context/ThemeConfigContext';

// [Dodane] Ustawienie bazowego URL dla axios w trybie Electron (prod):
const ua = navigator.userAgent.toLowerCase();
if (ua.includes('electron')) {
    api.defaults.baseURL = 'http://127.0.0.1:8000';
}

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <ThemeConfigProvider>
      <AuthProvider>
        <App />
      </AuthProvider>
    </ThemeConfigProvider>
  </React.StrictMode>
);
