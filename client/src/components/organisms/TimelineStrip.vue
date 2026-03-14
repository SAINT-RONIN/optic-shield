<script setup lang="ts">
const segments = [
  { flex: 3, type: 'safe' },
  { flex: 1, type: 'warning' },
  { flex: 2, type: 'safe' },
  { flex: 1, type: 'danger' },
  { flex: 3, type: 'safe' }
]

const segmentStyles: Record<string, string> = {
  safe: 'background: linear-gradient(135deg, #00C9A7, #40E8C8)',
  warning: 'background: linear-gradient(135deg, #FFB020, #FFD060)',
  danger: 'background: linear-gradient(135deg, #F04E98, #FF6BAA)'
}
</script>

<template>
  <div class="glass-card p-3.5">
    <div class="text-[11px] font-semibold text-text-tertiary mb-2 tracking-wide">TIMELINE RISK</div>
    <div class="flex gap-0.5 h-2">
      <div
        v-for="(seg, i) in segments"
        :key="i"
        class="rounded-[4px]"
        :style="[segmentStyles[seg.type], `flex: ${seg.flex}`]"
      />
    </div>
    <div class="flex justify-between mt-1.5">
      <span class="text-[8px] font-medium text-text-tertiary">0:00</span>
      <span class="text-[8px] font-medium text-text-tertiary">End</span>
    </div>
  </div>
</template>
