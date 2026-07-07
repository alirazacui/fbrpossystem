import axiosInstance from '@/apis/axiosInstance'

export interface Permission {
  id: number
  module: string
  module_display: string
  action: string
  action_display: string
  codename: string
  label: string
  description: string
  is_active: boolean
}

export interface PermissionPanelGroup {
  module: string
  module_display: string
  permissions: {
    id: number
    action: string
    label: string
    codename: string
    granted: boolean
  }[]
}

export interface UserPermission {
  id: number
  user: number
  permission: number
  permission_codename: string
  permission_label: string
  permission_module: string
  permission_module_display: string
  permission_action: string
  granted_by_email: string | null
  granted_at: string
}

class PermissionAPI {
  // Get all active permissions
  async getPermissions(): Promise<Permission[]> {
    const response = await axiosInstance.get('/permissions/')
    return response.data.results || response.data
  }

  // Get permission panel for a specific user (grouped by module)
  async getUserPermissionPanel(userId: number): Promise<PermissionPanelGroup[]> {
    const response = await axiosInstance.get(`/user-permissions/${userId}/panel/`)
    return response.data
  }

  // Assign permissions to a user (replaces existing)
  async assignUserPermissions(userId: number, permissionIds: number[]): Promise<{ detail: string }> {
    const response = await axiosInstance.post(`/user-permissions/${userId}/assign/`, {
      permission_ids: permissionIds,
    })
    return response.data
  }

  // List all permissions for a user
  async listUserPermissions(userId: number): Promise<UserPermission[]> {
    const response = await axiosInstance.get(`/user-permissions/${userId}/list/`)
    return response.data.results || response.data
  }
}

export default new PermissionAPI()
