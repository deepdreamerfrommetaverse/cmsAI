import { useEffect, useState } from 'react'
import Card from './ui/Card'
import { api } from '../api/client'

export default function SocialLimits() {
  const [limits, setLimits] = useState(null)
  useEffect(() => {
    api.get('/v1/social/limits').then(setLimits).catch(() => {})
  }, [])
  if (!limits) return null
  return (
    <Card title="Daily Social Limits">
      <ul>
        {Object.entries(limits).map(([svc, obj]) => (
          <li key={svc} className="flex justify-between">
            <span className="capitalize">{svc}</span>
            <span>{obj.count} / {obj.limit}</span>
          </li>
        ))}
      </ul>
    </Card>
  )
}
