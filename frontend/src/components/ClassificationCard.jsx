import React from "react";

export default function ClassificationCard({ data }) {
  return (
    <div className="bg-gray-800 rounded-2xl p-6 shadow-lg">
      <h2 className="text-2xl font-semibold mb-4">Model Accuracy</h2>
      <p>Random Forest: {(data.rf.accuracy * 100).toFixed(2)}%</p>
      <p>XGBoost: {(data.xgb.accuracy * 100).toFixed(2)}%</p>
      <p>DNN: {(data.dnn.accuracy * 100).toFixed(2)}%</p>
    </div>
  );
}
