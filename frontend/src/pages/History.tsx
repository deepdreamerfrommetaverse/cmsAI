import React from 'react';
import { useHistory } from '@/hooks/useHistory';
import PdfExportButton from '../components/PdfExportButton';

const History: React.FC = () => {
  const { articles, error } = useHistory();

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Article History</h1>
      {error && <p className="text-red-500">{error}</p>}
      <table className="w-full text-sm">
        <thead className="text-left bg-gray-200 dark:bg-gray-700">
          <tr>
            <th className="p-2">Title</th>
            <th className="p-2">Created</th>
            <th className="p-2">Status</th>
            <th className="p-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          {articles.map(article => (
            <tr key={article.id} className="border-b border-gray-300 dark:border-gray-700">
              <td className="p-2">{article.title}</td>
              <td className="p-2">{new Date(article.created_at).toLocaleString()}</td>
              <td className="p-2">
                {article.published_at ? (
                  <span className="text-green-600">Published</span>
                ) : (
                  <span className="text-yellow-600">Draft</span>
                )}
              </td>
              <td className="p-2">
                {article.wordpress_url &&
                  <a href={article.wordpress_url} target="_blank" className="text-primary underline mr-2">View</a>
                }
                <PdfExportButton articleId={article.id} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
export default History;
