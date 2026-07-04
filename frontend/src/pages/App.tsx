import { Routes, Route, Link, useLocation } from 'react-router-dom'
import { BarChart3, ChevronLeft, ChevronRight, FileText, Hospital, ShieldAlert, Users } from 'lucide-react'
import { useState } from 'react'
import { DashboardView } from './DashboardView'
import { ClaimsView } from './ClaimsView'
import { PatientsView } from './PatientsView'
import { ProvidersView } from './ProvidersView'
import { RiskQueueView } from './RiskQueueView'
import { CaseDetailView } from './CaseDetailView'

const navGroups = [
  {
    label: 'Operations',
    items: [
      { label: 'Dashboard', path: '/', icon: BarChart3 },
      { label: 'Risk Queue', path: '/risk-queue', icon: ShieldAlert },
    ],
  },
  {
    label: 'Data',
    items: [
      { label: 'Claims', path: '/claims', icon: FileText },
      { label: 'Patients', path: '/patients', icon: Users },
      { label: 'Providers', path: '/providers', icon: Hospital },
    ],
  },
]

export function App() {
  const [collapsed, setCollapsed] = useState(false)
  const location = useLocation()

  function isActive(path: string) {
    if (path === '/') return location.pathname === '/'
    return location.pathname.startsWith(path)
  }

  return (
    <div className={`app ${collapsed ? 'sidebar-collapsed' : ''}`}>
      <aside className="sidebar" aria-label="Primary navigation">
        <div className="brand-panel">
          <div className="brand-mark">AHIP</div>
          <div className="brand-copy">
            <span>AI Healthcare</span>
            <strong>Intelligence Platform</strong>
          </div>
        </div>

        <div className="capability-card">
          <span>Healthcare Operations Intelligence</span>
          <p>Deterministic workflows, explainable recommendations, and governance-first review.</p>
        </div>

        <nav className="sidebar-nav">
          {navGroups.map(group => (
            <div className="nav-group" key={group.label}>
              <span className="nav-group-label">{group.label}</span>
              {group.items.map(item => {
                const Icon = item.icon
                return (
                  <Link className={`nav-item ${isActive(item.path) ? 'active' : ''}`} to={item.path} key={item.path}>
                    <Icon size={18} aria-hidden="true" />
                    <span>{item.label}</span>
                  </Link>
                )
              })}
            </div>
          ))}
        </nav>

        <div className="sidebar-footer">
          <button className="sidebar-toggle" onClick={() => setCollapsed(!collapsed)} aria-label="Toggle sidebar">
            {collapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
          </button>
          <div>
            <strong>AHIP MVP</strong>
            <span>Demo Platform</span>
          </div>
        </div>
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
