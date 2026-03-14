<script setup lang="ts">
import MetricCard from '@/components/molecules/MetricCard.vue'

const metrics = [
  { label: 'FLASH RATE', value: '0', subtitle: 'flashes/sec (max)', color: '#F04E98' },
  { label: 'AVG LUMINANCE', value: '0', subtitle: 'cd/m² average', color: '#FFB020' },
  { label: 'MOTION INTENSITY', value: '0', subtitle: 'pixel diff avg', color: '#00C9A7' },
  { label: 'SCENE CUTS', value: '0', subtitle: 'total detected', color: '#5B8DEF' }
]
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
