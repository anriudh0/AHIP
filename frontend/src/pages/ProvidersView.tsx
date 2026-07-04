import { useEffect, useState } from 'react'
import { getProviders } from '../api/client'

export function ProvidersView() {
  const [providers, setProviders] = useState<any[]>([])

  useEffect(() => {
    getProviders().then(setProviders).catch(console.error)
  }, [])

  return (
    <>
      <h2>Providers Directory</h2>
      <p>List of all network and out-of-network providers.</p>
      <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ borderBottom: '2px solid #cbd5e1' }}>
            <th>Provider NPI</th>
            <th>Name</th>
            <th>Type</th>
            <th>Network Status</th>
          </tr>
        </thead>
        <tbody>
          {providers.map(prov => (
            <tr key={prov.id} style={{ borderBottom: '1px solid #e2e8f0' }}>
              <td>{prov.provider_id}</td>
              <td>{prov.name}</td>
              <td>{prov.provider_type}</td>
              <td>{prov.network_status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  )
}
