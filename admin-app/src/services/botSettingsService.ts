import axios from 'axios';

const API_URL = 'http://localhost:8000/api/'; // Adjust this to your backend API URL

export const createBotSettings = async (settings: {
  greetingMessage: string;
  fallbackReply: string;
  maxConvoHistory: number;
  confidenceThreshold: number;
}) => {
  try {
    const response = await axios.post(`${API_URL}bot-settings/`, settings);
    return response.data;
  } catch (error) {
    console.error('Error creating bot settings:', error);
    throw error;
  }
};
