import { useState } from "react"
import { api } from "../services/api"
export default function Evidence() {
  const [caseId, setCaseId] = useState("")
  const [items, setItems] = useState([])
  const [error, setError] = useState("")
  async function load() {
    setError("")
    try {
      const data = await api.getEvidence(caseId)
      setItems(data)
    } catch (err) {
      setError(err.message)
    }
  }
  return (
    <div className="content-page">
      <h2>Evidence Lookup</h2>
      <div className="search-bar">
        <input placeholder="Case ID" value={caseId} onChange={(e) => setCaseId(e.target.value)} />
        <button onClick={load}>Load</button>
      </div>
      {error && <p className="error">{error}</p>}
      <table className="table">
        <thead>
          <tr><th>Evidence ID</th><th>Type</th><th>Description</th><th>Status</th></tr>
        </thead>
        <tbody>
          {items.map((it) => (
            <tr key={it.evidenceId}>
              <td>{it.evidenceId}</td>
              <td>{it.type}</td>
              <td>{it.description}</td>
              <td>{it.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
