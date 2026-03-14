<script setup lang="ts">
defineProps<{ isOpen?: boolean }>()
</script>

<template>
  <div
    :class="[
      'h-full overflow-y-auto bg-surface-page transition-transform duration-500',
      isOpen ? 'translate-x-0' : 'translate-x-full'
    ]"
    style="transition-timing-function: cubic-bezier(0.16, 1, 0.3, 1)"
  >
    <div class="p-5 space-y-4">
      <slot />
    </div>
  </div>
</template>
