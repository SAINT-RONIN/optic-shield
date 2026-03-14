<script setup lang="ts">
import AppSidebar from '@/components/organisms/AppSidebar.vue'
import AiOrb from '@/components/organisms/AiOrb.vue'
import SuggestionChip from '@/components/molecules/SuggestionChip.vue'
import UploadArea from '@/components/organisms/UploadArea.vue'
import ChatContainer from '@/components/organisms/ChatContainer.vue'
import { useChat } from '@/composables/useChat'

const { sendMessage } = useChat()

const suggestions = [
  'What makes a video unsafe?',
  'Explain WCAG guidelines',
  'What is photosensitive epilepsy?'
]

function handleSuggestion(text: string): void {
  sendMessage(text)
}
</script>

<template>
  <div class="flex h-screen">
    <AppSidebar />
    <main class="flex-1 flex flex-col items-center max-w-3xl mx-auto w-full relative">
      <div class="flex-1 flex flex-col items-center justify-center gap-6 px-6 pt-8 pb-4 w-full">
        <AiOrb size="lg" state="idle" />
        <div class="text-center">
          <h1 class="text-xl font-bold text-text-primary mb-1">Optic Shield AI</h1>
          <p class="text-sm text-text-secondary">Your video safety assistant</p>
        </div>
        <div class="flex flex-wrap justify-center gap-2">
          <SuggestionChip
            v-for="s in suggestions"
            :key="s"
            :label="s"
            @click="handleSuggestion(s)"
          />
        </div>
        <UploadArea @file-selected="() => {}" />
      </div>
      <div class="w-full h-[200px] shrink-0">
        <ChatContainer />
      </div>
    </main>
  </div>
</template>
