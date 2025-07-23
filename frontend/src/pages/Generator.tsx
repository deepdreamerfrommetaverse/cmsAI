import React, { useState } from 'react';
import { useGenerator } from '../hooks/useGenerator';

const Generator: React.FC = () => {
  const [topic, setTopic] = useState('');
  const { result, loading, error, generateArticle, publishArticle } = useGenerator();

  const handleGenerate = async () => {
    if (!topic) return;
    await generateArticle(topic);
  };

  const handlePublish = async () => {
    if (result) {
      try {
        const published = await publishArticle(result.id);
        alert('Article published! You can view it at: ' + published.wordpress_url);
      } catch {
        alert('Publish failed.');
      }
    }
  };

  return (
    <div className="generator">
      <h1 className="text-2xl font-bold mb-4">AI Article Generator</h1>
      <div className="mb-4">
        <textarea
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          className="w-full p-2 border rounded"
          placeholder="Enter a topic for the article..."
          rows={3}
        />
      </div>
      <button
        onClick={handleGenerate}
        disabled={loading}
        className="bg-primary text-white px-4 py-2 rounded hover:bg-primary-dark disabled:opacity-50"
      >
        {loading ? 'Generating...' : 'Generate Article'}
      </button>
      {error && <p className="text-red-500 mt-2">{error}</p>}
      {result && (
        <div className="mt-6">
          <h2 className="text-xl font-bold mb-2">{result.title}</h2>
          {result.image_url && <img src={result.image_url} alt="Hero" className="my-2 max-w-full"/>}
          <p className="whitespace-pre-line">{result.content}</p>
          <div className="mt-4">
            {result.wordpress_url ? (
              <a href={result.wordpress_url} target="_blank" className="text-primary font-semibold underline">View on WordPress</a>
            ) : (
              <button onClick={handlePublish} className="bg-green-600 text-white px-3 py-2 rounded">Publish to WordPress</button>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
export default Generator;
