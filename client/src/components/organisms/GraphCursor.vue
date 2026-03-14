<script setup lang="ts">
import { computed } from 'vue'
import { formatTime } from '@/utils/formatters'

const props = defineProps<{
  currentTime: number
  duration: number
  width: number
}>()

const positionPct = computed(() =>
  props.duration > 0 ? (props.currentTime / props.duration) * 100 : 0
)

const visible = computed(() => props.currentTime > 0 && props.duration > 0)
</script>

<template>
  <div
    v-if="visible"
    class="absolute top-0 h-full pointer-events-none z-10"
    :style="{ left: `${positionPct}%` }"
  >
    <div class="w-[1.5px] h-full bg-text-primary/40" />
    <div
      class="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-full px-1.5 py-0.5 rounded bg-text-primary/80 text-[8px] font-mono text-white whitespace-nowrap"
    >
      {{ formatTime(currentTime) }}
    </div>
  </div>
</template>
