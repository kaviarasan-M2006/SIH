import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { api } from "../services/api"
import RiskBadge from "../components/RiskBadge"
export default function InvestigatorDashboard() {
  const [cases, setCases] = useState([])
  const [search, setSearch] = useState("")
  const navigate = useNavigate()
  useEffect(() => {
    api.listCases().then(setCases).catch(() => setCases([]))
  }, [])
  function handleSearch(e) {
    e.preventDefault()
    if (search.trim()) navigate(`/case/${search.trim()}`)
  }
  return (
    <div className="content-page">
      <h2>Investigator Dashboard</h2>
      <form onSubmit={handleSearch} className="search-bar">
        <input placeholder="Search Case ID (e.g. CL-1001)" value={search} onChange={(e) => setSearch(e.target.value)} />
        <button type="submit">Search</button>
      </form>
      <div className="stat-cards">
        <div className="stat-card">Total Cases<span>{cases.length}</span></div>
        <div className="stat-card">High Distress<span>{cases.filter((c) => c.latestRiskLevel === "HIGH" || c.latestRiskLevel === "CRITICAL").length}</span></div>
      </div>
      <table className="table">
        <thead>
          <tr><th>Case ID</th><th>Status</th><th>Risk</th><th>Score</th><th>Last Updated</th><th></th></tr>
        </thead>
        <tbody>
          {cases.map((c) => (
            <tr key={c.caseId}>
              <td>{c.caseId}</td>
              <td>{c.status}</td>
              <td><RiskBadge level={c.latestRiskLevel} /></td>
              <td>{c.latestScore}</td>
              <td>{new Date(c.updatedAt).toLocaleDateString()}</td>
              <td><button onClick={() => navigate(`/case/${c.caseId}`)}>Open</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
