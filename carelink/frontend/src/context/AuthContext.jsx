import { createContext, useContext, useState } from "react"
import { getSession, saveSession, clearSession } from "../services/authService"
const AuthContext = createContext(null)
export function AuthProvider({ children }) {
  const [user, setUser] = useState(getSession())
  function login(data) {
    saveSession(data)
    setUser({ userId: data.userId, role: data.role, displayName: data.displayName, preferredLanguage: data.preferredLanguage })
  }
  function logout() {
    clearSession()
    setUser(null)
  }
  return <AuthContext.Provider value={{ user, login, logout }}>{children}</AuthContext.Provider>
}
export function useAuth() {
  return useContext(AuthContext)
}
