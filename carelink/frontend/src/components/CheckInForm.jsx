import { useState } from "react"
import { en } from "../translations/en"
import { ta } from "../translations/ta"
import { api } from "../services/api"
const MOOD_KEYS = ["very_good", "good", "okay", "difficult", "very_difficult"]
const SLEEP_KEYS = ["normal", "slightly_disturbed", "frequently_disturbed", "very_difficult"]
const SAFETY_KEYS = ["no", "not_sure", "yes"]
const SUPPORT_KEYS = ["no", "maybe", "yes"]
export default function CheckInForm({ caseId, language, onSubmitted }) {
  const t = language === "ta" ? ta : en
  const [mood, setMood] = useState(MOOD_KEYS[0])
  const [sleep, setSleep] = useState(SLEEP_KEYS[0])
  const [stress, setStress] = useState(3)
  const [safety, setSafety] = useState(SAFETY_KEYS[0])
  const [support, setSupport] = useState(SUPPORT_KEYS[0])
  const [message, setMessage] = useState("")
  const [result, setResult] = useState(null)
  const [error, setError] = useState("")
  async function handleSubmit(e) {
    e.preventDefault()
    setError("")
    try {
      const res = await api.submitCheckin({
        caseId, mood, sleep, stressLevel: Number(stress), safetyConcern: safety, supportRequested: support, optionalMessage: message
      })
      setResult(res)
    } catch (err) {
      setError(err.message)
    }
  }
  return (
    <div className="card">
      <form onSubmit={handleSubmit}>
        <label>{t.moodQuestion}</label>
        <select value={mood} onChange={(e) => setMood(e.target.value)}>
          {MOOD_KEYS.map((k, i) => <option key={k} value={k}>{t.moodOptions[i]}</option>)}
        </select>
        <label>{t.sleepQuestion}</label>
        <select value={sleep} onChange={(e) => setSleep(e.target.value)}>
          {SLEEP_KEYS.map((k, i) => <option key={k} value={k}>{t.sleepOptions[i]}</option>)}
        </select>
        <label>{t.stressQuestion} ({stress})</label>
        <input type="range" min="0" max="10" value={stress} onChange={(e) => setStress(e.target.value)} />
        <label>{t.safetyQuestion}</label>
        <select value={safety} onChange={(e) => setSafety(e.target.value)}>
          {SAFETY_KEYS.map((k, i) => <option key={k} value={k}>{t.safetyOptions[i]}</option>)}
        </select>
        <label>{t.supportQuestion}</label>
        <select value={support} onChange={(e) => setSupport(e.target.value)}>
          {SUPPORT_KEYS.map((k, i) => <option key={k} value={k}>{t.supportOptions[i]}</option>)}
        </select>
        <label>{t.optionalMessage}</label>
        <textarea value={message} onChange={(e) => setMessage(e.target.value)} rows={3} />
        <button type="submit">{t.submitCheckin}</button>
      </form>
      {error && <p className="error">{error}</p>}
      {result && (
        <div className="result-box">
          <p>Risk Level: {result.risk.riskLevel} (Score {result.risk.score})</p>
          <p>{result.risk.recommendedAction}</p>
          <p className="disclaimer">{result.risk.disclaimer}</p>
        </div>
      )}
    </div>
  )
}
