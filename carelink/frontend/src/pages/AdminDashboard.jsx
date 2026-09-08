import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import { api } from "../services/api"
import RiskBadge from "../components/RiskBadge"
export default function AdminDashboard() {
  const [cases, setCases] = useState([])
  const [alerts, setAlerts] = useState([])
  useEffect(() => {
    api.listCases().then(setCases).catch(() => setCases([]))
    api.listAlerts().then(setAlerts).catch(() => setAlerts([]))
  }, [])
  const stageCounts = {}
  cases.forEach((c) => { stageCounts[c.caseStage] = (stageCounts[c.caseStage] || 0) + 1 })
  return (
    <div className="content-page">
      <h2>Administrator Dashboard</h2>
      <div className="stat-cards">
        <div className="stat-card">Total Cases<span>{cases.length}</span></div>
        <div className="stat-card">Pending Alerts<span>{alerts.filter((a) => a.status === "pending").length}</span></div>
        <div className="stat-card">High/Critical<span>{cases.filter((c) => c.latestRiskLevel === "HIGH" || c.latestRiskLevel === "CRITICAL").length}</span></div>
      </div>
      <h3>Cases by Stage</h3>
      <ul>
        {Object.entries(stageCounts).map(([stage, count]) => <li key={stage}>{stage}: {count}</li>)}
      </ul>
      <h3>All Cases</h3>
      <table className="table">
        <thead>
          <tr><th>Case ID</th><th>Stage</th><th>Risk</th><th></th></tr>
        </thead>
        <tbody>
          {cases.map((c) => (
            <tr key={c.caseId}>
              <td>{c.caseId}</td>
              <td>{c.caseStage}</td>
              <td><RiskBadge level={c.latestRiskLevel} /></td>
              <td><Link to={`/case/${c.caseId}`}>View</Link></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
