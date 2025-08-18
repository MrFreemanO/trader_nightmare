// frontend/src/components/Dashboard.jsx
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/Card'

export default function Dashboard() {
  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Dashboard</CardTitle>
      </CardHeader>
      <CardContent>
        <p>Dashboard content…</p>
      </CardContent>
      <CardFooter>
        <p className="text-sm text-gray-500">Updated just now</p>
      </CardFooter>
    </Card>
  )
}