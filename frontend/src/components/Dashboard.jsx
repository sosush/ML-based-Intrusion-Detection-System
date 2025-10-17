// import React, { useEffect, useState } from "react";
// import { connectWebSocket } from "./utils/websocket";

// function Dashboard() {
//   const [alerts, setAlerts] = useState([]);
//   const [timeline, setTimeline] = useState([]);
//   const [showMoreAlerts, setShowMoreAlerts] = useState(false);
//   const [showMoreTimeline, setShowMoreTimeline] = useState(false);

//   useEffect(() => {
//     connectWebSocket((data) => {
//       setAlerts((prev) => [data, ...prev]);
//       setTimeline((prev) => [data, ...prev]);
//     });
//   }, []);

//   const renderAlertCard = (alert, idx) => (
//     <div
//       key={idx}
//       className="p-4 border rounded shadow-sm hover:shadow-md transition duration-200 bg-white"
//     >
//       <p>
//         <span className="font-semibold">Type:</span> {alert.alert_type}
//       </p>
//       <p>
//         <span className="font-semibold">Description:</span> {alert.description}
//       </p>
//       {/* <p>Src IP: {alert.src_ip}</p> */}
//       <p className="text-gray-400 text-sm">
//         {new Date(alert.timestamp * 1000).toLocaleString()}
//       </p>
//     </div>
//   );

//   const renderTimelineCard = (item, idx) => (
//     <div
//       key={idx}
//       className="p-3 border-l-4 border-blue-400 bg-blue-50 rounded shadow-sm"
//     >
//       <p className="font-semibold">{item.alert_type}</p>
//       <p>{item.description}</p>
//       {/* <p>Src IP: {item.src_ip}</p> */}
//       <p className="text-gray-400 text-sm">
//         {new Date(item.timestamp * 1000).toLocaleString()}
//       </p>
//     </div>
//   );

//   return (
//     <div className="p-4 flex flex-col gap-6">
//       <h1 className="text-3xl font-bold text-center mb-6">
//         Intrusion Detection Dashboard
//       </h1>
//       <div className="flex gap-6 flex-wrap">
//         {/* Alerts Column */}
//         <div className="flex-1 min-w-[300px]">
//           <h2 className="text-2xl font-semibold mb-4">Live Alerts</h2>
//           {alerts.length === 0 ? (
//             <p className="text-gray-500">No alerts yet</p>
//           ) : (
//             <>
//               {alerts.slice(0, 5).map(renderAlertCard)}
//               {alerts.length > 5 && (
//                 <>
//                   <button
//                     onClick={() => setShowMoreAlerts(!showMoreAlerts)}
//                     className="mt-2 mb-2 text-blue-600 hover:underline"
//                   >
//                     {showMoreAlerts ? "Hide older alerts" : `Show ${alerts.length - 5} more`}
//                   </button>
//                   {showMoreAlerts &&
//                     alerts.slice(5).map(renderAlertCard)}
//                 </>
//               )}
//             </>
//           )}
//         </div>

//         {/* Timeline Column */}
//         <div className="flex-1 min-w-[300px]">
//           <h2 className="text-2xl font-semibold mb-4">Alert Timeline</h2>
//           {timeline.length === 0 ? (
//             <p className="text-gray-500">No timeline data yet</p>
//           ) : (
//             <>
//               {timeline.slice(0, 5).map(renderTimelineCard)}
//               {timeline.length > 5 && (
//                 <>
//                   <button
//                     onClick={() => setShowMoreTimeline(!showMoreTimeline)}
//                     className="mt-2 mb-2 text-blue-600 hover:underline"
//                   >
//                     {showMoreTimeline ? "Hide older events" : `Show ${timeline.length - 5} more`}
//                   </button>
//                   {showMoreTimeline &&
//                     timeline.slice(5).map(renderTimelineCard)}
//                 </>
//               )}
//             </>
//           )}
//         </div>
//       </div>
//     </div>
//   );
// }

// export default Dashboard;
