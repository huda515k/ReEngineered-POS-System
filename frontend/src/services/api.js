import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // For session cookies
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized - redirect to login
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Authentication API
export const authAPI = {
  login: (username, password) =>
    api.post('/auth/login/', { username, password }),
  
  logout: () =>
    api.post('/auth/logout/'),
};

// Employee API
export const employeeAPI = {
  list: () =>
    api.get('/employees/'),
  
  get: (id) =>
    api.get(`/employees/${id}/`),
  
  create: (data) =>
    api.post('/employees/', data),
  
  update: (id, data) =>
    api.put(`/employees/${id}/`, data),
  
  delete: (id) =>
    api.delete(`/employees/${id}/`),
};

// Item API
export const itemAPI = {
  list: (search = '') =>
    api.get('/items/', { params: { search } }),
  
  get: (id) =>
    api.get(`/items/${id}/`),
};

// Transaction API
export const transactionAPI = {
  list: () =>
    api.get('/transactions/'),
  
  get: (id) =>
    api.get(`/transactions/${id}/`),
  
  createSale: (items, couponCode = null) =>
    api.post('/transactions/sale/', {
      items: items.map(item => ({
        item_id: item.id,
        quantity: item.quantity
      })),
      coupon_code: couponCode
    }),
  
  createRental: (customerPhone, items) =>
    api.post('/transactions/rental/', {
      customer_phone: customerPhone,
      items: items.map(item => ({
        item_id: item.id,
        quantity: item.quantity
      }))
    }),
  
  processReturn: (customerPhone, itemIds) =>
    api.post('/transactions/return/', {
      customer_phone: customerPhone,
      item_ids: itemIds
    }),
  
  getOutstandingRentals: (customerPhone) =>
    api.get('/transactions/outstanding-rentals/', {
      params: { customer_phone: customerPhone }
    }),
};

export default api;

