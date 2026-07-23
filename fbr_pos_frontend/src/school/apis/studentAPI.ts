import axiosInstance from '@/apis/axiosInstance'

export interface Student {
  id: string
  tennant_id: number
  fullname: string
  email: string | null
  phone_number: string | null
  address: string | null
  cnic: string | null
  date_of_birth: string | null
  gender: 'male' | 'female' | null
  registration_number: string | null
  admission_date: string | null
  current_section_id: string | null
  status: 'active' | 'inactive'
  
  // Related
  section_name?: string
  grade_name?: string
}

export interface StudentPayload {
  fullname: string
  email?: string
  phone_number?: string
  address?: string
  cnic?: string
  date_of_birth?: string
  gender?: 'male' | 'female'
  registration_number?: string
  admission_date?: string
  current_section_id?: string
  status?: 'active' | 'inactive'
}

export const studentAPI = {
  list: (params?: Record<string, any>) =>
    axiosInstance.get<{ results: Student[]; count: number }>('/students/', { params }),

  retrieve: (id: string) =>
    axiosInstance.get<Student>(`/students/${id}/`),

  create: (payload: StudentPayload) =>
    axiosInstance.post<Student>('/students/', payload),

  update: (id: string, payload: Partial<StudentPayload>) =>
    axiosInstance.patch<Student>(`/students/${id}/`, payload),

  delete: (id: string) =>
    axiosInstance.delete(`/students/${id}/`),
}
