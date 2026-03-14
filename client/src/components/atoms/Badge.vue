<script setup lang="ts">
defineProps<{
  label: string
  variant?: 'danger' | 'warning' | 'safe' | 'info' | 'neutral'
}>()

const styles: Record<string, string> = {
  danger: 'bg-danger/8 text-danger',
  warning: 'bg-warning/10 text-[#C88600]',
  safe: 'bg-safe/10 text-[#00896E]',
  info: 'bg-brand-purple/8 text-brand-purple',
  neutral: 'bg-black/4 text-text-tertiary'
}
</script>

<template>
  <span :class="['inline-flex items-center px-2.5 py-1 rounded-lg text-[9px] font-semibold tracking-wide', styles[variant ?? 'neutral']]">
    {{ label }}
  </span>
</template>
