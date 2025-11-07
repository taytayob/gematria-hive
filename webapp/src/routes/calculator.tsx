import { createRoute } from '@tanstack/react-router'
import { rootRoute } from './__root'
import { useState, useEffect, useCallback } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Badge } from '@/components/ui/badge'
import { Calculator as CalcIcon, Zap } from 'lucide-react'
import { getGematriaCalculator, type GematriaResults } from '@/lib/gematria'
import { calculateWithDatabase, type DatabaseCalculationResult } from '@/lib/database-calculations'
import { Toggle } from '@/components/ui/toggle'

export const calculatorRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/calculator',
  component: CalculatorPage,
})

const METHOD_NAMES: Record<keyof GematriaResults, string> = {
  jewish: 'Jewish Gematria',
  english: 'English Gematria',
  simple: 'Simple Gematria',
  latin: 'Latin Gematria',
  greek: 'Greek Gematria',
  hebrew_full: 'Hebrew Full',
  hebrew_musafi: 'Hebrew Musafi',
  hebrew_katan: 'Hebrew Katan (Reduced)',
  hebrew_ordinal: 'Hebrew Ordinal',
  hebrew_atbash: 'Hebrew Atbash',
  hebrew_kidmi: 'Hebrew Kidmi',
  hebrew_perati: 'Hebrew Perati',
  hebrew_shemi: 'Hebrew Shemi',
}

function CalculatorPage() {
  const [input, setInput] = useState('')
  const [results, setResults] = useState<GematriaResults | null>(null)
  const [databaseResults, setDatabaseResults] = useState<DatabaseCalculationResult | null>(null)
  const [autoCalculate, setAutoCalculate] = useState(true)
  const [useDatabase, setUseDatabase] = useState(false)
  const [useAgents, setUseAgents] = useState(false)
  const [useInference, setUseInference] = useState(false)
  const [useTheorems, setUseTheorems] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const calculator = getGematriaCalculator()

  const handleCalculate = useCallback(async () => {
    if (!input.trim()) {
      setResults(null)
      setDatabaseResults(null)
      return
    }

    // Always calculate frontend first (instant)
    const calculated = calculator.calculateAll(input)
    setResults(calculated)

    // If any advanced features are enabled, use database integration
    if (useDatabase || useAgents || useInference || useTheorems) {
      setIsProcessing(true)
      try {
        const dbResult = await calculateWithDatabase({
          text: input,
          use_database: useDatabase,
          use_agents: useAgents,
          use_inference: useInference,
          use_theorems: useTheorems,
        })
        setDatabaseResults(dbResult)
      } catch (error) {
        console.error('Database calculation failed:', error)
        // Frontend results still work
      } finally {
        setIsProcessing(false)
      }
    } else {
      setDatabaseResults(null)
    }
  }, [input, calculator, useDatabase, useAgents, useInference, useTheorems])

  useEffect(() => {
    if (autoCalculate && input.trim()) {
      handleCalculate()
    }
  }, [input, autoCalculate, handleCalculate])

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Gematria Calculator</h1>
        <p className="text-muted-foreground mt-2">
          Calculate gematria values using all 13 methods - 100% frontend, no backend needed!
        </p>
        <Badge variant="outline" className="mt-2">
          <Zap className="h-3 w-3 mr-1" />
          Client-side calculations
        </Badge>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Section */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <CalcIcon className="h-5 w-5" />
              Input Text
            </CardTitle>
            <CardDescription>
              Enter text to calculate gematria values using all methods
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="input">Text</Label>
              <Input
                id="input"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Enter text here... (e.g., LOVE, Hebrew text, etc.)"
                className="text-lg"
              />
            </div>
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  id="auto-calc"
                  checked={autoCalculate}
                  onChange={(e) => setAutoCalculate(e.target.checked)}
                  className="rounded"
                />
                <Label htmlFor="auto-calc" className="text-sm cursor-pointer">
                  Auto-calculate on input
                </Label>
              </div>
              
              {/* Advanced Options */}
              <div className="border-t pt-3 space-y-2">
                <Label className="text-sm font-semibold">Advanced Processing (Optional)</Label>
                <div className="grid grid-cols-2 gap-2">
                  <div className="flex items-center gap-2">
                    <input
                      type="checkbox"
                      id="use-database"
                      checked={useDatabase}
                      onChange={(e) => setUseDatabase(e.target.checked)}
                      className="rounded"
                    />
                    <Label htmlFor="use-database" className="text-xs cursor-pointer">
                      Database (Related Terms)
                    </Label>
                  </div>
                  <div className="flex items-center gap-2">
                    <input
                      type="checkbox"
                      id="use-agents"
                      checked={useAgents}
                      onChange={(e) => setUseAgents(e.target.checked)}
                      className="rounded"
                    />
                    <Label htmlFor="use-agents" className="text-xs cursor-pointer">
                      MCP/Agents
                    </Label>
                  </div>
                  <div className="flex items-center gap-2">
                    <input
                      type="checkbox"
                      id="use-inference"
                      checked={useInference}
                      onChange={(e) => setUseInference(e.target.checked)}
                      className="rounded"
                    />
                    <Label htmlFor="use-inference" className="text-xs cursor-pointer">
                      Inference
                    </Label>
                  </div>
                  <div className="flex items-center gap-2">
                    <input
                      type="checkbox"
                      id="use-theorems"
                      checked={useTheorems}
                      onChange={(e) => setUseTheorems(e.target.checked)}
                      className="rounded"
                    />
                    <Label htmlFor="use-theorems" className="text-xs cursor-pointer">
                      Theorems/Math
                    </Label>
                  </div>
                </div>
                {isProcessing && (
                  <div className="text-xs text-muted-foreground">
                    Processing with database/agents...
                  </div>
                )}
              </div>
            </div>
            {!autoCalculate && (
              <Button onClick={handleCalculate} className="w-full">
                Calculate All Methods
              </Button>
            )}
          </CardContent>
        </Card>

        {/* Results Summary */}
        {results && (
          <Card>
            <CardHeader>
              <CardTitle>Quick Results</CardTitle>
              <CardDescription>Most common methods</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="grid grid-cols-2 gap-3">
                <div className="p-4 border rounded-lg">
                  <div className="text-xs text-muted-foreground mb-1">English</div>
                  <div className="text-2xl font-bold text-primary">{results.english}</div>
                </div>
                <div className="p-4 border rounded-lg">
                  <div className="text-xs text-muted-foreground mb-1">Simple</div>
                  <div className="text-2xl font-bold text-blue-600">{results.simple}</div>
                </div>
                <div className="p-4 border rounded-lg">
                  <div className="text-xs text-muted-foreground mb-1">Jewish</div>
                  <div className="text-2xl font-bold text-green-600">{results.jewish}</div>
                </div>
                <div className="p-4 border rounded-lg">
                  <div className="text-xs text-muted-foreground mb-1">Hebrew Katan</div>
                  <div className="text-2xl font-bold text-purple-600">{results.hebrew_katan}</div>
                </div>
              </div>
            </CardContent>
          </Card>
        )}
      </div>

      {/* Database/Agent Results */}
      {databaseResults && (databaseResults.database_results || databaseResults.agent_results || databaseResults.inference_results || databaseResults.theorem_results) && (
        <Card>
          <CardHeader>
            <CardTitle>Advanced Processing Results</CardTitle>
            <CardDescription>Database, agents, inference, and theorem results</CardDescription>
          </CardHeader>
          <CardContent>
            <Tabs defaultValue="database" className="w-full">
              <TabsList>
                {databaseResults.database_results && <TabsTrigger value="database">Database</TabsTrigger>}
                {databaseResults.agent_results && <TabsTrigger value="agents">Agents/MCP</TabsTrigger>}
                {databaseResults.inference_results && <TabsTrigger value="inference">Inference</TabsTrigger>}
                {databaseResults.theorem_results && <TabsTrigger value="theorems">Theorems</TabsTrigger>}
              </TabsList>
              
              {databaseResults.database_results && (
                <TabsContent value="database" className="space-y-4 mt-4">
                  {databaseResults.database_results.related_terms && databaseResults.database_results.related_terms.length > 0 && (
                    <div>
                      <h4 className="font-semibold mb-2">Related Terms</h4>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                        {databaseResults.database_results.related_terms.map((term, idx) => (
                          <div key={idx} className="p-3 border rounded-lg">
                            <div className="font-medium">{term.word}</div>
                            <div className="text-sm text-muted-foreground">
                              {term.method}: {term.value}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </TabsContent>
              )}
              
              {databaseResults.agent_results && (
                <TabsContent value="agents" className="space-y-4 mt-4">
                  <div className="text-sm text-muted-foreground">
                    Agent processing results from MCP orchestrator
                  </div>
                  {databaseResults.agent_results.pattern_analysis && (
                    <div>
                      <h4 className="font-semibold mb-2">Pattern Analysis</h4>
                      <pre className="text-xs bg-muted p-3 rounded overflow-auto">
                        {JSON.stringify(databaseResults.agent_results.pattern_analysis, null, 2)}
                      </pre>
                    </div>
                  )}
                </TabsContent>
              )}
              
              {databaseResults.inference_results && (
                <TabsContent value="inference" className="space-y-4 mt-4">
                  {databaseResults.inference_results.hunches && databaseResults.inference_results.hunches.length > 0 && (
                    <div>
                      <h4 className="font-semibold mb-2">Inference Hunches</h4>
                      <div className="space-y-2">
                        {databaseResults.inference_results.hunches.map((hunch, idx) => (
                          <div key={idx} className="p-3 border rounded-lg">
                            <div className="font-medium">{hunch.content}</div>
                            <div className="text-xs text-muted-foreground">
                              Confidence: {(hunch.confidence * 100).toFixed(1)}%
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </TabsContent>
              )}
              
              {databaseResults.theorem_results && (
                <TabsContent value="theorems" className="space-y-4 mt-4">
                  {databaseResults.theorem_results.proofs && databaseResults.theorem_results.proofs.length > 0 && (
                    <div>
                      <h4 className="font-semibold mb-2">Mathematical Proofs</h4>
                      <div className="space-y-2">
                        {databaseResults.theorem_results.proofs.map((proof, idx) => (
                          <div key={idx} className="p-3 border rounded-lg">
                            <div className="font-medium">{proof.theorem}</div>
                            <div className="text-sm text-muted-foreground mt-1">{proof.proof}</div>
                            <div className="text-xs text-muted-foreground mt-1">
                              Accuracy: {(proof.accuracy * 100).toFixed(1)}%
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </TabsContent>
              )}
            </Tabs>
          </CardContent>
        </Card>
      )}

      {/* All Results */}
      {results && (
        <Card>
          <CardHeader>
            <CardTitle>All Calculation Methods</CardTitle>
            <CardDescription>Complete gematria results for: "{input}"</CardDescription>
          </CardHeader>
          <CardContent>
            <Tabs defaultValue="standard" className="w-full">
              <TabsList className="grid w-full grid-cols-3">
                <TabsTrigger value="standard">Standard Methods</TabsTrigger>
                <TabsTrigger value="hebrew">Hebrew Variants</TabsTrigger>
                <TabsTrigger value="all">All Methods</TabsTrigger>
              </TabsList>
              
              <TabsContent value="standard" className="space-y-4 mt-4">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {(['english', 'simple', 'jewish', 'latin', 'greek'] as const).map((method) => (
                    <div key={method} className="p-4 border rounded-lg">
                      <div className="text-sm text-muted-foreground mb-1">{METHOD_NAMES[method]}</div>
                      <div className="text-3xl font-bold text-primary">{results[method]}</div>
                    </div>
                  ))}
                </div>
              </TabsContent>

              <TabsContent value="hebrew" className="space-y-4 mt-4">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {(['hebrew_full', 'hebrew_musafi', 'hebrew_katan', 'hebrew_ordinal', 'hebrew_atbash', 'hebrew_kidmi', 'hebrew_perati', 'hebrew_shemi'] as const).map((method) => (
                    <div key={method} className="p-4 border rounded-lg">
                      <div className="text-sm text-muted-foreground mb-1">{METHOD_NAMES[method]}</div>
                      <div className="text-3xl font-bold text-purple-600">{results[method]}</div>
                    </div>
                  ))}
                </div>
              </TabsContent>

              <TabsContent value="all" className="space-y-4 mt-4">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {(Object.keys(METHOD_NAMES) as Array<keyof GematriaResults>).map((method) => (
                    <div key={method} className="p-4 border rounded-lg">
                      <div className="text-sm text-muted-foreground mb-1">{METHOD_NAMES[method]}</div>
                      <div className="text-3xl font-bold text-primary">{results[method]}</div>
                    </div>
                  ))}
                </div>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>
      )}

      {/* Information Card */}
      <Card>
        <CardHeader>
          <CardTitle>About Gematria</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3 text-sm text-muted-foreground">
          <p>
            <strong>All calculations happen in your browser</strong> - no backend server needed!
            This calculator implements all 13 gematria methods based on exact gematrix.org algorithms.
          </p>
          <div className="space-y-2">
            <p><strong>Standard Methods:</strong></p>
            <ul className="list-disc list-inside space-y-1 ml-4">
              <li><strong>English/Simple:</strong> A=1, B=2, ..., Z=26</li>
              <li><strong>Jewish:</strong> Hebrew letter values (א=1, ב=2, etc.)</li>
              <li><strong>Latin:</strong> Qabala Simplex (23-letter alphabet)</li>
              <li><strong>Greek:</strong> Classical Greek alphabet values</li>
            </ul>
            <p className="mt-3"><strong>Hebrew Variants:</strong></p>
            <ul className="list-disc list-inside space-y-1 ml-4">
              <li><strong>Full:</strong> Same as Jewish</li>
              <li><strong>Musafi:</strong> Base + (letter_count × 1000)</li>
              <li><strong>Katan:</strong> Reduced to single digit (1-9)</li>
              <li><strong>Ordinal:</strong> Position in alphabet</li>
              <li><strong>Atbash:</strong> Reversed alphabet mapping</li>
              <li><strong>Kidmi:</strong> Cumulative sum</li>
              <li><strong>Perati:</strong> Product of values</li>
              <li><strong>Shemi:</strong> Full letter name values</li>
            </ul>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}


