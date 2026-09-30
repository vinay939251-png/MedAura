import { useState, useEffect } from 'react'
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet'
import { getRoadscanIncidents } from '../../../core/api/client.js'

const severityColors = {
  low: '#10b981',
  medium: '#f59e0b',
  high: '#f97316',
  critical: '#ef4444',
}

const defaultCenter = [20.5937, 78.9629] // Center of India

export default function PotholeMap() {
  const [incidents, setIncidents] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('all')

  useEffect(() => {
    const fetchIncidents = async () => {
      try {
        const params = filter !== 'all' ? { severity: filter, page_size: 100 } : { page_size: 100 }
        const res = await getRoadscanIncidents(params)
        setIncidents(res.data.items || [])
      } catch (e) {
        console.error('Failed to fetch incidents:', e)
      }
      setLoading(false)
    }
    fetchIncidents()
    const interval = setInterval(fetchIncidents, 15000)
    return () => clearInterval(interval)
  }, [filter])

  const center = incidents.length > 0
    ? [incidents[0].latitude, incidents[0].longitude]
    : defaultCenter

  return (
    <div className="animate-fade-in">
      <div className="page-header">
        <h1>Pothole <span className="text-gradient">Map</span></h1>
        <p>Geospatial visualization of detected potholes — real-time updates</p>
      </div>

      {/* Toolbar */}
      <div className="map-toolbar">
        {['all', 'low', 'medium', 'high', 'critical'].map(sev => (
          <button
            key={sev}
            className={`btn ${filter === sev ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setFilter(sev)}
            style={{ textTransform: 'capitalize', fontSize: 'var(--text-xs)', padding: '6px 14px' }}
          >
            {sev === 'all' ? `All (${incidents.length})` : sev}
          </button>
        ))}
      </div>

      {/* Map */}
      <div className="map-container">
        <MapContainer center={center} zoom={incidents.length > 0 ? 14 : 5} style={{ height: '100%', width: '100%' }}>
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            className="map-tiles"
          />
          {incidents.map(inc => (
            <CircleMarker
              key={inc.id}
              center={[inc.latitude, inc.longitude]}
              radius={8}
              pathOptions={{
                color: severityColors[inc.severity] || '#f59e0b',
                fillColor: severityColors[inc.severity] || '#f59e0b',
                fillOpacity: 0.7,
                weight: 2,
              }}
            >
              <Popup>
                <div style={{ fontFamily: 'Inter, sans-serif', minWidth: 180 }}>
                  <div style={{ fontWeight: 700, marginBottom: 4 }}>🕳️ Pothole Detected</div>
                  <div style={{ fontSize: 12, lineHeight: 1.6 }}>
                    <strong>Severity:</strong> <span style={{ color: severityColors[inc.severity], textTransform: 'uppercase' }}>{inc.severity}</span><br />
                    <strong>Confidence:</strong> {(inc.confidence * 100).toFixed(1)}%<br />
                    <strong>Location:</strong> {inc.latitude?.toFixed(5)}, {inc.longitude?.toFixed(5)}<br />
                    <strong>GPS Accuracy:</strong> ±{inc.gps_accuracy?.toFixed(1)}m<br />
                    <strong>Status:</strong> {inc.status}<br />
                    <strong>Detected:</strong> {new Date(inc.detected_at).toLocaleString()}<br />
                    {inc.runtime_mode && <><strong>Runtime:</strong> {inc.runtime_mode}<br /></>}
                  </div>
                </div>
              </Popup>
            </CircleMarker>
          ))}
        </MapContainer>
      </div>

      {/* Incident Count */}
      {incidents.length === 0 && !loading && (
        <div style={{ textAlign: 'center', padding: 'var(--space-xl)', color: 'var(--color-text-muted)' }}>
          No incidents found. Start a scan session to detect potholes.
        </div>
      )}
    </div>
  )
}
