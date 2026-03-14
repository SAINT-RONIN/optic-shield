import { API_BASE } from '@/utils/constants'
import type { ApiResponse } from '@/types/api'
import type { AnalysisResult } from '@/types/analysis'

export async function uploadVideo(file: File): Promise<ApiResponse<{ videoId: string }>> {
  const formData = new FormData()
  formData.append('file', file)
  const response = await fetch(`${API_BASE}/analyze`, { method: 'POST', body: formData })
  return response.json() as Promise<ApiResponse<{ videoId: string }>>
}

export async function getAnalysis(videoId: string): Promise<ApiResponse<AnalysisResult>> {
  const response = await fetch(`${API_BASE}/analyze/${videoId}`)
  return response.json() as Promise<ApiResponse<AnalysisResult>>
}
