import numpy as np

EXPECTED_FEATURES = 78

def prepare_packet(packet_data, scaler):
    packet_data = np.array(packet_data).flatten()
    n_features = packet_data.shape[0]

    if n_features > EXPECTED_FEATURES:
        packet_data = packet_data[:EXPECTED_FEATURES]
        print(f"Warning: packet has more features than expected. Truncated to {EXPECTED_FEATURES}.")
    elif n_features < EXPECTED_FEATURES:
        padded = np.zeros(EXPECTED_FEATURES)
        padded[:n_features] = packet_data
        packet_data = padded

    scaled_packet = scaler.transform([packet_data])
    return scaled_packet
