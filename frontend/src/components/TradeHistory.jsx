import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/Card'

export default function TradeHistory() {
  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Trade History</CardTitle>
      </CardHeader>
      <CardContent>
        {/* Здесь можешь выводить список сделок */}
        <p>No trades yet.</p>
      </CardContent>
      <CardFooter>
        <p className="text-sm text-gray-500">Updated just now</p>
      </CardFooter>
    </Card>
  )
}