import axios from "axios";

interface SigninUserData {
  username: string;
  email: string;
  password: string;
}

interface LoginUserData {
  email: string;
  password: string;
}

const API_URL = process.env.NEXT_PUBLIC_BACKEND_API_URL as string;

// Create an Axios instance for authenticated requests
const authAxios = axios.create({
  baseURL: API_URL,
});

// Request interceptor to add the Authorization header
authAxios.interceptors.request.use(
  (config) => {
    const accessToken = localStorage.getItem("accessToken");
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Helper functions for token management
export const setAuthTokens = (accessToken: string, refreshToken: string) => {
  localStorage.setItem("accessToken", accessToken);
  localStorage.setItem("refreshToken", refreshToken);
};

export const clearAuthTokens = () => {
  localStorage.removeItem("accessToken");
  localStorage.removeItem("refreshToken");
};

// Google OAuth function (existing)
export const googleAuth = async (idToken: string) => {
  try {
    const response = await axios.post(`${API_URL}/auth/google/`, {
      id_token: idToken,
    });
    const { access, refresh } = response.data;
    setAuthTokens(access, refresh);
    return response.data;
  } catch (error) {
    console.error("Google authentication failed:", error);
    throw error;
  }
};

// User Registration
export const registerUser = async (userData: SigninUserData) => {
  try {
    const response = await axios.post(`${API_URL}/auth/register/`, userData);
    const { access, refresh } = response.data.tokens; // Assuming backend sends tokens in response.data.tokens
    setAuthTokens(access, refresh);
    return response.data;
  } catch (error) {
    console.error("User registration failed:", error);
    throw error;
  }
};

// User Login
export const loginUser = async (credentials: LoginUserData) => {
  try {
    const response = await axios.post(`${API_URL}/auth/login/`, credentials);
    const { access, refresh } = response.data.tokens; // Assuming backend sends tokens in response.data.tokens
    setAuthTokens(access, refresh);
    return response.data;
  } catch (error) {
    console.error("User login failed:", error);
    throw error;
  }
};

// Get Current User (protected route)
export const getMe = async () => {
  try {
    const response = await authAxios.get("/auth/me/");
    return response.data;
  } catch (error) {
    console.error("Failed to fetch user data:", error);
    throw error;
  }
};

// Delete User (protected route)
export const deleteMe = async () => {
  try {
    const response = await authAxios.delete("/auth/delete-me/");
    clearAuthTokens(); // Clear tokens after successful deletion
    return response.data;
  } catch (error) {
    console.error("Failed to delete user:", error);
    throw error;
  }
};
