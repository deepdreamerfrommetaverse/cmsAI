import { useEffect, useState } from 'react'
import Card from '../components/ui/Card'
import { api } from '../api/client'

export default function Stats() {
  const [stats, setStats] = useState(null)
  const [revenue, setRevenue] = useState(null)

  useEffect(() => {
    api.get('/v1/analytics/stats').then(setStats)
    api.get('/v1/analytics/stripe/revenue').then(setRevenue)
  }, [])

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-3xl font-bold mb-4">Site Statistics</h1>
      {stats && (
        <Card title="Page views (last 7 days)">
          <p className="text-2xl font-semibold">{stats.total}</p>
          <ul className="mt-2 space-y-1">
            {stats.by_day.map(d => (
              <li key={d.date} className="flex justify-between">
                <span>{d.date}</span>
                <span>{d.views}</span>
              </li>
            ))}
          </ul>
        </Card>
      )}
      {revenue && (
        <Card title="Stripe revenue (30 dni)">
          <p className="text-2xl font-semibold">${revenue.revenue.toFixed(2)}</p>
        </Card>
      )}
    </div>
  )
}
