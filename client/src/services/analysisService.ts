import { API_BASE } from '@/utils/constants'
import type { ApiResponse } from '@/types/api'
import type { AnalysisResult } from '@/types/analysis'
import { transformKeys } from '@/utils/caseTransform'

export async function uploadVideo(file: File): Promise<ApiResponse<{ videoId: string; filename: string }>> {
  const formData = new FormData()
  formData.append('file', file)
  const response = await fetch(`${API_BASE}/analyze`, { method: 'POST', body: formData })
  const json = await response.json()
  return transformKeys<ApiResponse<{ videoId: string; filename: string }>>(json)
}

export async function getAnalysis(videoId: string): Promise<ApiResponse<AnalysisResult>> {
  const response = await fetch(`${API_BASE}/analyze/${videoId}`)
  const json = await response.json()
  return transformKeys<ApiResponse<AnalysisResult>>(json)
}
