import { useState, useRef, useEffect, useCallback } from 'react'
import { Camera, CameraOff, Play, Square, MapPin, Cpu, Gauge, Thermometer } from 'lucide-react'
import { getRoadscanConfig, getRoadscanModelInfo } from '../../../core/api/client.js'

export default function ScanView() {
  const videoRef = useRef(null)
  const canvasRef = useRef(null)
  const [streaming, setStreaming] = useState(false)
  const [gps, setGps] = useState(null)
  const [gpsError, setGpsError] = useState(null)
  const [config, setConfig] = useState(null)
  const [modelInfo, setModelInfo] = useState(null)
  const [detectionCount, setDetectionCount] = useState(0)
  const [fps, setFps] = useState(0)

  // Fetch module config & model info
  useEffect(() => {
    const fetchInfo = async () => {
      try {
        const [cfgRes, modelRes] = await Promise.allSettled([
          getRoadscanConfig(),
          getRoadscanModelInfo(),
        ])
        if (cfgRes.status === 'fulfilled') setConfig(cfgRes.value.data.config)
        if (modelRes.status === 'fulfilled') setModelInfo(modelRes.value.data.model)
      } catch (e) {
        console.error('Failed to fetch ROADSCAN config:', e)
      }
    }
    fetchInfo()
  }, [])

  // GPS tracking
  useEffect(() => {
    if (!navigator.geolocation) {
      setGpsError('Geolocation not supported')
      return
    }
    const watchId = navigator.geolocation.watchPosition(
      (pos) => {
        setGps({
          lat: pos.coords.latitude,
          lng: pos.coords.longitude,
          accuracy: pos.coords.accuracy,
          speed: pos.coords.speed,
        })
        setGpsError(null)
      },
      (err) => setGpsError(err.message),
      { enableHighAccuracy: true, maximumAge: 5000 }
    )
    return () => navigator.geolocation.clearWatch(watchId)
  }, [])

  // Camera start/stop
  const startCamera = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } },
        audio: false,
      })
      if (videoRef.current) {
        videoRef.current.srcObject = stream
        await videoRef.current.play()
        setStreaming(true)
      }
    } catch (err) {
      console.error('Camera error:', err)
      alert('Camera access denied or unavailable. Please allow camera permissions.')
    }
  }, [])

  const stopCamera = useCallback(() => {
    if (videoRef.current?.srcObject) {
      videoRef.current.srcObject.getTracks().forEach(t => t.stop())
      videoRef.current.srcObject = null
    }
    setStreaming(false)
  }, [])

  useEffect(() => {
    return () => stopCamera()
  }, [stopCamera])

  return (
    <div className="animate-fade-in">
      <div className="page-header">
        <h1>Live <span className="text-gradient">Scan</span></h1>
        <p>Real-time pothole detection using edge AI inference</p>
      </div>

      <div className="scan-container">
        {/* Camera Panel */}
        <div className="camera-panel">
          <video ref={videoRef} playsInline muted style={{ display: streaming ? 'block' : 'none' }} />
          <canvas ref={canvasRef} style={{ display: streaming ? 'block' : 'none' }} />

          {!streaming && (
            <div className="camera-placeholder">
              <div className="camera-placeholder-icon">📷</div>
              <h3 style={{ color: 'var(--color-text-secondary)', fontSize: 'var(--text-lg)' }}>Camera Inactive</h3>
              <p style={{ color: 'var(--color-text-muted)', fontSize: 'var(--text-sm)', maxWidth: 320 }}>
                Click "Start Scan" to activate the camera and begin real-time pothole detection.
                AI inference runs locally on your device.
              </p>
              <button className="btn btn-primary" onClick={startCamera} style={{ marginTop: 'var(--space-md)' }}>
                <Play size={18} /> Start Scan
              </button>
            </div>
          )}

          {streaming && (
            <div className="camera-overlay-badge">
              <span className="status-badge healthy" style={{ backdropFilter: 'blur(8px)', background: 'rgba(16,185,129,0.2)' }}>
                ● LIVE
              </span>
              <span className="status-badge" style={{ backdropFilter: 'blur(8px)', background: 'rgba(6,182,212,0.2)', color: 'var(--color-accent-cyan)' }}>
                EDGE AI
              </span>
            </div>
          )}
        </div>

        {/* Info Panels */}
        <div className="info-panels">
          {/* Controls */}
          <div className="info-panel">
            <h3>Controls</h3>
            <div style={{ display: 'flex', gap: 'var(--space-sm)' }}>
              {!streaming ? (
                <button className="btn btn-primary" onClick={startCamera} style={{ flex: 1 }}>
                  <Camera size={16} /> Start
                </button>
              ) : (
                <button className="btn btn-danger" onClick={stopCamera} style={{ flex: 1 }}>
                  <Square size={16} /> Stop
                </button>
              )}
            </div>
          </div>

          {/* AI Status */}
          <div className="info-panel">
            <h3>🧠 AI Status</h3>
            <div className="info-row">
              <span className="label">Runtime</span>
              <span className="value" style={{ color: 'var(--color-accent-cyan)' }}>EDGE</span>
            </div>
            <div className="info-row">
              <span className="label">Model</span>
              <span className="value">{modelInfo?.status === 'not_loaded' ? 'Not Loaded' : 'RoadScan v1'}</span>
            </div>
            <div className="info-row">
              <span className="label">Inference FPS</span>
              <span className="value" style={{ color: 'var(--color-accent-emerald)' }}>{fps || '—'}</span>
            </div>
            <div className="info-row">
              <span className="label">Detections</span>
              <span className="value">{detectionCount}</span>
            </div>
            <div className="info-row">
              <span className="label">Confidence</span>
              <span className="value">{config?.confidence_threshold || 0.5}</span>
            </div>
          </div>

          {/* GPS Status */}
          <div className="info-panel">
            <h3>📍 GPS Status</h3>
            {gpsError ? (
              <div style={{ color: 'var(--status-unhealthy)', fontSize: 'var(--text-sm)' }}>
                ⚠ {gpsError}
              </div>
            ) : gps ? (
              <>
                <div className="info-row">
                  <span className="label">Latitude</span>
                  <span className="value">{gps.lat.toFixed(6)}</span>
                </div>
                <div className="info-row">
                  <span className="label">Longitude</span>
                  <span className="value">{gps.lng.toFixed(6)}</span>
                </div>
                <div className="info-row">
                  <span className="label">Accuracy</span>
                  <span className="value" style={{ color: gps.accuracy < 15 ? 'var(--status-healthy)' : 'var(--status-degraded)' }}>
                    ±{gps.accuracy?.toFixed(1)}m
                  </span>
                </div>
                <div className="info-row">
                  <span className="label">Speed</span>
                  <span className="value">{gps.speed ? `${(gps.speed * 3.6).toFixed(1)} km/h` : '—'}</span>
                </div>
              </>
            ) : (
              <div style={{ color: 'var(--color-text-muted)', fontSize: 'var(--text-sm)' }}>
                Acquiring GPS signal...
              </div>
            )}
          </div>

          {/* Session Info */}
          <div className="info-panel">
            <h3>📊 Session</h3>
            <div className="info-row">
              <span className="label">Status</span>
              <span className="value" style={{ color: streaming ? 'var(--status-healthy)' : 'var(--color-text-muted)' }}>
                {streaming ? 'ACTIVE' : 'IDLE'}
              </span>
            </div>
            <div className="info-row">
              <span className="label">Mode</span>
              <span className="value">Edge Inference</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
