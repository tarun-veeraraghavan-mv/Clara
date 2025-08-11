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
  greetingMessage: string;
  fallbackReply: string;
  maxConvoHistory: number;
  confidenceThreshold: number;
}) => {
  try {
    const response = await axios.post(`${API_URL}/bot-settings/`, settings);
    return response.data;
  } catch (error) {
    console.error('Error creating bot settings:', error);
    throw error;
  }
};