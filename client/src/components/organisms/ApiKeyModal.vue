<script setup lang="ts">
import { ref } from 'vue'
import GradientButton from '@/components/atoms/GradientButton.vue'
import InputField from '@/components/atoms/InputField.vue'
import { useApiKey } from '@/composables/useApiKey'

const props = defineProps<{ isOpen: boolean }>()
const emit = defineEmits<{ close: [] }>()

const { setKey } = useApiKey()
const keyInput = ref('')

function handleSubmit(): void {
  if (keyInput.value.trim()) {
    setKey(keyInput.value.trim())
    emit('close')
  }
}
</script>

<template>
  <Teleport to="body">
    <div v-if="props.isOpen" class="fixed inset-0 z-50 flex items-center justify-center">
      <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="emit('close')" />
      <div class="relative bg-white rounded-[20px] p-7 w-[420px] shadow-[0_8px_40px_rgba(80,60,120,0.10)]">
        <h2 class="text-lg font-bold text-text-primary">Enter your API key</h2>
        <p class="text-[13px] text-text-secondary mt-1 leading-relaxed">Your key is used for AI features and is never stored permanently.</p>
        <div class="mt-4">
          <InputField v-model="keyInput" placeholder="sk-ant-..." type="password" />
        </div>
        <p class="text-[11px] text-text-tertiary mt-2">Your key is never stored. It lives in session memory only.</p>
        <div class="mt-4">
          <GradientButton label="Connect" size="lg" @click="handleSubmit" />
        </div>
      </div>
    </div>
  </Teleport>
</template>
