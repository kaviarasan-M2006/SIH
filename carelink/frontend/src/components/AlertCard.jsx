export default function AlertCard({ alert, onReview }) {
  return (
    <div className={`alert-card severity-${alert.severity.toLowerCase()}`}>
      <div className="alert-header">
        <span>{alert.severity}</span>
        <span>{alert.caseId}</span>
      </div>
      <p>{alert.reason}</p>
      <ul>
        {alert.signals.map((s, i) => <li key={i}>{s}</li>)}
      </ul>
      <p>Status: {alert.status}</p>
      {alert.status === "pending" && onReview && (
        <button onClick={() => onReview(alert.alertId)}>Mark Reviewed</button>
      )}
    </div>
  )
}
