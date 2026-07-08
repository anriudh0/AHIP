const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'
const GOVERNANCE_HEADERS = { 'X-User-Role': 'Operations Analyst' }

export async function getDashboardSummary() {
  const response = await fetch(`${API_BASE_URL}/dashboard/summary`)
  if (!response.ok) throw new Error('Failed to load dashboard summary')
  return response.json()
}

export async function runCaseReview(caseId: string) {
  const response = await fetch(`${API_BASE_URL}/agents/run-case-review`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ case_id: caseId })
  })
  if (!response.ok) throw new Error('Failed to run agent review')
  return response.json()
}

export async function getClaims() {
  const response = await fetch(`${API_BASE_URL}/claims`)
  if (!response.ok) throw new Error('Failed to fetch claims')
  return response.json()
}

export async function getPatients() {
  const response = await fetch(`${API_BASE_URL}/patients`)
  if (!response.ok) throw new Error('Failed to fetch patients')
  return response.json()
}

export async function getProviders() {
  const response = await fetch(`${API_BASE_URL}/providers`)
  if (!response.ok) throw new Error('Failed to fetch providers')
  return response.json()
}

export async function getPriorityQueue() {
  const response = await fetch(`${API_BASE_URL}/agents/priority-queue`)
  if (!response.ok) throw new Error('Failed to fetch priority queue')
  return response.json()
}

export async function getCaseContext(caseId: string) {
  const response = await fetch(`${API_BASE_URL}/agents/context/${encodeURIComponent(caseId)}`)
  if (!response.ok) throw new Error('Failed to fetch case context')
  return response.json()
}

export async function getExecutionHistory() {
  const response = await fetch(`${API_BASE_URL}/agents/execution-history`, {
    headers: GOVERNANCE_HEADERS,
  })
  if (!response.ok) throw new Error('Failed to fetch execution history')
  return response.json()
}

export async function getAuditLogs() {
  const response = await fetch(`${API_BASE_URL}/agents/audit-logs`, {
    headers: GOVERNANCE_HEADERS,
  })
  if (!response.ok) throw new Error('Failed to fetch audit logs')
  return response.json()
}

export async function getGovernanceSummary() {
  const response = await fetch(`${API_BASE_URL}/agents/governance-summary`, {
    headers: GOVERNANCE_HEADERS,
  })
  if (!response.ok) throw new Error('Failed to fetch governance summary')
  return response.json()
}
