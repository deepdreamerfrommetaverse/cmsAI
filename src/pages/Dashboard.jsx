import { useArticles } from '../hooks/useArticles'
import Card from '../components/ui/Card'

export default function Dashboard() {
  const { articles, loading } = useArticles()
  return (
    <div className="p-6 space-y-4">
      <h1 className="text-3xl font-bold mb-4">Dashboard</h1>
      {loading && <p>Loading...</p>}
      {!loading && (
        <Card title="Latest Articles">
          <ul className="space-y-2">
            {articles.map(a => (
              <li key={a.id} className="border-b border-gray-700 pb-2">
                <span className="text-monday">{a.title}</span>
              </li>
            ))}
          </ul>
        </Card>
      )}
    </div>
  )
}
