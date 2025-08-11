import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_BACKEND_API_URL || 'http://localhost:8000/api';

export const googleAuth = async (idToken: string) => {
  try {
    const response = await axios.post(`${API_URL}/auth/google/`, {
      id_token: idToken,
    });
    return response.data;
  } catch (error) {
    console.error('Google authentication failed:', error);
    throw error;
  }
};
