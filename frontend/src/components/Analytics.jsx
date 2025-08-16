import { useState, useEffect } from 'react'
import { PnLChart } from './PnLChart'
import { PerformanceMetrics } from './PerformanceMetrics'

export function Analytics() {
  const [performanceData, setPerformanceData] = useState(null)
  const [pnlChartData, setPnlChartData] = useState([])
  const [tokenPerformance, setTokenPerformance] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedPeriod, setSelectedPeriod] = useState('24h')

  useEffect(() => {
    fetchAnalyticsData()
  }, [selectedPeriod])

  const fetchAnalyticsData = async () => {
    setLoading(true)
    try {
      const [performanceRes, chartRes, tokenRes] = await Promise.all([
        fetch(`/api/trading/performance?period=${selectedPeriod}`),
        fetch(`/api/trading/analytics/pnl-chart?period=${selectedPeriod}`),
        fetch('/api/trading/analytics/token-performance')
      ])

      const [performance, chart, tokens] = await Promise.all([
        performanceRes.json(),
        chartRes.json(),
        tokenRes.json()
      ])

      if (performance.success) setPerformanceData(performance.data)
      if (chart.success) setPnlChartData(chart.data)
      if (tokens.success) setTokenPerformance(tokens.data)
    } catch (error) {
      console.error('Failed to fetch analytics data:', error)
    } finally {
      setLoading(false)
    }
  }

  const periods = [
    { value: '24h', label: '24 Hours' },
    { value: '7d', label: '7 Days' },
    { value: '30d', label: '30 Days' }
  ]

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Analytics</h1>
          <p className="text-muted-foreground">
            Detailed performance analysis and insights
          </p>
        </div>
        
        <div className="flex items-center space-x-2">
          <div className="flex rounded-lg bg-gray-100 p-1">
            {periods.map((period) => (
              <button
                key={period.value}
                onClick={() => setSelectedPeriod(period.value)}
                className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${
                  selectedPeriod === period.value
                    ? 'bg-white text-blue-600 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                {period.label}
              </button>
            ))}
          </div>
          
          <button
            onClick={fetchAnalyticsData}
            className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            🔄 Refresh
          </button>
        </div>
      </div>

      {/* P&L Chart */}
      <div className="bg-white rounded-lg border border-gray-200 shadow-sm">
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">P&L Performance ({selectedPeriod})</h3>
          <p className="text-sm text-gray-600">
            Cumulative profit and loss over the selected period
          </p>
        </div>
        <div className="p-6">
          <PnLChart data={pnlChartData} />
        </div>
      </div>

      {/* Performance Metrics */}
      <div className="bg-white rounded-lg border border-gray-200 shadow-sm">
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Performance Metrics</h3>
          <p className="text-sm text-gray-600">
            Comprehensive trading performance statistics for {selectedPeriod}
          </p>
        </div>
        <div className="p-6">
          <PerformanceMetrics data={performanceData} />
        </div>
      </div>

      {/* Token Performance */}
      <div className="bg-white rounded-lg border border-gray-200 shadow-sm">
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Token Performance</h3>
          <p className="text-sm text-gray-600">
            Performance breakdown by individual tokens
          </p>
        </div>
        <div className="p-6">
          {tokenPerformance.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">
              No token performance data available
            </div>
          ) : (
            <div className="space-y-4">
              {tokenPerformance.map((token, index) => (
                <div key={index} className="flex items-center justify-between p-4 rounded-lg border border-border">
                  <div className="flex items-center space-x-4">
                    <div className="font-medium text-foreground">
                      {token.token_symbol}
                    </div>
                    <div className="text-sm text-muted-foreground">
                      {token.trades_count} trades
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-3 gap-8 text-right">
                    <div>
                      <div className="text-sm text-muted-foreground">Total P&L</div>
                      <div className={`font-medium ${
                        token.total_pnl >= 0 ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {token.total_pnl >= 0 ? '+' : ''}${token.total_pnl.toFixed(2)}
                      </div>
                    </div>
                    
                    <div>
                      <div className="text-sm text-muted-foreground">Win Rate</div>
                      <div className="font-medium">
                        {token.win_rate.toFixed(1)}%
                      </div>
                    </div>
                    
                    <div>
                      <div className="text-sm text-muted-foreground">Avg Hold Time</div>
                      <div className="font-medium">
                        {token.avg_hold_time}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

