import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Camera, Map, BarChart3, AlertTriangle, Activity, Cpu, MapPin, Radio } from 'lucide-react'
import { getHealth, getModules, getIncidents } from '../core/api/client.js'

export default function Dashboard() {
  const [health, setHealth] = useState(null)
  const [modules, setModules] = useState({})
  const [incidents, setIncidents] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [healthRes, modulesRes, incidentsRes] = await Promise.allSettled([
          getHealth(),
          getModules(),
          getIncidents({ page_size: 5 }),
        ])
        if (healthRes.status === 'fulfilled') setHealth(healthRes.value.data)
        if (modulesRes.status === 'fulfilled') setModules(modulesRes.value.data.modules || {})
        if (incidentsRes.status === 'fulfilled') setIncidents(incidentsRes.value.data.items || [])
      } catch (e) {
        console.error('Dashboard fetch error:', e)
      }
      setLoading(false)
    }
    fetchData()
    const interval = setInterval(fetchData, 10000)
    return () => clearInterval(interval)
  }, [])

  const moduleList = Object.values(modules)
  const moduleCount = moduleList.length

  return (
    <div className="animate-fade-in">
      <div className="page-header">
        <h1>Platform <span className="text-gradient">Dashboard</span></h1>
        <p>Smart City Infrastructure Monitoring — Real-time overview</p>
      </div>

      {/* Stats Grid */}
      <div className="stats-grid">
        <StatCard
          label="Active Modules"
          value={moduleCount}
          detail={moduleCount > 0 ? moduleList.map(m => m.name).join(', ') : 'No modules loaded'}
          color="var(--color-accent-blue)"
        />
        <StatCard
          label="Total Incidents"
          value={incidents.length > 0 ? '—' : '0'}
          detail="Across all modules"
          color="var(--color-accent-amber)"
        />
        <StatCard
          label="AI Runtime"
          value="EDGE"
          detail="ONNX Runtime Web (primary)"
          color="var(--color-accent-cyan)"
        />
        <StatCard
          label="Platform Status"
          value={health ? 'ONLINE' : 'CONNECTING'}
          detail={health ? health.environment : 'Checking backend...'}
          color={health ? 'var(--color-accent-emerald)' : 'var(--color-text-muted)'}
        />
      </div>

      {/* Content Grid */}
      <div className="content-grid">
        {/* Registered Modules */}
        <div className="card">
          <div className="card-header">
            <h2>📦 Registered Modules</h2>
            <span className="status-badge healthy">Active</span>
          </div>
          <div className="card-body">
            {moduleCount === 0 ? (
              <div className="empty-state">
                <div className="empty-state-icon">📦</div>
                <h3>No modules registered</h3>
                <p>Start the backend to auto-discover detection modules</p>
              </div>
            ) : (
              moduleList.map(mod => (
                <div key={mod.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '12px 0', borderBottom: '1px solid var(--border-subtle)' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <span style={{ fontSize: '1.5rem' }}>{mod.frontend?.icon || '📦'}</span>
                    <div>
                      <div style={{ fontWeight: 600, fontSize: 'var(--text-sm)' }}>{mod.name}</div>
                      <div style={{ fontSize: 'var(--text-xs)', color: 'var(--color-text-muted)' }}>v{mod.version} — {mod.incident_types?.join(', ')}</div>
                    </div>
                  </div>
                  <span className="status-badge healthy">Healthy</span>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="card">
          <div className="card-header">
            <h2>⚡ Quick Actions</h2>
          </div>
          <div className="card-body" style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-md)' }}>
            <Link to="/roadscan/scan" className="btn btn-primary" style={{ justifyContent: 'flex-start' }}>
              <Camera size={18} /> Start Live Scan
            </Link>
            <Link to="/roadscan/map" className="btn btn-secondary" style={{ justifyContent: 'flex-start' }}>
              <Map size={18} /> View Pothole Map
            </Link>
            <Link to="/roadscan/reports" className="btn btn-secondary" style={{ justifyContent: 'flex-start' }}>
              <BarChart3 size={18} /> View Reports
            </Link>
          </div>
        </div>

        {/* Recent Incidents */}
        <div className="card content-grid-full">
          <div className="card-header">
            <h2>🚨 Recent Incidents</h2>
            <Link to="/roadscan/map" style={{ fontSize: 'var(--text-sm)', color: 'var(--color-accent-blue)' }}>View all →</Link>
          </div>
          <div className="card-body no-pad">
            {incidents.length === 0 ? (
              <div className="empty-state">
                <div className="empty-state-icon">🔍</div>
                <h3>No incidents detected yet</h3>
                <p>Start a live scan session to begin detecting potholes. Incidents will appear here in real-time.</p>
              </div>
            ) : (
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Type</th>
                    <th>Severity</th>
                    <th>Confidence</th>
                    <th>Location</th>
                    <th>Status</th>
                    <th>Time</th>
                  </tr>
                </thead>
                <tbody>
                  {incidents.map(inc => (
                    <tr key={inc.id}>
                      <td style={{ fontWeight: 600 }}>{inc.incident_type}</td>
                      <td><span className={`severity-badge ${inc.severity}`}>{inc.severity}</span></td>
                      <td style={{ fontFamily: 'var(--font-mono)' }}>{(inc.confidence * 100).toFixed(1)}%</td>
                      <td style={{ fontFamily: 'var(--font-mono)', fontSize: 'var(--text-xs)' }}>{inc.latitude?.toFixed(5)}, {inc.longitude?.toFixed(5)}</td>
                      <td><span className={`status-badge ${inc.status === 'detected' ? 'healthy' : 'inactive'}`}>{inc.status}</span></td>
                      <td style={{ fontSize: 'var(--text-xs)', color: 'var(--color-text-muted)' }}>{new Date(inc.detected_at).toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

function StatCard({ label, value, detail, color }) {
  return (
    <div className="stat-card">
      <span className="stat-label">{label}</span>
      <span className="stat-value" style={color ? { background: `linear-gradient(135deg, ${color}, ${color}dd)`, WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' } : undefined}>
        {value}
      </span>
      <span className="stat-detail">{detail}</span>
    </div>
  )
}
