import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authAPI, type AuthUser, type LoginCredentials } from '@/apis/auth/authAPI'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<AuthUser | null>(null)
  const accessToken = ref<string | null>(sessionStorage.getItem('access_token'))
  const refreshToken = ref<string | null>(sessionStorage.getItem('refresh_token'))
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

      sessionStorage.setItem('access_token', access)
      sessionStorage.setItem('refresh_token', refresh)

      // Fetch user data
      await fetchCurrentUser()
      
      // Clear all other sessionStorage keys from previous sessions
      clearAllSessionStorage()
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
      sessionStorage.removeItem('access_token')
      sessionStorage.removeItem('refresh_token')
      
      // Clear all sessionStorage to prevent data leakage
      clearAllSessionStorage()
      
      // Clear all Pinia stores
      clearAllPiniaStores()
    }
  }
  
  const clearAllSessionStorage = () => {
    // Clear all sessionStorage except auth tokens (which are handled separately)
    const keysToKeep = ['access_token', 'refresh_token']
    for (let i = 0; i < sessionStorage.length; i++) {
      const key = sessionStorage.key(i)
      if (key && !keysToKeep.includes(key)) {
        sessionStorage.removeItem(key)
      }
    }
  }
  
  const clearAllPiniaStores = () => {
    // This will be called from the main app to clear all stores
    // Pinia stores need to be reset individually
    const pinia = (window as any).__PINIA__
    if (pinia) {
      Object.values(pinia._s).forEach((store: any) => {
        if (store.$reset) {
          store.$reset()
        }
      })
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
      sessionStorage.setItem('access_token', access)
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
    clearAllSessionStorage,
    clearAllPiniaStores,
  }
})
