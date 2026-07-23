import axiosInstance from '@/apis/axiosInstance'

export interface FeeHead {
  id: string
  tennant_id: number
  name: string
  description: string | null
  is_recurring: boolean
  default_pct_code: string | null
  is_active: boolean
}

export interface FeeHeadPayload {
  name: string
  description?: string
  is_recurring?: boolean
  default_pct_code?: string
  is_active?: boolean
}

export const feeHeadAPI = {
  list: (params?: Record<string, any>) =>
    axiosInstance.get<{ results: FeeHead[]; count: number }>('/fee-heads/', { params }),

  retrieve: (id: string) =>
    axiosInstance.get<FeeHead>(`/fee-heads/${id}/`),

  create: (payload: FeeHeadPayload) =>
    axiosInstance.post<FeeHead>('/fee-heads/', payload),

  update: (id: string, payload: Partial<FeeHeadPayload>) =>
    axiosInstance.patch<FeeHead>(`/fee-heads/${id}/`, payload),

  delete: (id: string) =>
    axiosInstance.delete(`/fee-heads/${id}/`),
}
