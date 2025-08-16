import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Sidebar } from './components/Sidebar'
import { Dashboard } from './components/Dashboard'
import { Positions } from './components/Positions'
import { TradeHistory } from './components/TradeHistory'
import { Analytics } from './components/Analytics'
import { Settings } from './components/Settings'
import { Signals } from './components/Signals'
import './App.css'

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [systemStatus, setSystemStatus] = useState(null)

  useEffect(() => {
    // Fetch initial system status
    fetchSystemStatus()
    
    // Set up periodic status updates
    const interval = setInterval(fetchSystemStatus, 30000) // Every 30 seconds
    
    return () => clearInterval(interval)
  }, [])

  const fetchSystemStatus = async () => {
    try {
      const response = await fetch('/api/trading/status')
      const data = await response.json()
      if (data.success) {
        setSystemStatus(data.data)
      }
    } catch (error) {
      console.error('Failed to fetch system status:', error)
    }
  }

  return (
    <Router>
      <div className="flex h-screen bg-background">
        <Sidebar 
          isOpen={sidebarOpen} 
          onToggle={() => setSidebarOpen(!sidebarOpen)}
          systemStatus={systemStatus}
        />
        
        <main className={`flex-1 transition-all duration-300 ${sidebarOpen ? 'ml-64' : 'ml-16'}`}>
          <div className="h-full overflow-auto">
            <Routes>
              <Route path="/" element={<Dashboard systemStatus={systemStatus} />} />
              <Route path="/positions" element={<Positions />} />
              <Route path="/trades" element={<TradeHistory />} />
              <Route path="/analytics" element={<Analytics />} />
              <Route path="/signals" element={<Signals />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </div>
        </main>
      </div>
    </Router>
  )
}

export default App

