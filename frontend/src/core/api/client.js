import axios from 'axios'

const IS_PROD = import.meta.env.PROD
const PROD_BACKEND_URL = 'https://medaura-1.onrender.com'
const PROD_WS_URL = 'wss://medaura-1.onrender.com'

const API_BASE = IS_PROD ? `${PROD_BACKEND_URL}/api/v1` : '/api/v1'

const api = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
})

// ── Platform APIs ──
export const getHealth = () => api.get('/health')
export const getModules = () => api.get('/modules')
export const getModuleHealth = (id) => api.get(`/modules/${id}/health`)

// ── Incidents (cross-module) ──
export const getIncidents = (params = {}) => api.get('/incidents', { params })
export const getIncident = (id) => api.get(`/incidents/${id}`)
export const updateIncident = (id, data) => api.patch(`/incidents/${id}`, data)

// ── Sessions ──
export const createSession = (data) => api.post('/sessions', data)
export const getSessions = () => api.get('/sessions')

// ── Devices ──
export const getDevices = () => api.get('/devices')

// ── Analytics ──
export const getAnalyticsSummary = () => api.get('/analytics/summary')

// ── ROADSCAN AI Module ──
export const getRoadscanConfig = () => api.get('/roadscan_ai/config')
export const updateRoadscanConfig = (data) => api.put('/roadscan_ai/config', data)
export const getRoadscanModelInfo = () => api.get('/roadscan_ai/model/info')
export const getRoadscanIncidents = (params = {}) => api.get('/roadscan_ai/incidents', { params })
export const createRoadscanIncident = (data) => api.post('/roadscan_ai/incidents', data)
export const getRoadscanStats = () => api.get('/roadscan_ai/incidents/stats')

// ── WebSocket ──
export function createWebSocket(channel = 'incidents') {
  if (IS_PROD) {
    return new WebSocket(`${PROD_WS_URL}/ws/${channel}`)
  }
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  const host = window.location.host
  return new WebSocket(`${protocol}//${host}/ws/${channel}`)
}

export default api
