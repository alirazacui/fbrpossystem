import axiosInstance from '@/apis/axiosInstance'

export interface Category {
  id: number
  company: number
  company_name: string
  parent: number | null
  parent_name: string | null
  name: string
  description: string
  is_active: boolean
  product_count: number
}

export const categoriesAPI = {
  fetchCategories: async (): Promise<Category[]> => {
    // We assume backend returns unpaginated or we fetch a lot
    const response = await axiosInstance.get('/categories/', { params: { limit: 1000 } })
    return response.data.results || response.data
  },
  
  createCategory: async (payload: { name: string; parent?: number | null }): Promise<Category> => {
    const response = await axiosInstance.post('/categories/', payload)
    return response.data
  },
  
  updateCategory: async (id: number, payload: Partial<{ name: string; parent: number | null }>): Promise<Category> => {
    const response = await axiosInstance.patch(`/categories/${id}/`, payload)
    return response.data
  }
}
