<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import ChatInputBar from '@/components/molecules/ChatInputBar.vue'
import MarkdownText from '@/components/atoms/MarkdownText.vue'
import Spinner from '@/components/atoms/Spinner.vue'
import AnalysisProgressVue from '@/components/organisms/AnalysisProgress.vue'
import { useChat } from '@/composables/useChat'
import { useAnalysis } from '@/composables/useAnalysis'

const { messages, isLoading, error, sendMessage } = useChat()
const { isAnalyzing, progress } = useAnalysis()
const chatArea = ref<HTMLElement | null>(null)

async function handleSend(message: string): Promise<void> {
  await sendMessage(message)
}

async function scrollToBottom(): Promise<void> {
  await nextTick()
  if (chatArea.value) {
    const last = chatArea.value.lastElementChild
    last?.scrollIntoView({ behavior: 'smooth', block: 'end' })
  }
}

watch(messages, scrollToBottom, { deep: true })

const welcomeMessage =
  "I'm your video safety assistant. Ask me anything about visual accessibility, or upload a video for analysis."
</script>

<template>
  <div class="flex flex-col h-full">
    <div ref="chatArea" class="flex-1 overflow-y-auto px-6 py-4 space-y-4">
      <div v-if="messages.length === 0" class="flex items-start gap-3">
        <div class="bg-brand-purple/5 rounded-[14px] rounded-bl-[4px] px-4 py-2.5 max-w-[88%]">
          <MarkdownText :content="welcomeMessage" />
        </div>
      </div>

      <div
        v-for="msg in messages"
        :key="msg.timestamp ?? msg.content"
        :class="msg.role === 'user' ? 'flex justify-end' : 'flex justify-start'"
      >
        <div
          :class="[
            'px-4 py-2.5 max-w-[85%] text-[12.5px] leading-relaxed',
            msg.role === 'user'
              ? 'bg-brand-gradient text-white rounded-[14px] rounded-br-[4px]'
              : 'bg-brand-purple/5 text-text-primary rounded-[14px] rounded-bl-[4px]'
          ]"
        >
          <MarkdownText v-if="msg.role === 'assistant'" :content="msg.content" />
          <span v-else>{{ msg.content }}</span>
        </div>
      </div>

      <div v-if="isAnalyzing && progress" class="flex justify-start">
        <AnalysisProgressVue :progress="progress" />
      </div>

      <div v-if="isLoading" class="flex justify-start">
        <div class="bg-brand-purple/5 rounded-[14px] rounded-bl-[4px] px-4 py-3">
          <Spinner size="sm" />
        </div>
      </div>

      <div v-if="error" class="flex justify-start">
        <div class="bg-red-50 border border-red-200 text-red-600 rounded-[14px] rounded-bl-[4px] px-4 py-2.5 max-w-[85%] text-[12.5px] leading-relaxed">
          {{ error }}
        </div>
      </div>
    </div>

    <div class="px-6 pb-4">
      <ChatInputBar :disabled="isLoading" @send="handleSend" />
    </div>
  </div>
</template>
