class WSClient {
  constructor() {
    this.ws = null
    this.listeners = []
  }

  connect() {
    const proto = location.protocol === 'https:' ? 'wss' : 'ws'
    const wsUrl = `${proto}://${location.host}/ws/cases`
    this.ws = new WebSocket(wsUrl)
    this.ws.onmessage = e => {
      try {
        const data = JSON.parse(e.data)
        this.listeners.forEach(fn => fn(data))
      } catch {}
    }
    this.ws.onclose = () => setTimeout(() => this.connect(), 3000)
    this.ws.onerror = () => this.ws.close()
  }

  on(fn) { this.listeners.push(fn) }
  off(fn) { this.listeners = this.listeners.filter(l => l !== fn) }
  disconnect() { if (this.ws) this.ws.close() }
}

export const wsClient = new WSClient()
