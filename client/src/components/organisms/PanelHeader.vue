<script setup lang="ts">
import { X } from 'lucide-vue-next'
import { useAnalysisStore } from '@/stores/analysisStore'

defineEmits<{ close: [] }>()

const store = useAnalysisStore()
const filename = store.currentAnalysis?.videoMetadata.filename ?? 'Analysis'
</script>

<template>
  <div class="flex items-center justify-between px-5 py-3 border-b border-black/4 bg-white/50 backdrop-blur-sm sticky top-0 z-10">
    <span class="text-sm font-bold text-text-primary">{{ filename }}</span>
    <button class="text-text-tertiary hover:text-text-primary transition-colors" @click="$emit('close')">
      <X :size="18" />
    </button>
  </div>
</template>
