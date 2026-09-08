export default function CaseTimeline({ events }) {
  return (
    <div className="timeline">
      {events.map((ev, i) => (
        <div className="timeline-item" key={i}>
          <div className="timeline-date">{ev.date}</div>
          <div className="timeline-event">{ev.event}</div>
        </div>
      ))}
    </div>
  )
}
