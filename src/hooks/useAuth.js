import { useState } from 'react'
import { api } from '../api/client'

export function useAuth() {
  const [token, setToken] = useState(() => localStorage.getItem('token'))

  async function login(email, password) {
    const data = await api.post('/v1/auth/login', { email, password })
    setToken(data.access_token)
    localStorage.setItem('token', data.access_token)
  }

  function logout() {
    setToken(null)
    localStorage.removeItem('token')
  }

  return { token, login, logout }
}
