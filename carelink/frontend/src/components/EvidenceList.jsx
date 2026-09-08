export default function EvidenceList({ items }) {
  return (
    <table className="table">
      <thead>
        <tr><th>Evidence ID</th><th>Type</th><th>Description</th><th>Uploaded By</th><th>Status</th></tr>
      </thead>
      <tbody>
        {items.map((it) => (
          <tr key={it.evidenceId}>
            <td>{it.evidenceId}</td>
            <td>{it.type}</td>
            <td>{it.description}</td>
            <td>{it.uploadedBy}</td>
            <td>{it.status}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
