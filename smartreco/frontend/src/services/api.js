import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:8000';

export const fetchProducts = async () => {
  // Placeholder for fetching products
  return axios.get(`${API_BASE}/products`);
};

export const sendChatMessage = async (message) => {
  // Placeholder for sending chat message
  return axios.post(`${API_BASE}/chat`, { message });
};
