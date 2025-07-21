import { Routes, Route, Link, Navigate } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Generator from './pages/Generator'
import Stats from './pages/Stats'
import History from './pages/History'
import Settings from './pages/Settings'
import Feedback from './pages/Feedback'
import useTrack from './hooks/useTrack'

function App() {
  useTrack()
  return (
    <div className="flex h-screen">
      <aside className="w-56 bg-gray-800 p-4">
        <nav className="space-y-2">
          <Link to="/" className="block text-monday font-semibold">Dashboard</Link>
          <Link to="/generator" className="block">Generator</Link>
          <Link to="/stats" className="block">Stats</Link>
          <Link to="/history" className="block">History</Link>
          <Link to="/settings" className="block">Settings</Link>
          <Link to="/feedback" className="block">Feedback</Link>
        </nav>
      </aside>
      <main className="flex-1 overflow-y-auto">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/generator" element={<Generator />} />
          <Route path="/stats" element={<Stats />} />
          <Route path="/history" element={<History />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/feedback" element={<Feedback />} />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
