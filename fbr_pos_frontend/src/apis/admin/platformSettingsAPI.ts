import axiosInstance from '@/apis/axiosInstance'

export interface PlatformSettings {
  primary_color: string
  secondary_color: string
  accent_color: string
  smtp_host: string
  smtp_port: number
  smtp_use_tls: boolean
  smtp_username: string
  smtp_password: string
  default_from_email: string
  reply_to_email: string
  updated_at?: string
}

class PlatformSettingsAPI {
  async getSettings(): Promise<PlatformSettings> {
    const response = await axiosInstance.get('/platform-settings/')
    return response.data
  }

  async updateSettings(data: Partial<PlatformSettings>): Promise<PlatformSettings> {
    const response = await axiosInstance.patch('/platform-settings/', data)
    return response.data
  }

  async changeAdminPassword(data: { current_password: string; new_password: string; confirm_password: string }): Promise<any> {
    const response = await axiosInstance.post('/platform-settings/change-password/', data)
    return response.data
  }
}

export default new PlatformSettingsAPI()