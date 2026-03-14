import { ref } from 'vue'
import { defineStore } from 'pinia'
import type { AnalysisResult, AnalysisProgress } from '@/types/analysis'

export const useAnalysisStore = defineStore('analysis', () => {
  const currentAnalysis = ref<AnalysisResult | null>(null)
  const progress = ref<AnalysisProgress | null>(null)
  const isAnalyzing = ref(false)
  const error = ref<string | null>(null)

  function setAnalysis(result: AnalysisResult): void {
    currentAnalysis.value = result
    isAnalyzing.value = false
    progress.value = null
  }

  function setProgress(p: AnalysisProgress): void {
    progress.value = p
  }

  function clearAnalysis(): void {
    currentAnalysis.value = null
    progress.value = null
    isAnalyzing.value = false
    error.value = null
  }

  function setError(msg: string): void {
    error.value = msg
    isAnalyzing.value = false
  }

  return { currentAnalysis, progress, isAnalyzing, error, setAnalysis, setProgress, clearAnalysis, setError }
})
