import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/"; // Adjust this to your backend API URL

export const getAnalytics = async () => {
  try {
    const response = await axios.get(`${API_URL}analytics/`);
    return response.data;
  } catch (error) {
    console.error("Error fetching analytics:", error);
    throw error;
  }
};
