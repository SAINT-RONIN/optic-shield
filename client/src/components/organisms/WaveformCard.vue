<script setup lang="ts">
import GraphHeader from '@/components/molecules/GraphHeader.vue'

defineProps<{
  title: string
  badgeLabel?: string
  badgeVariant?: 'danger' | 'warning' | 'safe' | 'info' | 'neutral'
  explanation?: string
}>()
</script>

<template>
  <div class="glass-card overflow-hidden">
    <div class="px-4 pt-3.5">
      <GraphHeader :title="title" :badge-label="badgeLabel" :badge-variant="badgeVariant" />
    </div>
    <div class="px-4 py-2 h-20 flex items-center justify-center">
      <span class="text-[11px] text-text-tertiary">No data available</span>
    </div>
    <div
      v-if="explanation"
      class="mx-4 mb-4 p-3 rounded-[12px] border-l-[3px] border-brand-purple/30"
      style="background: linear-gradient(135deg, rgba(0,201,167,0.04), rgba(124,92,252,0.04))"
    >
      <p class="text-[11px] text-text-secondary leading-relaxed">{{ explanation }}</p>
    </div>
  </div>
</template>
