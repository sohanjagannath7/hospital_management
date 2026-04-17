class WSClient {
  constructor() {
    this.ws = null
    this.listeners = []
  }

  connect() {
    const proto = location.protocol === 'https:' ? 'wss' : 'ws'
    this.ws = new WebSocket(`${proto}://${location.host}/ws/cases`)
    this.ws.onmessage = (e) => {
      const data = JSON.parse(e.data)
      this.listeners.forEach(fn => fn(data))
    }
    this.ws.onclose = () => setTimeout(() => this.connect(), 3000)
  }

  on(fn) { this.listeners.push(fn) }
  off(fn) { this.listeners = this.listeners.filter(l => l !== fn) }

  disconnect() {
    if (this.ws) this.ws.close()
  }
}

export const wsClient = new WSClient()
