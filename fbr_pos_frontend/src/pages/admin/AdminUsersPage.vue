<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Users Management</h1>
        <p class="text-gray-600 mt-1">Manage platform admins and view company owners</p>
      </div>
      <button
        @click="openAddUserModal"
        class="flex items-center space-x-2 px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition font-medium"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        <span>Add User</span>
      </button>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="bg-white rounded-lg shadow p-6 border-l-4 border-teal-600">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 text-sm font-medium">Total Users</p>
            <p class="text-3xl font-bold text-gray-900 mt-2">{{ users.length }}</p>
          </div>
          <svg class="w-12 h-12 text-teal-100" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 8.048M12 4.354L8.646 7.708M12 4.354l3.354 3.354M9 12a4 4 0 11-8 0 4 4 0 018 0zm12 0a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow p-6 border-l-4 border-blue-600">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 text-sm font-medium">Admin Staff</p>
            <p class="text-3xl font-bold text-gray-900 mt-2">{{ adminCount }}</p>
          </div>
          <svg class="w-12 h-12 text-blue-100" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow p-6 border-l-4 border-green-600">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 text-sm font-medium">Company Owners</p>
            <p class="text-3xl font-bold text-gray-900 mt-2">{{ ownerCount }}</p>
          </div>
          <svg class="w-12 h-12 text-green-100" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5.586a1 1 0 00-.707.293l-2.414-2.414a1 1 0 00-.707-.293h-3.172a1 1 0 00-1 1v2m0-5V7a2 2 0 012-2h2.586a1 1 0 01.707.293l2.414 2.414a1 1 0 00.707.293H17a2 2 0 012 2v3m-5 4h2m-2 0h-2" />
          </svg>
        </div>
      </div>
    </div>

    <!-- Search and Filters -->
    <div class="bg-white rounded-lg shadow p-6">
      <div class="flex items-center space-x-4">
        <div class="flex-1 relative">
          <svg class="w-5 h-5 absolute left-3 top-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search by email or name..."
            class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
          />
        </div>
        <select
          v-model="filterRole"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
        >
          <option value="">All Roles</option>
          <option value="admin">Admin</option>
          <option value="admin_staff">Admin Staff</option>
          <option value="owner">Owner</option>
        </select>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="bg-white rounded-lg shadow p-12 text-center">
      <svg class="animate-spin h-12 w-12 mx-auto text-teal-600" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      <p class="text-gray-600 mt-4">Loading users...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-lg">
      {{ error }}
    </div>

    <!-- Users Table -->
    <div v-else class="bg-white rounded-lg shadow overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase">Email</th>
            <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase">Full Name</th>
            <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase">Role</th>
            <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase">Company</th>
            <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase">Status</th>
            <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase">Joined</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
          <tr 
            v-for="user in filteredUsers" 
            :key="user.id" 
            @click="goToUserDetail(user.id)"
            class="hover:bg-teal-50 transition cursor-pointer"
          >
            <td class="px-6 py-4 text-sm text-teal-600 font-medium hover:text-teal-700">{{ user.email }}</td>
            <td class="px-6 py-4 text-sm text-gray-600">{{ user.full_name || '-' }}</td>
            <td class="px-6 py-4 text-sm">
              <span :class="getRoleBadgeClass(user.role)">
                {{ formatRole(user.role) }}
              </span>
            </td>
            <td class="px-6 py-4 text-sm text-gray-600">{{ user.company_name || '-' }}</td>
            <td class="px-6 py-4 text-sm">
              <span :class="getStatusBadgeClass(user.status)">
                {{ formatStatus(user.status) }}
              </span>
            </td>
            <td class="px-6 py-4 text-sm text-gray-600">{{ formatDate(user.date_joined) }}</td>
          </tr>
        </tbody>
      </table>

      <!-- No Results -->
      <div v-if="filteredUsers.length === 0" class="text-center py-12">
        <svg class="w-12 h-12 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4v.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p class="text-gray-600">No users found</p>
      </div>
    </div>
  </div>

  <!-- Add User Modal -->
  <AddUserModal
    :is-open="showAddUserModal"
    @close="showAddUserModal = false"
    @user-created="loadUsers"
  />
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AddUserModal from '@/components/admin/AddUserModal.vue'
import userAPI, { type User } from '@/apis/admin/userAPI'

const router = useRouter()

const users = ref<User[]>([])
const loading = ref(false)
const error = ref('')
const showAddUserModal = ref(false)
const searchQuery = ref('')
const filterRole = ref('')

const adminCount = computed(() => users.value.filter(u => u.role === 'admin' || u.role === 'admin_staff').length)
const ownerCount = computed(() => users.value.filter(u => u.role === 'owner').length)

const filteredUsers = computed(() => {
  return users.value.filter(user => {
    const platformRoles = ['admin', 'admin_staff', 'owner']
    const isPlatformUser = platformRoles.includes(user.role)
    const matchesSearch = !searchQuery.value ||
      user.email.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      (user.full_name && user.full_name.toLowerCase().includes(searchQuery.value.toLowerCase()))

    const matchesRole = !filterRole.value || user.role === filterRole.value

    return isPlatformUser && matchesSearch && matchesRole
  })
})

const loadUsers = async () => {
  loading.value = true
  error.value = ''
  try {
    users.value = await userAPI.getAllUsers()
  } catch (err: any) {
    error.value = 'Failed to load users'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const openAddUserModal = () => {
  showAddUserModal.value = true
}

const goToUserDetail = (userId: number) => {
  router.push(`/admin/users/${userId}`)
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
    day: 'numeric'
  })
}

const getRoleBadgeClass = (role: string) => {
  const baseClass = 'px-3 py-1 rounded-full text-sm font-medium'
  if (role === 'admin') return `${baseClass} bg-purple-100 text-purple-800`
  if (role === 'admin_staff') return `${baseClass} bg-blue-100 text-blue-800`
  if (role === 'owner') return `${baseClass} bg-green-100 text-green-800`
  return `${baseClass} bg-gray-100 text-gray-800`
}

const getStatusBadgeClass = (status: string) => {
  const baseClass = 'px-3 py-1 rounded-full text-sm font-medium'
  if (status === 'active') return `${baseClass} bg-green-100 text-green-800`
  if (status === 'inactive') return `${baseClass} bg-gray-100 text-gray-800`
  if (status === 'suspended') return `${baseClass} bg-red-100 text-red-800`
  return `${baseClass} bg-gray-100 text-gray-800`
}

onMounted(() => {
  loadUsers()
})
</script>

<style scoped>
/* Smooth transitions */
</style>
