import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
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