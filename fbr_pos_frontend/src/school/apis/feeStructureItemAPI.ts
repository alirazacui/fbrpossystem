import axiosInstance from '@/apis/axiosInstance'

export interface FeeStructureItem {
  id: string
  fee_structure_id: string
  fee_head_id: string
  amount: string
  due_date: string | null
  is_active: boolean
  frequency: 'once' | 'monthly' | 'quarterly' | 'yearly'

  // Related
  fee_head_name?: string
  fee_structure_name?: string
}

export interface FeeStructureItemPayload {
  fee_structure_id: string
  fee_head_id: string
  amount: number
  due_date?: string
  is_active?: boolean
  frequency?: 'once' | 'monthly' | 'quarterly' | 'yearly'
}

export const feeStructureItemAPI = {
  list: (params?: Record<string, any>) =>
    axiosInstance.get<{ results: FeeStructureItem[]; count: number }>('/school/fee-structure-items/', { params }),

  retrieve: (id: string) =>
    axiosInstance.get<FeeStructureItem>(`/school/fee-structure-items/${id}/`),

  create: (payload: FeeStructureItemPayload) =>
    axiosInstance.post<FeeStructureItem>('/school/fee-structure-items/', payload),

  update: (id: string, payload: Partial<FeeStructureItemPayload>) =>
    axiosInstance.patch<FeeStructureItem>(`/school/fee-structure-items/${id}/`, payload),

  delete: (id: string) =>
    axiosInstance.delete(`/school/fee-structure-items/${id}/`),
}
