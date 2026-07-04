import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { getPriorityQueue } from '../api/client'
import { StatusBadge } from '../components/StatusBadge'
import type { DecisionRecommendation, PriorityQueueResponse } from '../types/ahip'

function operationalStatus(item: DecisionRecommendation) {
  return ['Critical', 'High'].includes(item.priority) ? 'Escalated' : 'Open Review'
}

export function RiskQueueView() {
  const [recommendations, setRecommendations] = useState<DecisionRecommendation[]>([])
  const [riskFilter, setRiskFilter] = useState('All')
  const [priorityFilter, setPriorityFilter] = useState('All')
  const [statusFilter, setStatusFilter] = useState('All')
  const [caseSearch, setCaseSearch] = useState('')
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    getPriorityQueue()
      .then((data: PriorityQueueResponse) => setRecommendations(data.recommendations || []))
      .catch(error => setError(error.message))
  }, [])

  const filteredRecommendations = useMemo(() => {
    return recommendations.filter(item => {
      const matchesRisk = riskFilter === 'All' || item.risk_level === riskFilter
      const matchesPriority = priorityFilter === 'All' || item.priority === priorityFilter
      const matchesStatus = statusFilter === 'All' || operationalStatus(item) === statusFilter
      const matchesCase = item.case_id.toLowerCase().includes(caseSearch.trim().toLowerCase())
      return matchesRisk && matchesPriority && matchesStatus && matchesCase
    })
  }, [caseSearch, priorityFilter, recommendations, riskFilter, statusFilter])

  return (
    <>
      <span className="badge">Phase 7 Risk Queue</span>
      <h2>Risk Queue</h2>
      <p>Prioritized healthcare operations recommendations from the existing decision layer.</p>

      <section className="section">
        <div className="filters">
          <label>
            Case ID
            <input value={caseSearch} onChange={(event: any) => setCaseSearch(event.target.value)} placeholder="Search case" />
          </label>
          <label>
            Risk
            <select value={riskFilter} onChange={(event: any) => setRiskFilter(event.target.value)}>
              <option>All</option>
              <option>Critical</option>
              <option>High</option>
              <option>Medium</option>
              <option>Low</option>
            </select>
          </label>
          <label>
            Priority
            <select value={priorityFilter} onChange={(event: any) => setPriorityFilter(event.target.value)}>
              <option>All</option>
              <option>Critical</option>
              <option>High</option>
              <option>Medium</option>
              <option>Low</option>
            </select>
          </label>
          <label>
            Status
            <select value={statusFilter} onChange={(event: any) => setStatusFilter(event.target.value)}>
              <option>All</option>
              <option>Escalated</option>
              <option>Open Review</option>
            </select>
          </label>
        </div>
      </section>

      {error && <p className="error-state">{error}</p>}

      <section className="section">
        <div className="section-heading">
          <h3>Prioritized Recommendations</h3>
          <span>{filteredRecommendations.length} visible</span>
        </div>
        {filteredRecommendations.length === 0 ? (
          <p className="empty-state">No recommendations match the current filters.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Case</th>
                <th>Risk</th>
                <th>Score</th>
                <th>Priority</th>
                <th>Status</th>
                <th>Owner</th>
                <th>Recommendation</th>
              </tr>
            </thead>
            <tbody>
              {filteredRecommendations.map(item => (
                <tr key={item.case_id}>
                  <td><Link to={`/case/${item.case_id}`}>{item.case_id}</Link></td>
                  <td><StatusBadge value={item.risk_level} /></td>
                  <td>{item.risk_score}</td>
                  <td><StatusBadge value={item.priority} /></td>
                  <td><StatusBadge value={operationalStatus(item)} /></td>
                  <td>{item.escalation_owner}</td>
                  <td>{item.recommendation}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </>
  )
}
