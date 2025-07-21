import { useEffect, useState } from 'react'
import { api } from '../api/client'

export function useArticles() {
  const [articles, setArticles] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/v1/articles/').then(data => {
      setArticles(data)
      setLoading(false)
    })
  }, [])

  return { articles, loading }
}
