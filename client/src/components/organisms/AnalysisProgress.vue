<script setup lang="ts">
import ProgressBar from '@/components/atoms/ProgressBar.vue'
import DotIndicator from '@/components/atoms/DotIndicator.vue'
import type { AnalysisProgress } from '@/types/analysis'
import { ANALYSIS_STAGES } from '@/utils/constants'

defineProps<{ progress: AnalysisProgress }>()

function getStageStatus(stageIndex: number, currentStage: string): 'done' | 'active' | 'pending' {
  const currentIndex = ANALYSIS_STAGES.indexOf(currentStage as typeof ANALYSIS_STAGES[number])
  if (stageIndex < currentIndex) return 'done'
  if (stageIndex === currentIndex) return 'active'
  return 'pending'
}
</script>

<template>
  <div class="bg-brand-purple/5 rounded-[14px] rounded-bl-[4px] px-4 py-3 space-y-3">
    <ProgressBar :progress="progress.progress * 100" />
    <p class="font-mono text-[11px] text-text-secondary">
      Analyzing frame {{ progress.currentFrame.toLocaleString() }} / {{ progress.totalFrames.toLocaleString() }}
    </p>
    <div class="space-y-1.5">
      <div v-for="(stage, i) in ANALYSIS_STAGES" :key="stage" class="flex items-center gap-2">
        <DotIndicator
          :color="getStageStatus(i, progress.stage) === 'done' ? '#00C9A7' : getStageStatus(i, progress.stage) === 'active' ? '#7C5CFC' : '#9D97B5'"
          :size="6"
        />
        <span
          :class="[
            'text-[11px]',
            getStageStatus(i, progress.stage) === 'active' ? 'text-brand-purple font-semibold' : 'text-text-tertiary'
          ]"
        >
          {{ stage }}
        </span>
      </div>
    </div>
  </div>
</template>
