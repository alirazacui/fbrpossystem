import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authAPI, type AuthUser, type LoginCredentials, type TokenResponse } from '@/apis/auth/authAPI'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<AuthUser | null>(null)
  const accessToken = ref<string | null>(localStorage.getItem('access_token'))
  const refreshToken = ref<string | null>(localStorage.getItem('refresh_token'))
  const loading = ref(false)
  const error = ref<string | null>(null)
  const isInitialized = ref(false)

  // Computed
  const isAuthenticated = computed(() => !!accessToken.value && !!user.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isOwner = computed(() => user.value?.role === 'owner')

  // Methods
  const login = async (credentials: LoginCredentials) => {
    loading.value = true
    error.value = null

    try {
      const response = await authAPI.login(credentials)
      const { access, refresh } = response.data

      accessToken.value = access
      refreshToken.value = refresh

      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', refresh)

      // Fetch user data
      await fetchCurrentUser()
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Login failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  const logout = async () => {
    try {
      if (refreshToken.value) {
        await authAPI.logout(refreshToken.value)
      }
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      user.value = null
      accessToken.value = null
      refreshToken.value = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    }
  }

  const fetchCurrentUser = async () => {
    try {
      const response = await authAPI.getCurrentUser()
      user.value = response.data
    } catch (err) {
      console.error('Failed to fetch current user:', err)
      throw err
    }
  }

  const refreshAccessToken = async () => {
    if (!refreshToken.value) return

    try {
      const response = await authAPI.refreshToken(refreshToken.value)
      const { access } = response.data

      accessToken.value = access
      localStorage.setItem('access_token', access)
    } catch (err) {
      console.error('Token refresh failed:', err)
      await logout()
      throw err
    }
  }

  // Initialize
  const initialize = async () => {
    if (accessToken.value) {
      try {
        await fetchCurrentUser()
      } catch (err) {
        await logout()
      }
    }
    isInitialized.value = true
  }

  return {
    // State
    user,
    accessToken,
    refreshToken,
    loading,
    error,
    isInitialized,

    // Computed
    isAuthenticated,
    isAdmin,
    isOwner,

    // Methods
    login,
    logout,
    fetchCurrentUser,
    refreshAccessToken,
    initialize,
  }
})
