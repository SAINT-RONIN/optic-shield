import { ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useChatStore } from '@/stores/chatStore'
import { useApiKey } from './useApiKey'
import { sendMessage as sendChatMessage } from '@/services/chatService'
import type { ChatMessage, ChatRequest } from '@/types/chat'

const showApiKeyModal = ref(false)

export function useChat() {
  const store = useChatStore()
  const { messages, isLoading, error } = storeToRefs(store)
  const { apiKey, hasKey } = useApiKey()

  async function sendMessage(content: string): Promise<void> {
    if (!hasKey.value) {
      showApiKeyModal.value = true
      return
    }

    const userMessage: ChatMessage = {
      role: 'user',
      content,
      timestamp: Date.now() / 1000
    }
    store.addMessage(userMessage)
    store.setLoading(true)
    store.setError(null)

    const request: ChatRequest = {
      message: content,
      apiKey: apiKey.value,
      conversationHistory: messages.value.slice(0, -1),
      analysisContext: null
    }

    try {
      const response = await sendChatMessage(request)
      if (response.success && response.data) {
        const assistantMessage: ChatMessage = {
          role: 'assistant',
          content: response.data.message,
          timestamp: Date.now() / 1000
        }
        store.addMessage(assistantMessage)
      } else {
        store.setError(response.error ?? 'An unexpected error occurred.')
      }
    } catch {
      store.setError('Failed to reach the server. Please try again.')
    } finally {
      store.setLoading(false)
    }
  }

  return {
    messages,
    isLoading,
    error,
    showApiKeyModal,
    sendMessage,
    clearMessages: store.clearMessages
  }
}
