import type { ChatMessage } from '@/types/chat'
import { formatTime } from '@/utils/formatters'

export interface FormattedMessage {
  content: string
  isUser: boolean
  time: string
}

export function formatMessage(message: ChatMessage): FormattedMessage {
  return {
    content: message.content,
    isUser: message.role === 'user',
    time: message.timestamp ? formatTime(message.timestamp) : ''
  }
}
