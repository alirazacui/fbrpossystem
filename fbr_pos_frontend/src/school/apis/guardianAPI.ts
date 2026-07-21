import axiosInstance from '@/apis/axiosInstance'

export interface Guardian {
  id: string
  tennant_id: number
  first_name: string
  last_name: string
  email: string | null
  phone_number: string | null
  address: string | null
  cnic: string | null
}

export interface GuardianPayload {
  first_name: string
  last_name: string
  email?: string
  phone_number?: string
  address?: string
  cnic?: string
}

export const guardianAPI = {
  list: (params?: Record<string, any>) =>
    axiosInstance.get<{ results: Guardian[]; count: number }>('/school/guardians/', { params }),

  retrieve: (id: string) =>
    axiosInstance.get<Guardian>(`/school/guardians/${id}/`),

  create: (payload: GuardianPayload) =>
    axiosInstance.post<Guardian>('/school/guardians/', payload),

  update: (id: string, payload: Partial<GuardianPayload>) =>
    axiosInstance.patch<Guardian>(`/school/guardians/${id}/`, payload),

  delete: (id: string) =>
    axiosInstance.delete(`/school/guardians/${id}/`),
}
