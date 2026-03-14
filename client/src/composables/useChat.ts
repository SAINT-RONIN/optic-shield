import { storeToRefs } from 'pinia'
import { useChatStore } from '@/stores/chatStore'
import type { ChatMessage } from '@/types/chat'

export function useChat() {
  const store = useChatStore()
  const { messages, isLoading, error } = storeToRefs(store)

  function sendMessage(content: string): void {
    const message: ChatMessage = { role: 'user', content, timestamp: Date.now() / 1000 }
    store.addMessage(message)
  }

  return { messages, isLoading, error, sendMessage, clearMessages: store.clearMessages }
}
