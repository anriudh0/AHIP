import { useEffect, useState } from 'react'
import { FileText } from 'lucide-react'
import { getClaims } from '../api/client'
import { StatusBadge } from '../components/StatusBadge'

export function ClaimsView() {
  const [claims, setClaims] = useState<any[]>([])

  useEffect(() => {
    getClaims().then(setClaims).catch(console.error)
  }, [])

  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <span className="eyebrow">Claims</span>
          <h1>Claims directory</h1>
          <p>Reference view for submitted, pended, paid, and reviewed claim records.</p>
        </div>
        <div className="header-chip"><FileText size={18} /> {claims.length} claims</div>
      </header>

      <section className="content-section">
        {claims.length === 0 ? (
          <div className="empty-state">
            <FileText size={24} aria-hidden="true" />
            <strong>No claims available</strong>
            <p>Seed or connect claim data to populate this directory.</p>
          </div>
        ) : (
          <div className="table-shell">
            <table>
              <thead>
                <tr>
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
                  <tr key={claim.id}>
                    <td><strong>{claim.claim_id}</strong></td>
                    <td>{claim.patient_member_id}</td>
                    <td>{claim.provider_id}</td>
                    <td>{claim.service_date}</td>
                    <td>${claim.amount.toFixed(2)}</td>
                    <td><StatusBadge value={claim.claim_status} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  )
}
