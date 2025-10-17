import React, { useEffect, useState } from "react";
import { connectWebSocket } from "../utils/websocket";

function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [showMore, setShowMore] = useState(false);

  useEffect(() => {
    connectWebSocket((data) => {
      setAlerts((prev) => [data, ...prev]); // prepend new alert
    });
  }, []);

  const toggleShowMore = () => setShowMore((prev) => !prev);

  const firstAlerts = alerts.slice(0, 6);
  const remainingAlerts = alerts.slice(6);

  return (
    <div className="w-full p-4 border rounded">
      <h2 className="text-2xl font-semibold mb-2">Live Alerts</h2>
      {alerts.length === 0 ? (
        <p>No alerts yet</p>
      ) : (
        <>
          <ul className="space-y-2">
            {firstAlerts.map((alert, idx) => (
              <li
                key={idx}
                className={`p-2 rounded ${
                  alert.alert_type === "Normal Traffic"
                    ? "bg-green-100 text-green-800"
                    : "bg-red-100 text-red-800"
                }`}
              >
                <strong>{alert.alert_type}</strong> - {alert.description}{" "}
                {/* src_ip: {alert.src_ip} */}
                <br />
                <small>{new Date(alert.timestamp * 1000).toLocaleTimeString()}</small>
              </li>
            ))}
          </ul>

          {remainingAlerts.length > 0 && (
            <div className="mt-2">
              <button
                onClick={toggleShowMore}
                className="text-blue-500 hover:underline"
              >
                {showMore ? "Hide older alerts ▲" : `Show ${remainingAlerts.length} more alerts ▼`}
              </button>
              {showMore && (
                <ul className="mt-2 space-y-2">
                  {remainingAlerts.map((alert, idx) => (
                    <li
                      key={idx}
                      className={`p-2 rounded ${
                        alert.alert_type === "Normal Traffic"
                          ? "bg-green-100 text-green-800"
                          : "bg-red-100 text-red-800"
                      }`}
                    >
                      <strong>{alert.alert_type}</strong> - {alert.description}{" "}
                      {/* src_ip: {alert.src_ip} */}
                      <br />
                      <small>{new Date(alert.timestamp * 1000).toLocaleTimeString()}</small>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default Alerts;
