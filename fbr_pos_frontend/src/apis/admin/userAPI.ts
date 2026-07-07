import axiosInstance from '@/apis/axiosInstance'

export interface CreateAdminStaffRequest {
  email: string
  first_name: string
  last_name: string
  phone: string
  password: string
  confirm_password: string
}

export interface CreateOwnerRequest {
  email: string
  first_name: string
  last_name: string
  phone: string
  company: number
  password: string
  confirm_password: string
}

export interface CreateCompanyUserRequest {
  email: string
  first_name: string
  last_name: string
  phone: string
  role: 'manager' | 'cashier' | 'salesperson'
  terminal?: string | null
  password: string
  confirm_password: string
}

export interface User {
  id: number
  email: string
  full_name: string
  role: string
  status: string
  company_id: number | null
  company_name: string | null
  terminal_id?: string | null
  terminal_name?: string | null
  date_joined: string
}

class UserAPI {
  // Get all users (Admin, Staff, Owners, Client Users)
  async getAllUsers(): Promise<User[]> {
    const response = await axiosInstance.get('/users/')
    return response.data.results || response.data
  }

  // Create Admin Staff
  async createAdminStaff(data: CreateAdminStaffRequest): Promise<User> {
    const response = await axiosInstance.post('/admin-users/', data)
    return response.data
  }

  // Get all owners
  async getOwners(): Promise<User[]> {
    const response = await axiosInstance.get('/owners/')
    return response.data.results || response.data
  }

  // Create Owner
  async createOwner(data: CreateOwnerRequest): Promise<User> {
    const response = await axiosInstance.post('/owners/', data)
    return response.data
  }

  // Get company users for the current owner
  async getCompanyUsers(): Promise<User[]> {
    const response = await axiosInstance.get('/company-users/')
    return response.data.results || response.data
  }

  // Create company user (manager/cashier/salesperson)
  async createCompanyUser(data: CreateCompanyUserRequest): Promise<User> {
    const response = await axiosInstance.post('/company-users/', data)
    return response.data
  }

  // Get user detail
  async getUserDetail(id: number): Promise<User> {
    const response = await axiosInstance.get(`/users/${id}/`)
    return response.data
  }

  // Update user
  async updateUser(id: number, data: Partial<User>): Promise<User> {
    const response = await axiosInstance.patch(`/users/${id}/`, data)
    return response.data
  }

  // Change user status
  async changeUserStatus(id: number, status: string, endpoint: string = 'users/'): Promise<User> {
    const response = await axiosInstance.patch(`/${endpoint}${id}/status/`, { status })
    return response.data
  }

  // Delete user
  async deleteUser(id: number): Promise<void> {
    await axiosInstance.delete(`/users/${id}/`)
  }
}

export default new UserAPI()
