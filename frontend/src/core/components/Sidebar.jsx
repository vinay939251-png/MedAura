import { NavLink, useLocation } from 'react-router-dom'
import { LayoutDashboard, Camera, Map, BarChart3, Settings, Activity, Wifi, WifiOff } from 'lucide-react'
import { useState, useEffect } from 'react'
import { getHealth } from '../api/client.js'

const platformNav = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
]

const roadscanNav = [
  { path: '/roadscan/scan', label: 'Live Scan', icon: Camera },
  { path: '/roadscan/map', label: 'Pothole Map', icon: Map },
  { path: '/roadscan/reports', label: 'Reports', icon: BarChart3 },
]

export default function Sidebar() {
  const location = useLocation()
  const [backendOnline, setBackendOnline] = useState(false)
  const [moduleCount, setModuleCount] = useState(0)

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await getHealth()
        setBackendOnline(true)
        setModuleCount(Object.keys(res.data.modules || {}).length)
      } catch {
        setBackendOnline(false)
      }
    }
    checkHealth()
    const interval = setInterval(checkHealth, 15000)
    return () => clearInterval(interval)
  }, [])

  return (
    <aside className="sidebar">
      {/* Brand */}
      <div className="sidebar-brand">
        <div className="sidebar-brand-icon">🛣️</div>
        <div>
          <h1>ROADSCAN AI</h1>
          <p>Smart City Monitor</p>
        </div>
      </div>

      {/* Platform Navigation */}
      <div className="sidebar-section">
        <div className="sidebar-section-title">Platform</div>
        <nav className="sidebar-nav">
          {platformNav.map(item => (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === '/'}
              className={({ isActive }) => `sidebar-link${isActive ? ' active' : ''}`}
            >
              <item.icon className="sidebar-link-icon" />
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>
      </div>

      {/* ROADSCAN AI Module Navigation */}
      <div className="sidebar-section">
        <div className="sidebar-section-title">🛣️ RoadScan AI</div>
        <nav className="sidebar-nav">
          {roadscanNav.map(item => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) => `sidebar-link${isActive ? ' active' : ''}`}
            >
              <item.icon className="sidebar-link-icon" />
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>
      </div>

      {/* Footer Status */}
      <div className="sidebar-footer">
        <div className="sidebar-status">
          <div className="sidebar-status-row">
            <span className="sidebar-status-label">Backend</span>
            <span className={`sidebar-status-value ${backendOnline ? 'online' : 'offline'}`}>
              {backendOnline ? '● ONLINE' : '○ OFFLINE'}
            </span>
          </div>
          <div className="sidebar-status-row">
            <span className="sidebar-status-label">AI Engine</span>
            <span className="sidebar-status-value edge">EDGE</span>
          </div>
          <div className="sidebar-status-row">
            <span className="sidebar-status-label">Modules</span>
            <span className="sidebar-status-value">{moduleCount}</span>
          </div>
        </div>
      </div>
    </aside>
  )
}
