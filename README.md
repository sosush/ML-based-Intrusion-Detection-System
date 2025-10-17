# 🛡️ ML-Based Intrusion Detection System  

A hybrid **Machine Learning and Deep Learning-based Intrusion Detection System (IDS)** designed to detect, classify, and predict network intrusions using the **CIC-IDS2017 dataset**.  
It includes real-time traffic monitoring, live alert visualization, and anomaly detection through a **frontend-backend-agent architecture**.

---

## 🚀 Features

- 🧠 **ML/DL-based detection** using trained models on CIC-IDS2017.  
- 🔍 **Live network capture** via `pyshark`.  
- ⚡ **Real-time alert streaming** over WebSocket.  
- 📊 **Frontend visualization** with timeline graph and collapsible alerts.  
- 🔒 **Anomaly detection** that triggers only when traffic patterns deviate from normal.  
- 📁 **CIC-IDS2017 dataset pre-included** via GitHub Releases for reproducibility.

---

## 🧩 Project Structure

```
ML-based-Intrusion-Detection-System/
│
├── backend/
│   ├── agent_capture.py
│   ├── agent_capture_demo.py
│   ├── utils.py
│   ├── main.py              # Flask / FastAPI backend
│   ├── model.pkl            # Trained ML/DL model
│   └── scaler.pkl           # Fitted StandardScaler
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── LiveAlerts.jsx
│   │   │   ├── Timeline.jsx
│   │   │   └── Navbar.jsx
│   │   ├── App.jsx
│   │   └── index.js
│   ├── package.json
│   └── tailwind.config.js
│
├── data/                    # Optional local dataset folder
├── README.md
└── requirements.txt
```

---

## 🧠 Dataset (CIC-IDS2017)

The **CIC-IDS2017** dataset is available in the **[GitHub Releases](../../releases)** section of this repository.  
Download and place it under the `data/` directory before training or testing.  
You do **not** need to manually extract or preprocess anything — the backend handles it automatically.

---

## ⚙️ Setup Guide

### 🐍 1. Create and Activate Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate     # Windows
```

### 📦 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 🧠 3. Run the Backend

```bash
cd backend
python3 main.py
```

- Starts the WebSocket + Flask/FastAPI backend.  
- Default WebSocket URL: `ws://127.0.0.1:8000/ws/agent`.

### 🔎 4. Run the Agent for Live Capture

```bash
sudo python3 agent_capture.py
```

This will:
- Start capturing live packets on your interface (`en0` by default).  
- Aggregate packets every 10 seconds.  
- Send **“Normal Traffic”** alert once initially.  
- Detect anomalies and stream them live to the backend.

### 🧪 5. (Optional) Run Demo Mode

For testing without live packets:

```bash
python3 agent_capture_demo.py
```

This simulates normal and abnormal traffic patterns for presentation/demo purposes.

---

## 💻 Frontend Setup

```bash
cd frontend
npm install
npm start
```

This launches the React dashboard at `http://localhost:3000` with:
- **Live Alerts Panel** (first 6 alerts shown, rest hidden under dropdown).  
- **Timeline Graph** showing traffic spikes when anomalies occur.  

---

## 📈 Live Alert Behavior

- **Normal Traffic** → Shown once until anomaly detected.  
- **Anomalous Activity** → Triggers spikes on timeline and alert cards.  
- **Post-Anomaly** → Returns to “Normal Traffic” alert once before silence.  

---

## 🧰 Troubleshooting

| Issue | Fix |
|-------|-----|
| `invalid literal for int()` | Some boolean fields weren’t numeric — safe to ignore or update `extract_features_from_packet()` |
| `unknown src_ip` | Depends on local interface capture visibility; may show unknown if packets lack IP layer |
| `WS connection failed` | Ensure backend (`main.py`) is running before agent |
| Permission denied | Run `sudo python3 agent_capture.py` for live capture |

---

## 📡 Testing Intrusion Alerts (Demo Mode)

You can test anomaly alerts manually with:

```bash
python3 agent_capture_demo.py
```

- Generates periodic “Normal Traffic” messages.  
- Simulates random anomalies like DDoS/Port Scan every few seconds.  
- Displays live graph spikes on frontend.

---

## 🧩 Example Alert (JSON)

```json
{
  "alert_type": "Possible DDoS",
  "src_ip": "192.168.1.24",
  "description": "High backward traffic detected",
  "timestamp": 1728824425.93532
}
```

---

## 🤖 Tech Stack

| Layer | Technology |
|-------|-------------|
| Backend | Python (Flask / FastAPI), WebSockets |
| Agent | PyShark, AsyncIO, Threading |
| Frontend | React, TailwindCSS, Chart.js |
| ML/DL | Scikit-Learn, TensorFlow / Keras |
| Dataset | CIC-IDS2017 |

---

## 🧑‍💻 Contributing

1. Fork this repo  
2. Create a new branch (`feature/my-feature`)  
3. Commit your changes  
4. Push and create a PR 🎉  

---

## 📜 License

This project is released under the **MIT License**.  
You are free to modify and distribute with attribution.

---

✅ **Ready-to-Run Summary**
```bash
# 1️⃣ Clone the repo
git clone https://github.com/sosush/ML-based-Intrusion-Detection-System.git
cd ML-based-Intrusion-Detection-System

# 2️⃣ Install backend deps
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py

# 3️⃣ Start the agent
sudo python3 agent_capture.py

# 4️⃣ Launch frontend
cd ../frontend
npm install
npm start
```
