<script setup lang="ts">
import { ref } from 'vue'
import { Paperclip, ArrowRight } from 'lucide-vue-next'

defineProps<{ disabled?: boolean }>()
const emit = defineEmits<{ send: [message: string] }>()

const input = ref('')

function handleSend(): void {
  const trimmed = input.value.trim()
  if (!trimmed) return
  emit('send', trimmed)
  input.value = ''
}
</script>

<template>
  <div class="flex items-center gap-2 bg-surface-input rounded-[14px] p-1 pl-4">
    <button class="text-text-tertiary hover:text-text-secondary transition-colors" :disabled="disabled">
      <Paperclip :size="18" />
    </button>
    <input
      v-model="input"
      placeholder="Ask about video accessibility..."
      :disabled="disabled"
      class="flex-1 bg-transparent text-sm text-text-primary placeholder:text-text-tertiary outline-none disabled:opacity-50"
      @keydown.enter="!disabled && handleSend()"
    />
    <button
      :disabled="disabled"
      class="flex items-center justify-center w-[34px] h-[34px] rounded-[10px] bg-brand-gradient text-white hover:brightness-110 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
      @click="handleSend"
    >
      <ArrowRight :size="14" />
    </button>
  </div>
</template>
