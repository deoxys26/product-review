import axios from "axios";

// Dynamically use the Vercel environment variable, or fallback to localhost for local testing
const API_BASE_URL = import.meta.env.VITE_BACKEND_URL || "http://127.0.0.1:8000";

const API = axios.create({
  baseURL: API_BASE_URL,
});

export const predictSentiment = (review) => {
  return API.post("/sentiment/predict", { review });
};

export const getStats = () => {
  return API.get("/sentiment/stats");
};

export const getAspectStats = () => {
  return API.get("/sentiment/aspect-stats");
};

export const getReviews = () => {
  return API.get("/sentiment/reviews");
};