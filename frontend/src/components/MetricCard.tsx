type Props = { label: string; value: number }

export function MetricCard({ label, value }: Props) {
  return <div className="card"><p>{label}</p><strong>{value}</strong></div>
}
