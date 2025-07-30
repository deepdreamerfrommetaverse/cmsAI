import { useEffect, useState } from 'react';
import api from "@/lib/api";

interface ArticleInfo {
  id: number;
  title: string;
  created_at: string;
  published_at?: string;
  wordpress_url?: string;
}

export function useHistory() {
  const [articles, setArticles] = useState<ArticleInfo[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await api.get<ArticleInfo[]>('/api/articles');
        setArticles(res.data);
      } catch (err) {
        console.error('Failed to load history:', err);
        setError('Unable to fetch article history');
      }
    };
    fetchHistory();
  }, []);

  return { articles, error };
}
