<script setup lang="ts">
import { ref } from 'vue'
import { MessageSquare, Upload, Settings, Shield } from 'lucide-vue-next'
import IconButton from '@/components/atoms/IconButton.vue'

const activeItem = ref('chat')

const navItems = [
  { id: 'chat', icon: MessageSquare, label: 'Chat' },
  { id: 'upload', icon: Upload, label: 'Upload' },
  { id: 'settings', icon: Settings, label: 'Settings' }
] as const
</script>

<template>
  <aside class="flex flex-col items-center w-16 h-screen bg-surface-sidebar border-r border-white/6 py-4 gap-2">
    <div class="flex items-center justify-center w-10 h-10 mb-4">
      <Shield :size="24" class="text-brand-purple" />
    </div>
    <nav class="flex flex-col gap-1.5">
      <IconButton
        v-for="item in navItems"
        :key="item.id"
        :active="activeItem === item.id"
        @click="activeItem = item.id"
      >
        <component :is="item.icon" :size="20" />
      </IconButton>
    </nav>
  </aside>
</template>
