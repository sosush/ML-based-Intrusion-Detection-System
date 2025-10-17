import React from "react";

export default function ClusteringCard({ data }) {
  return (
    <div className="bg-gray-800 rounded-2xl p-6 shadow-lg">
      <h2 className="text-2xl font-semibold mb-4">Clustering Metrics</h2>
      <p>KMeans Silhouette: {data.kmeans_silhouette.toFixed(3)}</p>
      <p>DBSCAN Silhouette: {data.dbscan_silhouette.toFixed(3)}</p>
      <p>Autoencoder KMeans: {data.ae_kmeans_silhouette.toFixed(3)}</p>
    </div>
  );
}
