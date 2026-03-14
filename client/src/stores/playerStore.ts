import { ref } from 'vue'
import { defineStore } from 'pinia'

export const usePlayerStore = defineStore('player', () => {
  const currentTime = ref(0)
  const duration = ref(0)
  const isPlaying = ref(false)
  const volume = ref(1)

  function setCurrentTime(time: number): void {
    currentTime.value = time
  }

  function setDuration(d: number): void {
    duration.value = d
  }

  function setPlaying(playing: boolean): void {
    isPlaying.value = playing
  }

  function setVolume(v: number): void {
    volume.value = v
  }

  return { currentTime, duration, isPlaying, volume, setCurrentTime, setDuration, setPlaying, setVolume }
})
