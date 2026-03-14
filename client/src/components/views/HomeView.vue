<script setup lang="ts">
import { computed, ref, watch } from 'vue'
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
import ExportButtons from '@/components/organisms/ExportButtons.vue'
import PanelHeader from '@/components/organisms/PanelHeader.vue'
import AnalysisPill from '@/components/organisms/AnalysisPill.vue'
import { useChat } from '@/composables/useChat'
import { useAnalysis } from '@/composables/useAnalysis'
import { useGraphSync } from '@/composables/useGraphSync'
import { useApiKey } from '@/composables/useApiKey'
import { useGraphData } from '@/viewmodels/graphDataMapper'

const { messages, isLoading, showApiKeyModal, sendMessage } = useChat()
const { currentAnalysis, isAnalyzing, youtubeInfo, startAnalysis, startYoutubeAnalysis } = useAnalysis()
const { isInDangerZone } = useGraphSync()
const { hasKey } = useApiKey()
const { flashData, redFlashData, lumData, motionData, sceneCutData, colorCycleData, explanations } = useGraphData(currentAnalysis)

const orbCompleting = ref(false)
const panelCollapsed = ref(false)

watch(currentAnalysis, (analysis) => {
  if (analysis) {
    orbCompleting.value = true
    panelCollapsed.value = false
    setTimeout(() => { orbCompleting.value = false }, 500)
    if (hasKey.value) {
      const score = analysis.safetyScore.toFixed(1)
      sendMessage(`Summarize the analysis for "${analysis.videoMetadata.filename}". Score: ${score}/100, verdict: "${analysis.verdict}", ${analysis.dangerZones.length} danger zone(s).`)
    }
  }
})

const hasMessages = computed(() => messages.value.length > 0)
const panelOpen = computed(() => currentAnalysis.value !== null && !panelCollapsed.value)
const showPill = computed(() => currentAnalysis.value !== null && panelCollapsed.value)
const orbState = computed(() => {
  if (orbCompleting.value) return 'complete' as const
  if (isInDangerZone.value) return 'alert' as const
  if (isAnalyzing.value) return 'analyzing' as const
  if (isLoading.value) return 'thinking' as const
  return 'idle' as const
})

const suggestions = ['What makes a video unsafe?', 'Explain WCAG guidelines', 'What is photosensitive epilepsy?']
</script>

<template>
  <div class="flex h-screen">
    <AppSidebar />

    <div
      :class="[
        'flex flex-col overflow-hidden transition-all duration-500',
        panelOpen ? 'hidden lg:flex lg:w-[38%]' : 'flex-1 max-w-3xl mx-auto'
      ]"
      style="transition-timing-function: cubic-bezier(0.16, 1, 0.3, 1)"
    >
      <AnalysisPill v-if="showPill" @reopen="panelCollapsed = false" />

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
          :title="youtubeInfo.title" :channel="youtubeInfo.channel"
          :duration="youtubeInfo.duration" :thumbnail="youtubeInfo.thumbnail"
        />
      </div>

      <div :class="['flex flex-col w-full', hasMessages || isAnalyzing ? 'flex-1 overflow-hidden' : 'h-[200px] shrink-0']">
        <ChatContainer />
      </div>
    </div>

    <Transition name="panel">
      <div
        v-if="panelOpen"
        class="w-full lg:w-[62%] absolute lg:relative inset-0 lg:inset-auto border-l border-black/4 overflow-y-auto bg-surface-page z-20 lg:z-0"
      >
        <PanelHeader @close="panelCollapsed = true" />
        <div class="p-5 space-y-4 card-stagger">
          <div class="flex items-center justify-between">
            <h2 class="text-sm font-semibold text-text-primary">Analysis Results</h2>
            <ExportButtons />
          </div>
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
.welcome-leave-active { transition: opacity 0.3s ease, transform 0.3s ease; }
.welcome-leave-to { opacity: 0; transform: translateY(-12px); }
.panel-enter-active { transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1); }
.panel-enter-from { transform: translateX(100%); }
</style>
