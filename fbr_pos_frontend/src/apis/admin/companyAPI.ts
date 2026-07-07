import axiosInstance from '@/apis/axiosInstance'
import type { Company } from '@/types'

class CompanyAPI {
  private getRequestConfig(data: FormData | object) {
    if (data instanceof FormData) {
      return { headers: { 'Content-Type': 'multipart/form-data' } }
    }
    return undefined
  }

  // Get all companies
  async getCompanies(): Promise<Company[]> {
    const response = await axiosInstance.get('/companies/')
    return response.data.results || response.data
  }

  // Get company detail
  async getCompanyDetail(id: number): Promise<Company> {
    const response = await axiosInstance.get(`/companies/${id}/`)
    return response.data
  }

  // Create company
  async createCompany(data: Partial<Company> | FormData): Promise<Company> {
    const response = await axiosInstance.post('/companies/', data, this.getRequestConfig(data))
    return response.data
  }

  // Update company (PUT - replace all)
  async updateCompany(id: number, data: Partial<Company> | FormData): Promise<Company> {
    const response = await axiosInstance.put(`/companies/${id}/`, data, this.getRequestConfig(data))
    return response.data
  }

  // Patch company (PATCH - partial update)
  async patchCompany(id: number, data: Partial<Company> | FormData): Promise<Company> {
    const response = await axiosInstance.patch(`/companies/${id}/`, data, this.getRequestConfig(data))
    return response.data
  }

  // Update company modules
  async updateModules(id: number, modules: Record<string, boolean>): Promise<Company> {
    const response = await axiosInstance.patch(`/companies/${id}/modules/`, modules)
    return response.data
  }

  // Activate company
  async activateCompany(id: number): Promise<any> {
    const response = await axiosInstance.post(`/companies/${id}/activate/`)
    return response.data
  }

  // Deactivate company
  async deactivateCompany(id: number): Promise<any> {
    const response = await axiosInstance.post(`/companies/${id}/deactivate/`)
    return response.data
  }

  // Change tenant owner password
  async changeOwnerPassword(id: number, data: { new_password: string; confirm_password: string }): Promise<any> {
    const response = await axiosInstance.post(`/companies/${id}/owner-password/`, data)
    return response.data
  }

  // Delete company
  async deleteCompany(id: number): Promise<any> {
    const response = await axiosInstance.delete(`/companies/${id}/`)
    return response.data
  }

  // Get payment settings
  async getPaymentSettings(id: number): Promise<any> {
    const response = await axiosInstance.get(`/companies/${id}/payment-settings/`)
    return response.data
  }

  // Patch payment settings
  async patchPaymentSettings(id: number, data: FormData | object): Promise<any> {
    // If it's FormData, it handles file uploads.
    const isFormData = data instanceof FormData
    const response = await axiosInstance.patch(`/companies/${id}/payment-settings/`, data, {
      headers: isFormData ? { 'Content-Type': 'multipart/form-data' } : undefined
    })
    return response.data
  }
}

export default new CompanyAPI()
