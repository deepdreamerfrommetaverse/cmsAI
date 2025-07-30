import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import Sidebar from './components/Sidebar';
import Generator from './pages/Generator';
import PromptAgent from './pages/PromptAgent';
import Gallery from './pages/Gallery';
import History from './pages/History';
import Stats from './pages/Stats';
import BricksPages from './pages/BricksPages';
import Settings from './pages/Settings';
import Feedback from './pages/Feedback';

function App() {
  const { user } = useAuth();
  // If not authenticated, show login form instead of app (simplified)
  if (!user) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-100 dark:bg-gray-800">
        <div className="p-6 bg-white dark:bg-gray-700 rounded shadow">
          <h1 className="text-2xl mb-4 font-bold text-center">AI CMS Login</h1>
          <LoginForm />
        </div>
      </div>
    );
  }
  return (
    <Router>
      <div className="flex h-screen">
        <Sidebar />
        <main className="flex-1 bg-gray-50 dark:bg-gray-900 p-4 overflow-auto">
          <Routes>
            <Route path="/generator" element={<Generator />} />
            <Route path="/prompt-agent" element={<PromptAgent />} />
            <Route path="/gallery" element={<Gallery />} />
            <Route path="/history" element={<History />} />
            <Route path="/stats" element={<Stats />} />
            <Route path="/bricks-pages" element={<BricksPages />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/feedback" element={<Feedback />} />
            <Route path="*" element={<Navigate to="/generator" replace />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;

// A simple login form component within App (for brevity)
import { useState } from 'react';
import React from 'react';

function LoginForm() {
  const { login, error } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await login(email, password);
  };
  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <input
        type="email"
        name="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="w-full p-2 border border-gray-300 rounded"
        required
      />
      <input
        type="password"
        name="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="w-full p-2 border border-gray-300 rounded"
        required
      />
      {error && <div className="text-red-500 text-sm">{error}</div>}
      <button
        type="submit"
        className="w-full bg-primary hover:bg-primary-dark text-white font-semibold py-2 px-4 rounded"
      >
        Login
      </button>
    </form>
  );
}
