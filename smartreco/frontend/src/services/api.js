import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';

const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:8000';

export function getOrCreateUserId() {
  let userId = localStorage.getItem('user_id');
  if (!userId) {
    userId = uuidv4();
    localStorage.setItem('user_id', userId);
  }
  return userId;
}

export const fetchProducts = async () => {
  // Placeholder for fetching products
  return axios.get(`${API_BASE}/products`);
};

export const sendChatMessage = async (message) => {
  // Placeholder for sending chat message
  return axios.post(`${API_BASE}/chat`, { message });
};

export const getRecommendation = async (query) => {
  const user_id = getOrCreateUserId();
  const response = await axios.post(`${API_BASE}/recommend`, {
    query,
    user_id,
  });
  return response.data;
};
