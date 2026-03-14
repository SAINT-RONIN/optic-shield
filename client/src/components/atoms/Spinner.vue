<script setup lang="ts">
defineProps<{ size?: 'sm' | 'md' | 'lg' }>()

const sizeMap: Record<string, string> = {
  sm: 'w-4 h-4',
  md: 'w-6 h-6',
  lg: 'w-8 h-8'
}
</script>

<template>
  <div
    :class="['rounded-full border-2 border-brand-purple/20 border-t-brand-purple animate-[spin_0.8s_linear_infinite]', sizeMap[size ?? 'md']]"
  />
</template>
