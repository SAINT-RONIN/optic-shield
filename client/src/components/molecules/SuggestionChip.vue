<script setup lang="ts">
defineProps<{ label: string }>()
defineEmits<{ click: [] }>()
</script>

<template>
  <button
    class="px-4 py-2 rounded-[10px] border border-brand-purple/15 bg-brand-purple/4 text-text-secondary text-xs font-medium hover:bg-brand-purple/10 hover:border-brand-purple/30 hover:text-brand-purple transition-all"
    @click="$emit('click')"
  >
    {{ label }}
  </button>
</template>
