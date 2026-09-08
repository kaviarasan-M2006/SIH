const BASE_URL = "https://carelink-ai-w5zr.onrender.com";
function getToken() {
  return localStorage.getItem("carelink_token")
}
async function request(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) }
  const token = getToken()
  if (token) headers["Authorization"] = `Bearer ${token}`
  const res = await fetch(`${BASE_URL}${path}`, { ...options, headers })
  if (!res.ok) {
    const errBody = await res.json().catch(() => ({}))
    throw new Error(errBody.detail || `Request failed with status ${res.status}`)
  }
  return res.json()
}
export const api = {
  login: (data) => request("/api/auth/login", { method: "POST", body: JSON.stringify(data) }),
  listCases: () => request("/api/cases"),
  getCase: (caseId) => request(`/api/cases/${caseId}`),
  getTimeline: (caseId) => request(`/api/cases/${caseId}/timeline`),
  getInvestigation: (caseId) => request(`/api/cases/${caseId}/investigation`),
  addInvestigationUpdate: (caseId, data) => request(`/api/cases/${caseId}/investigation`, { method: "POST", body: JSON.stringify(data) }),
  myCase: () => request("/api/cases/mine/victim"),
  submitCheckin: (data) => request("/api/checkins", { method: "POST", body: JSON.stringify(data) }),
  getCheckins: (caseId) => request(`/api/checkins/${caseId}`),
  getRisk: (caseId) => request(`/api/risk/${caseId}`),
  getTrend: (caseId) => request(`/api/risk/${caseId}/trend`),
  getEvidence: (caseId) => request(`/api/evidence/${caseId}`),
  uploadEvidence: (caseId, data) => request(`/api/evidence/${caseId}`, { method: "POST", body: JSON.stringify(data) }),
  listAlerts: () => request("/api/alerts"),
  alertsForCase: (caseId) => request(`/api/alerts/${caseId}`),
  reviewAlert: (alertId, data) => request(`/api/alerts/${alertId}/review`, { method: "POST", body: JSON.stringify(data) }),
  listInterventions: (caseId) => request(`/api/interventions/${caseId}`),
  addIntervention: (caseId, data) => request(`/api/interventions/${caseId}`, { method: "POST", body: JSON.stringify(data) }),
  chatMessage: (data) => request("/api/chatbot/message", { method: "POST", body: JSON.stringify(data) })
}
