<script setup lang="ts">
defineProps<{ progress: number }>()
</script>

<template>
  <div class="w-full h-1.5 rounded-full bg-brand-purple/10 overflow-hidden">
    <div
      class="h-full bg-brand-gradient rounded-full relative transition-all duration-300"
      :style="{ width: `${Math.min(100, Math.max(0, progress))}%` }"
    >
      <div class="absolute inset-0 overflow-hidden rounded-full">
        <div class="w-full h-full animate-[shimmer_2s_infinite]" style="background: linear-gradient(90deg, transparent, rgba(255,255,255,0.25), transparent)" />
      </div>
    </div>
  </div>
</template>
