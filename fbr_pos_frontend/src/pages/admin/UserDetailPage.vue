<template>
  <div class="space-y-6">
    <!-- Back Button & Header -->
    <div class="flex items-center justify-between">
      <div class="flex items-center space-x-4">
        <router-link 
          to="/admin/users" 
          class="text-teal-600 hover:text-teal-700 font-medium flex items-center space-x-2"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          <span>Back to Users</span>
        </router-link>
      </div>
      <div class="flex items-center space-x-3">
        <button
          @click="showEditModal = true"
          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium flex items-center space-x-2"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
          <span>Edit</span>
        </button>
        <button
          @click="showDeleteModal = true"
          class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition font-medium flex items-center space-x-2"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
          <span>Delete</span>
        </button>
        <router-link 
          :to="`/admin/users/${user?.id}/permissions`" 
          class="px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition font-medium flex items-center space-x-2"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
          </svg>
          <span>Manage Permissions</span>
        </router-link>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="bg-white rounded-lg shadow p-12 text-center">
      <svg class="animate-spin h-12 w-12 mx-auto text-teal-600" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      <p class="text-gray-600 mt-4">Loading user details...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-lg">
      {{ error }}
    </div>

    <!-- User Details -->
    <div v-else-if="user" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Main Info Card -->
      <div class="lg:col-span-2">
        <div class="bg-white rounded-lg shadow p-8">
          <div class="flex items-start space-x-6 mb-8">
            <!-- Avatar -->
            <div class="w-20 h-20 bg-teal-600 rounded-full flex items-center justify-center flex-shrink-0">
              <span class="text-white text-3xl font-bold">
                {{ (user.email[0] || 'U').toUpperCase() }}
              </span>
            </div>
            <div class="flex-1">
              <h1 class="text-3xl font-bold text-gray-900">{{ user.email }}</h1>
              <p class="text-gray-600 mt-1">{{ user.full_name || 'No name set' }}</p>
              <div class="flex items-center space-x-4 mt-4">
                <span :class="getRoleBadgeClass(user.role)">
                  {{ formatRole(user.role) }}
                </span>
                <span :class="getStatusBadgeClass(user.status)">
                  {{ formatStatus(user.status) }}
                </span>
              </div>
            </div>
          </div>

          <!-- Info Grid -->
          <div class="border-t border-gray-200 pt-8">
            <div class="grid grid-cols-2 gap-8">
              <div>
                <p class="text-sm text-gray-600 font-medium">Email</p>
                <p class="text-gray-900 mt-1">{{ user.email }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-600 font-medium">Full Name</p>
                <p class="text-gray-900 mt-1">{{ user.full_name || '-' }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-600 font-medium">Role</p>
                <p class="text-gray-900 mt-1">{{ formatRole(user.role) }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-600 font-medium">Status</p>
                <p class="text-gray-900 mt-1">{{ formatStatus(user.status) }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-600 font-medium">Company</p>
                <p class="text-gray-900 mt-1">{{ user.company_name || 'Platform User' }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-600 font-medium">Joined</p>
                <p class="text-gray-900 mt-1">{{ formatDate(user.date_joined) }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Side Panel -->
      <div class="space-y-6">
        <!-- Quick Actions -->
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-bold text-gray-900 mb-4">Quick Actions</h3>
          <div class="space-y-3">
            <button
              @click="showEditModal = true"
              class="w-full px-4 py-2 border border-blue-300 text-blue-600 rounded-lg hover:bg-blue-50 transition font-medium text-sm"
            >
              Edit User Details
            </button>
            <router-link 
              :to="`/admin/users/${user.id}/permissions`"
              class="block w-full px-4 py-2 border border-teal-300 text-teal-600 rounded-lg hover:bg-teal-50 transition font-medium text-sm text-center"
            >
              Manage Permissions
            </router-link>
            <button
              @click="showDeleteModal = true"
              class="w-full px-4 py-2 border border-red-300 text-red-600 rounded-lg hover:bg-red-50 transition font-medium text-sm"
            >
              Delete User
            </button>
          </div>
        </div>

        <!-- Status Info -->
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-bold text-gray-900 mb-4">Account Status</h3>
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-600">Status</span>
              <span :class="getStatusBadgeClass(user.status, 'text')">
                {{ formatStatus(user.status) }}
              </span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-600">Created</span>
              <span class="text-sm text-gray-900">{{ formatDate(user.date_joined) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modals -->
    <EditUserModal
      :is-open="showEditModal"
      :user="user"
      @close="showEditModal = false"
      @user-updated="handleUserUpdated"
    />

    <DeleteUserConfirmModal
      :is-open="showDeleteModal"
      :user="user"
      @close="showDeleteModal = false"
      @user-deleted="handleUserDeleted"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth/authStore'
import userAPI, { type User } from '@/apis/admin/userAPI'
import EditUserModal from '@/components/admin/EditUserModal.vue'
import DeleteUserConfirmModal from '@/components/admin/DeleteUserConfirmModal.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const user = ref<User | null>(null)
const loading = ref(false)
const error = ref('')
const showEditModal = ref(false)
const showDeleteModal = ref(false)

onMounted(async () => {
  const userId = parseInt(route.params.id as string)
  if (!userId) {
    error.value = 'Invalid user ID'
    return
  }
  await loadUser(userId)
})

const loadUser = async (userId: number) => {
  loading.value = true
  error.value = ''
  try {
    user.value = await userAPI.getUserDetail(userId)
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to load user'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const handleUserUpdated = async () => {
  const userId = parseInt(route.params.id as string)
  await loadUser(userId)
}

const handleUserDeleted = () => {
  router.push('/admin/users')
}

const formatRole = (role: string) => {
  return role
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

const formatStatus = (status: string) => {
  return status.charAt(0).toUpperCase() + status.slice(1)
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

const getRoleBadgeClass = (role: string) => {
  const baseClass = 'px-3 py-1 rounded-full text-sm font-medium'
  const roleMap: { [key: string]: string } = {
    admin: 'bg-purple-100 text-purple-700',
    admin_staff: 'bg-blue-100 text-blue-700',
    owner: 'bg-green-100 text-green-700',
    manager: 'bg-orange-100 text-orange-700',
    cashier: 'bg-yellow-100 text-yellow-700',
    salesperson: 'bg-indigo-100 text-indigo-700',
  }
  return `${baseClass} ${roleMap[role] || 'bg-gray-100 text-gray-700'}`
}

const getStatusBadgeClass = (status: string, format: 'badge' | 'text' = 'badge') => {
  if (format === 'text') {
    const statusMap: { [key: string]: string } = {
      active: 'text-green-600 font-medium',
      inactive: 'text-gray-600 font-medium',
      suspended: 'text-red-600 font-medium',
    }
    return statusMap[status] || 'text-gray-600'
  }

  const baseClass = 'px-3 py-1 rounded-full text-sm font-medium'
  const statusMap: { [key: string]: string } = {
    active: 'bg-green-100 text-green-700',
    inactive: 'bg-gray-100 text-gray-700',
    suspended: 'bg-red-100 text-red-700',
  }
  return `${baseClass} ${statusMap[status] || 'bg-gray-100 text-gray-700'}`
}
</script>

<style scoped>
/* Smooth transitions */
</style>
