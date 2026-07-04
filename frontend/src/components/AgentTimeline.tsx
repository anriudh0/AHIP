import type { AgentExecution } from '../types/ahip'
import { Activity } from 'lucide-react'

type Props = {
  executions: AgentExecution[]
}

function outputText(output: Record<string, unknown>, key: string) {
  const value = output[key]
  if (Array.isArray(value)) return value.join(', ')
  if (typeof value === 'string') return value
  return null
}

export function AgentTimeline({ executions }: Props) {
  if (!executions.length) {
    return (
      <div className="empty-state">
        <Activity size={22} aria-hidden="true" />
        <strong>No agent executions yet</strong>
        <p>Run a case review to populate this timeline with auditable agent activity.</p>
      </div>
    )
  }

  return (
    <ol className="timeline">
      {executions.map(execution => (
        <li key={execution.id} className="timeline-item">
          <div className="timeline-marker" aria-hidden="true" />
          <div className="timeline-content">
            <div className="timeline-heading">
              <strong>{execution.agent_name}</strong>
              <span>{new Date(execution.created_at).toLocaleString()}</span>
            </div>
            {outputText(execution.output, 'risk_level') && <p className="timeline-risk">Risk: {outputText(execution.output, 'risk_level')}</p>}
            {outputText(execution.output, 'observation') && <p>{outputText(execution.output, 'observation')}</p>}
            {outputText(execution.output, 'recommendation') && (
              <p>Recommendation: {outputText(execution.output, 'recommendation')}</p>
            )}
          </div>
        </li>
      ))}
    </ol>
  )
}
