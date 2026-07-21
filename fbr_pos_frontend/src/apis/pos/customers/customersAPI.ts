import axiosInstance from '@/apis/axiosInstance'

export interface Customer {
  id: number
  company: number
  company_name: string
  name: string
  ntn_cnic: string
  cnic: string
  ntn: string
  registration_type: 'Registered' | 'Unregistered'
  province?: string
  address?: string
  vendor_code?: string
  credit_limit: number
  notes?: string
  phone?: string
  email?: string
  is_walk_in: boolean
  is_active: boolean
  created_by?: number
  created_by_email?: string
  created_at: string
  updated_at: string
}

export interface CustomerCreatePayload {
  name: string
  phone?: string
  email?: string
  cnic?: string
  ntn?: string
  registration_type: 'Registered' | 'Unregistered'
  province?: string
  vendor_code?: string
  credit_limit?: number
  address?: string
  notes?: string
  is_active?: boolean
}

export const customersAPI = {
  // List customers
  list: (params?: Record<string, any>) =>
    axiosInstance.get<any>('/customers/', { params }),

  // Get single customer
  retrieve: (id: number) =>
    axiosInstance.get<Customer>(`/customers/${id}/`),

  // Create customer
  create: (payload: CustomerCreatePayload) =>
    axiosInstance.post<Customer>('/customers/', payload),

  // Update customer
  update: (id: number, payload: Partial<CustomerCreatePayload>) =>
    axiosInstance.patch<Customer>(`/customers/${id}/`, payload),

  // Search customers by name/phone/ntn/cnic
  search: (query: string) =>
    axiosInstance.get<Customer[]>('/customers/search/', { params: { q: query } }),

  // Get walk-in customer record
  walkin: () =>
    axiosInstance.get<Customer>('/customers/walkin/'),

  // Activate customer
  activate: (id: number) =>
    axiosInstance.post(`/customers/${id}/activate/`),

  // Deactivate customer
  deactivate: (id: number) =>
    axiosInstance.post(`/customers/${id}/deactivate/`),
}
