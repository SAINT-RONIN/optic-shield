import { ref, computed } from 'vue'

const apiKey = ref('')

export function useApiKey() {
  const hasKey = computed(() => apiKey.value.length > 0)

  function setKey(key: string): void {
    apiKey.value = key
  }

  function clearKey(): void {
    apiKey.value = ''
  }

  return { apiKey, hasKey, setKey, clearKey }
}
