import { storeToRefs } from 'pinia'
import { useAnalysisStore } from '@/stores/analysisStore'

export function useAnalysis() {
  const store = useAnalysisStore()
  const { currentAnalysis, progress, isAnalyzing, error } = storeToRefs(store)

  async function startAnalysis(file: File): Promise<void> {
    store.clearAnalysis()
    store.isAnalyzing = true
    void file
  }

  return { currentAnalysis, progress, isAnalyzing, error, startAnalysis, clearAnalysis: store.clearAnalysis }
}
