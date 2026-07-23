import axiosInstance from '@/apis/axiosInstance'

export interface FeeStructure {
  id: string
  tennant_id: number
  name: string
  description: string | null
  academic_session_id: string
  grade_id: string
  is_active: boolean

  // Related
  session_name?: string
  grade_name?: string
}

export interface FeeStructurePayload {
  name: string
  description?: string
  academic_session_id: string
  grade_id: string
  is_active?: boolean
}

export const feeStructureAPI = {
  list: (params?: Record<string, any>) =>
    axiosInstance.get<{ results: FeeStructure[]; count: number }>('/fee-structures/', { params }),

  retrieve: (id: string) =>
    axiosInstance.get<FeeStructure>(`/fee-structures/${id}/`),

  create: (payload: FeeStructurePayload) =>
    axiosInstance.post<FeeStructure>('/fee-structures/', payload),

  update: (id: string, payload: Partial<FeeStructurePayload>) =>
    axiosInstance.patch<FeeStructure>(`/fee-structures/${id}/`, payload),

  delete: (id: string) =>
    axiosInstance.delete(`/fee-structures/${id}/`),
}
