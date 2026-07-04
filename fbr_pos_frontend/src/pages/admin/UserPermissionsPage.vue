<template>
  <div class="space-y-6">
    <!-- Header & Breadcrumb -->
    <div class="flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <router-link 
          to="/admin/users" 
          class="text-teal-600 hover:text-teal-700 font-medium"
        >
          Users
        </router-link>
        <span class="text-gray-400">/</span>
        <router-link 
          :to="`/admin/users/${userId}`"
          class="text-teal-600 hover:text-teal-700 font-medium"
        >
          {{ userEmail }}
        </router-link>
        <span class="text-gray-400">/</span>
        <span class="text-gray-900 font-medium">Permissions</span>
      </div>
      <button
        @click="goBack"
        class="text-gray-600 hover:text-gray-900 font-medium flex items-center space-x-2"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        <span>Back</span>
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="bg-white rounded-lg shadow p-12 text-center">
      <svg class="animate-spin h-12 w-12 mx-auto text-teal-600" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      <p class="text-gray-600 mt-4">Loading permissions...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error && !permStore.permissionPanel.length" class="bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-lg">
      {{ error }}
    </div>

    <!-- Permissions Panel -->
    <div v-else-if="permStore.permissionPanel.length > 0" class="space-y-6">
      <!-- Page Title & Info -->
      <div class="bg-white rounded-lg shadow p-6">
        <h1 class="text-2xl font-bold text-gray-900">Manage Permissions for {{ userEmail }}</h1>
        <p class="text-gray-600 mt-2">
          Select permissions to assign to this user. 
          <span class="font-medium text-gray-900">{{ permStore.selectedCount }} permission(s) selected</span>
        </p>
      </div>

      <!-- Permission Groups (Cards) -->
      <div class="grid grid-cols-1 gap-6">
        <PermissionCard
          v-for="group in permStore.permissionPanel"
          :key="group.module"
          :group="group"
          :is-selected="isPermissionSelected"
          @select-all="selectAllInGroup(group.module)"
          @select-none="selectNoneInGroup(group.module)"
          @toggle="permStore.togglePermission"
        />
      </div>

      <!-- Error during save -->
      <div v-if="permStore.error" class="bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-lg whitespace-pre-wrap">
        {{ permStore.error }}
      </div>

      <!-- Action Buttons -->
      <div class="flex items-center justify-between gap-4 sticky bottom-0 bg-white rounded-lg shadow p-6 border-t border-gray-200">
        <button
          @click="goBack"
          class="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition font-medium"
        >
          Cancel
        </button>
        <div class="text-gray-600 font-medium">
          {{ permStore.selectedCount }} permission(s) selected
        </div>
        <button
          @click="handleSave"
          :disabled="permStore.loading"
          class="px-6 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
        >
          <span v-if="!permStore.loading">Save Permissions</span>
          <span v-else class="flex items-center space-x-2">
            <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>Saving...</span>
          </span>
        </button>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="bg-white rounded-lg shadow p-12 text-center">
      <svg class="w-12 h-12 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4v.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <p class="text-gray-600">No permissions available</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePermissionStore } from '@/stores/admin/permissionStore'
import PermissionCard from '@/components/admin/PermissionCard.vue'

const route = useRoute()
const router = useRouter()
const permStore = usePermissionStore()

const userId = parseInt(route.params.id as string)
const userEmail = ref('')
const loading = ref(false)
const error = ref('')

onMounted(async () => {
  if (!userId) {
    error.value = 'Invalid user ID'
    return
  }

  loading.value = true
  try {
    await permStore.loadPermissionPanel(userId)
    
    // Try to get user email from route params or set a default
    userEmail.value = (route.query.email as string) || `User ${userId}`
  } catch (err) {
    error.value = 'Failed to load permissions'
    console.error(err)
  } finally {
    loading.value = false
  }
})

// Clean up store on unmount
onBeforeUnmount(() => {
  // Optional: reset store when leaving the page
  // permStore.reset()
})

const isPermissionSelected = (permissionId: number): boolean => {
  return permStore.selectedPermissionIds.has(permissionId)
}

const selectAllInGroup = (module: string) => {
  permStore.togglePermissionGroup(module)
}

const selectNoneInGroup = (module: string) => {
  const group = permStore.permissionPanel.find(g => g.module === module)
  if (group) {
    group.permissions.forEach(p => {
      if (permStore.selectedPermissionIds.has(p.id)) {
        permStore.togglePermission(p.id)
      }
    })
  }
}

const handleSave = async () => {
  const success = await permStore.savePermissions(userId)
  if (success) {
    // Show success message and redirect
    router.push(`/admin/users/${userId}?message=Permissions updated successfully`)
  }
}

const goBack = () => {
  router.push(`/admin/users/${userId}`)
}
</script>

<style scoped>
/* Smooth transitions */
</style>
