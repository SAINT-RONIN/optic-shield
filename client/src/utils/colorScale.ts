import { SAFE_SCORE_THRESHOLD, WARNING_SCORE_THRESHOLD, CRITICAL_SCORE_THRESHOLD } from './constants'

const COLORS = {
  safe: '#00C9A7',
  warning: '#FFB020',
  danger: '#F04E98',
  critical: '#E53E3E',
  info: '#5B8DEF',
  neutral: '#9D97B5'
} as const

export function getScoreColor(score: number): string {
  if (score >= SAFE_SCORE_THRESHOLD) return COLORS.safe
  if (score >= WARNING_SCORE_THRESHOLD) return COLORS.warning
  if (score >= CRITICAL_SCORE_THRESHOLD) return COLORS.danger
  return COLORS.critical
}

export function getSeverityColor(severity: string): string {
  const map: Record<string, string> = {
    low: COLORS.safe,
    medium: COLORS.warning,
    high: COLORS.danger,
    critical: COLORS.critical
  }
  return map[severity] ?? COLORS.neutral
}
