import axiosInstance from '@/apis/axiosInstance'

export interface Branch {
  id?: number
  company?: number
  name: string
  code: string
  city: string
  province: string
  address: string
  is_active: boolean
  is_default?: boolean
  created_at?: string
}

export const branchesAPI = {
  getAll: (params?: Record<string, any>) => axiosInstance.get('/branches/', { params }),
  getById: (id: number) => axiosInstance.get(`/branches/${id}/`),
  create: (data: Partial<Branch>) => axiosInstance.post('/branches/', data),
  update: (id: number, data: Partial<Branch>) => axiosInstance.patch(`/branches/${id}/`, data),
  delete: (id: number) => axiosInstance.delete(`/branches/${id}/`),
}
