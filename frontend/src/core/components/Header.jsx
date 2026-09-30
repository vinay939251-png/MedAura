import { useLocation } from 'react-router-dom'
import { useState, useEffect } from 'react'

const pageTitles = {
  '/': 'Dashboard',
  '/roadscan/scan': 'Live Scan',
  '/roadscan/map': 'Pothole Map',
  '/roadscan/reports': 'Reports',
}

export default function Header() {
  const location = useLocation()
  const title = pageTitles[location.pathname] || 'ROADSCAN AI'
  const [time, setTime] = useState(new Date())

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000)
    return () => clearInterval(timer)
  }, [])

  return (
    <header className="header">
      <div className="header-left">
        <h2 className="header-title">{title}</h2>
      </div>

      <div className="header-right">
        <div className="header-status-strip">
          <div className="header-status-item">
            <span className="label">AI Engine</span>
            <span className="header-status-dot good"></span>
            <span className="value good">EDGE</span>
          </div>
          <div className="header-status-item">
            <span className="label">Model</span>
            <span className="value">RoadScan v1</span>
          </div>
          <div className="header-status-item">
            <span className="label">GPS</span>
            <span className="header-status-dot good"></span>
            <span className="value good">±4m</span>
          </div>
          <div className="header-status-item">
            <span className="label">Network</span>
            <span className="header-status-dot good"></span>
            <span className="value good">ONLINE</span>
          </div>
        </div>

        <div className="header-status-item">
          <span className="value" style={{ color: 'var(--color-text-muted)', fontFamily: 'var(--font-mono)', fontSize: '0.75rem' }}>
            {time.toLocaleTimeString()}
          </span>
        </div>
      </div>
    </header>
  )
}
