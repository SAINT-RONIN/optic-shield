export const API_BASE = '/api'
export const WS_BASE = `ws://${window.location.host}/ws`

export const MAX_FILE_SIZE_MB = 100
export const MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
export const ACCEPTED_VIDEO_TYPES = ['video/mp4', 'video/webm', 'video/quicktime']
export const MAX_VIDEO_DURATION_SECONDS = 300

export const SAFE_SCORE_THRESHOLD = 80
export const WARNING_SCORE_THRESHOLD = 50
export const CRITICAL_SCORE_THRESHOLD = 20

export const ANALYSIS_STAGES = [
  'Extracting frames',
  'Detecting flashes',
  'Analyzing luminance',
  'Measuring motion',
  'Detecting patterns',
  'Generating report'
] as const
