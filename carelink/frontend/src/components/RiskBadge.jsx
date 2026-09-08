const COLORS = { LOW: "#2e7d32", MODERATE: "#f9a825", HIGH: "#ef6c00", CRITICAL: "#c62828" }
export default function RiskBadge({ level }) {
  const color = COLORS[level] || "#555"
  return (
    <span style={{ background: color, color: "#fff", padding: "4px 10px", borderRadius: "12px", fontSize: "0.8rem", fontWeight: 600 }}>
      {level}
    </span>
  )
}
