import { API_BASE } from '@/utils/constants'
import type { ApiResponse } from '@/types/api'
import type { ChatRequest, ChatResponse } from '@/types/chat'

export async function sendMessage(request: ChatRequest): Promise<ApiResponse<ChatResponse>> {
  const response = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request)
  })

  if (!response.ok) {
    return {
      success: false,
      data: null,
      error: `Server error: ${response.status}`,
      errorCode: String(response.status)
    }
  }

  return response.json() as Promise<ApiResponse<ChatResponse>>
}
