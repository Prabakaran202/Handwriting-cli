class TerminalWebSocket {
  constructor() {
    this.socket = null;
    this.url = "ws://127.0.0.1:8000/ws/terminal";
    this.listeners = new Set();
  }

  connect(onOpen, onClose) {
    this.socket = new WebSocket(this.url);

    this.socket.onopen = () => {
      if (onOpen) onOpen();
    };

    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.listeners.forEach((listener) => listener(data));
    };

    this.socket.onclose = () => {
      if (onClose) onClose();
      // 5 வினாடிகளுக்குப் பிறகு மீண்டும் இணைக்க முயற்சிக்கும் (Auto Reconnect)
      setTimeout(() => this.connect(onOpen, onClose), 5000);
    };
  }

  subscribe(callback) {
    this.listeners.add(callback);
    return () => this.listeners.delete(callback);
  }

  sendStroke(strokeData) {
    if (this.socket?.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify({ type: "stroke", data: strokeData }));
    }
  }

  executeCommand(text) {
    if (this.socket?.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify({ type: "execute", text: text }));
    }
  }

  disconnect() {
    if (this.socket) this.socket.close();
  }
}

export const terminalWS = new TerminalWebSocket();
