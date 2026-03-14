<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAnalysisStore } from '@/stores/analysisStore'

const props = defineProps<{
  currentTime: number
  duration: number
}>()

const emit = defineEmits<{ seek: [time: number] }>()
const store = useAnalysisStore()
const trackRef = ref<HTMLElement | null>(null)

const progressPct = computed(() =>
  props.duration > 0 ? (props.currentTime / props.duration) * 100 : 0
)

const dangerSegments = computed(() => {
  const zones = store.currentAnalysis?.dangerZones ?? []
  const dur = props.duration
  if (!dur) return []
  return zones.map(z => ({
    left: (z.startTime / dur) * 100,
    width: ((z.endTime - z.startTime) / dur) * 100,
  }))
})

function handleClick(e: MouseEvent): void {
  const track = trackRef.value
  if (!track || !props.duration) return
  const rect = track.getBoundingClientRect()
  const pct = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width))
  emit('seek', pct * props.duration)
}
</script>

<template>
  <div
    ref="trackRef"
    class="relative h-1.5 flex-1 rounded-full bg-white/20 cursor-pointer group"
    @click="handleClick"
  >
    <div
      v-for="(seg, i) in dangerSegments" :key="i"
      class="absolute top-0 h-full rounded-full bg-danger/40"
      :style="{ left: `${seg.left}%`, width: `${seg.width}%` }"
    />
    <div
      class="absolute top-0 h-full rounded-full bg-brand-gradient"
      :style="{ width: `${progressPct}%` }"
    />
    <div
      class="absolute top-1/2 -translate-y-1/2 w-3 h-3 rounded-full bg-white shadow-md opacity-0 group-hover:opacity-100 transition-opacity"
      :style="{ left: `calc(${progressPct}% - 6px)` }"
    />
  </div>
</template>
