import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { 
  TrendingUp, 
  TrendingDown, 
  DollarSign, 
  Activity, 
  Wallet,
  AlertTriangle,
  Play,
  Pause,
  RefreshCw
} from 'lucide-react'
import { PnLChart } from './charts/PnLChart'
import { PerformanceMetrics } from './PerformanceMetrics'
import { RecentTrades } from './RecentTrades'
import { ActivePositions } from './ActivePositions'

export function Dashboard({ systemStatus }) {
  const [performanceData, setPerformanceData] = useState(null)
  const [pnlChartData, setPnlChartData] = useState([])
  const [recentTrades, setRecentTrades] = useState([])
  const [activePositions, setActivePositions] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    setLoading(true)
    try {
      // Fetch all dashboard data in parallel
      const [performanceRes, chartRes, tradesRes, positionsRes] = await Promise.all([
        fetch('/api/trading/performance'),
        fetch('/api/trading/analytics/pnl-chart?period=24h'),
        fetch('/api/trading/trades?limit=5'),
        fetch('/api/trading/positions?status=ACTIVE')
      ])

      const [performance, chart, trades, positions] = await Promise.all([
        performanceRes.json(),
        chartRes.json(),
        tradesRes.json(),
        positionsRes.json()
      ])

      if (performance.success) setPerformanceData(performance.data)
      if (chart.success) setPnlChartData(chart.data)
      if (trades.success) setRecentTrades(trades.data)
      if (positions.success) setActivePositions(positions.data)
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleControlAction = async (action) => {
    try {
      const response = await fetch(`/api/trading/control/${action}`, {
        method: 'POST'
      })
      const data = await response.json()
      if (data.success) {
        // Refresh system status
        setTimeout(() => window.location.reload(), 1000)
      }
    } catch (error) {
      console.error(`Failed to ${action}:`, error)
    }
  }

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
          <h1 className="text-3xl font-bold text-foreground">Trading Dashboard</h1>
          <p className="text-muted-foreground">
            Monitor your automated trading performance and system status
          </p>
        </div>
        
        <div className="flex items-center space-x-2">
          <Button
            variant={systemStatus?.system_running ? "destructive" : "default"}
            onClick={() => handleControlAction(systemStatus?.system_running ? 'stop' : 'start')}
            className="flex items-center space-x-2"
          >
            {systemStatus?.system_running ? (
              <>
                <Pause className="h-4 w-4" />
                <span>Stop Bot</span>
              </>
            ) : (
              <>
                <Play className="h-4 w-4" />
                <span>Start Bot</span>
              </>
            )}
          </Button>
          
          <Button
            variant="outline"
            onClick={() => handleControlAction('emergency-stop')}
            className="flex items-center space-x-2 text-destructive hover:text-destructive"
          >
            <AlertTriangle className="h-4 w-4" />
            <span>Emergency Stop</span>
          </Button>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total P&L</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {performanceData?.total_pnl >= 0 ? '+' : ''}
              ${performanceData?.total_pnl?.toFixed(2) || '0.00'}
            </div>
            <p className="text-xs text-muted-foreground">
              {performanceData?.total_pnl_percentage >= 0 ? '+' : ''}
              {performanceData?.total_pnl_percentage?.toFixed(2) || '0.00'}% overall
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Win Rate</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {performanceData?.win_rate?.toFixed(1) || '0.0'}%
            </div>
            <p className="text-xs text-muted-foreground">
              {performanceData?.winning_trades || 0} of {performanceData?.total_trades || 0} trades
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Positions</CardTitle>
            <Wallet className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {activePositions?.length || 0}
            </div>
            <p className="text-xs text-muted-foreground">
              Currently trading
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">System Status</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="flex items-center space-x-2">
              <Badge variant={systemStatus?.system_running ? "default" : "destructive"}>
                {systemStatus?.system_running ? 'Running' : 'Stopped'}
              </Badge>
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              {systemStatus?.uptime || 'N/A'} uptime
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Charts and Data */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* P&L Chart */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>P&L Performance (24h)</CardTitle>
            <CardDescription>
              Cumulative profit and loss over the last 24 hours
            </CardDescription>
          </CardHeader>
          <CardContent>
            <PnLChart data={pnlChartData} />
          </CardContent>
        </Card>
      </div>

      {/* Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Active Positions */}
        <Card>
          <CardHeader>
            <CardTitle>Active Positions</CardTitle>
            <CardDescription>
              Currently open trading positions
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ActivePositions positions={activePositions} />
          </CardContent>
        </Card>

        {/* Recent Trades */}
        <Card>
          <CardHeader>
            <CardTitle>Recent Trades</CardTitle>
            <CardDescription>
              Latest trading activity
            </CardDescription>
          </CardHeader>
          <CardContent>
            <RecentTrades trades={recentTrades} />
          </CardContent>
        </Card>
      </div>

      {/* Performance Metrics */}
      <Card>
        <CardHeader>
          <CardTitle>Performance Metrics</CardTitle>
          <CardDescription>
            Detailed trading performance statistics
          </CardDescription>
        </CardHeader>
        <CardContent>
          <PerformanceMetrics data={performanceData} />
        </CardContent>
      </Card>
    </div>
  )
}

