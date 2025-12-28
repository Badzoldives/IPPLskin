import { ref, computed } from 'vue'
import {
  loginUser,
  registerUser,
  logoutUser,
  getCurrentUser,
  getStoredUser,
  clearTokens,
  getAccessToken,
  setStoredUser
} from '@/utils/api'

// Reactive state
const user = ref(getStoredUser())
const token = ref(getAccessToken())
const isLoading = ref(false)
const error = ref(null)

export function useAuth() {
  // Computed
  const isAuthenticated = computed(() => !!token.value)

  // Methods
  const login = async (credentials) => {
    isLoading.value = true
    error.value = null
    try {
      const result = await loginUser(credentials)
      if (result.status === 'success' && result.data) {
        token.value = result.data.access_token || result.data.token
        user.value = result.data.user
        return { success: true }
      } else {
        error.value = result.message || 'Login gagal'
        throw new Error(error.value)
      }
    } catch (err) {
      error.value = err.message || 'Login gagal'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const register = async (userData) => {
    isLoading.value = true
    error.value = null
    try {
      const result = await registerUser(userData)
      if (result.status === 'success' && result.data) {
        token.value = result.data.access_token || result.data.token
        user.value = result.data.user
        return { success: true }
      } else {
        error.value = result.message || 'Registrasi gagal'
        throw new Error(error.value)
      }
    } catch (err) {
      error.value = err.message || 'Registrasi gagal'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const logout = async () => {
    isLoading.value = true
    try {
      await logoutUser()
      token.value = null
      user.value = null
      error.value = null
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      isLoading.value = false
    }
  }

  const fetchUser = async () => {
    if (!isAuthenticated.value) return null
    isLoading.value = true
    try {
      const result = await getCurrentUser()
      if (result.status === 'success' && result.data) {
        user.value = result.data
        setStoredUser(result.data)
        return result.data
      }
      return null
    } catch (err) {
      console.error('Fetch user error:', err)
      return null
    } finally {
      isLoading.value = false
    }
  }

  const initAuth = () => {
    const storedUser = getStoredUser()
    const t = getAccessToken()
    token.value = t
    if (storedUser && t) {
      user.value = storedUser
    } else {
      user.value = null
      clearTokens()
    }
  }

  return {
    user,
    token,
    isAuthenticated,
    isLoading,
    error,
    login,
    register,
    logout,
    fetchUser,
    initAuth
  }
}
