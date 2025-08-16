import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { TrendingUp, TrendingDown, RefreshCw, X } from 'lucide-react'
import { format } from 'date-fns'

export function Positions() {
  const [positions, setPositions] = useState([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('all')

  useEffect(() => {
    fetchPositions()
  }, [])

  const fetchPositions = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/trading/positions')
      const data = await response.json()
      if (data.success) {
        setPositions(data.data)
      }
    } catch (error) {
      console.error('Failed to fetch positions:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleClosePosition = async (positionId) => {
    // In a real implementation, this would call the API to close the position
    console.log('Closing position:', positionId)
  }

  const filteredPositions = positions.filter(position => {
    if (activeTab === 'all') return true
    return position.status.toLowerCase() === activeTab
  })

  const getStatusBadgeVariant = (status) => {
    switch (status) {
      case 'ACTIVE': return 'default'
      case 'CLOSED': return 'secondary'
      default: return 'outline'
    }
  }

  const getPnLColor = (pnl) => {
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
          <h1 className="text-3xl font-bold text-foreground">Positions</h1>
          <p className="text-muted-foreground">
            Manage and monitor your trading positions
          </p>
        </div>
        
        <Button onClick={fetchPositions} variant="outline">
          <RefreshCw className="h-4 w-4 mr-2" />
          Refresh
        </Button>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="all">All Positions</TabsTrigger>
          <TabsTrigger value="active">Active</TabsTrigger>
          <TabsTrigger value="closed">Closed</TabsTrigger>
        </TabsList>

        <TabsContent value={activeTab} className="mt-6">
          {filteredPositions.length === 0 ? (
            <Card>
              <CardContent className="text-center py-12">
                <div className="text-muted-foreground">
                  No {activeTab === 'all' ? '' : activeTab} positions found
                </div>
              </CardContent>
            </Card>
          ) : (
            <div className="grid gap-4">
              {filteredPositions.map((position) => (
                <Card key={position.id}>
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <CardTitle className="text-lg">
                          {position.token_symbol}
                        </CardTitle>
                        <Badge variant={getStatusBadgeVariant(position.status)}>
                          {position.status}
                        </Badge>
                      </div>
                      
                      {position.status === 'ACTIVE' && (
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleClosePosition(position.id)}
                          className="text-muted-foreground hover:text-destructive"
                        >
                          <X className="h-4 w-4 mr-1" />
                          Close
                        </Button>
                      )}
                    </div>
                    
                    <CardDescription>
                      {position.token_address}
                    </CardDescription>
                  </CardHeader>
                  
                  <CardContent>
                    <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
                      <div>
                        <div className="text-sm text-muted-foreground">Entry Price</div>
                        <div className="font-medium">${position.entry_price.toFixed(4)}</div>
                      </div>
                      
                      <div>
                        <div className="text-sm text-muted-foreground">Current Price</div>
                        <div className="font-medium">${position.current_price.toFixed(4)}</div>
                      </div>
                      
                      <div>
                        <div className="text-sm text-muted-foreground">Amount</div>
                        <div className="font-medium">${position.amount}</div>
                      </div>
                      
                      <div>
                        <div className="text-sm text-muted-foreground">P&L</div>
                        <div className={`font-medium flex items-center space-x-1 ${getPnLColor(position.pnl)}`}>
                          {position.pnl >= 0 ? (
                            <TrendingUp className="h-3 w-3" />
                          ) : (
                            <TrendingDown className="h-3 w-3" />
                          )}
                          <span>
                            ${position.pnl.toFixed(2)} ({position.pnl_percentage.toFixed(2)}%)
                          </span>
                        </div>
                      </div>
                      
                      <div>
                        <div className="text-sm text-muted-foreground">Target Price</div>
                        <div className="font-medium">${position.target_price.toFixed(4)}</div>
                      </div>
                      
                      <div>
                        <div className="text-sm text-muted-foreground">Stop Loss</div>
                        <div className="font-medium">${position.stop_loss.toFixed(4)}</div>
                      </div>
                    </div>
                    
                    <div className="mt-4 pt-4 border-t border-border">
                      <div className="grid grid-cols-2 gap-4 text-sm text-muted-foreground">
                        <div>
                          Entry Time: {format(new Date(position.entry_time), 'MMM dd, yyyy HH:mm')}
                        </div>
                        {position.exit_time && (
                          <div>
                            Exit Time: {format(new Date(position.exit_time), 'MMM dd, yyyy HH:mm')}
                          </div>
                        )}
                        {position.exit_reason && (
                          <div className="col-span-2">
                            Exit Reason: <Badge variant="outline">{position.exit_reason}</Badge>
                          </div>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  )
}

