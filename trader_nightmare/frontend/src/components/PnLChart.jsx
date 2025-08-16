import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { format } from 'date-fns'

export function PnLChart({ data }) {
  const formatXAxis = (tickItem) => {
    return format(new Date(tickItem), 'HH:mm')
  }

  const formatTooltip = (value, name, props) => {
    if (name === 'cumulative_pnl') {
      return [`$${value.toFixed(2)}`, 'P&L']
    }
    return [value, name]
  }

  const formatTooltipLabel = (label) => {
    return format(new Date(label), 'MMM dd, HH:mm')
  }

  return (
    <div className="h-80">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
          <XAxis 
            dataKey="timestamp" 
            tickFormatter={formatXAxis}
            className="text-muted-foreground"
          />
          <YAxis 
            tickFormatter={(value) => `$${value}`}
            className="text-muted-foreground"
          />
          <Tooltip 
            formatter={formatTooltip}
            labelFormatter={formatTooltipLabel}
            contentStyle={{
              backgroundColor: 'hsl(var(--card))',
              border: '1px solid hsl(var(--border))',
              borderRadius: '6px',
              color: 'hsl(var(--card-foreground))'
            }}
          />
          <Line 
            type="monotone" 
            dataKey="cumulative_pnl" 
            stroke="hsl(var(--primary))" 
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 4, fill: 'hsl(var(--primary))' }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

