import { storeToRefs } from 'pinia'
import { usePlayerStore } from '@/stores/playerStore'

export function useVideoPlayer() {
  const store = usePlayerStore()
  const { currentTime, duration, isPlaying, volume } = storeToRefs(store)

  function play(): void { store.setPlaying(true) }
  function pause(): void { store.setPlaying(false) }
  function seek(time: number): void { store.setCurrentTime(time) }
  function togglePlay(): void { store.setPlaying(!isPlaying.value) }

  return { currentTime, duration, isPlaying, volume, play, pause, seek, togglePlay }
}
