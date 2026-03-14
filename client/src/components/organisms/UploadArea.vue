<script setup lang="ts">
import { ref } from 'vue'
import { CloudUpload } from 'lucide-vue-next'

const emit = defineEmits<{ 'file-selected': [file: File] }>()

const isDragging = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)

function handleDrop(event: DragEvent): void {
  isDragging.value = false
  const file = event.dataTransfer?.files[0]
  if (file) emit('file-selected', file)
}

function handleFileChange(event: Event): void {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) emit('file-selected', file)
}
</script>

<template>
  <div
    :class="[
      'max-w-md mx-auto p-6 border-2 border-dashed rounded-[16px] text-center cursor-pointer transition-all',
      isDragging
        ? 'border-brand-purple bg-brand-purple/8 border-solid'
        : 'border-brand-purple/20 bg-brand-purple/[0.03] hover:border-brand-purple/40 hover:bg-brand-purple/[0.06]'
    ]"
    @dragover.prevent="isDragging = true"
    @dragleave="isDragging = false"
    @drop.prevent="handleDrop"
    @click="fileInput?.click()"
  >
    <CloudUpload :size="32" class="mx-auto text-brand-purple mb-2" />
    <p class="text-sm font-semibold text-text-primary">Drop a video to analyze</p>
    <p class="text-xs text-text-tertiary mt-1">or click to browse · MP4, MOV, WebM · Max 5 min</p>
    <input ref="fileInput" type="file" accept="video/*" class="hidden" @change="handleFileChange" />
  </div>
</template>
