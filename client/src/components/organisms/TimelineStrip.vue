<script setup lang="ts">
import { computed } from 'vue'
import { useAnalysisStore } from '@/stores/analysisStore'
import { useGraphSync } from '@/composables/useGraphSync'
import { formatTime } from '@/utils/formatters'

const store = useAnalysisStore()
const { seekTo } = useGraphSync()

interface Segment {
  flex: number
  type: 'safe' | 'warning' | 'danger'
}

const duration = computed(() => store.currentAnalysis?.videoMetadata.duration ?? 0)

const segments = computed((): Segment[] => {
  const a = store.currentAnalysis
  if (!a || !duration.value) {
    return [{ flex: 1, type: 'safe' }]
  }

  const zones = [...a.dangerZones].sort((x, y) => x.startTime - y.startTime)
  const result: Segment[] = []
  let cursor = 0

  for (const zone of zones) {
    if (zone.startTime > cursor) {
      result.push({ flex: zone.startTime - cursor, type: 'safe' })
    }
    const zoneType = zone.severity === 'critical' || zone.severity === 'high' ? 'danger' : 'warning'
    result.push({ flex: zone.endTime - zone.startTime || 0.1, type: zoneType })
    cursor = zone.endTime
  }

  if (cursor < duration.value) {
    result.push({ flex: duration.value - cursor, type: 'safe' })
  }

  return result.length ? result : [{ flex: 1, type: 'safe' }]
})

const segmentStyles: Record<string, string> = {
  safe: 'background: linear-gradient(135deg, #00C9A7, #40E8C8)',
  warning: 'background: linear-gradient(135deg, #FFB020, #FFD060)',
  danger: 'background: linear-gradient(135deg, #F04E98, #FF6BAA)'
}

function handleBarClick(e: MouseEvent): void {
  const target = e.currentTarget as HTMLElement
  const rect = target.getBoundingClientRect()
  const pct = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width))
  seekTo(pct * duration.value)
}
</script>

<template>
  <div class="glass-card p-3.5">
    <div class="text-[11px] font-semibold text-text-tertiary mb-2 tracking-wide">TIMELINE RISK</div>
    <div class="flex gap-0.5 h-2 cursor-pointer" @click="handleBarClick">
      <div
        v-for="(seg, i) in segments" :key="i"
        class="rounded-[4px]"
        :style="[segmentStyles[seg.type], `flex: ${seg.flex}`]"
      />
    </div>
    <div class="flex justify-between mt-1.5">
      <span class="text-[8px] font-medium text-text-tertiary">0:00</span>
      <span class="text-[8px] font-medium text-text-tertiary">{{ formatTime(duration) }}</span>
    </div>
  </div>
</template>
