import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import permissionAPI, { type PermissionPanelGroup } from '@/apis/admin/permissionAPI'

export const usePermissionStore = defineStore('permission', () => {
  // State
  const permissionPanel = ref<PermissionPanelGroup[]>([])
  const selectedPermissionIds = ref<Set<number>>(new Set())
  const loading = ref(false)
  const error = ref('')

  // Computed
  const selectedCount = computed(() => selectedPermissionIds.value.size)

  // Methods
  const loadPermissionPanel = async (userId: number) => {
    loading.value = true
    error.value = ''
    try {
      permissionPanel.value = await permissionAPI.getUserPermissionPanel(userId)
      
      // Initialize selected permissions from panel
      const selected = new Set<number>()
      for (const group of permissionPanel.value) {
        for (const perm of group.permissions) {
          if (perm.granted) {
            selected.add(perm.id)
          }
        }
      }
      selectedPermissionIds.value = selected
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to load permissions'
      console.error(err)
    } finally {
      loading.value = false
    }
  }

  const togglePermission = (permissionId: number) => {
    if (selectedPermissionIds.value.has(permissionId)) {
      selectedPermissionIds.value.delete(permissionId)
    } else {
      selectedPermissionIds.value.add(permissionId)
    }
  }

  const togglePermissionGroup = (module: string) => {
    const group = permissionPanel.value.find(g => g.module === module)
    if (!group) return

    // Check if all permissions in this group are selected
    const allSelected = group.permissions.every(p => selectedPermissionIds.value.has(p.id))

    // If all selected, deselect all; otherwise select all
    if (allSelected) {
      group.permissions.forEach(p => selectedPermissionIds.value.delete(p.id))
    } else {
      group.permissions.forEach(p => selectedPermissionIds.value.add(p.id))
    }
  }

  const isGroupFullySelected = (module: string): boolean => {
    const group = permissionPanel.value.find(g => g.module === module)
    if (!group || group.permissions.length === 0) return false
    return group.permissions.every(p => selectedPermissionIds.value.has(p.id))
  }

  const isGroupPartiallySelected = (module: string): boolean => {
    const group = permissionPanel.value.find(g => g.module === module)
    if (!group || group.permissions.length === 0) return false
    const selected = group.permissions.filter(p => selectedPermissionIds.value.has(p.id))
    return selected.length > 0 && selected.length < group.permissions.length
  }

  const savePermissions = async (userId: number) => {
    loading.value = true
    error.value = ''
    try {
      const permIds = Array.from(selectedPermissionIds.value)
      await permissionAPI.assignUserPermissions(userId, permIds)
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || err.response?.data?.permission_ids?.[0] || 'Failed to save permissions'
      console.error(err)
      return false
    } finally {
      loading.value = false
    }
  }

  const clearError = () => {
    error.value = ''
  }

  const reset = () => {
    permissionPanel.value = []
    selectedPermissionIds.value = new Set()
    error.value = ''
    loading.value = false
  }

  return {
    // State
    permissionPanel,
    selectedPermissionIds,
    loading,
    error,

    // Computed
    selectedCount,

    // Methods
    loadPermissionPanel,
    togglePermission,
    togglePermissionGroup,
    isGroupFullySelected,
    isGroupPartiallySelected,
    savePermissions,
    clearError,
    reset,
  }
})
