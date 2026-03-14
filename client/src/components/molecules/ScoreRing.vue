<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  score: number
  size?: number
}>()

const diameter = computed(() => props.size ?? 88)
const radius = computed(() => (diameter.value - 14) / 2)
const circumference = computed(() => 2 * Math.PI * radius.value)
const offset = computed(() => circumference.value * (1 - props.score / 100))
const center = computed(() => diameter.value / 2)
</script>

<template>
  <div class="relative inline-flex items-center justify-center" :style="{ width: `${diameter}px`, height: `${diameter}px` }">
    <svg :width="diameter" :height="diameter" class="-rotate-90">
      <circle :cx="center" :cy="center" :r="radius" fill="none" stroke="rgba(124,92,252,0.1)" stroke-width="7" />
      <circle
        :cx="center" :cy="center" :r="radius" fill="none"
        stroke="url(#scoreGradient)" stroke-width="7" stroke-linecap="round"
        :stroke-dasharray="circumference" :stroke-dashoffset="offset"
        class="transition-all duration-700"
      />
      <defs>
        <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#00C9A7" />
          <stop offset="100%" stop-color="#7C5CFC" />
        </linearGradient>
      </defs>
    </svg>
    <div class="absolute flex flex-col items-center">
      <span class="font-display text-[28px] bg-brand-gradient bg-clip-text text-transparent">{{ score }}</span>
      <span class="text-[10px] text-text-tertiary -mt-1">/100</span>
    </div>
  </div>
</template>
