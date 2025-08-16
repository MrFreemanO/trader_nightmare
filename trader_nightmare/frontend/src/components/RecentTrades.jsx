import { Badge } from '@/components/ui/badge'
import { TrendingUp, TrendingDown } from 'lucide-react'
import { format } from 'date-fns'

export function RecentTrades({ trades }) {
  if (!trades || trades.length === 0) {
    return (
      <div className="text-center text-muted-foreground py-8">
        No recent trades
      </div>
    )
  }

  return (
    <div className="space-y-3">
      {trades.map((trade) => (
        <div key={trade.id} className="flex items-center justify-between p-3 rounded-lg border border-border">
          <div className="flex items-center space-x-3">
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
              <div className="font-medium text-foreground">
                {trade.token_symbol}
              </div>
              <div className="text-sm text-muted-foreground">
                {format(new Date(trade.timestamp), 'MMM dd, HH:mm')}
              </div>
            </div>
          </div>
          
          <div className="text-right">
            <div className="font-medium text-foreground">
              ${trade.price.toFixed(4)}
            </div>
            <div className="text-sm text-muted-foreground">
              ${trade.amount}
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

