import time
import asyncio
import websockets
import json
import random

WS_URL = "ws://127.0.0.1:8000/ws/agent"

# Global traffic state
traffic_state = "normal"

# Predefined demo alerts
demo_alerts = [
    {"alert_type": "Normal Traffic", "description": "No intrusion detected"},
    {"alert_type": "Possible Port Scan", "description": "High number of forward packets"},
    {"alert_type": "Possible DDoS", "description": "High backward traffic detected"},
]

async def send_demo_ws():
    global traffic_state
    async with websockets.connect(WS_URL) as ws:
        print(f"[INFO] Connected to backend WS for demo at {WS_URL}")
        while True:
            # Randomly pick a demo alert (simulate normal vs abnormal)
            alert = random.choice(demo_alerts)
            alert["timestamp"] = time.time()

            # Stateful alerting
            if alert["alert_type"] == "Normal Traffic":
                if traffic_state == "normal":
                    await asyncio.sleep(2)  # skip repeated normal
                    continue
                else:
                    traffic_state = "normal"
                    await ws.send(json.dumps(alert))
                    print("[DEMO] Sent alert:", alert)
            else:
                traffic_state = "abnormal"
                await ws.send(json.dumps(alert))
                print("[DEMO] Sent alert:", alert)

            await asyncio.sleep(2)  # adjust time between alerts

if __name__ == "__main__":
    asyncio.run(send_demo_ws())
