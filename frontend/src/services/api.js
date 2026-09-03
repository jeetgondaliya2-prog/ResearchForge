import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});


// ==========================================
// START RESEARCH
// ==========================================

export const startResearch = async (query) => {
  const response = await api.post("/api/research", {
    query: query,
  });

  return response.data;
};


// ==========================================
// UPLOAD DOCUMENT
// ==========================================

export const uploadDocument = async (file) => {
  const formData = new FormData();

  formData.append("file", file);

  const response = await api.post(
    "/api/documents/upload",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};


// ==========================================
// HEALTH CHECK
// ==========================================

export const healthCheck = async () => {
  const response = await api.get("/");

  return response.data;
};


export default api;