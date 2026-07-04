type Props = {
  label: string
  value: number
  detail?: string
  icon?: any
}

export function MetricCard({ label, value, detail, icon: Icon }: Props) {
  return (
    <div className="metric-card">
      <div className="metric-card-top">
        <p>{label}</p>
        {Icon && (
          <span className="metric-icon">
            <Icon size={18} aria-hidden="true" />
          </span>
        )}
      </div>
      <strong>{value}</strong>
      {detail && <span>{detail}</span>}
    </div>
  )
}
