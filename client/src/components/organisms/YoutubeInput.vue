<script setup lang="ts">
import { ref } from 'vue'
import GradientButton from '@/components/atoms/GradientButton.vue'
import { isValidYouTubeUrl } from '@/utils/validators'

const emit = defineEmits<{ submit: [url: string] }>()
const url = ref('')
const isValid = ref(true)

function handleSubmit(): void {
  const trimmed = url.value.trim()
  if (!trimmed) return
  if (!isValidYouTubeUrl(trimmed)) {
    isValid.value = false
    return
  }
  isValid.value = true
  emit('submit', trimmed)
  url.value = ''
}
</script>

<template>
  <div class="max-w-md mx-auto flex gap-2">
    <input
      v-model="url"
      placeholder="Paste a YouTube link..."
      :class="[
        'flex-1 bg-surface-input rounded-[12px] px-4 py-2.5 text-sm text-text-primary placeholder:text-text-tertiary outline-none border transition-colors',
        isValid ? 'border-transparent focus:border-border-focus' : 'border-danger'
      ]"
      @keydown.enter="handleSubmit"
      @input="isValid = true"
    />
    <GradientButton label="Analyze" size="md" @click="handleSubmit" />
  </div>
</template>
