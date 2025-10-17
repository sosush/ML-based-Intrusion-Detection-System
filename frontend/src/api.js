import axios from "axios";

const API_BASE = "http://127.0.0.1:8000"; // change if backend deployed

export const fetchResults = async () => {
  const res = await axios.get(`${API_BASE}/results`);
  return res.data;
};
