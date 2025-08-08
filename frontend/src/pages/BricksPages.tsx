import React, { useEffect, useState } from 'react';
import api from "@/lib/api";
import ConflictModal from '../components/ConflictModal';

interface PageInfo {
  id: number;
  title: string;
  wordpress_url: string;
}

const BricksPages: React.FC = () => {
  const [pages, setPages] = useState<PageInfo[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [conflict, setConflict] = useState<{diff: string} | null>(null);

  useEffect(() => {
    const fetchPages = async () => {
      try {
        // We will reuse articles list for "Bricks Pages" for now
        const res = await api.get<PageInfo[]>('/articles?published=true');
        setPages(res.data);
      } catch (err) {
        console.error('Failed to load pages', err);
        setError('Failed to load pages');
      }
    };
    fetchPages();
  }, []);

  const handleRegenerate = async (id: number) => {
    // In a real scenario, we might check for conflict by comparing WP content vs DB content.
    // Here we'll simulate no conflict and directly call regenerate in backend (update content).
    try {
      await api.put(`/articles/${id}`, { });  // triggers an update (if needed)
      alert('Article content regenerated (new version saved).');
    } catch (err) {
      console.error('Regenerate failed:', err);
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Bricks Pages</h1>
      {error && <p className="text-red-500">{error}</p>}
      <ul>
        {pages.map(page => (
          <li key={page.id} className="mb-2">
            <a href={page.wordpress_url} target="_blank" className="text-primary underline">{page.title}</a>
            <button onClick={() => handleRegenerate(page.id)} className="ml-4 text-sm bg-primary text-white px-2 py-1 rounded">Regenerate</button>
          </li>
        ))}
      </ul>
      {conflict && (
        <ConflictModal
          diffText={conflict.diff}
          onClose={() => setConflict(null)}
          onConfirm={() => { /* Overwrite action */ setConflict(null); }}
        />
      )}
    </div>
  );
};
export default BricksPages;
