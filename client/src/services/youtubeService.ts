import { API_BASE } from '@/utils/constants'
import type { ApiResponse } from '@/types/api'
import { transformKeys } from '@/utils/caseTransform'

export interface YouTubeVideoInfo {
  title: string
  duration: number
  resolution: string
  thumbnail: string | null
  channel: string | null
}

export interface YouTubeDownloadResult {
  videoId: string
  filePath: string
  metadata: YouTubeVideoInfo
}

export async function submitUrl(url: string): Promise<ApiResponse<YouTubeDownloadResult>> {
  const response = await fetch(`${API_BASE}/youtube`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url })
  })
  const json = await response.json()
  return transformKeys<ApiResponse<YouTubeDownloadResult>>(json)
}
