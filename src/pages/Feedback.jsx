import { useState } from 'react'
import Button from '../components/ui/Button'
import { api } from '../api/client'

export default function Feedback() {
  const [message, setMessage] = useState('')
  const [sent, setSent] = useState(false)

  async function submit() {
    await api.post('/v1/feedback/', { message })
    setSent(true)
  }

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-4">Feedback</h1>
      {sent ? (
        <p className="text-green-400">Thank you for your feedback!</p>
      ) : (
        <>
          <textarea
            value={message}
            onChange={e => setMessage(e.target.value)}
            className="w-full p-3 rounded-lg bg-gray-800"
            rows={4}
          />
          <Button disabled={!message} onClick={submit}>Send</Button>
        </>
      )}
    </div>
  )
}
