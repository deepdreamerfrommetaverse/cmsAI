import { useState } from 'react'
import Button from '../components/ui/Button'
import Card from '../components/ui/Card'
import { api } from '../api/client'
import SEOPreview from '../components/SEOPreview'
import HeroImage from '../components/HeroImage'

export default function Generator() {
  const [prompt, setPrompt] = useState('')
  const [article, setArticle] = useState(null)
  const [loading, setLoading] = useState(false)

  async function handleGenerate() {
    setLoading(true)
    try {
      const data = await api.post('/v1/prompt-agent/', { prompt })
      setArticle(data)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-3xl font-bold mb-4">AI Prompt Agent</h1>
      <textarea
        value={prompt}
        onChange={e => setPrompt(e.target.value)}
        className="w-full p-3 rounded-lg bg-gray-800"
        placeholder="Describe the article you'd like..."
        rows={4}
      />
      <Button disabled={!prompt || loading} onClick={handleGenerate}>
        {loading ? 'Generating...' : 'Generate & Publish'}
      </Button>

      {article && (
        <Card title={article.title}>
          {article.hero_url && <HeroImage src={article.hero_url} alt={article.title} />}
          <SEOPreview title={article.meta_title} description={article.meta_description} />
          <p className="mt-4">WordPress ID: {article.wp_post_id}</p>
        </Card>
      )}
    </div>
  )
}
