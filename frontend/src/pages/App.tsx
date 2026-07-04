import { Routes, Route, Link } from 'react-router-dom'
import { DashboardView } from './DashboardView'
import { ClaimsView } from './ClaimsView'
import { PatientsView } from './PatientsView'
import { ProvidersView } from './ProvidersView'
import { RiskQueueView } from './RiskQueueView'
import { CaseDetailView } from './CaseDetailView'

export function App() {
  return (
    <div className="app">
      <aside className="sidebar">
        <h1>AHIP</h1>
        <p>AI Healthcare Intelligence Platform</p>
        <p>Agentic AI | Memory | Context | Decisions</p>
        <nav className="sidebar-nav">
          <Link to="/">Dashboard</Link>
          <Link to="/risk-queue">Risk Queue</Link>
          <Link to="/claims">Claims</Link>
          <Link to="/patients">Patients</Link>
          <Link to="/providers">Providers</Link>
        </nav>
      </aside>
      <main className="main">
        <Routes>
          <Route path="/" element={<DashboardView />} />
          <Route path="/risk-queue" element={<RiskQueueView />} />
          <Route path="/case/:caseId" element={<CaseDetailView />} />
          <Route path="/claims" element={<ClaimsView />} />
          <Route path="/patients" element={<PatientsView />} />
          <Route path="/providers" element={<ProvidersView />} />
        </Routes>
      </main>
    </div>
  )
}
