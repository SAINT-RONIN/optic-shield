import type { AnalysisProgress } from '@/types/analysis'

type ProgressCallback = (progress: AnalysisProgress) => void

export class SocketService {
  private ws: WebSocket | null = null
  private callbacks: ProgressCallback[] = []

  connect(url: string): void {
    this.ws = new WebSocket(url)
    this.ws.onmessage = (event: MessageEvent) => {
      const data = JSON.parse(String(event.data)) as AnalysisProgress
      this.callbacks.forEach(cb => cb(data))
    }
  }

  disconnect(): void {
    this.ws?.close()
    this.ws = null
  }

  onProgress(callback: ProgressCallback): void {
    this.callbacks.push(callback)
  }
}

export const socketService = new SocketService()
