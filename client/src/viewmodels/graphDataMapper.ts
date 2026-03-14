import { computed, type Ref } from 'vue'
import type { AnalysisResult } from '@/types/analysis'

interface DataPoint {
  timestamp: number
  value: number
}

function toDataPoints<T extends { timestamp: number }>(
  metrics: T[] | undefined,
  valueGetter: (m: T) => number
): DataPoint[] | undefined {
  return metrics?.map(m => ({ timestamp: m.timestamp, value: valueGetter(m) }))
}

export function useGraphData(analysis: Ref<AnalysisResult | null>) {
  const flashData = computed(() => toDataPoints(analysis.value?.flashMetrics, m => m.flashCountPerSecond))
  const redFlashData = computed(() => toDataPoints(analysis.value?.redFlashMetrics, m => m.redFlashIntensity))
  const lumData = computed(() => toDataPoints(analysis.value?.luminanceMetrics, m => m.avgLuminance))
  const motionData = computed(() => toDataPoints(analysis.value?.motionMetrics, m => m.motionIntensity))
  const sceneCutData = computed(() => toDataPoints(analysis.value?.sceneCutMetrics, m => m.cutConfidence))
  const colorCycleData = computed(() => toDataPoints(analysis.value?.colorCycleMetrics, m => m.hueShiftSpeed))
  const explanations = computed(() => analysis.value?.graphExplanations ?? {} as Record<string, string>)

  return { flashData, redFlashData, lumData, motionData, sceneCutData, colorCycleData, explanations }
}
