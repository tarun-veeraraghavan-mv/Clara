import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_BACKEND_API_URL || 'http://localhost:8000/api';

interface BotSettings {
  id?: number;
  greeting_message: string;
  fallback_reply: string;
  max_conversation_history: number;
  confidence_threshold: number;
}

export const getBotSettings = async (): Promise<BotSettings> => {
  try {
    const response = await axios.get(`${API_URL}/bot-settings/current/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching bot settings:', error);
    throw error;
  }
};

export const createBotSettings = async (settings: {
  greeting_message: string;
  fallback_reply: string;
  max_conversation_history: number;
  confidence_threshold: number;
}) => {
  try {
    const response = await axios.post(`${API_URL}/bot-settings/`, settings);
    return response.data;
  } catch (error) {
    console.error('Error creating bot settings:', error);
    throw error;
  }
};

export const uploadDocument = async (file: File, userId: number) => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("userId", userId.toString()); // Add userId to form data

  try {
    const response = await axios.post(`${API_URL}/upload-doc/`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error uploading document:", error);
    throw error;
  }
};