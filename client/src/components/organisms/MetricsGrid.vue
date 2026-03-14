<script setup lang="ts">
import { computed } from 'vue'
import MetricCard from '@/components/molecules/MetricCard.vue'
import { useAnalysisStore } from '@/stores/analysisStore'

const store = useAnalysisStore()

const metrics = computed(() => {
  const a = store.currentAnalysis
  const flashPeak = a?.flashMetrics.length
    ? Math.max(...a.flashMetrics.map(m => m.flashCountPerSecond))
    : 0
  const avgLum = a?.luminanceMetrics.length
    ? a.luminanceMetrics.reduce((s, m) => s + m.avgLuminance, 0) / a.luminanceMetrics.length
    : 0
  return [
    { label: 'FLASH RATE', value: flashPeak.toFixed(1), subtitle: 'flashes/sec (peak)', color: '#F04E98' },
    { label: 'AVG LUMINANCE', value: avgLum.toFixed(2), subtitle: 'relative (0-1)', color: '#FFB020' },
    { label: 'MOTION', value: '\u2014', subtitle: 'not yet analyzed', color: '#00C9A7' },
    { label: 'SCENE CUTS', value: '\u2014', subtitle: 'not yet analyzed', color: '#5B8DEF' }
  ]
})
</script>

<template>
  <div class="grid grid-cols-2 gap-2.5">
    <MetricCard
      v-for="m in metrics"
      :key="m.label"
      :label="m.label"
      :value="m.value"
      :subtitle="m.subtitle"
      :color="m.color"
    />
  </div>
</template>
