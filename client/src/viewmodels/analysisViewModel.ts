import type { TimestampedMetric } from '@/types/analysis'
import { getScoreColor } from '@/utils/colorScale'
import { SAFE_SCORE_THRESHOLD, WARNING_SCORE_THRESHOLD } from '@/utils/constants'

export interface ChartData {
  labels: number[]
  values: number[]
}

export function toChartData(metrics: TimestampedMetric[]): ChartData {
  return {
    labels: metrics.map(m => m.timestamp),
    values: metrics.map(m => m.value)
  }
}

export function toSafetyVerdict(score: number): { label: string; color: string } {
  if (score >= SAFE_SCORE_THRESHOLD) return { label: 'Safe — no issues detected', color: getScoreColor(score) }
  if (score >= WARNING_SCORE_THRESHOLD) return { label: 'Caution — needs review', color: getScoreColor(score) }
  return { label: 'Unsafe — immediate fixes needed', color: getScoreColor(score) }
}
