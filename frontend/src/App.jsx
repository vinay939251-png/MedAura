import { Routes, Route } from 'react-router-dom'
import Layout from './core/components/Layout.jsx'
import Dashboard from './pages/Dashboard.jsx'
import NotFound from './pages/NotFound.jsx'

// Module pages (ROADSCAN AI)
import ScanView from './modules/roadscan_ai/pages/ScanView.jsx'
import PotholeMap from './modules/roadscan_ai/pages/PotholeMap.jsx'
import Reports from './modules/roadscan_ai/pages/Reports.jsx'

function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        {/* Platform */}
        <Route path="/" element={<Dashboard />} />

        {/* ROADSCAN AI Module */}
        <Route path="/roadscan/scan" element={<ScanView />} />
        <Route path="/roadscan/map" element={<PotholeMap />} />
        <Route path="/roadscan/reports" element={<Reports />} />

        {/* Catch-all */}
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  )
}

export default App
