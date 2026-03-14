<script setup lang="ts">
import DotIndicator from '@/components/atoms/DotIndicator.vue'

defineProps<{
  label: string
  value: string | number
  subtitle?: string
  color?: string
}>()
</script>

<template>
  <div class="glass-card p-3.5 hover:-translate-y-0.5 hover:shadow-[0_8px_40px_rgba(80,60,120,0.10)] transition-all cursor-default">
    <div class="flex items-center gap-1.5 mb-1.5">
      <DotIndicator :color="color" />
      <span class="text-[10px] font-medium text-text-tertiary tracking-wide">{{ label }}</span>
    </div>
    <div class="text-[26px] font-extrabold tracking-tight" :style="{ color: color ?? '#1A1630' }">
      {{ value }}
    </div>
    <div v-if="subtitle" class="text-[10px] text-text-tertiary mt-0.5">{{ subtitle }}</div>
  </div>
</template>
