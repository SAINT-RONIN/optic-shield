export function timeToPosition(currentTime: number, duration: number, width: number): number {
  if (duration <= 0) return 0
  return (currentTime / duration) * width
}

export function positionToTime(x: number, width: number, duration: number): number {
  if (width <= 0) return 0
  return (x / width) * duration
}
