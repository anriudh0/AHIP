import type { AgentExecution } from '../types/ahip'

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
    return <p className="empty-state">No agent executions are available for this case yet.</p>
  }

  return (
    <ol className="timeline">
      {executions.map(execution => (
        <li key={execution.id} className="timeline-item">
          <div>
            <strong>{execution.agent_name}</strong>
            <span>{new Date(execution.created_at).toLocaleString()}</span>
          </div>
          {outputText(execution.output, 'risk_level') && <p>Risk: {outputText(execution.output, 'risk_level')}</p>}
          {outputText(execution.output, 'observation') && <p>{outputText(execution.output, 'observation')}</p>}
          {outputText(execution.output, 'recommendation') && (
            <p>Recommendation: {outputText(execution.output, 'recommendation')}</p>
          )}
        </li>
      ))}
    </ol>
  )
}
