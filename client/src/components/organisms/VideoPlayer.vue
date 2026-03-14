<script setup lang="ts">
import { MonitorPlay } from 'lucide-vue-next'
</script>

<template>
  <div class="rounded-[16px] overflow-hidden bg-black shadow-[0_4px_24px_rgba(80,60,120,0.06)] aspect-video flex items-center justify-center">
    <div class="text-center text-white/40">
      <MonitorPlay :size="40" class="mx-auto mb-2" />
      <p class="text-sm">No video loaded</p>
    </div>
  </div>
</template>
