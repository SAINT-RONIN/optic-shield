<script setup lang="ts">
import { computed } from 'vue'
import ScoreRing from '@/components/molecules/ScoreRing.vue'
import Badge from '@/components/atoms/Badge.vue'
import { useAnalysisStore } from '@/stores/analysisStore'
import { toSafetyVerdict } from '@/viewmodels/analysisViewModel'

const store = useAnalysisStore()
const score = computed(() => store.currentAnalysis?.safetyScore ?? 0)
const verdict = computed(() => toSafetyVerdict(score.value))
</script>

<template>
  <div class="glass-card p-5 flex items-center gap-5">
    <ScoreRing :score="score" />
    <div>
      <h3 class="text-[15px] font-bold text-text-primary">{{ verdict.label }}</h3>
      <p class="text-[11px] text-text-secondary mt-1 leading-relaxed">
        Overall safety assessment based on flash frequency, luminance, motion, and pattern analysis.
      </p>
      <div class="flex gap-1.5 mt-2">
        <Badge label="WCAG 2.1" variant="info" />
        <Badge label="SC 2.3.1" variant="info" />
      </div>
    </div>
  </div>
</template>
