import type { AnalysisProgress } from '@/types/analysis'

type ProgressCallback = (progress: AnalysisProgress) => void

const RECONNECT_DELAY_MS = 2000

export class SocketService {
  private ws: WebSocket | null = null
  private callbacks: ProgressCallback[] = []
  private currentUrl: string | null = null
  private hasReconnected = false

  connect(url: string): void {
    this.currentUrl = url
    this.hasReconnected = false
    this.createSocket(url)
  }

  private createSocket(url: string): void {
    this.ws = new WebSocket(url)

    this.ws.onmessage = (event: MessageEvent) => {
      const data = JSON.parse(String(event.data)) as AnalysisProgress
      this.callbacks.forEach(cb => cb(data))
    }

    this.ws.onerror = () => {
      this.attemptReconnect()
    }

    this.ws.onclose = (event: CloseEvent) => {
      if (!event.wasClean) {
        this.attemptReconnect()
      }
    }
  }

  private attemptReconnect(): void {
    if (this.hasReconnected || !this.currentUrl) return
    this.hasReconnected = true
    const url = this.currentUrl
    setTimeout(() => {
      this.createSocket(url)
    }, RECONNECT_DELAY_MS)
  }

  disconnect(): void {
    this.currentUrl = null
    this.hasReconnected = true
    this.ws?.close()
    this.ws = null
    this.callbacks = []
  }

  onProgress(callback: ProgressCallback): void {
    this.callbacks.push(callback)
  }
}

export const socketService = new SocketService()
