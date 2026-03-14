<script setup lang="ts">
import { ref, watch } from 'vue'
import { MonitorPlay } from 'lucide-vue-next'
import PlayerControls from '@/components/molecules/PlayerControls.vue'
import PlayerScrubber from '@/components/organisms/PlayerScrubber.vue'
import DangerOverlay from '@/components/organisms/DangerOverlay.vue'
import { useVideoPlayer } from '@/composables/useVideoPlayer'
import { useGraphSync } from '@/composables/useGraphSync'
import { useAnalysisStore } from '@/stores/analysisStore'
import { API_BASE } from '@/utils/constants'

const store = useAnalysisStore()
const { currentTime, duration, isPlaying, seek, togglePlay } = useVideoPlayer()
const { isInDangerZone } = useGraphSync()
const videoRef = ref<HTMLVideoElement | null>(null)
const videoUrl = ref<string | null>(null)

watch(() => store.currentAnalysis, (analysis) => {
  videoUrl.value = analysis ? `${API_BASE}/video/${analysis.videoId}` : null
})

function onTimeUpdate(): void {
  const el = videoRef.value
  if (el) currentTime.value = el.currentTime
}

function onLoadedMetadata(): void {
  const el = videoRef.value
  if (el) duration.value = el.duration
}

function handleSeek(time: number): void {
  seek(time)
  if (videoRef.value) videoRef.value.currentTime = time
}

function handleTogglePlay(): void {
  togglePlay()
  const el = videoRef.value
  if (!el) return
  if (isPlaying.value) { el.play() } else { el.pause() }
}

watch(currentTime, (t) => {
  const el = videoRef.value
  if (el && Math.abs(el.currentTime - t) > 0.5) el.currentTime = t
})
</script>

<template>
  <div class="relative rounded-[16px] overflow-hidden bg-black shadow-[0_4px_24px_rgba(80,60,120,0.06)] aspect-video">
    <video
      v-if="videoUrl"
      ref="videoRef"
      :src="videoUrl"
      class="w-full h-full object-contain"
      @timeupdate="onTimeUpdate"
      @loadedmetadata="onLoadedMetadata"
      @ended="isPlaying = false"
    />
    <div v-else class="w-full h-full flex items-center justify-center text-white/40">
      <div class="text-center">
        <MonitorPlay :size="40" class="mx-auto mb-2" />
        <p class="text-sm">No video loaded</p>
      </div>
    </div>
    <DangerOverlay :active="isInDangerZone" />
    <div
      v-if="videoUrl"
      class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 to-transparent px-4 py-3 flex items-center gap-3"
    >
      <PlayerControls
        :is-playing="isPlaying"
        :current-time="currentTime"
        :duration="duration"
        @toggle-play="handleTogglePlay"
        @seek="handleSeek"
      />
      <PlayerScrubber
        :current-time="currentTime"
        :duration="duration"
        @seek="handleSeek"
      />
    </div>
  </div>
</template>
