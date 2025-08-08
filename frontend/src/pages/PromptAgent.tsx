import React, { useState } from 'react';
import { useAgent } from '@/hooks/useAgent';

const PromptAgent: React.FC = () => {
  const [prompt, setPrompt] = useState('');
  const { result, loading, error, generateArticle } = useAgent();

  const handleSubmit = () => {
    if (!prompt) return;
    generateArticle(prompt);
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Prompt Agent</h1>
      <p className="mb-4 text-sm text-gray-600 dark:text-gray-300">This tool generates article text, layout, SEO, and image in one go from a single prompt.</p>
      <textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Enter a prompt describing the desired content..."
        className="w-full p-2 border rounded mb-2"
        rows={4}
      />
      <button onClick={handleSubmit} disabled={loading} className="bg-primary text-white px-4 py-2 rounded">
        {loading ? 'Generating...' : 'Generate'}
      </button>
      {error && <div className="text-red-500 mt-2">{error}</div>}
      {result && (
        <div className="mt-6">
          <h2 className="text-xl font-bold">{result.title}</h2>
          {result.image_url && <img src={result.image_url} alt="Hero" className="my-2 max-w-full" />}
          <p className="whitespace-pre-line">{result.content}</p>
          <p className="text-sm text-gray-500 mt-2">SEO Meta Description: {result.meta_description}</p>
        </div>
      )}
    </div>
  );
};
export default PromptAgent;
