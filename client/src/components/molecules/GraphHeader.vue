<script setup lang="ts">
import Badge from '@/components/atoms/Badge.vue'

defineProps<{
  title: string
  badgeLabel?: string
  badgeVariant?: 'danger' | 'warning' | 'safe' | 'info' | 'neutral'
}>()
</script>

<template>
  <div class="flex items-center justify-between">
    <span class="text-[13px] font-bold text-text-primary">{{ title }}</span>
    <Badge v-if="badgeLabel" :label="badgeLabel" :variant="badgeVariant" />
  </div>
</template>
