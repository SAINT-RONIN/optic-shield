<script setup lang="ts">
import { Download, FileJson } from 'lucide-vue-next'
import { useAnalysisStore } from '@/stores/analysisStore'
import { exportAsJson, exportAsPdf } from '@/utils/reportExport'

const store = useAnalysisStore()

function handlePdf(): void {
  if (store.currentAnalysis) exportAsPdf(store.currentAnalysis)
}

function handleJson(): void {
  if (store.currentAnalysis) exportAsJson(store.currentAnalysis)
}
</script>

<template>
  <div class="flex gap-2">
    <button
      class="flex items-center gap-1.5 px-3 py-1.5 text-[11px] font-semibold text-brand-purple bg-brand-purple/5 rounded-lg hover:bg-brand-purple/10 transition-colors"
      @click="handlePdf"
    >
      <Download :size="14" /> PDF
    </button>
    <button
      class="flex items-center gap-1.5 px-3 py-1.5 text-[11px] font-semibold text-brand-purple bg-brand-purple/5 rounded-lg hover:bg-brand-purple/10 transition-colors"
      @click="handleJson"
    >
      <FileJson :size="14" /> JSON
    </button>
  </div>
</template>
