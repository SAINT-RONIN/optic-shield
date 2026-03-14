<script setup lang="ts">
import { computed } from 'vue'
import { marked } from 'marked'

const props = defineProps<{ content: string }>()

const html = computed(() => marked.parse(props.content) as string)
</script>

<template>
  <div class="prose prose-sm text-text-secondary text-[13px] leading-relaxed" v-html="html" />
</template>
