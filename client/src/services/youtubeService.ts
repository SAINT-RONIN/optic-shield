import { API_BASE } from '@/utils/constants'
import type { ApiResponse } from '@/types/api'

export interface YouTubeVideoInfo {
  title: string
  duration: number
  resolution: string
  thumbnail: string | null
  channel: string | null
}

export async function submitUrl(url: string): Promise<ApiResponse<{ videoId: string; metadata: YouTubeVideoInfo }>> {
  const response = await fetch(`${API_BASE}/youtube`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url })
  })
  return response.json() as Promise<ApiResponse<{ videoId: string; metadata: YouTubeVideoInfo }>>
}
