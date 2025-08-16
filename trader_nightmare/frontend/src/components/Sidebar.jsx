import { Link, useLocation } from 'react-router-dom'
import { 
  BarChart3, 
  TrendingUp, 
  Wallet, 
  History, 
  Settings, 
  Activity,
  Menu,
  X,
  Circle
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'

const navigation = [
  { name: 'Dashboard', href: '/', icon: BarChart3 },
  { name: 'Positions', href: '/positions', icon: Wallet },
  { name: 'Trade History', href: '/trades', icon: History },
  { name: 'Analytics', href: '/analytics', icon: TrendingUp },
  { name: 'Signals', href: '/signals', icon: Activity },
  { name: 'Settings', href: '/settings', icon: Settings },
]

export function Sidebar({ isOpen, onToggle, systemStatus }) {
  const location = useLocation()

  const getStatusColor = () => {
    if (!systemStatus) return 'text-gray-400'
    return systemStatus.system_running ? 'text-green-500' : 'text-red-500'
  }

  const getStatusText = () => {
    if (!systemStatus) return 'Unknown'
    return systemStatus.system_running ? 'Online' : 'Offline'
  }

  return (
    <div className={cn(
      "fixed left-0 top-0 z-40 h-screen bg-card border-r border-border transition-all duration-300",
      isOpen ? "w-64" : "w-16"
    )}>
      <div className="flex h-full flex-col">
        {/* Header */}
        <div className="flex h-16 items-center justify-between px-4 border-b border-border">
          {isOpen && (
            <div className="flex items-center space-x-2">
              <div className="h-8 w-8 rounded-lg bg-primary flex items-center justify-center">
                <TrendingUp className="h-5 w-5 text-primary-foreground" />
              </div>
              <span className="font-semibold text-foreground">TradingBot</span>
            </div>
          )}
          <Button
            variant="ghost"
            size="icon"
            onClick={onToggle}
            className="h-8 w-8"
          >
            {isOpen ? <X className="h-4 w-4" /> : <Menu className="h-4 w-4" />}
          </Button>
        </div>

        {/* System Status */}
        <div className="px-4 py-3 border-b border-border">
          <div className="flex items-center space-x-2">
            <Circle className={cn("h-2 w-2 fill-current", getStatusColor())} />
            {isOpen && (
              <div className="flex-1">
                <div className="text-sm font-medium text-foreground">
                  System {getStatusText()}
                </div>
                {systemStatus && (
                  <div className="text-xs text-muted-foreground">
                    {systemStatus.active_positions} active positions
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 space-y-1 px-2 py-4">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href
            return (
              <Link
                key={item.name}
                to={item.href}
                className={cn(
                  "group flex items-center px-2 py-2 text-sm font-medium rounded-md transition-colors",
                  isActive
                    ? "bg-primary text-primary-foreground"
                    : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                )}
              >
                <item.icon
                  className={cn(
                    "h-5 w-5 flex-shrink-0",
                    isOpen ? "mr-3" : "mx-auto"
                  )}
                />
                {isOpen && item.name}
              </Link>
            )
          })}
        </nav>

        {/* Footer */}
        {isOpen && systemStatus && (
          <div className="border-t border-border p-4">
            <div className="text-xs text-muted-foreground space-y-1">
              <div>Uptime: {systemStatus.uptime || 'N/A'}</div>
              <div>Cache: {systemStatus.cache_size || 0} items</div>
              <div>Executions: {systemStatus.total_executions || 0}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

