import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { usePlayerStore } from '@/stores/playerStore'
import { useAnalysisStore } from '@/stores/analysisStore'

export function useGraphSync() {
  const playerStore = usePlayerStore()
  const analysisStore = useAnalysisStore()
  const { currentTime, duration } = storeToRefs(playerStore)

  function seekTo(time: number): void {
    playerStore.setCurrentTime(time)
  }

  function cursorX(width: number): number {
    if (duration.value <= 0) return 0
    return (currentTime.value / duration.value) * width
  }

  const isInDangerZone = computed(() => {
    const analysis = analysisStore.currentAnalysis
    if (!analysis) return false
    return analysis.dangerZones.some(
      zone => currentTime.value >= zone.startTime && currentTime.value <= zone.endTime
    )
  })

  return { currentTime, duration, seekTo, cursorX, isInDangerZone }
}
