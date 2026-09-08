import { useEffect, useState } from "react"
import { useAuth } from "../context/AuthContext"
import { api } from "../services/api"
import CheckInForm from "../components/CheckInForm"
export default function CheckIn() {
  const { user } = useAuth()
  const [caseId, setCaseId] = useState(null)
  useEffect(() => {
    api.myCase().then((c) => setCaseId(c.caseId)).catch(() => setCaseId(null))
  }, [])
  if (!caseId) return <div className="content-page"><p>Loading your case information...</p></div>
  return (
    <div className="content-page">
      <h2>Wellbeing Check-in</h2>
      <CheckInForm caseId={caseId} language={user.preferredLanguage} />
    </div>
  )
}
