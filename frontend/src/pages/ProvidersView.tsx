import { useEffect, useState } from 'react'
import { Hospital } from 'lucide-react'
import { getProviders } from '../api/client'
import { StatusBadge } from '../components/StatusBadge'

export function ProvidersView() {
  const [providers, setProviders] = useState<any[]>([])

  useEffect(() => {
    getProviders().then(setProviders).catch(console.error)
  }, [])

  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <span className="eyebrow">Providers</span>
          <h1>Provider directory</h1>
          <p>Network and contract reference data used by provider review workflows.</p>
        </div>
        <div className="header-chip"><Hospital size={18} /> {providers.length} providers</div>
      </header>

      <section className="content-section">
        {providers.length === 0 ? (
          <div className="empty-state">
            <Hospital size={24} aria-hidden="true" />
            <strong>No providers available</strong>
            <p>Seed or connect provider data to populate this directory.</p>
          </div>
        ) : (
          <div className="table-shell">
            <table>
              <thead>
                <tr>
                  <th>Provider NPI</th>
                  <th>Name</th>
                  <th>Type</th>
                  <th>Network Status</th>
                </tr>
              </thead>
              <tbody>
                {providers.map(prov => (
                  <tr key={prov.id}>
                    <td><strong>{prov.provider_id}</strong></td>
                    <td>{prov.name}</td>
                    <td>{prov.provider_type}</td>
                    <td><StatusBadge value={prov.network_status} /></td>
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
