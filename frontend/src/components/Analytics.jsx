import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Button } from '@/components/ui/button'
import { RefreshCw } from 'lucide-react'
import { PnLChart } from './charts/PnLChart'
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
        <RefreshCw className="h-8 w-8 animate-spin text-muted-foreground" />
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
          <Tabs value={selectedPeriod} onValueChange={setSelectedPeriod}>
            <TabsList>
              {periods.map((period) => (
                <TabsTrigger key={period.value} value={period.value}>
                  {period.label}
                </TabsTrigger>
              ))}
            </TabsList>
          </Tabs>
          
          <Button onClick={fetchAnalyticsData} variant="outline">
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </Button>
        </div>
      </div>

      {/* P&L Chart */}
      <Card>
        <CardHeader>
          <CardTitle>P&L Performance ({selectedPeriod})</CardTitle>
          <CardDescription>
            Cumulative profit and loss over the selected period
          </CardDescription>
        </CardHeader>
        <CardContent>
          <PnLChart data={pnlChartData} />
        </CardContent>
      </Card>

      {/* Performance Metrics */}
      <Card>
        <CardHeader>
          <CardTitle>Performance Metrics</CardTitle>
          <CardDescription>
            Comprehensive trading performance statistics for {selectedPeriod}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <PerformanceMetrics data={performanceData} />
        </CardContent>
      </Card>

      {/* Token Performance */}
      <Card>
        <CardHeader>
          <CardTitle>Token Performance</CardTitle>
          <CardDescription>
            Performance breakdown by individual tokens
          </CardDescription>
        </CardHeader>
        <CardContent>
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
        </CardContent>
      </Card>
    </div>
  )
}

