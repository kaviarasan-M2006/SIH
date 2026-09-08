import { NavLink } from "react-router-dom"
export default function Sidebar({ role }) {
  const linksByRole = {
    victim: [
      { to: "/victim", label: "My Wellbeing" },
      { to: "/checkin", label: "Complete Check-in" },
      { to: "/privacy", label: "Privacy & Consent" }
    ],
    counsellor: [
      { to: "/counsellor", label: "Dashboard" },
      { to: "/alerts", label: "Alerts" }
    ],
    investigator: [
      { to: "/investigator", label: "Dashboard" },
      { to: "/alerts", label: "Alerts" }
    ],
    admin: [
      { to: "/admin", label: "Dashboard" },
      { to: "/alerts", label: "Alerts" }
    ]
  }
  const links = linksByRole[role] || []
  return (
    <div className="sidebar">
      {links.map((l) => (
        <NavLink key={l.to} to={l.to} className={({ isActive }) => (isActive ? "active" : "")}>
          {l.label}
        </NavLink>
      ))}
    </div>
  )
}
