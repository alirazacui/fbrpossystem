import axiosInstance from '@/apis/axiosInstance'

export interface Terminal {
  id: string
  company?: number
  company_name?: string
  branch: number
  branch_name?: string
  name: string
  device_fingerprint?: string
  terminal_index?: string
  pairing_code?: string
  pairing_code_expires_at?: string | null
  paired_at?: string | null
  os_version?: string
  app_version?: string
  printer_config?: Record<string, any>
  scanner_config?: Record<string, any>
  drawer_config?: Record<string, any>
  customer_display_enabled: boolean
  is_active: boolean
  last_seen_at?: string | null
  last_synced_at?: string | null
  created_at?: string
  updated_at?: string
}

export interface CreateTerminalRequest {
  branch: number
  name: string
  device_fingerprint?: string
  terminal_index?: string
  os_version?: string
  app_version?: string
  printer_config?: Record<string, any>
  scanner_config?: Record<string, any>
  drawer_config?: Record<string, any>
  customer_display_enabled?: boolean
  is_active?: boolean
}

export const terminalsAPI = {
  getAll: (params?: Record<string, any>) => axiosInstance.get('/terminals/', { params }),
  getById: (id: string) => axiosInstance.get(`/terminals/${id}/`),
  create: (data: CreateTerminalRequest) => axiosInstance.post('/terminals/', data),
  update: (id: string, data: Partial<CreateTerminalRequest>) => axiosInstance.patch(`/terminals/${id}/`, data),
  delete: (id: string) => axiosInstance.delete(`/terminals/${id}/`),
}