import axiosInstance from '@/apis/axiosInstance'
import type { Branch } from './branchesAPI'

export interface Warehouse {
  id?: number
  company?: number
  branch?: number | null
  branch_name?: string | null
  name: string
  code: string
  city: string
  address: string
  is_active: boolean
  is_default?: boolean
  created_at?: string
}

export const warehousesAPI = {
  getAll: () => axiosInstance.get('/warehouses/'),
  getById: (id: number) => axiosInstance.get(`/warehouses/${id}/`),
  create: (data: Partial<Warehouse>) => axiosInstance.post('/warehouses/', data),
  update: (id: number, data: Partial<Warehouse>) => axiosInstance.patch(`/warehouses/${id}/`, data),
  delete: (id: number) => axiosInstance.delete(`/warehouses/${id}/`),
}
