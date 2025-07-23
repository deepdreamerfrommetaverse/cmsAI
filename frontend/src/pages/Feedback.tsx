import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface FeedbackItem {
  id: number;
  message: string;
  email?: string;
  name?: string;
  resolved: boolean;
  created_at: string;
}

const Feedback: React.FC = () => {
  const [feedbackList, setFeedbackList] = useState<FeedbackItem[]>([]);
  const [filter, setFilter] = useState<'all' | 'resolved' | 'unresolved'>('unresolved');
  const [error, setError] = useState<string | null>(null);

  const loadFeedback = async () => {
    try {
      const url = filter === 'all' ? '/api/feedback' : `/api/feedback?resolved=${filter === 'resolved'}`;
      const res = await axios.get<FeedbackItem[]>(url);
      setFeedbackList(res.data);
    } catch (err) {
      console.error('Failed to fetch feedback', err);
      setError('Could not load feedback');
    }
  };

  useEffect(() => { loadFeedback(); }, [filter]);

  const markResolved = async (id: number, resolved: boolean) => {
    try {
      await axios.patch(`/api/feedback/${id}`, { resolved });
      // update list in state:
      setFeedbackList(prev => prev.map(f => f.id === id ? { ...f, resolved, resolved_at: resolved ? new Date().toISOString() : null } : f));
    } catch (err) {
      console.error('Failed to update feedback', err);
    }
  };

  const deleteFeedback = async (id: number) => {
    if (!confirm('Delete this feedback?')) return;
    try {
      await axios.delete(`/api/feedback/${id}`);
      setFeedbackList(prev => prev.filter(f => f.id !== id));
    } catch (err) {
      console.error('Failed to delete feedback', err);
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Reader Feedback</h1>
      {error && <p className="text-red-500">{error}</p>}
      <div className="mb-2">
        <label>Show: </label>
        <select value={filter} onChange={e => setFilter(e.target.value as any)} className="border p-1 rounded">
          <option value="unresolved">Unresolved</option>
          <option value="resolved">Resolved</option>
          <option value="all">All</option>
        </select>
      </div>
      <ul>
        {feedbackList.map(item => (
          <li key={item.id} className="border-b py-2">
            <div>
              <span className="font-semibold">{item.name || 'Anonymous'}</span> &lt;{item.email || 'no email'}&gt;
              <span className="text-xs text-gray-500 ml-2">{new Date(item.created_at).toLocaleString()}</span>
            </div>
            <p className="mb-1">{item.message}</p>
            <div className="text-sm">
              Status: {item.resolved ? <span className="text-green-600">Resolved</span> : <span className="text-yellow-600">Pending</span>}
            </div>
            <div className="mt-1 space-x-2 text-sm">
              {!item.resolved && <button onClick={() => markResolved(item.id, true)} className="px-2 py-1 bg-primary text-white rounded">Mark Resolved</button>}
              {item.resolved && <button onClick={() => markResolved(item.id, false)} className="px-2 py-1 bg-yellow-600 text-white rounded">Reopen</button>}
              <button onClick={() => deleteFeedback(item.id)} className="px-2 py-1 bg-red-500 text-white rounded">Delete</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};
export default Feedback;
