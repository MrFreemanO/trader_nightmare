import { Badge } from '@/components/ui/badge'
import { TrendingUp, TrendingDown } from 'lucide-react'

export function PerformanceMetrics({ data }) {
  if (!data) {
    return (
      <div className="text-center text-muted-foreground py-8">
        No performance data available
      </div>
    )
  }

  const metrics = [
    {
      label: 'Total Trades',
      value: data.total_trades,
      format: (val) => val.toString()
    },
    {
      label: 'Winning Trades',
      value: data.winning_trades,
      format: (val) => val.toString(),
      color: 'text-green-600'
    },
    {
      label: 'Losing Trades',
      value: data.losing_trades,
      format: (val) => val.toString(),
      color: 'text-red-600'
    },
    {
      label: 'Win Rate',
      value: data.win_rate,
      format: (val) => `${val.toFixed(1)}%`,
      color: data.win_rate >= 50 ? 'text-green-600' : 'text-red-600'
    },
    {
      label: 'Best Trade',
      value: data.best_trade,
      format: (val) => `$${val.toFixed(2)}`,
      color: 'text-green-600'
    },
    {
      label: 'Worst Trade',
      value: data.worst_trade,
      format: (val) => `$${val.toFixed(2)}`,
      color: 'text-red-600'
    },
    {
      label: 'Avg Trade Duration',
      value: data.avg_trade_duration,
      format: (val) => val
    },
    {
      label: 'Sharpe Ratio',
      value: data.sharpe_ratio,
      format: (val) => val.toFixed(2),
      color: data.sharpe_ratio >= 0 ? 'text-green-600' : 'text-red-600'
    },
    {
      label: 'Max Drawdown',
      value: data.max_drawdown,
      format: (val) => `${val.toFixed(2)}%`,
      color: 'text-red-600'
    },
    {
      label: 'Profit Factor',
      value: data.profit_factor,
      format: (val) => val.toFixed(3),
      color: data.profit_factor >= 1 ? 'text-green-600' : 'text-red-600'
    }
  ]

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
      {metrics.map((metric, index) => (
        <div key={index} className="text-center p-4 rounded-lg border border-border">
          <div className="text-sm text-muted-foreground mb-1">
            {metric.label}
          </div>
          <div className={`text-lg font-semibold ${metric.color || 'text-foreground'}`}>
            {metric.format(metric.value)}
          </div>
        </div>
      ))}
    </div>
  )
}

