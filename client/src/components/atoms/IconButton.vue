<script setup lang="ts">
defineProps<{ active?: boolean }>()
defineEmits<{ click: [] }>()
</script>

<template>
  <button
    :class="[
      'flex items-center justify-center w-10 h-10 rounded-[12px] transition-colors',
      active
        ? 'bg-brand-purple/15 text-white'
        : 'text-text-tertiary hover:bg-surface-sidebar-hover hover:text-white'
    ]"
    @click="$emit('click')"
  >
    <slot />
  </button>
</template>
