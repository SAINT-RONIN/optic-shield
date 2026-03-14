<script setup lang="ts">
import { ref } from 'vue'
import ChatInputBar from '@/components/molecules/ChatInputBar.vue'
import MarkdownText from '@/components/atoms/MarkdownText.vue'
import { useChat } from '@/composables/useChat'

const { messages, sendMessage } = useChat()
const chatArea = ref<HTMLElement | null>(null)

function handleSend(message: string): void {
  sendMessage(message)
}

const welcomeMessage = "I'm your video safety assistant. Ask me anything about visual accessibility, or upload a video for analysis."
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
        v-for="(msg, i) in messages"
        :key="msg.timestamp ?? i"
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
          {{ msg.content }}
        </div>
      </div>
    </div>
    <div class="px-6 pb-4">
      <ChatInputBar @send="handleSend" />
    </div>
  </div>
</template>
