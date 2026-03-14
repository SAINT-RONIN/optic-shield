<script setup lang="ts">
defineProps<{
  color?: string
  size?: number
}>()
</script>

<template>
  <span
    class="inline-block rounded-full"
    :style="{ width: `${size ?? 6}px`, height: `${size ?? 6}px`, backgroundColor: color ?? '#9D97B5' }"
  />
</template>
