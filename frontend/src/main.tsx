import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import { AuthProvider } from './context/AuthContext';
import { ThemeConfigProvider } from './context/ThemeConfigContext';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <ThemeConfigProvider>
      <AuthProvider>
        <App />
      </AuthProvider>
    </ThemeConfigProvider>
  </React.StrictMode>
);
