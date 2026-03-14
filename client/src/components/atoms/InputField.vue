<script setup lang="ts">
defineProps<{
  modelValue: string
  placeholder?: string
  type?: string
}>()

defineEmits<{ 'update:modelValue': [value: string] }>()
</script>

<template>
  <input
    :value="modelValue"
    :type="type ?? 'text'"
    :placeholder="placeholder"
    class="w-full bg-surface-input rounded-[12px] px-4 py-2.5 text-sm text-text-primary placeholder:text-text-tertiary outline-none border border-transparent focus:border-border-focus transition-colors"
    @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
  />
</template>
