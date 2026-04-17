class WSClient {
  constructor() {
    this.ws = null
    this.listeners = []
  }

  connect() {
    const apiUrl = import.meta.env.VITE_API_URL
    let wsUrl
    if (apiUrl) {
      wsUrl = apiUrl.replace(/^http/, 'ws') + '/ws/cases'
    } else {
      const proto = location.protocol === 'https:' ? 'wss' : 'ws'
      wsUrl = `${proto}://${location.host}/ws/cases`
    }
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
