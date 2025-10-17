import pyshark
import time
import asyncio
import websockets
import json
from utils import extract_features_from_packet, aggregate_window
from queue import Queue
import threading

# -----------------------
# CONFIG
# -----------------------
WS_URL = "ws://127.0.0.1:8000/ws/agent"
TSHARK_IFACE = "en0"  # your live network interface
WINDOW = 10  # aggregation window in seconds

# -----------------------
# THREAD-SAFE QUEUE
# -----------------------
packet_queue = Queue()

# -----------------------
# HELPER: Create human-readable alert
# -----------------------
def create_alert_from_features(features: dict):
    """
    Convert aggregated features into a meaningful alert dictionary.
    Customize thresholds based on your needs.
    """
    # Example logic
    if features.get("total fwd packets", 0) > 1000:
        alert_type = "Possible Port Scan"
        description = "High number of forward packets"
    elif features.get("total backward packets", 0) > 500:
        alert_type = "Possible DDoS"
        description = "High backward traffic detected"
    else:
        alert_type = "Normal Traffic"
        description = "No intrusion detected"

    return {
        "alert_type": alert_type,
        "src_ip": features.get("src_ip", "unknown"),
        "description": description,
        "timestamp": time.time()
    }

# -----------------------
# PACKET CAPTURE
# -----------------------
def capture_packets():
    """Capture live packets and push aggregated features to the queue."""
    print(f"[INFO] Starting live capture on interface: {TSHARK_IFACE}")
    capture = pyshark.LiveCapture(interface=TSHARK_IFACE)
    window = []
    last_time = time.time()

    for pkt in capture.sniff_continuously():
        # Extract features
        features = extract_features_from_packet(pkt)
        if features:
            window.append(features)

        # Aggregate every WINDOW seconds
        if time.time() - last_time >= WINDOW:
            agg = aggregate_window(window)
            if agg:
                packet_queue.put(agg)
            window = []
            last_time = time.time()

# -----------------------
# WEBSOCKET SENDER
# -----------------------
async def send_ws():
    """Send alerts to backend via WebSocket."""
    traffic_state = None  # None, "normal", or "abnormal"
    
    while True:
        try:
            async with websockets.connect(WS_URL) as ws:
                print(f"[INFO] Connected to backend WebSocket at {WS_URL}")
                while True:
                    if not packet_queue.empty():
                        agg = packet_queue.get()
                        alert = create_alert_from_features(agg)

                        # Logic to send normal alert only once until abnormal traffic
                        if alert["alert_type"] == "Normal Traffic":
                            if traffic_state != "normal":
                                await ws.send(json.dumps(alert))
                                print("[INFO] Sent alert:", alert)
                                traffic_state = "normal"
                            # else: skip sending repeated normal alerts
                        else:
                            # Always send abnormal alerts
                            await ws.send(json.dumps(alert))
                            print("[INFO] Sent alert:", alert)
                            traffic_state = "abnormal"
                    await asyncio.sleep(0.1)
        except Exception as e:
            print(f"[ERROR] WS connection failed, retrying in 5s: {e}")
            await asyncio.sleep(5)

# -----------------------
# MAIN
# -----------------------
if __name__ == "__main__":
    # Start packet capture in a separate thread
    capture_thread = threading.Thread(target=capture_packets, daemon=True)
    capture_thread.start()

    # Run websocket sender in main asyncio loop
    asyncio.run(send_ws())
