import { useEffect } from 'react'
import { useLocation } from 'react-router-dom'
import { api } from '../api/client'

export default function useTrack() {
  const location = useLocation()
  useEffect(() => {
    api.post('/v1/analytics/track', { path: location.pathname }).catch(() => {})
  }, [location.pathname])
}
