import { useState, useEffect } from 'react'
import { getRoadscanStats, getRoadscanConfig } from '../../../core/api/client.js'

export default function Reports() {
  const [stats, setStats] = useState(null)
  const [config, setConfig] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsRes, cfgRes] = await Promise.allSettled([
          getRoadscanStats(),
          getRoadscanConfig(),
        ])
        if (statsRes.status === 'fulfilled') setStats(statsRes.value.data)
        if (cfgRes.status === 'fulfilled') setConfig(cfgRes.value.data.config)
      } catch (e) {
        console.error('Reports fetch error:', e)
      }
      setLoading(false)
    }
    fetchData()
  }, [])

  const severityData = stats?.by_severity || {}
  const total = stats?.total_incidents || 0
  const severities = ['low', 'medium', 'high', 'critical']
  const severityColors = { low: 'var(--severity-low)', medium: 'var(--severity-medium)', high: 'var(--severity-high)', critical: 'var(--severity-critical)' }

  return (
    <div className="animate-fade-in">
      <div className="page-header">
        <h1>RoadScan <span className="text-gradient">Reports</span></h1>
        <p>Analytics and statistics for pothole detection operations</p>
      </div>

      {/* Stats Overview */}
      <div className="stats-grid">
        <div className="stat-card">
          <span className="stat-label">Total Incidents</span>
          <span className="stat-value">{total}</span>
          <span className="stat-detail">All time</span>
        </div>
        {severities.map(sev => (
          <div className="stat-card" key={sev}>
            <span className="stat-label">{sev} Severity</span>
            <span className="stat-value" style={{ background: severityColors[sev], WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              {severityData[sev] || 0}
            </span>
            <span className="stat-detail">
              {total > 0 ? `${(((severityData[sev] || 0) / total) * 100).toFixed(1)}%` : '0%'} of total
            </span>
          </div>
        ))}
      </div>

      {/* Severity Distribution Bar */}
      <div className="reports-grid">
        <div className="card">
          <div className="card-header">
            <h2>📊 Severity Distribution</h2>
          </div>
          <div className="card-body">
            {total > 0 ? (
              <>
                <div className="severity-bar">
                  {severities.map(sev => {
                    const count = severityData[sev] || 0
                    const pct = total > 0 ? (count / total) * 100 : 0
                    return (
                      <div
                        key={sev}
                        className="severity-bar-segment"
                        style={{ width: `${pct}%`, background: severityColors[sev] }}
                        title={`${sev}: ${count} (${pct.toFixed(1)}%)`}
                      />
                    )
                  })}
                </div>
                <div style={{ display: 'flex', gap: 'var(--space-lg)', marginTop: 'var(--space-md)', flexWrap: 'wrap' }}>
                  {severities.map(sev => (
                    <div key={sev} style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 'var(--text-xs)' }}>
                      <div style={{ width: 10, height: 10, borderRadius: '50%', background: severityColors[sev] }} />
                      <span style={{ color: 'var(--color-text-secondary)', textTransform: 'capitalize' }}>{sev}: {severityData[sev] || 0}</span>
                    </div>
                  ))}
                </div>
              </>
            ) : (
              <div className="empty-state">
                <div className="empty-state-icon">📊</div>
                <h3>No data yet</h3>
                <p>Start detecting potholes to see severity distribution analytics.</p>
              </div>
            )}
          </div>
        </div>

        {/* Current Configuration */}
        <div className="card">
          <div className="card-header">
            <h2>⚙️ Active Configuration</h2>
          </div>
          <div className="card-body">
            {config ? (
              <>
                <div className="info-row">
                  <span className="label">Runtime Mode</span>
                  <span className="value" style={{ color: 'var(--color-accent-cyan)' }}>{config.runtime_mode?.toUpperCase()}</span>
                </div>
                <div className="info-row">
                  <span className="label">Confidence Threshold</span>
                  <span className="value">{config.confidence_threshold}</span>
                </div>
                <div className="info-row">
                  <span className="label">IoU Threshold</span>
                  <span className="value">{config.iou_threshold}</span>
                </div>
                <div className="info-row">
                  <span className="label">Inference Resolution</span>
                  <span className="value">{config.inference_resolution}px</span>
                </div>
                <div className="info-row">
                  <span className="label">Max Inference FPS</span>
                  <span className="value">{config.max_inference_fps}</span>
                </div>
                <div className="info-row">
                  <span className="label">Tracker Confirm Frames</span>
                  <span className="value">{config.tracker_confirm_frames}</span>
                </div>
                <div className="info-row">
                  <span className="label">Spatial Dedup</span>
                  <span className="value">{config.incident_spatial_dedup_meters}m</span>
                </div>
                <div className="info-row">
                  <span className="label">GPS Accuracy Limit</span>
                  <span className="value">±{config.gps_accuracy_threshold_m}m</span>
                </div>
              </>
            ) : (
              <div style={{ color: 'var(--color-text-muted)', fontSize: 'var(--text-sm)' }}>
                Connect to backend to load configuration.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
