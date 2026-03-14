<script setup lang="ts">
defineProps<{ active: boolean }>()
</script>

<template>
  <div
    v-if="active"
    class="absolute inset-0 rounded-[16px] pointer-events-none z-10 border-2 border-danger/60 animate-[danger-pulse_0.5s_ease-in-out_infinite_alternate]"
    style="box-shadow: inset 0 0 30px rgba(240, 78, 152, 0.1)"
  />
</template>
