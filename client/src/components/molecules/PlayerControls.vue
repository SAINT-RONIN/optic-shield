<script setup lang="ts">
import { Play, Pause } from 'lucide-vue-next'
import { formatTime } from '@/utils/formatters'

defineProps<{
  isPlaying: boolean
  currentTime: number
  duration: number
}>()

defineEmits<{
  'toggle-play': []
  seek: [time: number]
}>()
</script>

<template>
  <div class="flex items-center gap-3">
    <button class="text-white hover:opacity-80 transition-opacity" @click="$emit('toggle-play')">
      <component :is="isPlaying ? Pause : Play" :size="20" />
    </button>
    <span class="font-mono text-[11px] text-white/80">
      {{ formatTime(currentTime) }} / {{ formatTime(duration) }}
    </span>
  </div>
</template>
