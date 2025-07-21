import { useState } from 'react'
import Button from '../components/ui/Button'
import Card from '../components/ui/Card'
import { api } from '../api/client'
import SEOPreview from '../components/SEOPreview'

export default function Generator() {
  const [prompt, setPrompt] = useState('')
  const [generated, setGenerated] = useState(null)
  const [loading, setLoading] = useState(false)

  async function handleGenerate() {
    setLoading(true)
    try {
      const data = await api.post('/v1/articles/', {
        title: prompt.slice(0, 60) || 'Untitled',
        slug: prompt.toLowerCase().replace(/\s+/g, '-') + Date.now(),
        body: prompt
      })
      setGenerated(data)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-3xl font-bold mb-4">AI Article Generator</h1>
      <textarea
        value={prompt}
        onChange={e => setPrompt(e.target.value)}
        className="w-full p-3 rounded-lg bg-gray-800"
        placeholder="Type your prompt..."
        rows={4}
      />
      <Button disabled={!prompt || loading} onClick={handleGenerate}>
        {loading ? 'Generating...' : 'Generate'}
      </Button>
      {generated && (
        <Card title={generated.title}>
          <SEOPreview title={generated.title} description={generated.body.slice(0, 155)} />
        </Card>
      )}
    </div>
  )
}
