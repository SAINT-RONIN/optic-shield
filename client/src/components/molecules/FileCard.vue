<script setup lang="ts">
import { Film } from 'lucide-vue-next'

defineProps<{
  filename: string
  size?: string
  duration?: string
  resolution?: string
}>()
</script>

<template>
  <div class="inline-flex items-center gap-3 bg-brand-purple/5 border border-brand-purple/10 rounded-[12px] px-3.5 py-2.5">
    <div class="flex items-center justify-center w-10 h-10 rounded-lg bg-brand-purple/10">
      <Film :size="20" class="text-brand-purple" />
    </div>
    <div>
      <div class="text-[13px] font-semibold text-text-primary">{{ filename }}</div>
      <div class="text-[11px] text-text-tertiary">
        <span v-if="duration">{{ duration }}</span>
        <span v-if="size"> · {{ size }}</span>
        <span v-if="resolution"> · {{ resolution }}</span>
      </div>
    </div>
  </div>
</template>
