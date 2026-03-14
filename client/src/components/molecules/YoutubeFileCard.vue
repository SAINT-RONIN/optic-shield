<script setup lang="ts">
import { Film } from 'lucide-vue-next'
import { formatTime } from '@/utils/formatters'

defineProps<{
  title: string
  channel: string | null
  duration: number
  thumbnail: string | null
}>()
</script>

<template>
  <div class="inline-flex items-center gap-3 bg-brand-purple/5 border border-brand-purple/10 rounded-[12px] px-3.5 py-2.5 max-w-md">
    <div class="relative shrink-0 w-16 h-10 rounded-md overflow-hidden bg-brand-purple/10">
      <img v-if="thumbnail" :src="thumbnail" :alt="title" class="w-full h-full object-cover" />
      <div v-else class="w-full h-full flex items-center justify-center">
        <Film :size="18" class="text-brand-purple" />
      </div>
      <span class="absolute bottom-0.5 right-0.5 px-1 py-0.5 rounded bg-black/60 text-[8px] font-mono text-white">
        {{ formatTime(duration) }}
      </span>
    </div>
    <div class="min-w-0">
      <div class="text-[13px] font-semibold text-text-primary truncate">{{ title }}</div>
      <div class="flex items-center gap-1 text-[11px] text-text-tertiary">
        <svg class="w-3 h-3 text-[#FF0000] shrink-0" viewBox="0 0 24 24" fill="currentColor">
          <path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.5 12 3.5 12 3.5s-7.5 0-9.4.6A3 3 0 0 0 .5 6.2 31 31 0 0 0 0 12a31 31 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.6 9.4.6 9.4.6s7.5 0 9.4-.6a3 3 0 0 0 2.1-2.1A31 31 0 0 0 24 12a31 31 0 0 0-.5-5.8z"/>
          <polygon fill="#FFF" points="9.75,15.02 15.5,12 9.75,8.98"/>
        </svg>
        <span class="truncate">{{ channel ?? 'YouTube' }}</span>
      </div>
    </div>
  </div>
</template>
