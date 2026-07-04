import axios, { AxiosInstance } from 'axios'

const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

const axiosInstance: AxiosInstance = axios.create({
  baseURL,
  timeout: 10000,
})

// Request interceptor to add JWT token
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle token refresh
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest: any = error.config || {}
    const requestUrl = originalRequest.url || ''
    const isAuthEndpoint = requestUrl.includes('/auth/login/') || requestUrl.includes('/auth/refresh/')

    if (error.response?.status === 401 && !isAuthEndpoint) {
      const refresh = localStorage.getItem('refresh_token')

      if (refresh && !originalRequest._retry) {
        originalRequest._retry = true
        try {
          const refreshResponse = await axios.post(`${baseURL}/auth/refresh/`, { refresh })
          const newAccessToken = refreshResponse.data?.access
          if (newAccessToken) {
            localStorage.setItem('access_token', newAccessToken)
            originalRequest.headers = originalRequest.headers || {}
            originalRequest.headers.Authorization = `Bearer ${newAccessToken}`
            return axiosInstance(originalRequest)
          }
        } catch (_err) {
          // Fall through to logout redirect.
        }
      }

      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      if (!window.location.pathname.startsWith('/login')) {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

export default axiosInstance
