import React, { useState, useEffect } from "react";
import Alerts from "./components/Alerts";
import Timeline from "./components/Timeline";

function App() {
  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6 text-center">
        Intrusion Detection Dashboard
      </h1>
      <div className="flex flex-col md:flex-row gap-6">
        {/* Alerts Column */}
        <div className="flex-1">
          <Alerts prettify />
        </div>

        {/* Timeline Column */}
        <div className="flex-1">
          <Timeline prettify />
        </div>
      </div>
    </div>
  );
}

export default App;
