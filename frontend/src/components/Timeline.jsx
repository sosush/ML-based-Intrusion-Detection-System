import React, { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { connectWebSocket } from "../utils/websocket";

function Timeline() {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    connectWebSocket((data) => {
      setAlerts((prev) => [...prev, data]);
    });
  }, []);

  // Create graph data for last 1 minute
  const bucketSize = 5; // seconds
  const now = Math.floor(Date.now() / 1000);
  const startTime = now - 60;
  const data = [];

  for (let t = startTime; t <= now; t += bucketSize) {
    const bucketAlerts = alerts.filter(
      (a) =>
        Math.floor(a.timestamp) >= t &&
        Math.floor(a.timestamp) < t + bucketSize
    );

    // Value is 0 for normal traffic, 1 (or # of abnormal alerts) for spikes
    const count = bucketAlerts.filter(
      (a) => a.alert_type !== "Normal Traffic"
    ).length;

    data.push({
      time: new Date(t * 1000).toLocaleTimeString(),
      alerts: count, // spikes only for abnormal alerts
    });
  }

  return (
    <div className="w-full p-4 border rounded">
      <h2 className="text-2xl font-semibold mb-2">Alert Timeline</h2>
      {alerts.length === 0 ? (
        <p>No timeline data yet</p>
      ) : (
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis allowDecimals={false} />
            <Tooltip />
            <Line
              type="monotone"
              dataKey="alerts"
              stroke="#ff4d4f"
              strokeWidth={2}
              dot={{ r: 3 }}
              isAnimationActive={false}
            />
          </LineChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}

export default Timeline;
