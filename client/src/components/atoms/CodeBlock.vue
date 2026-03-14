<script setup lang="ts">
defineProps<{
  code: string
  language?: string
}>()
</script>

<template>
  <div class="bg-surface-code rounded-lg p-3 overflow-x-auto">
    <pre class="text-[11px] leading-relaxed font-mono text-[#E4E2DC]"><code>{{ code }}</code></pre>
  </div>
</template>
