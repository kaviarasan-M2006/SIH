import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { useAuth } from "../context/AuthContext"
import { api } from "../services/api"
import RiskBadge from "../components/RiskBadge"
import CaseTimeline from "../components/CaseTimeline"
import EvidenceList from "../components/EvidenceList"
import TrendChart from "../components/TrendChart"
const TABS_BY_ROLE = {
  victim: ["Overview", "Wellbeing", "AI Risk"],
  counsellor: ["Overview", "Wellbeing", "AI Risk", "Alerts", "Interventions", "Timeline"],
  investigator: ["Overview", "Case Details", "Investigation", "Evidence", "Wellbeing", "AI Risk", "Alerts", "Timeline", "Audit Log"],
  admin: ["Overview", "Case Details", "Investigation", "Evidence", "Wellbeing", "AI Risk", "Alerts", "Interventions", "Timeline", "Audit Log"]
}
export default function CaseDetails() {
  const { caseId } = useParams()
  const { user } = useAuth()
  const tabs = TABS_BY_ROLE[user.role] || ["Overview"]
  const [activeTab, setActiveTab] = useState(tabs[0])
  const [caseData, setCaseData] = useState(null)
  const [timeline, setTimeline] = useState([])
  const [evidence, setEvidence] = useState([])
  const [trend, setTrend] = useState([])
  const [risk, setRisk] = useState(null)
  const [alerts, setAlerts] = useState([])
  const [interventions, setInterventions] = useState([])
  const [investigation, setInvestigation] = useState([])
  const [error, setError] = useState("")
  useEffect(() => {
    api.getCase(caseId).then(setCaseData).catch((e) => setError(e.message))
    api.getTimeline(caseId).then(setTimeline).catch(() => {})
    api.getTrend(caseId).then((r) => setTrend(r.points)).catch(() => {})
    api.getRisk(caseId).then(setRisk).catch(() => {})
    if (user.role !== "victim") {
      api.getEvidence(caseId).then(setEvidence).catch(() => {})
      api.getInvestigation(caseId).then(setInvestigation).catch(() => {})
    }
    api.alertsForCase(caseId).then(setAlerts).catch(() => {})
    if (user.role !== "victim") {
      api.listInterventions(caseId).then(setInterventions).catch(() => {})
    }
  }, [caseId])
  if (error) return <div className="content-page"><p className="error">{error}</p></div>
  if (!caseData) return <div className="content-page"><p>Loading case...</p></div>
  return (
    <div className="content-page">
      <h2>Case {caseData.caseId}</h2>
      <p>Status: {caseData.status} <RiskBadge level={caseData.latestRiskLevel} /></p>
      <div className="tabs">
        {tabs.map((t) => (
          <button key={t} className={activeTab === t ? "tab active" : "tab"} onClick={() => setActiveTab(t)}>{t}</button>
        ))}
      </div>
      <div className="tab-content">
        {activeTab === "Overview" && (
          <div>
            <p>Stage: {caseData.caseStage}</p>
            <p>Location: {caseData.location}</p>
            <p>Incident Category: {caseData.incidentCategory}</p>
            <p>Assigned Investigator: {caseData.assignedInvestigatorId}</p>
            <p>Assigned Counsellor: {caseData.assignedCounsellorId}</p>
          </div>
        )}
        {activeTab === "Case Details" && (
          <div>
            <p>FIR Reference: {caseData.firReference}</p>
            <p>Investigation Status: {caseData.investigationStatus}</p>
            <p>Court Status: {caseData.courtStatus}</p>
            <p>Compensation Status: {caseData.compensationStatus}</p>
          </div>
        )}
        {activeTab === "Investigation" && (
          <div>
            {investigation.map((u, i) => (
              <div className="card" key={i}>
                <p>Date: {u.date}</p>
                <p>Status: {u.status}</p>
                <p>Description: {u.description}</p>
                <p>Next Action: {u.nextAction}</p>
              </div>
            ))}
          </div>
        )}
        {activeTab === "Evidence" && <EvidenceList items={evidence} />}
        {activeTab === "Wellbeing" && <TrendChart points={trend} />}
        {activeTab === "AI Risk" && risk && (
          <div className="card">
            <p>Score: {risk.score}/100</p>
            <p>Risk Level: <RiskBadge level={risk.riskLevel} /></p>
            <p className="disclaimer">{risk.disclaimer}</p>
          </div>
        )}
        {activeTab === "Alerts" && (
          <div>
            {alerts.map((a) => (
              <div className="card" key={a.alertId}>
                <p>{a.severity} - {a.reason}</p>
                <p>Status: {a.status}</p>
              </div>
            ))}
          </div>
        )}
        {activeTab === "Interventions" && (
          <div>
            {interventions.map((iv, i) => (
              <div className="card" key={i}>
                <p>{iv.type} - {iv.date}</p>
                <p>{iv.action}</p>
                <p>Status: {iv.status}</p>
              </div>
            ))}
          </div>
        )}
        {activeTab === "Timeline" && <CaseTimeline events={timeline} />}
        {activeTab === "Audit Log" && <p>Audit trail available to authorized roles only.</p>}
      </div>
    </div>
  )
}
