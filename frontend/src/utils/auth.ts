export type AuthUser = {
  id: number
  username: string
  email: string
  phone_num: string | null
  is_deliverer: boolean
}

export function saveAuthUser(user: AuthUser) {
  localStorage.setItem('auth', JSON.stringify(user))
}

export function getAuthUser(): AuthUser | null {
  const currAuth = localStorage.getItem('auth')

  if (!currAuth) {
    return null
  }

  try {
    return JSON.parse(currAuth) as AuthUser
  } catch {
    return null
  }
}

export function getPostAuthRoute(user: AuthUser) {
  return user.is_deliverer ? '/DelivererLanding' : '/CustomerLanding'
}
