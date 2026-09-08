import { useEffect, useState } from "react"
import { api } from "../services/api"
import AlertCard from "../components/AlertCard"
export default function Alerts() {
  const [alerts, setAlerts] = useState([])
  useEffect(() => {
    load()
  }, [])
  function load() {
    api.listAlerts().then(setAlerts).catch(() => setAlerts([]))
  }
  async function handleReview(alertId) {
    await api.reviewAlert(alertId, { status: "reviewed", notes: "Reviewed by staff via dashboard" })
    load()
  }
  return (
    <div className="content-page">
      <h2>Alerts</h2>
      <div className="alerts-grid">
        {alerts.map((a) => (
          <AlertCard key={a.alertId} alert={a} onReview={handleReview} />
        ))}
      </div>
    </div>
  )
}
