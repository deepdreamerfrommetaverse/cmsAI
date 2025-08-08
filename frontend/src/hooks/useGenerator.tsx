import { useState } from 'react';
import api from '@/lib/api';

interface GeneratedArticle {
  id: number;
  title: string;
  content: string;
  meta_description: string;
  image_url?: string;
  wordpress_url?: string;
}

export function useGenerator() {
  const [result, setResult] = useState<GeneratedArticle | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const generateArticle = async (topic: string) => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.post<GeneratedArticle>('/articles/generate', { topic });
      setResult(res.data);
    } catch (err: any) {
      console.error('Generation failed:', err);
      setError('Failed to generate article');
    } finally {
      setLoading(false);
    }
  };

  const publishArticle = async (articleId: number) => {
    // Publish a generated article
    try {
      const res = await api.post<GeneratedArticle>(`/articles/${articleId}/publish`);
      setResult(res.data);  // update with published info (wordpress_url etc.)
      return res.data;
    } catch (err) {
      console.error('Publish failed:', err);
      throw err;
    }
  };

  return { result, loading, error, generateArticle, publishArticle };
}
