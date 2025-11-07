import { useStatistics } from '@/lib/queries'
import { Card, CardContent } from '@/components/ui/card'

export function StatisticsPanel() {
  const { data: stats, isLoading } = useStatistics()

  if (isLoading) {
    return (
      <Card className="bg-white shadow-lg">
        <CardContent className="p-6">
          <div className="text-muted-foreground">Loading statistics...</div>
        </CardContent>
      </Card>
    )
  }

  if (!stats) return null

  return (
    <Card className="bg-white shadow-lg">
      <CardContent className="p-6">
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          <div className="text-center">
            <div className="text-3xl font-bold text-primary">{stats.total}</div>
            <div className="text-sm text-muted-foreground mt-1">Total Tasks</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-600">{stats.by_status?.pending || 0}</div>
            <div className="text-sm text-muted-foreground mt-1">Pending</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-yellow-600">{stats.by_status?.in_progress || 0}</div>
            <div className="text-sm text-muted-foreground mt-1">In Progress</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600">{stats.by_status?.completed || 0}</div>
            <div className="text-sm text-muted-foreground mt-1">Completed</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-purple-600">${(stats.total_cost || 0).toFixed(2)}</div>
            <div className="text-sm text-muted-foreground mt-1">Total Cost</div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

