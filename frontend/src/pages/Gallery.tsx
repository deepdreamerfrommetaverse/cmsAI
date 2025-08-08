import React from 'react';
import { useGallery } from '@/hooks/useGallery';

const Gallery: React.FC = () => {
  const { items, error } = useGallery();

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Image Gallery</h1>
      {error && <p className="text-red-500">{error}</p>}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {items.map(item => (
          <div key={item.id} className="border p-2 rounded">
            {item.image_url ? (
              <img src={item.image_url} alt={item.title} className="w-full h-auto mb-2"/>
            ) : (
              <div className="bg-gray-300 text-center py-8 mb-2">No Image</div>
            )}
            <h3 className="font-semibold text-sm">{item.title}</h3>
            {item.wordpress_url &&
              <a href={item.wordpress_url} target="_blank" className="text-primary text-xs underline">View Post</a>
            }
          </div>
        ))}
      </div>
    </div>
  );
};
export default Gallery;
