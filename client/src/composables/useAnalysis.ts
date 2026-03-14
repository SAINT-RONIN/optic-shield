import { ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useAnalysisStore } from '@/stores/analysisStore'
import { uploadVideo, getAnalysis } from '@/services/analysisService'
import { submitUrl } from '@/services/youtubeService'
import type { YouTubeVideoInfo } from '@/services/youtubeService'
import { socketService } from '@/services/socketService'
import { transformKeys } from '@/utils/caseTransform'
import type { AnalysisProgress } from '@/types/analysis'
import { useApiKey } from './useApiKey'

export function useAnalysis() {
  const store = useAnalysisStore()
  const { currentAnalysis, progress, isAnalyzing, error } = storeToRefs(store)
  const { apiKey } = useApiKey()
  const youtubeInfo = ref<YouTubeVideoInfo | null>(null)

  async function startAnalysis(file: File): Promise<void> {
    store.clearAnalysis()
    store.isAnalyzing = true

    try {
      const uploadResponse = await uploadVideo(file, apiKey.value || undefined)
      if (!uploadResponse.success || !uploadResponse.data) {
        store.setError(uploadResponse.error ?? 'Upload failed')
        return
      }

      const videoId = uploadResponse.data.videoId
      connectProgress(videoId)
    } catch {
      store.setError('Failed to start analysis')
    }
  }

  function connectProgress(videoId: string): void {
    socketService.disconnect()
    const wsUrl = `ws://${window.location.hostname}:8000/ws/${videoId}`
    socketService.connect(wsUrl)
    socketService.onProgress((raw) => {
      const p = transformKeys<AnalysisProgress>(raw)
      store.setProgress(p)
      if (p.stage === 'Complete') {
        fetchResult(videoId)
        socketService.disconnect()
      }
    })
  }

  async function fetchResult(videoId: string): Promise<void> {
    try {
      const response = await getAnalysis(videoId)
      if (response.success && response.data) {
        store.setAnalysis(response.data)
      } else {
        store.setError(response.error ?? 'Failed to fetch results')
      }
    } catch {
      store.setError('Failed to fetch analysis results')
    }
  }

  async function startYoutubeAnalysis(url: string): Promise<void> {
    store.clearAnalysis()
    youtubeInfo.value = null
    store.isAnalyzing = true

    try {
      const response = await submitUrl(url, apiKey.value || undefined)
      if (!response.success || !response.data) {
        store.setError(response.error ?? 'YouTube download failed')
        return
      }

      youtubeInfo.value = response.data.metadata
      const videoId = response.data.videoId
      connectProgress(videoId)
    } catch {
      store.setError('Failed to start YouTube analysis')
    }
  }

  return {
    currentAnalysis, progress, isAnalyzing, error, youtubeInfo,
    startAnalysis, startYoutubeAnalysis, clearAnalysis: store.clearAnalysis,
  }
}
