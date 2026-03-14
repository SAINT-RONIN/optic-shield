<script setup lang="ts">
defineProps<{
  label: string
  disabled?: boolean
  size?: 'sm' | 'md' | 'lg'
}>()

defineEmits<{ click: [] }>()

const sizeClasses: Record<string, string> = {
  sm: 'px-3 py-1.5 text-xs',
  md: 'px-4 py-2 text-sm',
  lg: 'px-6 py-3 text-base'
}
</script>

<template>
  <button
    :class="[
      'bg-brand-gradient text-white font-semibold rounded-[10px] transition-all hover:brightness-110 disabled:opacity-50 disabled:cursor-not-allowed',
      sizeClasses[size ?? 'md']
    ]"
    :disabled="disabled"
    @click="$emit('click')"
  >
    {{ label }}
  </button>
</template>
