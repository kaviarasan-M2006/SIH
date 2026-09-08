import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"
import { api } from "../services/api"
const ROLE_HOME = { victim: "/victim", counsellor: "/counsellor", investigator: "/investigator", admin: "/admin" }
export default function Login() {
  const [email, setEmail] = useState("victim.demo@example.com")
  const [password, setPassword] = useState("demo123")
  const [role, setRole] = useState("victim")
  const [error, setError] = useState("")
  const { login } = useAuth()
  const navigate = useNavigate()
  async function handleSubmit(e) {
    e.preventDefault()
    setError("")
    try {
      const data = await api.login({ email, password, role })
      login(data)
      navigate(ROLE_HOME[data.role] || "/")
    } catch (err) {
      setError(err.message)
    }
  }
  return (
    <div className="login-page">
      <form className="login-form" onSubmit={handleSubmit}>
        <h2>Care-Link AI Login</h2>
        <p className="disclaimer">This is an academic prototype. Do not enter real victim, medical, legal, or personally identifiable information.</p>
        <label>User ID / Email</label>
        <input value={email} onChange={(e) => setEmail(e.target.value)} />
        <label>Password</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <label>Role</label>
        <select value={role} onChange={(e) => setRole(e.target.value)}>
          <option value="victim">Victim/Witness</option>
          <option value="counsellor">Counsellor</option>
          <option value="investigator">Investigator</option>
          <option value="admin">Administrator</option>
        </select>
        <button type="submit">Login</button>
        {error && <p className="error">{error}</p>}
        <div className="demo-hint">
          <p>Demo accounts (password: demo123):</p>
          <ul>
            <li>victim.demo@example.com</li>
            <li>counsellor.demo@example.com</li>
            <li>investigator.demo@example.com</li>
            <li>admin.demo@example.com</li>
          </ul>
        </div>
      </form>
    </div>
  )
}
