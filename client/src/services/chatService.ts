import { API_BASE } from '@/utils/constants'
import type { ApiResponse } from '@/types/api'
import type { ChatRequest, ChatResponse } from '@/types/chat'

export async function sendMessage(request: ChatRequest): Promise<ApiResponse<ChatResponse>> {
  const response = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request)
  })
  return response.json() as Promise<ApiResponse<ChatResponse>>
}
