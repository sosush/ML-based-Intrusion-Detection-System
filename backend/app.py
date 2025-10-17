import os
import joblib
import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from utils import FEATURE_ORDER, preprocess_features

# -----------------------------
# FASTAPI SETUP
# -----------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins for frontend
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# LOAD MODELS & SCALER
# -----------------------------
MODELS_DIR = "models"
try:
    rf_model = joblib.load(os.path.join(MODELS_DIR, "rf_model.joblib"))
    xgb_model = joblib.load(os.path.join(MODELS_DIR, "xgb_model.joblib"))
    scaler = joblib.load(os.path.join(MODELS_DIR, "scaler.joblib"))
except FileNotFoundError as e:
    raise FileNotFoundError(
        f"Missing model/scaler file: {e.filename}. Make sure models exist in {MODELS_DIR}"
    )

# -----------------------------
# PREDICTION FUNCTION
# -----------------------------
def predict_intrusion(features: dict):
    """Accepts dict of features, preprocesses, scales, and predicts."""
    processed = preprocess_features(features, scaler)
    rf_pred = rf_model.predict(processed)
    xgb_pred = xgb_model.predict(processed)
    return {"rf_pred": rf_pred.tolist(), "xgb_pred": xgb_pred.tolist()}

# -----------------------------
# MANUAL FEATURE PREDICTION
# -----------------------------
@app.post("/predict")
async def manual_predict(features: dict):
    if "features" not in features:
        return JSONResponse(content={"error": "Missing 'features' key"}, status_code=400)
    preds = predict_intrusion(features["features"])
    return JSONResponse(content=preds)

# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get("/health")
async def health():
    return {"status": "ok"}

# -----------------------------
# LIVE WEBSOCKET
# -----------------------------
frontend_clients = set()
agent_client = None

@app.websocket("/ws/frontend")
async def frontend_ws(ws: WebSocket):
    await ws.accept()
    frontend_clients.add(ws)
    print(f"[INFO] Frontend connected: {ws.client}")
    try:
        while True:
            await asyncio.sleep(1)  # keep connection alive
    except WebSocketDisconnect:
        print(f"[INFO] Frontend disconnected: {ws.client}")
        frontend_clients.remove(ws)


# -----------------------------
# LIVE WEBSOCKET
# -----------------------------
frontend_clients = set()
agent_client = None

@app.websocket("/ws/frontend")
async def frontend_ws(ws: WebSocket):
    await ws.accept()
    frontend_clients.add(ws)
    print(f"[INFO] Frontend connected: {ws.client}")
    try:
        while True:
            await asyncio.sleep(1)  # keep connection alive
    except WebSocketDisconnect:
        print(f"[INFO] Frontend disconnected: {ws.client}")
        frontend_clients.remove(ws)

@app.websocket("/ws/agent")
async def agent_ws(ws: WebSocket):
    await ws.accept()
    global agent_client
    agent_client = ws
    print(f"[INFO] Agent connected: {ws.client}")

    try:
        while True:
            data = await ws.receive_text()  # receive alert from agent
            print("[DEBUG] Received from agent:", data)

            # Broadcast to all connected frontend clients
            disconnected = []
            for client in frontend_clients:
                try:
                    await client.send_text(data)  # data is already JSON string
                    print(f"[DEBUG] Sent to frontend {client.client}: {str(data)[:100]}...")
                except WebSocketDisconnect:
                    disconnected.append(client)
            # Remove disconnected frontends
            for d in disconnected:
                frontend_clients.remove(d)

    except WebSocketDisconnect:
        print(f"[INFO] Agent disconnected: {ws.client}")
        agent_client = None
    except Exception as e:
        print(f"[ERROR] WS error: {e}")
        agent_client = None
        await ws.close()





# -----------------------------
# START SERVER
# -----------------------------
if __name__ == "__main__":
    import uvicorn
    print("[INFO] Starting FastAPI backend on http://127.0.0.1:8000")
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
