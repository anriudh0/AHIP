import { useEffect, useState } from 'react'
import { Users } from 'lucide-react'
import { getPatients } from '../api/client'
import { StatusBadge } from '../components/StatusBadge'

export function PatientsView() {
  const [patients, setPatients] = useState<any[]>([])

  useEffect(() => {
    getPatients().then(setPatients).catch(console.error)
  }, [])

  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <span className="eyebrow">Patients</span>
          <h1>Member directory</h1>
          <p>Operational member reference data used by patient journey and claims workflows.</p>
        </div>
        <div className="header-chip"><Users size={18} /> {patients.length} members</div>
      </header>

      <section className="content-section">
        {patients.length === 0 ? (
          <div className="empty-state">
            <Users size={24} aria-hidden="true" />
            <strong>No members available</strong>
            <p>Seed or connect member data to populate this directory.</p>
          </div>
        ) : (
          <div className="table-shell">
            <table>
              <thead>
                <tr>
                  <th>Member ID</th>
                  <th>Name</th>
                  <th>Plan ID</th>
                  <th>Risk Category</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {patients.map(patient => (
                  <tr key={patient.id}>
                    <td><strong>{patient.member_id}</strong></td>
                    <td>{patient.name}</td>
                    <td>{patient.plan_id}</td>
                    <td><StatusBadge value={patient.risk_category} /></td>
                    <td><StatusBadge value={patient.status} /></td>
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
