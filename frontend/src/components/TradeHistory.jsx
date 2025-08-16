import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { TrendingUp, TrendingDown, RefreshCw, ChevronLeft, ChevronRight } from 'lucide-react'
import { format } from 'date-fns'

export function TradeHistory() {
  const [trades, setTrades] = useState([])
  const [loading, setLoading] = useState(true)
  const [pagination, setPagination] = useState({
    page: 1,
    limit: 10,
    total: 0,
    pages: 0
  })

  useEffect(() => {
    fetchTrades()
  }, [pagination.page])

  const fetchTrades = async () => {
    setLoading(true)
    try {
      const response = await fetch(`/api/trading/trades?page=${pagination.page}&limit=${pagination.limit}`)
      const data = await response.json()
      if (data.success) {
        setTrades(data.data)
        setPagination(prev => ({ ...prev, ...data.pagination }))
      }
    } catch (error) {
      console.error('Failed to fetch trades:', error)
    } finally {
      setLoading(false)
    }
  }

  const handlePageChange = (newPage) => {
    setPagination(prev => ({ ...prev, page: newPage }))
  }

  const getActionBadgeVariant = (action) => {
    switch (action) {
      case 'BUY': return 'default'
      case 'SELL': return 'destructive'
      default: return 'outline'
    }
  }

  const getPnLColor = (pnl) => {
    if (pnl === undefined) return 'text-muted-foreground'
    return pnl >= 0 ? 'text-green-600' : 'text-red-600'
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
          <h1 className="text-3xl font-bold text-foreground">Trade History</h1>
          <p className="text-muted-foreground">
            Complete history of all trading activities
          </p>
        </div>
        
        <Button onClick={fetchTrades} variant="outline">
          <RefreshCw className="h-4 w-4 mr-2" />
          Refresh
        </Button>
      </div>

      {/* Trades List */}
      <Card>
        <CardHeader>
          <CardTitle>All Trades</CardTitle>
          <CardDescription>
            Showing {trades.length} of {pagination.total} trades
          </CardDescription>
        </CardHeader>
        
        <CardContent>
          {trades.length === 0 ? (
            <div className="text-center py-12 text-muted-foreground">
              No trades found
            </div>
          ) : (
            <div className="space-y-4">
              {trades.map((trade) => (
                <div key={trade.id} className="flex items-center justify-between p-4 rounded-lg border border-border">
                  <div className="flex items-center space-x-4">
                    <div className={`p-2 rounded-full ${
                      trade.action === 'BUY' ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'
                    }`}>
                      {trade.action === 'BUY' ? (
                        <TrendingUp className="h-4 w-4" />
                      ) : (
                        <TrendingDown className="h-4 w-4" />
                      )}
                    </div>
                    
                    <div>
                      <div className="flex items-center space-x-2">
                        <span className="font-medium text-foreground">
                          {trade.token_symbol}
                        </span>
                        <Badge variant={getActionBadgeVariant(trade.action)}>
                          {trade.action}
                        </Badge>
                      </div>
                      <div className="text-sm text-muted-foreground">
                        {format(new Date(trade.timestamp), 'MMM dd, yyyy HH:mm:ss')}
                      </div>
                    </div>
                  </div>
                  
                  <div className="text-right space-y-1">
                    <div className="font-medium text-foreground">
                      ${trade.price.toFixed(4)}
                    </div>
                    <div className="text-sm text-muted-foreground">
                      Amount: ${trade.amount}
                    </div>
                    {trade.viability_score && (
                      <div className="text-xs text-muted-foreground">
                        Score: {trade.viability_score.toFixed(1)}
                      </div>
                    )}
                  </div>
                  
                  {trade.pnl !== undefined && (
                    <div className="text-right">
                      <div className={`font-medium ${getPnLColor(trade.pnl)}`}>
                        {trade.pnl >= 0 ? '+' : ''}${trade.pnl.toFixed(2)}
                      </div>
                      <div className={`text-sm ${getPnLColor(trade.pnl)}`}>
                        {trade.pnl_percentage >= 0 ? '+' : ''}{trade.pnl_percentage.toFixed(2)}%
                      </div>
                      {trade.exit_reason && (
                        <div className="text-xs text-muted-foreground mt-1">
                          {trade.exit_reason}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
          
          {/* Pagination */}
          {pagination.pages > 1 && (
            <div className="flex items-center justify-between mt-6 pt-4 border-t border-border">
              <div className="text-sm text-muted-foreground">
                Page {pagination.page} of {pagination.pages}
              </div>
              
              <div className="flex items-center space-x-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handlePageChange(pagination.page - 1)}
                  disabled={pagination.page <= 1}
                >
                  <ChevronLeft className="h-4 w-4" />
                  Previous
                </Button>
                
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handlePageChange(pagination.page + 1)}
                  disabled={pagination.page >= pagination.pages}
                >
                  Next
                  <ChevronRight className="h-4 w-4" />
                </Button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

