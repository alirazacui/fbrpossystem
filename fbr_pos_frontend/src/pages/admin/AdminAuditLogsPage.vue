<template>
  <div class="px-8 py-8 w-full flex flex-col h-[calc(100vh-64px)] overflow-hidden">
    <!-- Header -->
    <div class="mb-4 flex items-center text-sm text-gray-500">
      <span>Audit</span>
      <svg class="w-4 h-4 mx-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
      <span class="font-bold text-gray-900">Audit logs</span>
      <span class="ml-2 text-gray-500">{{ filteredLogs.length }} results ({{ logs.length }} total)</span>
    </div>

    <!-- Search Bar -->
    <div class="flex justify-between items-center mb-6">
      <div class="relative w-96">
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <input 
          type="text" 
          v-model="searchQuery" 
          class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-teal-500 focus:border-teal-500 sm:text-sm" 
          placeholder="Type to search" 
        />
      </div>
    </div>

    <!-- Table -->
    <div class="flex-1 bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden flex flex-col">
      <div class="overflow-x-auto flex-1 custom-scrollbar">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50 sticky top-0 z-10">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Created at</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Tenant</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">User</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Entity type</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Entity id</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Action</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="loading">
              <td colspan="6" class="px-6 py-10 text-center">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-teal-600 mx-auto"></div>
              </td>
            </tr>
            <tr v-else-if="filteredLogs.length === 0">
              <td colspan="6" class="px-6 py-10 text-center text-sm text-gray-500">No audit logs found matching your criteria.</td>
            </tr>
            <tr v-else v-for="log in filteredLogs" :key="log.id" @click="$router.push(`/admin/audit-logs/${log.id}`)" class="hover:bg-gray-50 cursor-pointer">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ formatDate(log.created_at) }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ log.tenant_name }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                 {{ log.user_email || '-' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatEntity(log.entity_type) }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-mono text-xs">{{ log.entity_id }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatAction(log.entity_type, log.action) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="px-6 py-3 bg-gray-50 border-t border-gray-200 text-sm text-gray-500">
        {{ filteredLogs.length }} audit logs
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { adminAuditLogsAPI, type AdminAuditLogItem } from '@/apis/admin/adminAuditLogsAPI'

const logs = ref<AdminAuditLogItem[]>([])
const loading = ref(true)

const searchQuery = ref('')

const fetchData = async () => {
  loading.value = true
  try {
    const res = await adminAuditLogsAPI.getAll()
    logs.value = res.data
  } catch (error) {
    console.error('Failed to fetch admin audit logs:', error)
  } finally {
    loading.value = false
  }
}

const formatEntity = (entity: string) => {
  if (!entity) return '-'
  if (entity === 'fbr_token') return 'FBR Token'
  if (entity === 'cash_session') return 'Cash Session'
  if (entity === 'user_account' || entity === 'user') return 'User Account'
  if (entity === 'fbr_processing') return 'FBR Processing'
  return entity.charAt(0).toUpperCase() + entity.slice(1)
}

const formatAction = (entity: string, action: string) => {
  if (!action) return '-'
  
  if (entity === 'user' || entity === 'user_account') {
    if (action === 'login') return 'User Account Logged In'
    if (action === 'logout') return 'User Account Logged Out'
  }

  if (entity === 'fbr_processing') {
    if (action === 'submit') return 'FBR Processing Submitted to FBR'
  }

  if (action === 'create') return `${formatEntity(entity)} Created`
  if (action === 'update') return `${formatEntity(entity)} Updated`
  if (action === 'delete') return `${formatEntity(entity)} Deleted`
  
  if (action === 'open') return `${formatEntity(entity)} Opened`
  if (action === 'close') return `${formatEntity(entity)} Closed`
  if (action === 'open_order_fire') return `${formatEntity(entity)} Order Fired`
  
  if (action === 'fbr_validated') return `${formatEntity(entity)} Validated with FBR`
  if (action === 'resubmit') return `${formatEntity(entity)} Resubmitted to FBR`
  if (action === 'activate_production') return `${formatEntity(entity)} Activated Production`

  return `${formatEntity(entity)} ${action.replace(/_/g, ' ')}`
}

const filteredLogs = computed(() => {
  return logs.value.filter(log => {
    if (searchQuery.value) {
       const q = searchQuery.value.toLowerCase()
       const matchesTenant = log.tenant_name.toLowerCase().includes(q)
       const matchesUser = log.user_email?.toLowerCase().includes(q)
       const matchesEntityId = log.entity_id?.toLowerCase().includes(q)
       if (!matchesTenant && !matchesUser && !matchesEntityId) return false
    }
    return true
  })
})

const formatDate = (dateString: string) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('en-US', {
    month: 'long',
    day: 'numeric',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  }).format(date)
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #d1d5db;
  border-radius: 20px;
}
</style>
