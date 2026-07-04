type Props = {
  value?: string | null
}

function badgeClass(value?: string | null) {
  const normalized = (value || 'Unknown').toLowerCase()
  if (['critical', 'high', 'overridden', 'denied', 'escalated', 'out-of-network'].includes(normalized)) return 'status-badge status-danger'
  if (['medium', 'pending', 'pended', 'open review', 'submitted'].includes(normalized)) return 'status-badge status-warning'
  if (['low', 'accepted', 'paid', 'active', 'in-network'].includes(normalized)) return 'status-badge status-success'
  return 'status-badge status-neutral'
}

export function StatusBadge({ value }: Props) {
  return <span className={badgeClass(value)}>{value || 'Unknown'}</span>
}
