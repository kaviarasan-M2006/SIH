import { useAuth } from "../context/AuthContext"
import { useNavigate } from "react-router-dom"
export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  function handleLogout() {
    logout()
    navigate("/login")
  }
  return (
    <div className="navbar">
      <div className="navbar-title">Care-Link AI</div>
      {user && (
        <div className="navbar-user">
          <span>{user.displayName} ({user.role})</span>
          <button onClick={handleLogout}>Logout</button>
        </div>
      )}
    </div>
  )
}
