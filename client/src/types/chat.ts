import type { AnalysisResult } from './analysis'

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  timestamp: number | null
}

export interface ChatRequest {
  message: string
  apiKey: string
  conversationHistory: ChatMessage[]
  analysisContext: AnalysisResult | null
}

export interface ChatResponse {
  message: string
  conversationHistory: ChatMessage[]
}
