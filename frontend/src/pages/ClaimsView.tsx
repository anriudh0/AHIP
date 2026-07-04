import { useEffect, useState } from 'react'
import { getClaims } from '../api/client'

export function ClaimsView() {
  const [claims, setClaims] = useState<any[]>([])

  useEffect(() => {
    getClaims().then(setClaims).catch(console.error)
  }, [])

  return (
    <>
      <h2>Claims Directory</h2>
      <p>List of all processed and pending claims.</p>
      <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ borderBottom: '2px solid #cbd5e1' }}>
            <th>Claim ID</th>
            <th>Member ID</th>
            <th>Provider NPI</th>
            <th>Service Date</th>
            <th>Amount</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {claims.map(claim => (
            <tr key={claim.id} style={{ borderBottom: '1px solid #e2e8f0' }}>
              <td>{claim.claim_id}</td>
              <td>{claim.patient_member_id}</td>
              <td>{claim.provider_id}</td>
              <td>{claim.service_date}</td>
              <td>${claim.amount.toFixed(2)}</td>
              <td>{claim.claim_status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  )
}
