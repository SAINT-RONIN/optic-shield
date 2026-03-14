import { ACCEPTED_VIDEO_TYPES, MAX_FILE_SIZE_BYTES } from './constants'

const YOUTUBE_URL_PATTERN = /^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)[\w-]+/

export function isValidVideoFile(file: File): boolean {
  return ACCEPTED_VIDEO_TYPES.includes(file.type) && file.size <= MAX_FILE_SIZE_BYTES
}

export function isValidYouTubeUrl(url: string): boolean {
  return YOUTUBE_URL_PATTERN.test(url)
}

export function isValidApiKey(key: string): boolean {
  return key.length >= 10 && key.startsWith('sk-')
}
