import { createRoute } from '@tanstack/react-router'
import { rootRoute } from './__root'
import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Badge } from '@/components/ui/badge'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { 
  Code, 
  Lightbulb, 
  FileText, 
  Search, 
  Plus, 
  ExternalLink, 
  CheckCircle2,
  Clock,
  AlertCircle,
  Bot,
  Network,
  Zap
} from 'lucide-react'
import { useToast } from '@/hooks/use-toast'

export const researchRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/research',
  component: ResearchPage,
})

interface ResearchItem {
  id: string
  title: string
  type: 'paper' | 'library' | 'practice' | 'skill' | 'mcp' | 'agentic'
  category: string
  description: string
  url?: string
  tags: string[]
  status: 'reviewed' | 'in_progress' | 'pending' | 'applied'
  priority: 'low' | 'medium' | 'high' | 'critical'
  application_phase?: string
  segmentation?: string
  notes?: string
  added_at: string
  reviewed_at?: string
  applied_at?: string
  metadata?: Record<string, any>
}

const CATEGORIES = [
  'AI/ML',
  'LLM',
  'Agentic Systems',
  'MCP',
  'Vector Databases',
  'Embeddings',
  'Gematria',
  'Esoteric',
  'Mathematics',
  'Architecture',
  'Best Practices',
  'Tools',
  'Frameworks',
] as const

const TYPES = [
  { id: 'paper', label: 'Research Paper', icon: FileText },
  { id: 'library', label: 'Library', icon: Code },
  { id: 'practice', label: 'Best Practice', icon: Lightbulb },
  { id: 'skill', label: 'Claude Skill', icon: Bot },
  { id: 'mcp', label: 'MCP', icon: Network },
  { id: 'agentic', label: 'Agentic', icon: Zap },
] as const

const PHASES = [
  'phase1_basic',
  'phase2_deep',
  'phase3_advanced',
  'phase4_scale',
] as const

function ResearchPage() {
  const { toast } = useToast()
  const [searchQuery, setSearchQuery] = useState('')
  const [typeFilter, setTypeFilter] = useState<string>('all')
  const [categoryFilter, setCategoryFilter] = useState<string>('all')
  const [statusFilter, setStatusFilter] = useState<string>('all')
  const [isDialogOpen, setIsDialogOpen] = useState(false)
  const [editingItem, setEditingItem] = useState<ResearchItem | null>(null)
  
  const [items, setItems] = useState<ResearchItem[]>([
    // Example items
    {
      id: '1',
      title: 'LangGraph: Building Stateful, Multi-Actor Applications with LLMs',
      type: 'library',
      category: 'Agentic Systems',
      description: 'Framework for building stateful, multi-actor applications with LLMs',
      url: 'https://langchain-ai.github.io/langgraph/',
      tags: ['langgraph', 'llm', 'agents', 'stateful'],
      status: 'applied',
      priority: 'high',
      application_phase: 'phase1_basic',
      segmentation: 'Orchestration layer',
      notes: 'Currently used in orchestrator.py',
      added_at: new Date().toISOString(),
      applied_at: new Date().toISOString(),
    },
    {
      id: '2',
      title: 'Supabase: Open Source Firebase Alternative',
      type: 'library',
      category: 'Vector Databases',
      description: 'PostgreSQL database with vector extensions, real-time subscriptions',
      url: 'https://supabase.com/',
      tags: ['supabase', 'postgres', 'vector', 'realtime'],
      status: 'applied',
      priority: 'high',
      application_phase: 'phase1_basic',
      segmentation: 'Database layer',
      notes: 'Primary database for hunches, bookmarks, tasks',
      added_at: new Date().toISOString(),
      applied_at: new Date().toISOString(),
    },
    {
      id: '3',
      title: 'MCP (Model Context Protocol)',
      type: 'mcp',
      category: 'MCP',
      description: 'Protocol for connecting AI assistants to external data sources and tools',
      url: 'https://modelcontextprotocol.io/',
      tags: ['mcp', 'protocol', 'orchestration'],
      status: 'applied',
      priority: 'critical',
      application_phase: 'phase1_basic',
      segmentation: 'Core orchestration',
      notes: 'Used in orchestrator for agent coordination',
      added_at: new Date().toISOString(),
      applied_at: new Date().toISOString(),
    },
    {
      id: '4',
      title: 'Claude Skills',
      type: 'skill',
      category: 'AI/ML',
      description: 'Custom skills for Claude AI assistant',
      tags: ['claude', 'skills', 'ai'],
      status: 'in_progress',
      priority: 'high',
      application_phase: 'phase2_deep',
      segmentation: 'AI capabilities',
      notes: 'Developing custom skills for gematria and esoteric analysis',
      added_at: new Date().toISOString(),
    },
    {
      id: '5',
      title: 'StringZilla: Fast String Processing',
      type: 'library',
      category: 'Tools',
      description: 'Fast string processing library for embeddings and text analysis',
      url: 'https://github.com/ashvardanian/StringZilla',
      tags: ['stringzilla', 'performance', 'text'],
      status: 'pending',
      priority: 'medium',
      application_phase: 'phase2_deep',
      segmentation: 'Performance optimization',
      added_at: new Date().toISOString(),
    },
  ])

  const [formData, setFormData] = useState<{
    title: string
    type: ResearchItem['type']
    category: string
    description: string
    url: string
    tags: string[]
    status: ResearchItem['status']
    priority: ResearchItem['priority']
    application_phase: string
    segmentation: string
    notes: string
  }>({
    title: '',
    type: 'paper',
    category: '',
    description: '',
    url: '',
    tags: [],
    status: 'pending',
    priority: 'medium',
    application_phase: '',
    segmentation: '',
    notes: '',
  })
  const [tagInput, setTagInput] = useState('')

  const filteredItems = items.filter(item => {
    const matchesSearch = !searchQuery || 
      item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()))
    
    const matchesType = typeFilter === 'all' || item.type === typeFilter
    const matchesCategory = categoryFilter === 'all' || item.category === categoryFilter
    const matchesStatus = statusFilter === 'all' || item.status === statusFilter

    return matchesSearch && matchesType && matchesCategory && matchesStatus
  })

  const handleAddTag = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && tagInput.trim()) {
      e.preventDefault()
      setFormData({
        ...formData,
        tags: [...formData.tags, tagInput.trim()],
      })
      setTagInput('')
    }
  }

  const handleRemoveTag = (index: number) => {
    setFormData({
      ...formData,
      tags: formData.tags.filter((_, i) => i !== index),
    })
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    if (editingItem) {
      // Update existing item
      setItems(items.map(item => 
        item.id === editingItem.id 
          ? { ...item, ...formData, reviewed_at: formData.status === 'reviewed' ? new Date().toISOString() : item.reviewed_at }
          : item
      ))
      toast({
        title: 'Item updated',
        description: 'Research item has been updated successfully.',
      })
    } else {
      // Create new item
      const newItem: ResearchItem = {
        id: Date.now().toString(),
        ...formData,
        added_at: new Date().toISOString(),
        reviewed_at: formData.status === 'reviewed' ? new Date().toISOString() : undefined,
        applied_at: formData.status === 'applied' ? new Date().toISOString() : undefined,
      }
      setItems([...items, newItem])
      toast({
        title: 'Item added',
        description: 'Research item has been added successfully.',
      })
    }
    
    setIsDialogOpen(false)
    setEditingItem(null)
    setFormData({
      title: '',
      type: 'paper',
      category: '',
      description: '',
      url: '',
      tags: [],
      status: 'pending',
      priority: 'medium',
      application_phase: '',
      segmentation: '',
      notes: '',
    })
  }

  const handleEdit = (item: ResearchItem) => {
    setEditingItem(item)
    setFormData({
      title: item.title,
      type: item.type,
      category: item.category,
      description: item.description,
      url: item.url || '',
      tags: item.tags,
      status: item.status,
      priority: item.priority,
      application_phase: item.application_phase || '',
      segmentation: item.segmentation || '',
      notes: item.notes || '',
    })
    setIsDialogOpen(true)
  }

  const handleStatusChange = (itemId: string, newStatus: ResearchItem['status']) => {
    setItems(items.map(item => {
      if (item.id === itemId) {
        return {
          ...item,
          status: newStatus,
          reviewed_at: newStatus === 'reviewed' ? new Date().toISOString() : item.reviewed_at,
          applied_at: newStatus === 'applied' ? new Date().toISOString() : item.applied_at,
        }
      }
      return item
    }))
    toast({
      title: 'Status updated',
      description: 'Item status has been updated.',
    })
  }

  const getStatusIcon = (status: ResearchItem['status']) => {
    if (status === 'applied') {
      return <CheckCircle2 className="h-4 w-4 text-green-600" />
    }
    if (status === 'reviewed') {
      return <CheckCircle2 className="h-4 w-4 text-blue-600" />
    }
    if (status === 'in_progress') {
      return <Clock className="h-4 w-4 text-yellow-600" />
    }
    return <AlertCircle className="h-4 w-4 text-gray-600" />
  }

  const getTypeIcon = (type: ResearchItem['type']) => {
    const typeConfig = TYPES.find(t => t.id === type)
    if (typeConfig) {
      const Icon = typeConfig.icon
      return <Icon className="h-4 w-4" />
    }
    return <FileText className="h-4 w-4" />
  }

  const stats = {
    total: items.length,
    applied: items.filter(i => i.status === 'applied').length,
    reviewed: items.filter(i => i.status === 'reviewed').length,
    in_progress: items.filter(i => i.status === 'in_progress').length,
    pending: items.filter(i => i.status === 'pending').length,
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold">Research & Knowledge Base</h1>
        <p className="text-muted-foreground mt-2">
          Review, explore, and log research papers, libraries, best practices, Claude skills, MCP, and agentic work
        </p>
      </div>

      {/* Statistics */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <Card>
          <CardContent className="pt-6">
            <div className="text-2xl font-bold">{stats.total}</div>
            <div className="text-sm text-muted-foreground">Total Items</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="text-2xl font-bold text-green-600">{stats.applied}</div>
            <div className="text-sm text-muted-foreground">Applied</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="text-2xl font-bold text-blue-600">{stats.reviewed}</div>
            <div className="text-sm text-muted-foreground">Reviewed</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="text-2xl font-bold text-yellow-600">{stats.in_progress}</div>
            <div className="text-sm text-muted-foreground">In Progress</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="text-2xl font-bold text-gray-600">{stats.pending}</div>
            <div className="text-sm text-muted-foreground">Pending</div>
          </CardContent>
        </Card>
      </div>

      {/* Filters and Search */}
      <Card>
        <CardHeader>
          <CardTitle>Filters & Search</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="space-y-2">
              <Label>Search</Label>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search items..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            <div className="space-y-2">
              <Label>Type</Label>
              <Select value={typeFilter} onValueChange={setTypeFilter}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Types</SelectItem>
                  {TYPES.map(type => (
                    <SelectItem key={type.id} value={type.id}>
                      {type.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label>Category</Label>
              <Select value={categoryFilter} onValueChange={setCategoryFilter}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Categories</SelectItem>
                  {CATEGORIES.map(cat => (
                    <SelectItem key={cat} value={cat}>
                      {cat}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label>Status</Label>
              <Select value={statusFilter} onValueChange={setStatusFilter}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Statuses</SelectItem>
                  <SelectItem value="applied">Applied</SelectItem>
                  <SelectItem value="reviewed">Reviewed</SelectItem>
                  <SelectItem value="in_progress">In Progress</SelectItem>
                  <SelectItem value="pending">Pending</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Main Content */}
      <Tabs defaultValue="grid" className="w-full">
        <TabsList>
          <TabsTrigger value="grid">Grid View</TabsTrigger>
          <TabsTrigger value="list">List View</TabsTrigger>
          <TabsTrigger value="by-phase">By Phase</TabsTrigger>
          <TabsTrigger value="by-segmentation">By Segmentation</TabsTrigger>
        </TabsList>

        <TabsContent value="grid" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredItems.map(item => (
              <Card key={item.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex items-center gap-2">
                      {getTypeIcon(item.type)}
                      <CardTitle className="text-lg">{item.title}</CardTitle>
                    </div>
                    {getStatusIcon(item.status)}
                  </div>
                  <CardDescription className="mt-2">{item.description}</CardDescription>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex items-center gap-2">
                    <Badge variant="outline">{item.category}</Badge>
                    <Badge variant={item.priority === 'critical' ? 'destructive' : 'secondary'}>
                      {item.priority}
                    </Badge>
                  </div>
                  
                  {item.tags.length > 0 && (
                    <div className="flex flex-wrap gap-1">
                      {item.tags.slice(0, 3).map((tag, idx) => (
                        <Badge key={idx} variant="outline" className="text-xs">
                          {tag}
                        </Badge>
                      ))}
                      {item.tags.length > 3 && (
                        <Badge variant="outline" className="text-xs">
                          +{item.tags.length - 3}
                        </Badge>
                      )}
                    </div>
                  )}

                  {item.application_phase && (
                    <div className="text-sm text-muted-foreground">
                      Phase: {item.application_phase.replace('phase', 'P').replace('_', ' ')}
                    </div>
                  )}

                  {item.segmentation && (
                    <div className="text-sm text-muted-foreground">
                      Segment: {item.segmentation}
                    </div>
                  )}

                  {item.url && (
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => window.open(item.url, '_blank')}
                      className="w-full"
                    >
                      <ExternalLink className="h-4 w-4 mr-2" />
                      Open Link
                    </Button>
                  )}

                  <div className="flex gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleEdit(item)}
                      className="flex-1"
                    >
                      Edit
                    </Button>
                    <Select
                      value={item.status}
                      onValueChange={(value) => handleStatusChange(item.id, value as ResearchItem['status'])}
                    >
                      <SelectTrigger className="flex-1">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="pending">Pending</SelectItem>
                        <SelectItem value="in_progress">In Progress</SelectItem>
                        <SelectItem value="reviewed">Reviewed</SelectItem>
                        <SelectItem value="applied">Applied</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="list" className="space-y-4">
          <div className="space-y-2">
            {filteredItems.map(item => (
              <Card key={item.id}>
                <CardContent className="pt-6">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        {getTypeIcon(item.type)}
                        <h3 className="font-semibold">{item.title}</h3>
                        {getStatusIcon(item.status)}
                      </div>
                      <p className="text-sm text-muted-foreground mb-2">{item.description}</p>
                      <div className="flex items-center gap-2 flex-wrap">
                        <Badge variant="outline">{item.category}</Badge>
                        {item.application_phase && (
                          <Badge variant="outline">
                            {item.application_phase.replace('phase', 'P').replace('_', ' ')}
                          </Badge>
                        )}
                        {item.segmentation && (
                          <Badge variant="outline">{item.segmentation}</Badge>
                        )}
                        {item.tags.map((tag, idx) => (
                          <Badge key={idx} variant="outline" className="text-xs">
                            {tag}
                          </Badge>
                        ))}
                      </div>
                      {item.notes && (
                        <div className="mt-2 text-sm text-muted-foreground">
                          <strong>Notes:</strong> {item.notes}
                        </div>
                      )}
                    </div>
                    <div className="flex flex-col gap-2 ml-4">
                      {item.url && (
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => window.open(item.url, '_blank')}
                        >
                          <ExternalLink className="h-4 w-4" />
                        </Button>
                      )}
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleEdit(item)}
                      >
                        Edit
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="by-phase" className="space-y-4">
          {PHASES.map(phase => {
            const phaseItems = filteredItems.filter(item => item.application_phase === phase)
            if (phaseItems.length === 0) return null
            
            return (
              <Card key={phase}>
                <CardHeader>
                  <CardTitle>{phase.replace('phase', 'Phase ').replace('_', ': ')}</CardTitle>
                  <CardDescription>{phaseItems.length} item(s)</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {phaseItems.map(item => (
                      <Card key={item.id} className="hover:shadow-lg transition-shadow">
                        <CardHeader>
                          <div className="flex items-start justify-between">
                            <CardTitle className="text-base">{item.title}</CardTitle>
                            {getStatusIcon(item.status)}
                          </div>
                        </CardHeader>
                        <CardContent>
                          <div className="space-y-2">
                            <Badge variant="outline">{item.category}</Badge>
                            {item.segmentation && (
                              <div className="text-sm text-muted-foreground">
                                Segment: {item.segmentation}
                              </div>
                            )}
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => handleEdit(item)}
                              className="w-full"
                            >
                              Edit
                            </Button>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )
          })}
        </TabsContent>

        <TabsContent value="by-segmentation" className="space-y-4">
          {Array.from(new Set(filteredItems.map(item => item.segmentation).filter(Boolean))).map(segment => {
            const segmentItems = filteredItems.filter(item => item.segmentation === segment)
            
            return (
              <Card key={segment}>
                <CardHeader>
                  <CardTitle>{segment}</CardTitle>
                  <CardDescription>{segmentItems.length} item(s)</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {segmentItems.map(item => (
                      <Card key={item.id} className="hover:shadow-lg transition-shadow">
                        <CardHeader>
                          <div className="flex items-start justify-between">
                            <CardTitle className="text-base">{item.title}</CardTitle>
                            {getStatusIcon(item.status)}
                          </div>
                        </CardHeader>
                        <CardContent>
                          <div className="space-y-2">
                            <Badge variant="outline">{item.category}</Badge>
                            {item.application_phase && (
                              <div className="text-sm text-muted-foreground">
                                Phase: {item.application_phase.replace('phase', 'P').replace('_', ' ')}
                              </div>
                            )}
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => handleEdit(item)}
                              className="w-full"
                            >
                              Edit
                            </Button>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )
          })}
        </TabsContent>
      </Tabs>

      {/* Add Button */}
      <div className="flex justify-end">
        <Button onClick={() => {
          setEditingItem(null)
          setFormData({
            title: '',
            type: 'paper',
            category: '',
            description: '',
            url: '',
            tags: [],
            status: 'pending',
            priority: 'medium',
            application_phase: '',
            segmentation: '',
            notes: '',
          })
          setIsDialogOpen(true)
        }}>
          <Plus className="h-4 w-4 mr-2" />
          Add Research Item
        </Button>
      </div>

      {/* Add/Edit Dialog */}
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>{editingItem ? 'Edit Research Item' : 'Add Research Item'}</DialogTitle>
            <DialogDescription>
              {editingItem ? 'Update the research item details.' : 'Add a new research paper, library, best practice, skill, MCP, or agentic work.'}
            </DialogDescription>
          </DialogHeader>
          <form onSubmit={handleSubmit}>
            <div className="space-y-4 py-4">
              <div className="space-y-2">
                <Label htmlFor="title">Title *</Label>
                <Input
                  id="title"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="type">Type *</Label>
                  <Select
                    value={formData.type}
                    onValueChange={(value) => setFormData({ ...formData, type: value as ResearchItem['type'] })}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {TYPES.map(type => (
                        <SelectItem key={type.id} value={type.id}>
                          {type.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="category">Category *</Label>
                  <Select
                    value={formData.category}
                    onValueChange={(value) => setFormData({ ...formData, category: value })}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {CATEGORIES.map(cat => (
                        <SelectItem key={cat} value={cat}>
                          {cat}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="description">Description *</Label>
                <Textarea
                  id="description"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  required
                  rows={3}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="url">URL</Label>
                <Input
                  id="url"
                  type="url"
                  value={formData.url}
                  onChange={(e) => setFormData({ ...formData, url: e.target.value })}
                  placeholder="https://example.com"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="status">Status</Label>
                  <Select
                    value={formData.status}
                    onValueChange={(value) => setFormData({ ...formData, status: value as ResearchItem['status'] })}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="pending">Pending</SelectItem>
                      <SelectItem value="in_progress">In Progress</SelectItem>
                      <SelectItem value="reviewed">Reviewed</SelectItem>
                      <SelectItem value="applied">Applied</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="priority">Priority</Label>
                  <Select
                    value={formData.priority}
                    onValueChange={(value) => setFormData({ ...formData, priority: value as ResearchItem['priority'] })}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="low">Low</SelectItem>
                      <SelectItem value="medium">Medium</SelectItem>
                      <SelectItem value="high">High</SelectItem>
                      <SelectItem value="critical">Critical</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="application_phase">Application Phase</Label>
                  <Select
                    value={formData.application_phase}
                    onValueChange={(value) => setFormData({ ...formData, application_phase: value })}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="">None</SelectItem>
                      {PHASES.map(phase => (
                        <SelectItem key={phase} value={phase}>
                          {phase.replace('phase', 'Phase ').replace('_', ': ')}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="segmentation">Segmentation</Label>
                  <Input
                    id="segmentation"
                    value={formData.segmentation}
                    onChange={(e) => setFormData({ ...formData, segmentation: e.target.value })}
                    placeholder="e.g., Orchestration layer, Database layer"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="tags">Tags</Label>
                <Input
                  id="tags"
                  value={tagInput}
                  onChange={(e) => setTagInput(e.target.value)}
                  onKeyDown={handleAddTag}
                  placeholder="Add tag and press Enter"
                />
                {formData.tags.length > 0 && (
                  <div className="flex flex-wrap gap-2 mt-2">
                    {formData.tags.map((tag, index) => (
                      <Badge key={index} variant="outline" className="flex items-center gap-1">
                        {tag}
                        <button
                          type="button"
                          onClick={() => handleRemoveTag(index)}
                          className="ml-1 hover:text-destructive"
                        >
                          ×
                        </button>
                      </Badge>
                    ))}
                  </div>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="notes">Notes</Label>
                <Textarea
                  id="notes"
                  value={formData.notes}
                  onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                  rows={4}
                  placeholder="Additional notes, implementation details, etc."
                />
              </div>
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => setIsDialogOpen(false)}>
                Cancel
              </Button>
              <Button type="submit">
                {editingItem ? 'Update' : 'Add'}
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  )
}

