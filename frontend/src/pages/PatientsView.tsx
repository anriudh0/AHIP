import { useEffect, useState } from 'react'
import { getPatients } from '../api/client'

export function PatientsView() {
  const [patients, setPatients] = useState<any[]>([])

  useEffect(() => {
    getPatients().then(setPatients).catch(console.error)
  }, [])

  return (
    <>
      <h2>Patients Directory</h2>
      <p>List of all members.</p>
      <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ borderBottom: '2px solid #cbd5e1' }}>
            <th>Member ID</th>
            <th>Name</th>
            <th>Plan ID</th>
            <th>Risk Category</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {patients.map(patient => (
            <tr key={patient.id} style={{ borderBottom: '1px solid #e2e8f0' }}>
              <td>{patient.member_id}</td>
              <td>{patient.name}</td>
              <td>{patient.plan_id}</td>
              <td>{patient.risk_category}</td>
              <td>{patient.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  )
}
