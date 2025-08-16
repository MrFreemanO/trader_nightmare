import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Switch } from '@/components/ui/switch'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Badge } from '@/components/ui/badge'
import { RefreshCw, Save, AlertTriangle } from 'lucide-react'

export function Settings() {
  const [config, setConfig] = useState({
    viability_threshold: 70.0,
    max_position_size: 1000.0,
    slippage_tolerance: 0.02,
    stop_loss_percentage: 0.15,
    take_profit_percentage: 0.25,
    max_concurrent_positions: 5,
    trading_enabled: true,
    auto_trading: false
  })
  const [systemStatus, setSystemStatus] = useState(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    fetchConfig()
    fetchSystemStatus()
  }, [])

  const fetchConfig = async () => {
    try {
      const response = await fetch('/api/trading/config')
      const data = await response.json()
      if (data.success) {
        setConfig(data.data)
      }
    } catch (error) {
      console.error('Failed to fetch config:', error)
    } finally {
      setLoading(false)
    }
  }

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

  const handleConfigChange = (key, value) => {
    setConfig(prev => ({ ...prev, [key]: value }))
  }

  const handleSaveConfig = async () => {
    setSaving(true)
    try {
      const response = await fetch('/api/trading/config', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(config)
      })
      const data = await response.json()
      if (data.success) {
        // Show success message
        console.log('Configuration saved successfully')
      }
    } catch (error) {
      console.error('Failed to save config:', error)
    } finally {
      setSaving(false)
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
          <h1 className="text-3xl font-bold text-foreground">Settings</h1>
          <p className="text-muted-foreground">
            Configure trading bot parameters and system settings
          </p>
        </div>
        
        <Button onClick={handleSaveConfig} disabled={saving}>
          {saving ? (
            <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
          ) : (
            <Save className="h-4 w-4 mr-2" />
          )}
          Save Changes
        </Button>
      </div>

      <Tabs defaultValue="trading" className="space-y-6">
        <TabsList>
          <TabsTrigger value="trading">Trading Parameters</TabsTrigger>
          <TabsTrigger value="risk">Risk Management</TabsTrigger>
          <TabsTrigger value="system">System Status</TabsTrigger>
        </TabsList>

        <TabsContent value="trading" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Trading Configuration</CardTitle>
              <CardDescription>
                Core trading parameters and thresholds
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <Label htmlFor="viability_threshold">Viability Threshold (%)</Label>
                  <Input
                    id="viability_threshold"
                    type="number"
                    min="0"
                    max="100"
                    step="0.1"
                    value={config.viability_threshold}
                    onChange={(e) => handleConfigChange('viability_threshold', parseFloat(e.target.value))}
                  />
                  <p className="text-sm text-muted-foreground">
                    Minimum viability score required to execute trades
                  </p>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="max_position_size">Max Position Size ($)</Label>
                  <Input
                    id="max_position_size"
                    type="number"
                    min="0"
                    step="100"
                    value={config.max_position_size}
                    onChange={(e) => handleConfigChange('max_position_size', parseFloat(e.target.value))}
                  />
                  <p className="text-sm text-muted-foreground">
                    Maximum amount to invest in a single position
                  </p>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="slippage_tolerance">Slippage Tolerance (%)</Label>
                  <Input
                    id="slippage_tolerance"
                    type="number"
                    min="0"
                    max="10"
                    step="0.01"
                    value={config.slippage_tolerance * 100}
                    onChange={(e) => handleConfigChange('slippage_tolerance', parseFloat(e.target.value) / 100)}
                  />
                  <p className="text-sm text-muted-foreground">
                    Maximum acceptable price slippage
                  </p>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="max_concurrent_positions">Max Concurrent Positions</Label>
                  <Input
                    id="max_concurrent_positions"
                    type="number"
                    min="1"
                    max="20"
                    value={config.max_concurrent_positions}
                    onChange={(e) => handleConfigChange('max_concurrent_positions', parseInt(e.target.value))}
                  />
                  <p className="text-sm text-muted-foreground">
                    Maximum number of simultaneous open positions
                  </p>
                </div>
              </div>

              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Trading Enabled</Label>
                    <p className="text-sm text-muted-foreground">
                      Enable or disable all trading activities
                    </p>
                  </div>
                  <Switch
                    checked={config.trading_enabled}
                    onCheckedChange={(checked) => handleConfigChange('trading_enabled', checked)}
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Auto Trading</Label>
                    <p className="text-sm text-muted-foreground">
                      Automatically execute trades based on signals
                    </p>
                  </div>
                  <Switch
                    checked={config.auto_trading}
                    onCheckedChange={(checked) => handleConfigChange('auto_trading', checked)}
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="risk" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Risk Management</CardTitle>
              <CardDescription>
                Configure stop loss, take profit, and risk parameters
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <Label htmlFor="stop_loss_percentage">Stop Loss (%)</Label>
                  <Input
                    id="stop_loss_percentage"
                    type="number"
                    min="0"
                    max="50"
                    step="0.01"
                    value={config.stop_loss_percentage * 100}
                    onChange={(e) => handleConfigChange('stop_loss_percentage', parseFloat(e.target.value) / 100)}
                  />
                  <p className="text-sm text-muted-foreground">
                    Default stop loss percentage for new positions
                  </p>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="take_profit_percentage">Take Profit (%)</Label>
                  <Input
                    id="take_profit_percentage"
                    type="number"
                    min="0"
                    max="100"
                    step="0.01"
                    value={config.take_profit_percentage * 100}
                    onChange={(e) => handleConfigChange('take_profit_percentage', parseFloat(e.target.value) / 100)}
                  />
                  <p className="text-sm text-muted-foreground">
                    Default take profit percentage for new positions
                  </p>
                </div>
              </div>

              <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                <div className="flex items-center space-x-2">
                  <AlertTriangle className="h-4 w-4 text-yellow-600" />
                  <span className="text-sm font-medium text-yellow-800">Risk Warning</span>
                </div>
                <p className="text-sm text-yellow-700 mt-1">
                  Cryptocurrency trading involves substantial risk of loss. Only trade with funds you can afford to lose.
                  Past performance does not guarantee future results.
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="system" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>System Status</CardTitle>
              <CardDescription>
                Current system health and data provider status
              </CardDescription>
            </CardHeader>
            <CardContent>
              {systemStatus ? (
                <div className="space-y-6">
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="text-center p-4 rounded-lg border border-border">
                      <div className="text-sm text-muted-foreground mb-1">System Status</div>
                      <Badge variant={systemStatus.system_running ? "default" : "destructive"}>
                        {systemStatus.system_running ? 'Running' : 'Stopped'}
                      </Badge>
                    </div>
                    
                    <div className="text-center p-4 rounded-lg border border-border">
                      <div className="text-sm text-muted-foreground mb-1">Active Positions</div>
                      <div className="text-lg font-semibold">{systemStatus.active_positions}</div>
                    </div>
                    
                    <div className="text-center p-4 rounded-lg border border-border">
                      <div className="text-sm text-muted-foreground mb-1">Total Executions</div>
                      <div className="text-lg font-semibold">{systemStatus.total_executions}</div>
                    </div>
                    
                    <div className="text-center p-4 rounded-lg border border-border">
                      <div className="text-sm text-muted-foreground mb-1">Cache Size</div>
                      <div className="text-lg font-semibold">{systemStatus.cache_size}</div>
                    </div>
                  </div>

                  <div>
                    <h3 className="text-lg font-medium mb-4">Data Providers</h3>
                    <div className="space-y-3">
                      {Object.entries(systemStatus.data_providers).map(([name, status]) => (
                        <div key={name} className="flex items-center justify-between p-3 rounded-lg border border-border">
                          <div className="flex items-center space-x-3">
                            <div className={`h-2 w-2 rounded-full ${
                              status.connected ? 'bg-green-500' : 'bg-red-500'
                            }`} />
                            <span className="font-medium">{name}</span>
                          </div>
                          
                          <div className="text-right">
                            <Badge variant={status.connected ? "default" : "destructive"}>
                              {status.connected ? 'Connected' : 'Disconnected'}
                            </Badge>
                            {status.latency && (
                              <div className="text-xs text-muted-foreground mt-1">
                                {status.latency}ms
                              </div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              ) : (
                <div className="text-center py-8 text-muted-foreground">
                  Unable to fetch system status
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

