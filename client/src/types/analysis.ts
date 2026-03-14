export interface TimestampedMetric {
  timestamp: number
  value: number
}

export interface FlashMetric extends TimestampedMetric {
  flashCountPerSecond: number
}

export interface RedFlashMetric extends TimestampedMetric {
  redFlashIntensity: number
}

export interface LuminanceMetric extends TimestampedMetric {
  avgLuminance: number
}

export interface LuminanceTransitionMetric extends TimestampedMetric {
  delta: number
}

export interface MotionMetric extends TimestampedMetric {
  motionIntensity: number
}

export interface SceneCutMetric extends TimestampedMetric {
  cutConfidence: number
}

export interface ColorCycleMetric extends TimestampedMetric {
  hueShiftSpeed: number
}

export interface PatternRegion {
  x: number
  y: number
  width: number
  height: number
}

export interface PatternMetric extends TimestampedMetric {
  patternScore: number
  flaggedRegions: PatternRegion[]
}

export interface DangerZone {
  startTime: number
  endTime: number
  severity: 'low' | 'medium' | 'high' | 'critical'
  reason: string
}

export interface VideoMetadata {
  filename: string
  duration: number
  fps: number
  width: number
  height: number
  fileSizeBytes: number
}

export interface AnalysisResult {
  videoId: string
  videoMetadata: VideoMetadata
  safetyScore: number
  verdict: string
  flashMetrics: FlashMetric[]
  redFlashMetrics: RedFlashMetric[]
  luminanceMetrics: LuminanceMetric[]
  luminanceTransitions: LuminanceTransitionMetric[]
  motionMetrics: MotionMetric[]
  sceneCutMetrics: SceneCutMetric[]
  colorCycleMetrics: ColorCycleMetric[]
  patternMetrics: PatternMetric[]
  dangerZones: DangerZone[]
  aiReport: string | null
  graphExplanations: Record<string, string>
}

export interface AnalysisProgress {
  videoId: string
  stage: string
  progress: number
  currentFrame: number
  totalFrames: number
  message: string
}
