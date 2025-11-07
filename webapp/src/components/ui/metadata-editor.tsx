import * as React from "react"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Plus, X } from "lucide-react"

interface MetadataEditorProps {
  value: Record<string, any>
  onChange: (value: Record<string, any>) => void
}

export function MetadataEditor({ value, onChange }: MetadataEditorProps) {
  const [entries, setEntries] = React.useState<Array<{ key: string; val: string }>>(() => {
    return Object.entries(value || {}).map(([k, v]) => ({
      key: k,
      val: typeof v === 'string' ? v : JSON.stringify(v),
    }))
  })

  React.useEffect(() => {
    const newEntries = Object.entries(value || {}).map(([k, v]) => ({
      key: k,
      val: typeof v === 'string' ? v : JSON.stringify(v),
    }))
    setEntries(newEntries)
  }, [value])

  const handleAdd = () => {
    setEntries([...entries, { key: '', val: '' }])
  }

  const handleRemove = (index: number) => {
    const newEntries = entries.filter((_, i) => i !== index)
    setEntries(newEntries)
    updateMetadata(newEntries)
  }

  const handleChange = (index: number, field: 'key' | 'val', newValue: string) => {
    const newEntries = [...entries]
    newEntries[index][field] = newValue
    setEntries(newEntries)
    updateMetadata(newEntries)
  }

  const updateMetadata = (newEntries: Array<{ key: string; val: string }>) => {
    const metadata: Record<string, any> = {}
    newEntries.forEach(({ key, val }) => {
      if (key.trim()) {
        try {
          metadata[key] = JSON.parse(val)
        } catch {
          metadata[key] = val
        }
      }
    })
    onChange(metadata)
  }

  return (
    <div className="space-y-2">
      <Label>Metadata (JSON)</Label>
      <div className="space-y-2">
        {entries.map((entry, index) => (
          <div key={index} className="flex gap-2">
            <input
              type="text"
              value={entry.key}
              onChange={(e) => handleChange(index, 'key', e.target.value)}
              placeholder="Key"
              className="flex-1 px-3 py-2 text-sm border rounded-md"
            />
            <input
              type="text"
              value={entry.val}
              onChange={(e) => handleChange(index, 'val', e.target.value)}
              placeholder="Value (JSON)"
              className="flex-1 px-3 py-2 text-sm border rounded-md"
            />
            <Button
              type="button"
              variant="ghost"
              size="icon"
              onClick={() => handleRemove(index)}
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
        ))}
        <Button
          type="button"
          variant="outline"
          size="sm"
          onClick={handleAdd}
          className="w-full"
        >
          <Plus className="h-4 w-4 mr-2" />
          Add Metadata Entry
        </Button>
      </div>
    </div>
  )
}
