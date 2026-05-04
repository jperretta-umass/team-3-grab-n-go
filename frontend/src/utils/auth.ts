export type AuthUser = {
  id: number
  username: string
  email: string
  phone_num: string | null
  is_deliverer: boolean
}

export type AuthSession = {
  access_token: string
  token_type: string
  user: AuthUser
}

const TOKEN_KEY = 'token'
const API_BASE = (import.meta.env.VITE_API_BASE as string | undefined) ?? 'http://localhost:8000'

let currentUser: AuthUser | null = null

export function saveAuthSession(session: AuthSession) {
  localStorage.setItem(TOKEN_KEY, session.access_token)
  currentUser = session.user
}

export function clearAuthSession() {
  localStorage.removeItem(TOKEN_KEY)
  currentUser = null
}

export function getAuthToken() {
  return localStorage.getItem(TOKEN_KEY)
}

export function getAuthUser() {
  return currentUser
}

export async function fetchAuthUser() {
  const token = getAuthToken()

  if (!token) {
    currentUser = null
    return null
  }

  const response = await fetch(`${API_BASE}/auth/me`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  if (!response.ok) {
    clearAuthSession()
    return null
  }

  currentUser = await response.json() as AuthUser
  return currentUser
}

export function getPostAuthRoute(user: AuthUser) {
  return user.is_deliverer ? '/DelivererLanding' : '/CustomerLanding'
}
