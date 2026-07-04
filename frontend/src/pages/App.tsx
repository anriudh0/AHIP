import { Routes, Route, Link } from 'react-router-dom'
import { DashboardView } from './DashboardView'
import { ClaimsView } from './ClaimsView'
import { PatientsView } from './PatientsView'
import { ProvidersView } from './ProvidersView'

export function App() {
  return (
    <div className="app">
      <aside className="sidebar">
        <h1>AHIP</h1>
        <p>AI Healthcare Intelligence Platform</p>
        <p>Agentic AI • Memory • Context • Decisions</p>
        <nav style={{ marginTop: '20px', display: 'flex', flexDirection: 'column', gap: '10px' }}>
          <Link to="/" style={{ color: '#0f3d5e', textDecoration: 'none', fontWeight: 'bold' }}>Dashboard</Link>
          <Link to="/claims" style={{ color: '#0f3d5e', textDecoration: 'none', fontWeight: 'bold' }}>Claims</Link>
          <Link to="/patients" style={{ color: '#0f3d5e', textDecoration: 'none', fontWeight: 'bold' }}>Patients</Link>
          <Link to="/providers" style={{ color: '#0f3d5e', textDecoration: 'none', fontWeight: 'bold' }}>Providers</Link>
        </nav>
      </aside>
      <main className="main">
        <Routes>
          <Route path="/" element={<DashboardView />} />
          <Route path="/claims" element={<ClaimsView />} />
          <Route path="/patients" element={<PatientsView />} />
          <Route path="/providers" element={<ProvidersView />} />
        </Routes>
      </main>
    </div>
  )
}
