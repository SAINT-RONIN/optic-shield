<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  size?: 'lg' | 'md' | 'sm'
  state?: 'idle' | 'thinking' | 'analyzing' | 'alert'
}>()

const sizeMap: Record<string, string> = {
  lg: 'w-[180px] h-[180px]',
  md: 'w-12 h-12',
  sm: 'w-9 h-9'
}

const sizeClass = computed(() => sizeMap[props.size ?? 'lg'])
const isActive = computed(() => props.state === 'thinking' || props.state === 'analyzing')
</script>

<template>
  <div
    :class="[
      'rounded-full bg-brand-gradient shadow-[0_0_40px_rgba(124,92,252,0.3)]',
      sizeClass,
      isActive ? 'animate-[pulse-slow_2s_ease-in-out_infinite]' : 'animate-[pulse-slow_4s_ease-in-out_infinite]'
    ]"
  />
</template>
