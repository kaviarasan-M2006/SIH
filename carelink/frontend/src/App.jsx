import { BrowserRouter, Routes, Route } from "react-router-dom"
import { AuthProvider, useAuth } from "./context/AuthContext"
import Navbar from "./components/Navbar"
import Sidebar from "./components/Sidebar"
import ProtectedRoute from "./components/ProtectedRoute"
import Home from "./pages/Home"
import Login from "./pages/Login"
import Register from "./pages/Register"
import VictimDashboard from "./pages/VictimDashboard"
import CounsellorDashboard from "./pages/CounsellorDashboard"
import InvestigatorDashboard from "./pages/InvestigatorDashboard"
import AdminDashboard from "./pages/AdminDashboard"
import CaseDetails from "./pages/CaseDetails"
import CheckIn from "./pages/CheckIn"
import Evidence from "./pages/Evidence"
import Alerts from "./pages/Alerts"
import Privacy from "./pages/Privacy"
function Layout({ children }) {
  const { user } = useAuth()
  return (
    <div className="app-shell">
      <Navbar />
      <div className="app-body">
        {user && <Sidebar role={user.role} />}
        <div className="app-content">{children}</div>
      </div>
    </div>
  )
}
export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/privacy" element={<Privacy />} />
            <Route path="/checkin" element={<ProtectedRoute allowedRoles={["victim"]}><CheckIn /></ProtectedRoute>} />
            <Route path="/victim" element={<ProtectedRoute allowedRoles={["victim"]}><VictimDashboard /></ProtectedRoute>} />
            <Route path="/counsellor" element={<ProtectedRoute allowedRoles={["counsellor"]}><CounsellorDashboard /></ProtectedRoute>} />
            <Route path="/investigator" element={<ProtectedRoute allowedRoles={["investigator"]}><InvestigatorDashboard /></ProtectedRoute>} />
            <Route path="/admin" element={<ProtectedRoute allowedRoles={["admin"]}><AdminDashboard /></ProtectedRoute>} />
            <Route path="/case/:caseId" element={<ProtectedRoute allowedRoles={["victim", "counsellor", "investigator", "admin"]}><CaseDetails /></ProtectedRoute>} />
            <Route path="/evidence" element={<ProtectedRoute allowedRoles={["investigator", "admin"]}><Evidence /></ProtectedRoute>} />
            <Route path="/alerts" element={<ProtectedRoute allowedRoles={["counsellor", "investigator", "admin"]}><Alerts /></ProtectedRoute>} />
          </Routes>
        </Layout>
      </BrowserRouter>
    </AuthProvider>
  )
}
