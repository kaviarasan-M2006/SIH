export function saveSession(data) {
  localStorage.setItem("carelink_token", data.token)
  localStorage.setItem("carelink_user", JSON.stringify({ userId: data.userId, role: data.role, displayName: data.displayName, preferredLanguage: data.preferredLanguage }))
}
export function getSession() {
  const raw = localStorage.getItem("carelink_user")
  return raw ? JSON.parse(raw) : null
}
export function clearSession() {
  localStorage.removeItem("carelink_token")
  localStorage.removeItem("carelink_user")
}
