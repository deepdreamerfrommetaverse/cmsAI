import { useEffect, useState } from 'react';
import api from '@/lib/api';

interface ArticleBrief {
  id: number;
  title: string;
  image_url?: string;
  wordpress_url?: string;
}

export function useGallery() {
  const [items, setItems] = useState<ArticleBrief[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchGallery = async () => {
      try {
        // Fetch all articles that have images (for simplicity fetch all and filter)
        const res = await api.get<ArticleBrief[]>('/api/articles?published=true');
        const allArticles = res.data;
        const withImages = allArticles.filter(article => article.image_url);
        setItems(withImages);
      } catch (err) {
        console.error('Failed to load gallery:', err);
        setError('Failed to load gallery');
      }
    };
    fetchGallery();
  }, []);

  return { items, error };
}
