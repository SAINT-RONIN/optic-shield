<script setup lang="ts">
import { computed } from 'vue'
import AppSidebar from '@/components/organisms/AppSidebar.vue'
import AiOrb from '@/components/organisms/AiOrb.vue'
import SuggestionChip from '@/components/molecules/SuggestionChip.vue'
import UploadArea from '@/components/organisms/UploadArea.vue'
import YoutubeInput from '@/components/organisms/YoutubeInput.vue'
import YoutubeFileCard from '@/components/molecules/YoutubeFileCard.vue'
import ChatContainer from '@/components/organisms/ChatContainer.vue'
import ApiKeyModal from '@/components/organisms/ApiKeyModal.vue'
import SafetyScoreCard from '@/components/organisms/SafetyScoreCard.vue'
import MetricsGrid from '@/components/organisms/MetricsGrid.vue'
import WaveformCard from '@/components/organisms/WaveformCard.vue'
import TimelineStrip from '@/components/organisms/TimelineStrip.vue'
import VideoPlayer from '@/components/organisms/VideoPlayer.vue'
import { useChat } from '@/composables/useChat'
import { useAnalysis } from '@/composables/useAnalysis'
import { useGraphSync } from '@/composables/useGraphSync'

const { messages, isLoading, showApiKeyModal, sendMessage } = useChat()
const { currentAnalysis, isAnalyzing, youtubeInfo, startAnalysis, startYoutubeAnalysis } = useAnalysis()
const { isInDangerZone } = useGraphSync()

const hasMessages = computed(() => messages.value.length > 0)
const panelOpen = computed(() => currentAnalysis.value !== null)
const orbState = computed(() => {
  if (isInDangerZone.value) return 'alert' as const
  if (isAnalyzing.value) return 'analyzing' as const
  if (isLoading.value) return 'thinking' as const
  return 'idle' as const
})

const suggestions = [
  'What makes a video unsafe?',
  'Explain WCAG guidelines',
  'What is photosensitive epilepsy?'
]

interface DataPoint { timestamp: number; value: number }

function toDataPoints<T extends { timestamp: number }>(
  metrics: T[] | undefined,
  valueGetter: (m: T) => number
): DataPoint[] | undefined {
  return metrics?.map(m => ({ timestamp: m.timestamp, value: valueGetter(m) }))
}

const flashData = computed(() => toDataPoints(currentAnalysis.value?.flashMetrics, m => m.flashCountPerSecond))
const redFlashData = computed(() => toDataPoints(currentAnalysis.value?.redFlashMetrics, m => m.redFlashIntensity))
const lumData = computed(() => toDataPoints(currentAnalysis.value?.luminanceMetrics, m => m.avgLuminance))
const motionData = computed(() => toDataPoints(currentAnalysis.value?.motionMetrics, m => m.motionIntensity))
const sceneCutData = computed(() => toDataPoints(currentAnalysis.value?.sceneCutMetrics, m => m.cutConfidence))
const colorCycleData = computed(() => toDataPoints(currentAnalysis.value?.colorCycleMetrics, m => m.hueShiftSpeed))

const explanations = computed(() => currentAnalysis.value?.graphExplanations ?? {})
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
          <div class="text-[11px] text-text-tertiary">or</div>
          <YoutubeInput @submit="startYoutubeAnalysis" />
        </div>
      </Transition>

      <div v-if="youtubeInfo" class="px-6 pt-4">
        <YoutubeFileCard
          :title="youtubeInfo.title"
          :channel="youtubeInfo.channel"
          :duration="youtubeInfo.duration"
          :thumbnail="youtubeInfo.thumbnail"
        />
      </div>

      <div :class="['flex flex-col w-full', hasMessages || isAnalyzing ? 'flex-1 overflow-hidden' : 'h-[200px] shrink-0']">
        <ChatContainer />
      </div>
    </div>

    <Transition name="panel">
      <div v-if="panelOpen" class="w-[62%] border-l border-black/4 overflow-y-auto bg-surface-page">
        <div class="p-5 space-y-4">
          <VideoPlayer />
          <SafetyScoreCard />
          <TimelineStrip />
          <MetricsGrid />
          <WaveformCard title="Flash Frequency" badge-label="Flashes" badge-variant="danger"
            :data="flashData" :explanation="explanations.flash" />
          <WaveformCard title="Red Flash" badge-label="Red" badge-variant="danger"
            :data="redFlashData" :explanation="explanations.red_flash" />
          <WaveformCard title="Luminance" badge-label="Brightness" badge-variant="warning"
            :data="lumData" :explanation="explanations.luminance" />
          <WaveformCard title="Motion Intensity" badge-label="Motion" badge-variant="safe"
            :data="motionData" :explanation="explanations.motion" />
          <WaveformCard title="Scene Cuts" badge-label="Cuts" badge-variant="info"
            :data="sceneCutData" :explanation="explanations.scene_cut" />
          <WaveformCard title="Color Cycling" badge-label="Hue" badge-variant="info"
            :data="colorCycleData" :explanation="explanations.color_cycle" />
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
