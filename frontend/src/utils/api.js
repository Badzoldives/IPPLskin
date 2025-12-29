import axios from 'axios'

// API Base URL
const ML_API_URL = import.meta.env.VITE_API_URL || '/api'

// =============================================================================
// AXIOS INSTANCE
// =============================================================================

export const mlApi = axios.create({
  baseURL: ML_API_URL,
  timeout: 30000
})

// Add auth token interceptor
mlApi.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token') || localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// =============================================================================
// TOKEN MANAGEMENT
// =============================================================================

export function getAccessToken() {
  return localStorage.getItem('access_token') || localStorage.getItem('token')
}

export function getRefreshToken() {
  return localStorage.getItem('refresh_token')
}

export function setTokens(accessToken, refreshToken) {
  localStorage.setItem('access_token', accessToken)
  localStorage.setItem('token', accessToken) // backwards compat
  if (refreshToken) {
    localStorage.setItem('refresh_token', refreshToken)
  }
}

export function clearTokens() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('token')
  localStorage.removeItem('user')
}

export function getStoredUser() {
  const user = localStorage.getItem('user')
  return user ? JSON.parse(user) : null
}

export function setStoredUser(user) {
  localStorage.setItem('user', JSON.stringify(user))
}

export function isLoggedIn() {
  return !!getAccessToken()
}

// =============================================================================
// AUTH API
// =============================================================================

export const loginUser = async (credentials) => {
  const response = await mlApi.post('/auth/login', credentials)
  const data = response.data
  if (data.status === 'success' && data.data) {
    setTokens(data.data.access_token, data.data.refresh_token)
    setStoredUser(data.data.user)
  }
  return data
}

export const registerUser = async (userData) => {
  const response = await mlApi.post('/auth/register', userData)
  const data = response.data
  if (data.status === 'success' && data.data) {
    setTokens(data.data.access_token, data.data.refresh_token)
    setStoredUser(data.data.user)
  }
  return data
}

export const logoutUser = async () => {
  clearTokens()
  return { status: 'success' }
}

export const getCurrentUser = async () => {
  const response = await mlApi.get('/auth/me')
  return response.data
}

// =============================================================================
// PREDICTION API
// =============================================================================

export const predictImage = async (imageFile) => {
  const formData = new FormData()
  formData.append('file', imageFile)
  // Let the browser/axios set the Content-Type (including boundary)
  // to avoid issues where manually setting multipart Content-Type
  // causes the boundary string to be omitted and the server
  // cannot parse the uploaded file (resulting in 400).
  const response = await mlApi.post('/predict', formData)
  return response.data
}

// =============================================================================
// HISTORY API
// =============================================================================

export const getAnalysisHistory = async (page = 1, perPage = 10) => {
  const response = await mlApi.get('/history', {
    params: { page, per_page: perPage }
  })
  return response.data
}

export const getHistoryById = async (id) => {
  const response = await mlApi.get(`/history/${id}`)
  return response.data
}

export const deleteAnalysisById = async (id) => {
  const response = await mlApi.delete(`/history/${id}`)
  return response.data
}

export const getHistoryStats = async () => {
  const response = await mlApi.get('/history/stats')
  return response.data
}

// Legacy names for backwards compatibility
export const deleteHistoryItem = deleteAnalysisById
export const deleteAllHistory = async () => {
  const response = await mlApi.delete('/history')
  return response.data
}

// =============================================================================
// CHATBOT API
// =============================================================================

export const chatWithBot = async (message, context = null) => {
  const response = await mlApi.post('/chatbot', {
    message,
    context
  })
  // Backend returns { status: 'success', data: { reply: '...' } }
  // Return the inner `data` object so callers can use `response.reply`.
  return response.data && response.data.data ? response.data.data : response.data
}

// =============================================================================
// MODEL INFO & CLASSES
// =============================================================================

export const getModelInfo = async () => {
  const response = await mlApi.get('/model-info')
  return response.data
}

export const getClasses = async () => {
  const response = await mlApi.get('/classes')
  return response.data
}

// =============================================================================
// UTILITY
// =============================================================================

export function getImageUrl(filename) {
  if (!filename) return null
  if (filename.startsWith('http')) return filename
  return `${ML_API_URL}/uploads/${filename}`
}

// =============================================================================
// DEFAULT EXPORT (for compatibility)
// =============================================================================

export default {
  // Auth
  registerUser,
  loginUser,
  logoutUser,
  getCurrentUser,
  isLoggedIn,
  getStoredUser,
  setStoredUser,
  clearTokens,
  getAccessToken,
  getRefreshToken,
  setTokens,
  
  // Prediction
  predictImage,
  
  // History
  getAnalysisHistory,
  getHistoryById,
  deleteAnalysisById,
  deleteHistoryItem,
  deleteAllHistory,
  getHistoryStats,
  
  // Chatbot
  chatWithBot,
  
  // Model
  getModelInfo,
  getClasses,
  
  // Utility
  getImageUrl,
  mlApi
}
