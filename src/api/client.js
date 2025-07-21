export const api = {
  async get(path) {
    const res = await fetch('/api' + path)
    if (!res.ok) throw new Error('API error')
    return res.json()
  },
  async post(path, body) {
    const res = await fetch('/api' + path, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    })
    if (!res.ok) throw new Error('API error')
    return res.json()
  }
}
