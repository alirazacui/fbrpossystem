import axiosInstance from '@/apis/axiosInstance'

export interface Lead {
  id: string
  lead_type: 'demo_request' | 'business_automation'
  business_name: string
  contact_name: string | null
  email: string
  phone: string
  cnic: string | null
  address: string | null
  message: string | null
  status: 'new' | 'contacted' | 'in_progress' | 'converted' | 'closed'
  created_at: string
  updated_at: string
}

export interface LeadPayload {
  lead_type: 'demo_request' | 'business_automation'
  business_name: string
  contact_name?: string
  email: string
  phone: string
  cnic?: string
  address?: string
  message?: string
}

export interface Notification {
  id: string
  notification_type: 'lead_submission' | 'system_alert' | 'subscription' | 'support'
  title: string
  message: string
  related_lead: string | null
  lead_business_name?: string
  lead_type?: string
  is_read: boolean
  created_at: string
}

export const publicAPI = {
  // Lead submissions
  submitLead: (payload: LeadPayload) =>
    axiosInstance.post<Lead>('/api/public/leads/', payload),

  // Admin lead management
  getLeads: (params?: Record<string, any>) =>
    axiosInstance.get<{ results: Lead[]; count: number }>('/api/public/leads/', { params }),

  getLead: (id: string) =>
    axiosInstance.get<Lead>(`/api/public/leads/${id}/`),

  updateLead: (id: string, payload: Partial<LeadPayload>) =>
    axiosInstance.patch<Lead>(`/api/public/leads/${id}/`, payload),

  deleteLead: (id: string) =>
    axiosInstance.delete(`/api/public/leads/${id}/`),

  getLeadStats: () =>
    axiosInstance.get<{
      total_leads: number
      new_leads: number
      demo_requests: number
      automation_requests: number
    }>('/api/public/leads/stats/'),

  // Notifications
  getNotifications: (params?: Record<string, any>) =>
    axiosInstance.get<{ results: Notification[]; count: number }>('/api/public/notifications/', { params }),

  getNotification: (id: string) =>
    axiosInstance.get<Notification>(`/api/public/notifications/${id}/`),

  updateNotification: (id: string, payload: { is_read: boolean }) =>
    axiosInstance.patch<Notification>(`/api/public/notifications/${id}/`, payload),

  markNotificationRead: (id: string) =>
    axiosInstance.post<Notification>(`/api/public/notifications/${id}/mark_read/`),

  getUnreadCount: () =>
    axiosInstance.get<{ unread_count: number }>('/api/public/notifications/unread/'),

  markAllRead: () =>
    axiosInstance.post<{ message: string }>('/api/public/notifications/mark_all_read/'),
}
