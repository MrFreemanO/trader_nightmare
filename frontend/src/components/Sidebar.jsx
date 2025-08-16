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
    <div className={`fixed left-0 top-0 z-40 h-screen bg-white border-r border-gray-200 shadow-sm transition-all duration-300 ${
      isOpen ? "w-64" : "w-16"
    }`}>
      <div className="flex h-full flex-col">
        {/* Header */}
        <div className="flex h-16 items-center justify-between px-4 border-b border-gray-200">
          {isOpen && (
            <div className="flex items-center space-x-2">
              <div className="h-8 w-8 rounded-lg bg-blue-600 flex items-center justify-center">
                <TrendingUp className="h-5 w-5 text-white" />
              </div>
              <span className="font-semibold text-gray-900">TradingBot</span>
            </div>
          )}
          <button
            onClick={onToggle}
            className="h-8 w-8 inline-flex items-center justify-center rounded-md text-gray-500 hover:text-gray-600 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {isOpen ? <X className="h-4 w-4" /> : <Menu className="h-4 w-4" />}
          </button>
        </div>

        {/* System Status */}
        <div className="px-4 py-3 border-b border-gray-200">
          <div className="flex items-center space-x-2">
            <Circle className={`h-2 w-2 fill-current ${getStatusColor()}`} />
            {isOpen && (
              <div className="flex-1">
                <div className="text-sm font-medium text-gray-900">
                  System {getStatusText()}
                </div>
                {systemStatus && (
                  <div className="text-xs text-gray-500">
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
                className={`group flex items-center px-2 py-2 text-sm font-medium rounded-md transition-colors ${
                  isActive
                    ? "bg-blue-600 text-white"
                    : "text-gray-600 hover:bg-gray-100 hover:text-gray-900"
                }`}
              >
                <item.icon
                  className={`h-5 w-5 flex-shrink-0 ${
                    isOpen ? "mr-3" : "mx-auto"
                  }`}
                />
                {isOpen && item.name}
              </Link>
            )
          })}
        </nav>

        {/* Footer */}
        {isOpen && systemStatus && (
          <div className="border-t border-gray-200 p-4">
            <div className="text-xs text-gray-500 space-y-1">
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