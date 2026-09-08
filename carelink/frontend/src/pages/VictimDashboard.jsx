import { useEffect, useState } from "react"
import { useAuth } from "../context/AuthContext"
import { api } from "../services/api"
import Chatbot from "../components/Chatbot"
import RiskBadge from "../components/RiskBadge"
export default function VictimDashboard() {
  const { user } = useAuth()
  const [myCase, setMyCase] = useState(null)
  useEffect(() => {
    api.myCase().then(setMyCase).catch(() => setMyCase(null))
  }, [])
  return (
    <div className="content-page">
      <h2>Welcome, {user.displayName}</h2>
      <p className="disclaimer">This is an academic prototype. Do not enter real victim, medical, legal, or personally identifiable information.</p>
      {myCase && myCase.caseId ? (
        <div className="card">
          <h3>My Case Status</h3>
          <p>Case ID: {myCase.caseId}</p>
          <p>Stage: {myCase.caseStage}</p>
          <p>Status: {myCase.status}</p>
          <p>Wellbeing: <RiskBadge level={myCase.latestRiskLevel} /></p>
        </div>
      ) : (
        <p>No case linked to your account yet.</p>
      )}
      <h3>Support Chat</h3>
      <Chatbot language={user.preferredLanguage} />
    </div>
  )
}
