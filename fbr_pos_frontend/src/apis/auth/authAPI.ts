import axiosInstance from '@/apis/axiosInstance'

export interface LoginCredentials {
  email: string
  password: string
}

export interface TokenResponse {
  access: string
  refresh: string
}

export interface AuthUser {
  id: number
  email: string
  username: string
  first_name?: string
  last_name?: string
  full_name?: string
  role: string
  status: string
  company_id?: number
  company_name?: string | null
  company_ntn?: string | null
  terminal_id?: string | null
  terminal_name?: string | null
}

export const authAPI = {
  login: (credentials: LoginCredentials) =>
    axiosInstance.post<TokenResponse>('/auth/login/', credentials),

  logout: (refreshToken: string) => axiosInstance.post('/auth/logout/', { refresh: refreshToken }),

  getCurrentUser: () =>
    axiosInstance.get<AuthUser>('/me/me/'),

  refreshToken: (refreshToken: string) =>
    axiosInstance.post<TokenResponse>('/auth/refresh/', { refresh: refreshToken }),

  changePassword: (oldPassword: string, newPassword: string) =>
    axiosInstance.post('/me/password/', { old_password: oldPassword, new_password: newPassword }),

  requestPasswordReset: (email: string) =>
    axiosInstance.post('/auth/password-reset/request/', { email }),

  verifyPasswordResetOtp: (email: string, otp: string) =>
    axiosInstance.post('/auth/password-reset/verify/', { email, otp }),

  confirmPasswordReset: (resetToken: string, newPassword: string, confirmPassword: string) =>
    axiosInstance.post('/auth/password-reset/confirm/', {
      reset_token: resetToken,
      new_password: newPassword,
      confirm_password: confirmPassword,
    }),
}
