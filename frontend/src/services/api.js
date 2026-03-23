import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

export const fetchFeaturedProducts = async () => {
  const res = await axios.get(`${API_BASE_URL}/featured`);
  return res.data;
};

export const fetchTopRatedProducts = async () => {
  const res = await axios.get(`${API_BASE_URL}/top-rated`);
  return res.data;
};

export const fetchProductsByCategory = async (category) => {
  const res = await axios.get(`${API_BASE_URL}/category/${encodeURIComponent(category)}`);
  return res.data;
};

export const searchProducts = async (query) => {
  const res = await axios.get(`${API_BASE_URL}/search?q=${encodeURIComponent(query)}`);
  return res.data;
};

export const fetchProductById = async (id) => {
  const res = await axios.get(`${API_BASE_URL}/product/${id}`);
  return res.data;
};

export const fetchRecommendations = async (id) => {
  const res = await axios.get(`${API_BASE_URL}/recommend/${id}`);
  return res.data;
};
