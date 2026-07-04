import axiosInstance from '../axiosInstance'

export const subscriptionsAPI = {
  getPlans: async () => {
    const response = await axiosInstance.get('/subscription-plans/')
    return response.data.results || response.data
  },
  
  getPlan: async (id: number) => {
    const response = await axiosInstance.get(`/subscription-plans/${id}/`)
    return response.data
  },
  
  createPlan: async (data: any) => {
    const response = await axiosInstance.post('/subscription-plans/', data)
    return response.data
  },
  
  updatePlan: async (id: number, data: any) => {
    const response = await axiosInstance.patch(`/subscription-plans/${id}/`, data)
    return response.data
  },
  
  deletePlan: async (id: number) => {
    const response = await axiosInstance.delete(`/subscription-plans/${id}/`)
    return response.data
  },
  
  assignPlan: async (data: { company_id: number; plan_id: number; notes?: string }) => {
    const response = await axiosInstance.post('/subscriptions/assign/', data)
    return response.data
  }
}
