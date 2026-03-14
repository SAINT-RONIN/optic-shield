<script setup lang="ts">
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Filler,
  Tooltip,
} from 'chart.js'
import GraphHeader from '@/components/molecules/GraphHeader.vue'

ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale, Filler, Tooltip)

interface DataPoint {
  timestamp: number
  value: number
}

const props = defineProps<{
  title: string
  badgeLabel?: string
  badgeVariant?: 'danger' | 'warning' | 'safe' | 'info' | 'neutral'
  explanation?: string
  data?: DataPoint[]
}>()

const chartData = computed(() => ({
  labels: (props.data ?? []).map(d => d.timestamp.toFixed(1)),
  datasets: [{
    data: (props.data ?? []).map(d => d.value),
    borderColor: '#7C5CFC',
    backgroundColor: 'rgba(124, 92, 252, 0.1)',
    fill: true,
    tension: 0.3,
    pointRadius: 0,
    borderWidth: 2,
  }]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false }, tooltip: { enabled: true } },
  scales: {
    x: { display: false },
    y: { display: false }
  }
}
</script>

<template>
  <div class="glass-card overflow-hidden">
    <div class="px-4 pt-3.5">
      <GraphHeader :title="title" :badge-label="badgeLabel" :badge-variant="badgeVariant" />
    </div>
    <div class="px-4 py-2 h-20">
      <Line v-if="data?.length" :data="chartData" :options="chartOptions" />
      <div v-else class="h-full flex items-center justify-center">
        <span class="text-[11px] text-text-tertiary">No data available</span>
      </div>
    </div>
    <div
      v-if="explanation"
      class="mx-4 mb-4 p-3 rounded-[12px] border-l-[3px] border-brand-purple/30"
      style="background: linear-gradient(135deg, rgba(0,201,167,0.04), rgba(124,92,252,0.04))"
    >
      <p class="text-[11px] text-text-secondary leading-relaxed">{{ explanation }}</p>
    </div>
  </div>
</template>
