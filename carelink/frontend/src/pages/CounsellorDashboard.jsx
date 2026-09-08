import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import { api } from "../services/api"
import RiskBadge from "../components/RiskBadge"
export default function CounsellorDashboard() {
  const [cases, setCases] = useState([])
  useEffect(() => {
    api.listCases().then(setCases).catch(() => setCases([]))
  }, [])
  const counts = { LOW: 0, MODERATE: 0, HIGH: 0, CRITICAL: 0 }
  cases.forEach((c) => { counts[c.latestRiskLevel] = (counts[c.latestRiskLevel] || 0) + 1 })
  return (
    <div className="content-page">
      <h2>Counsellor Dashboard</h2>
      <div className="stat-cards">
        <div className="stat-card">Assigned Cases<span>{cases.length}</span></div>
        <div className="stat-card">Low Risk<span>{counts.LOW}</span></div>
        <div className="stat-card">Moderate Risk<span>{counts.MODERATE}</span></div>
        <div className="stat-card">High Risk<span>{counts.HIGH}</span></div>
        <div className="stat-card">Critical<span>{counts.CRITICAL}</span></div>
      </div>
      <table className="table">
        <thead>
          <tr><th>Case ID</th><th>Stage</th><th>Risk Level</th><th>Score</th><th>Trend</th><th></th></tr>
        </thead>
        <tbody>
          {cases.map((c) => (
            <tr key={c.caseId}>
              <td>{c.caseId}</td>
              <td>{c.caseStage}</td>
              <td><RiskBadge level={c.latestRiskLevel} /></td>
              <td>{c.latestScore}</td>
              <td>{c.trend}</td>
              <td><Link to={`/case/${c.caseId}`}>View</Link></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
