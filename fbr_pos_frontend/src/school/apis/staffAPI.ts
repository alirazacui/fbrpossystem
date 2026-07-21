import axiosInstance from '@/apis/axiosInstance'

export interface Staff {
  id: string
  tennant_id: number
  fullname: string
  email: string | null
  phone_number: string | null
  address: string | null
  cnic: string | null
  date_of_birth: string | null
  designation: string | null
  date_of_joining: string | null
  status: 'active' | 'inactive'
}

export interface StaffPayload {
  fullname: string
  email?: string
  phone_number?: string
  address?: string
  cnic?: string
  date_of_birth?: string
  designation?: string
  date_of_joining?: string
  status?: 'active' | 'inactive'
}

export const staffAPI = {
  list: (params?: Record<string, any>) =>
    axiosInstance.get<{ results: Staff[]; count: number }>('/school/staff/', { params }),

  retrieve: (id: string) =>
    axiosInstance.get<Staff>(`/school/staff/${id}/`),

  create: (payload: StaffPayload) =>
    axiosInstance.post<Staff>('/school/staff/', payload),

  update: (id: string, payload: Partial<StaffPayload>) =>
    axiosInstance.patch<Staff>(`/school/staff/${id}/`, payload),

  delete: (id: string) =>
    axiosInstance.delete(`/school/staff/${id}/`),
}
