<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { OrbScene } from '@/utils/orbScene'
import type { OrbState } from '@/utils/orbScene'

const props = defineProps<{
  size?: 'lg' | 'md' | 'sm'
  state?: OrbState
}>()

const containerRef = ref<HTMLElement | null>(null)
let orbScene: OrbScene | null = null

const sizeMap: Record<string, string> = {
  lg: 'w-[180px] h-[180px]',
  md: 'w-12 h-12',
  sm: 'w-9 h-9',
}

const sizeClass = ref(sizeMap[props.size ?? 'lg'])

onMounted(() => {
  if (containerRef.value) {
    orbScene = new OrbScene(containerRef.value)
    orbScene.setState(props.state ?? 'idle')
  }
})

onUnmounted(() => {
  orbScene?.dispose()
  orbScene = null
})

watch(() => props.state, (newState) => {
  orbScene?.setState(newState ?? 'idle')
})

watch(() => props.size, (newSize) => {
  sizeClass.value = sizeMap[newSize ?? 'lg']
  if (containerRef.value && orbScene) {
    const w = containerRef.value.clientWidth
    const h = containerRef.value.clientHeight
    orbScene.resize(w, h)
  }
})
</script>

<template>
  <div ref="containerRef" :class="['rounded-full overflow-hidden', sizeClass]" />
</template>
