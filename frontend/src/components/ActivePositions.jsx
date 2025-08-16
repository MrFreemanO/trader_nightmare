import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { TrendingUp, TrendingDown, X } from 'lucide-react'

export function ActivePositions({ positions }) {
  if (!positions || positions.length === 0) {
    return (
      <div className="text-center text-muted-foreground py-8">
        No active positions
      </div>
    )
  }

  const handleClosePosition = async (positionId) => {
    // In a real implementation, this would call the API to close the position
    console.log('Closing position:', positionId)
  }

  return (
    <div className="space-y-3">
      {positions.map((position) => (
        <div key={position.id} className="p-4 rounded-lg border border-border">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center space-x-2">
              <span className="font-medium text-foreground">
                {position.token_symbol}
              </span>
              <Badge variant={position.status === 'ACTIVE' ? 'default' : 'secondary'}>
                {position.status}
              </Badge>
            </div>
            
            <Button
              variant="ghost"
              size="sm"
              onClick={() => handleClosePosition(position.id)}
              className="h-6 w-6 p-0 text-muted-foreground hover:text-destructive"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
          
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <div className="text-muted-foreground">Entry Price</div>
              <div className="font-medium">${position.entry_price.toFixed(4)}</div>
            </div>
            
            <div>
              <div className="text-muted-foreground">Current Price</div>
              <div className="font-medium">${position.current_price.toFixed(4)}</div>
            </div>
            
            <div>
              <div className="text-muted-foreground">Amount</div>
              <div className="font-medium">${position.amount}</div>
            </div>
            
            <div>
              <div className="text-muted-foreground">P&L</div>
              <div className={`font-medium flex items-center space-x-1 ${
                position.pnl >= 0 ? 'text-green-600' : 'text-red-600'
              }`}>
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
          </div>
          
          <div className="mt-3 pt-3 border-t border-border">
            <div className="grid grid-cols-2 gap-4 text-xs text-muted-foreground">
              <div>
                Target: ${position.target_price.toFixed(4)}
              </div>
              <div>
                Stop Loss: ${position.stop_loss.toFixed(4)}
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

