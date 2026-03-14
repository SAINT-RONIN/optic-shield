<script setup lang="ts">
defineProps<{ height?: string; width?: string }>()
</script>

<template>
  <div
    class="rounded-[16px] bg-brand-purple/5 animate-pulse"
    :style="{ height: height ?? '80px', width: width ?? '100%' }"
  />
</template>
