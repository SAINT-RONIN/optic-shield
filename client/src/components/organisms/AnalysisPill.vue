<script setup lang="ts">
import { computed } from 'vue'
import ScoreRing from '@/components/molecules/ScoreRing.vue'
import { useAnalysisStore } from '@/stores/analysisStore'

defineEmits<{ reopen: [] }>()

const store = useAnalysisStore()
const analysis = computed(() => store.currentAnalysis)
</script>

<template>
  <div
    v-if="analysis"
    class="flex items-center justify-between px-4 py-2 bg-white/80 backdrop-blur-sm border-b border-black/4 sticky top-0 z-10"
  >
    <div class="flex items-center gap-2">
      <ScoreRing :score="analysis.safetyScore" :size="20" />
      <span class="text-xs font-medium text-text-primary truncate max-w-[150px]">{{ analysis.videoMetadata.filename }}</span>
      <span class="text-xs font-semibold bg-brand-gradient bg-clip-text text-transparent">{{ analysis.safetyScore.toFixed(0) }}</span>
    </div>
    <button class="text-xs font-semibold text-brand-purple hover:underline" @click="$emit('reopen')">View analysis</button>
  </div>
</template>
