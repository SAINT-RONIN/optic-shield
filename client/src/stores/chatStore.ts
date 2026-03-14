import { ref } from 'vue'
import { defineStore } from 'pinia'
import type { ChatMessage } from '@/types/chat'

export const useChatStore = defineStore('chat', () => {
  const messages = ref<ChatMessage[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  function addMessage(message: ChatMessage): void {
    messages.value.push(message)
  }

  function setLoading(loading: boolean): void {
    isLoading.value = loading
  }

  function setError(msg: string | null): void {
    error.value = msg
  }

  function clearMessages(): void {
    messages.value = []
    error.value = null
  }

  return { messages, isLoading, error, addMessage, setLoading, setError, clearMessages }
})
