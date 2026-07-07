import axiosInstance from '@/apis/axiosInstance'

export interface FbrTokenItem {
  id: string
  tenant_name: string
  environment: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export const fbrTokensAPI = {
  getAll: () => axiosInstance.get('/admin-dashboard/fbr-tokens/'),
  getById: (id: string) => axiosInstance.get(`/admin-dashboard/fbr-tokens/${id}/`),
}
