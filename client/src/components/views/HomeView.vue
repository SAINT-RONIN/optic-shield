<script setup lang="ts">
import { computed } from 'vue'
import AppSidebar from '@/components/organisms/AppSidebar.vue'
import AiOrb from '@/components/organisms/AiOrb.vue'
import SuggestionChip from '@/components/molecules/SuggestionChip.vue'
import UploadArea from '@/components/organisms/UploadArea.vue'
import ChatContainer from '@/components/organisms/ChatContainer.vue'
import ApiKeyModal from '@/components/organisms/ApiKeyModal.vue'
import SafetyScoreCard from '@/components/organisms/SafetyScoreCard.vue'
import MetricsGrid from '@/components/organisms/MetricsGrid.vue'
import WaveformCard from '@/components/organisms/WaveformCard.vue'
import TimelineStrip from '@/components/organisms/TimelineStrip.vue'
import VideoPlayer from '@/components/organisms/VideoPlayer.vue'
import { useChat } from '@/composables/useChat'
import { useAnalysis } from '@/composables/useAnalysis'

const { messages, isLoading, showApiKeyModal, sendMessage } = useChat()
const { currentAnalysis, isAnalyzing, startAnalysis } = useAnalysis()

const hasMessages = computed(() => messages.value.length > 0)
const panelOpen = computed(() => currentAnalysis.value !== null)
const orbState = computed(() => {
  if (isAnalyzing.value) return 'analyzing' as const
  if (isLoading.value) return 'thinking' as const
  return 'idle' as const
})

const suggestions = [
  'What makes a video unsafe?',
  'Explain WCAG guidelines',
  'What is photosensitive epilepsy?'
]

const flashData = computed(() =>
  currentAnalysis.value?.flashMetrics.map(m => ({ timestamp: m.timestamp, value: m.flashCountPerSecond }))
)
const lumData = computed(() =>
  currentAnalysis.value?.luminanceMetrics.map(m => ({ timestamp: m.timestamp, value: m.avgLuminance }))
)
</script>

<template>
  <div class="flex h-screen">
    <AppSidebar />

    <div
      :class="[
        'flex flex-col overflow-hidden transition-all duration-500',
        panelOpen ? 'w-[38%]' : 'flex-1 max-w-3xl mx-auto'
      ]"
      style="transition-timing-function: cubic-bezier(0.16, 1, 0.3, 1)"
    >
      <Transition name="welcome">
        <div
          v-if="!hasMessages && !isAnalyzing"
          class="flex flex-col items-center justify-center gap-6 px-6 pt-8 pb-4 w-full shrink-0"
        >
          <AiOrb size="lg" :state="orbState" />
          <div class="text-center">
            <h1 class="text-xl font-bold text-text-primary mb-1">Optic Shield AI</h1>
            <p class="text-sm text-text-secondary">Your video safety assistant</p>
          </div>
          <div class="flex flex-wrap justify-center gap-2">
            <SuggestionChip v-for="s in suggestions" :key="s" :label="s" @click="sendMessage(s)" />
          </div>
          <UploadArea @file-selected="startAnalysis" />
        </div>
      </Transition>

      <div :class="['flex flex-col w-full', hasMessages || isAnalyzing ? 'flex-1 overflow-hidden' : 'h-[200px] shrink-0']">
        <ChatContainer />
      </div>
    </div>

    <Transition name="panel">
      <div
        v-if="panelOpen"
        class="w-[62%] border-l border-black/4 overflow-y-auto bg-surface-page"
      >
        <div class="p-5 space-y-4">
          <VideoPlayer />
          <SafetyScoreCard />
          <TimelineStrip />
          <MetricsGrid />
          <WaveformCard title="Flash Frequency" badge-label="Primary" badge-variant="danger" :data="flashData" />
          <WaveformCard title="Luminance" badge-label="Active" badge-variant="warning" :data="lumData" />
        </div>
      </div>
    </Transition>

    <ApiKeyModal :is-open="showApiKeyModal" @close="showApiKeyModal = false" />
  </div>
</template>

<style scoped>
.welcome-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.welcome-leave-to {
  opacity: 0;
  transform: translateY(-12px);
}
.panel-enter-active {
  transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}
.panel-enter-from {
  transform: translateX(100%);
}
</style>
