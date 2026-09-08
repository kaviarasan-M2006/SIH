import { Link } from "react-router-dom"
export default function Home() {
  return (
    <div className="home">
      <h1>Care-Link AI</h1>
      <p>AI-Powered Dynamic Mental Health Monitoring, Distress Risk Prediction & Case Management System for Victims and Witnesses of Atrocities.</p>
      <p className="disclaimer">This is an academic prototype. Do not enter real victim, medical, legal, or personally identifiable information.</p>
      <Link to="/login"><button>Enter Platform</button></Link>
    </div>
  )
}
