let socket;
let messageQueue = []; // store messages until connection opens

export const connectWebSocket = (onMessage) => {
  socket = new WebSocket("ws://127.0.0.1:8000/ws/frontend");

  socket.onopen = () => {
    console.log("WebSocket connected, readyState =", socket.readyState);

    // send any queued messages
    while (messageQueue.length > 0) {
      const msg = messageQueue.shift();
      socket.send(JSON.stringify(msg));
    }
  };

  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      console.log("Received WS data:", data);
      onMessage(data); // send data to React components
    } catch (err) {
      console.error("Error parsing WS message:", err);
    }
  };

  socket.onclose = () => {
    console.log("WebSocket disconnected, retrying in 5s...", socket.readyState);
    setTimeout(() => connectWebSocket(onMessage), 5000);
  };

  socket.onerror = (err) => {
    console.error("WebSocket error:", err);
    socket.close();
  };
};

