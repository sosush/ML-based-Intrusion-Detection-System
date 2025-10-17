import numpy as np
from collections import Counter

# Full 78-feature order (replace/add real features from your training dataset)
FEATURE_ORDER = [
    "destination port",
    "flow duration",
    "total fwd packets",
    "total backward packets",
    "total length of fwd packets",
    "total length of bwd packets",
    "fwd packet length max",
    "fwd packet length min",
    "fwd packet length mean",
    "fwd packet length std",
    "bwd packet length max",
    "bwd packet length min",
    "bwd packet length mean",
    "bwd packet length std",
    "flow bytes/s",
    "flow packets/s",
    "flow iat mean",
    "flow iat std",
    "flow iat max",
    "flow iat min",
    "fwd iat total",
    "fwd iat mean",
    "fwd iat std",
    "fwd iat max",
    "fwd iat min",
    "bwd iat total",
    "bwd iat mean",
    "bwd iat std",
    "bwd iat max",
    "bwd iat min",
    "fwd psh flags",
    "bwd psh flags",
    "fwd urg flags",
    "bwd urg flags",
    "fwd header length",
    "bwd header length",
    "fwd packets/s",
    "bwd packets/s",
    "min packet length",
    "max packet length",
    "packet length mean",
    "packet length std",
    "packet length variance",
    "fin flag count",
    "syn flag count",
    "rst flag count",
    "psh flag count",
    "ack flag count",
    "urg flag count",
    "cwe flag count",
    "ece flag count",
    "down/up ratio",
    "average packet size",
    "avg fwd segment size",
    "avg bwd segment size",
    "fwd header length.1",
    "fwd avg bytes/bulk",
    "fwd avg packets/bulk",
    "fwd avg bulk rate",
    "bwd avg bytes/bulk",
    "bwd avg packets/bulk",
    "bwd avg bulk rate",
    "subflow fwd packets",
    "subflow fwd bytes",
    "subflow bwd packets",
    "subflow bwd bytes",
    "init_win_bytes_forward",
    "init_win_bytes_backward",
    "act_data_pkt_fwd",
    "min_seg_size_forward",
    "active mean",
    "active std",
    "active max",
    "active min",
    "idle mean",
    "idle std",
    "idle max",
    "idle min",
] + [f"f{i}" for i in range(72)]  # 72 zero-padded features for now

def extract_features_from_packet(pkt):
    """
    Extracts features from a single packet and returns a dict.
    """
    features = {}
    try:
        features["duration"] = getattr(pkt, "duration", 0.01)
        features["tot_bytes"] = int(getattr(pkt, "length", 0))
        features["tot_packets"] = 1

        # TCP info
        if hasattr(pkt, "tcp"):
            features["src_port"] = int(getattr(pkt.tcp, "srcport", 0))
            features["dst_port"] = int(getattr(pkt.tcp, "dstport", 0))
            features["src_ip"] = pkt.ip.src if hasattr(pkt, "ip") else "unknown"
            features["dst_ip"] = pkt.ip.dst if hasattr(pkt, "ip") else "unknown"
        else:
            features["src_port"] = 0
            features["dst_port"] = 0
            features["src_ip"] = getattr(pkt, "ip_src", "unknown")
            features["dst_ip"] = getattr(pkt, "ip_dst", "unknown")

        features["protocol"] = 6 if getattr(pkt, "transport_layer", "") == "TCP" else 17
    except Exception as e:
        print(f"[WARN] Could not parse packet: {e}")

    # Zero-fill remaining features
    for f in FEATURE_ORDER:
        if f not in features:
            features[f] = 0



    # Keep consistent order
    ordered_features = {f: features[f] for f in FEATURE_ORDER}
    return ordered_features



def preprocess_features(features: dict, scaler):
    """
    Converts a feature dict to a 78-feature numpy array and scales it.
    """
    X = np.array([features[f] for f in FEATURE_ORDER], dtype=float).reshape(1, -1)
    X_scaled = scaler.transform(X)
    return X_scaled

def aggregate_window(window):
    """
    Aggregates a list of packet dicts into summary statistics
    (mean, std, min, max) for numeric features.
    Also keeps the most common src_ip in the window.
    """
    if not window:
        agg = {f"{f}_mean": 0 for f in FEATURE_ORDER}
        agg.update({f"{f}_std": 0 for f in FEATURE_ORDER})
        agg.update({f"{f}_min": 0 for f in FEATURE_ORDER})
        agg.update({f"{f}_max": 0 for f in FEATURE_ORDER})
        agg["src_ip"] = "unknown"
        return agg

    agg = {}
    # Numeric feature statistics
    for f in FEATURE_ORDER:
        values = [pkt.get(f, 0) for pkt in window]
        agg[f"{f}_mean"] = float(np.mean(values))
        agg[f"{f}_std"] = float(np.std(values))
        agg[f"{f}_min"] = float(np.min(values))
        agg[f"{f}_max"] = float(np.max(values))

    # Most common src_ip in window
    src_ips = [pkt.get("src_ip") for pkt in window if "src_ip" in pkt]
    agg["src_ip"] = Counter(src_ips).most_common(1)[0][0] if src_ips else "unknown"

    return agg
