import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
});

export async function analyzeFile(file) {
  const formData = new FormData();
  formData.append("file", file);
  const { data } = await api.post("/api/analyze/", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
}

export async function generateReport(payload) {
  const { data } = await api.post("/api/report/generate/", payload);
  return data;
}

export async function getReport(caseId) {
  const { data } = await api.get(`/api/report/${caseId}/`);
  return data;
}

export default api;
