<template>
  <div class="flex flex-col h-[calc(100vh-64px)] overflow-hidden bg-gray-50/50">
    <!-- Header -->
    <div class="px-8 py-6 bg-white border-b border-gray-200 flex items-center justify-between">
      <div class="flex items-center text-sm text-gray-500">
        <button @click="$router.push('/admin/audit-logs')" class="hover:text-gray-900 transition-colors mr-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
        </button>
        <RouterLink to="/admin/audit-logs" class="hover:text-gray-900 transition-colors">Audit</RouterLink>
        <svg class="w-4 h-4 mx-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
        <RouterLink to="/admin/audit-logs" class="hover:text-gray-900 transition-colors">Audit logs</RouterLink>
        <svg class="w-4 h-4 mx-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
        <span class="font-bold text-gray-900" v-if="log">AuditLog object ({{ log.id }})</span>
        <span class="font-bold text-gray-900" v-else>Loading...</span>
      </div>
      <button class="inline-flex items-center px-4 py-2 border border-gray-300 rounded shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none">
        <svg class="w-4 h-4 mr-2 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        History
      </button>
    </div>

    <!-- Main Content -->
    <div class="flex-1 overflow-y-auto px-8 py-6 custom-scrollbar">
      <div v-if="loading" class="flex justify-center items-center py-20">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-teal-600"></div>
      </div>
      <div v-else-if="log" class="bg-white border border-gray-200 rounded-lg shadow-sm">
        <dl>
          <!-- Id -->
          <div class="px-6 py-4 grid grid-cols-3 gap-4 border-b border-gray-200">
            <dt class="text-sm font-bold text-gray-900">Id</dt>
            <dd class="text-sm text-gray-700 col-span-2 font-mono">{{ log.id }}</dd>
          </div>
          
          <!-- Tenant -->
          <div class="px-6 py-4 grid grid-cols-3 gap-4 border-b border-gray-200 bg-gray-50/50">
            <dt class="text-sm font-bold text-gray-900">Tenant</dt>
            <dd class="text-sm text-teal-600 font-medium uppercase col-span-2">{{ log.tenant_name }}</dd>
          </div>
          
          <!-- User -->
          <div class="px-6 py-4 grid grid-cols-3 gap-4 border-b border-gray-200">
            <dt class="text-sm font-bold text-gray-900">User</dt>
            <dd class="text-sm text-teal-600 font-medium col-span-2">{{ log.user_email || '-' }}</dd>
          </div>

          <!-- Entity type -->
          <div class="px-6 py-4 grid grid-cols-3 gap-4 border-b border-gray-200 bg-gray-50/50">
            <dt class="text-sm font-bold text-gray-900">Entity type</dt>
            <dd class="text-sm text-gray-700 col-span-2">{{ log.entity_type }}</dd>
          </div>

          <!-- Entity id -->
          <div class="px-6 py-4 grid grid-cols-3 gap-4 border-b border-gray-200">
            <dt class="text-sm font-bold text-gray-900">Entity id</dt>
            <dd class="text-sm text-gray-700 col-span-2 font-mono text-xs">{{ log.entity_id }}</dd>
          </div>

          <!-- Action -->
          <div class="px-6 py-4 grid grid-cols-3 gap-4 border-b border-gray-200 bg-gray-50/50">
            <dt class="text-sm font-bold text-gray-900">Action</dt>
            <dd class="text-sm text-gray-700 col-span-2">{{ log.action }}</dd>
          </div>

          <!-- Before data -->
          <div class="px-6 py-4 grid grid-cols-3 gap-4 border-b border-gray-200">
            <dt class="text-sm font-bold text-gray-900">Before data</dt>
            <dd class="text-sm text-green-600 font-mono col-span-2 font-medium">{{ log.before_data === null ? 'null' : log.before_data }}</dd>
          </div>

          <!-- After data -->
          <div class="px-6 py-4 grid grid-cols-3 gap-4 border-b border-gray-200 bg-gray-50/50">
            <dt class="text-sm font-bold text-gray-900">After data</dt>
            <dd class="text-sm text-green-600 font-mono col-span-2 font-medium">
              <pre v-if="log.after_data" class="whitespace-pre-wrap">{{ JSON.stringify(log.after_data, null, 2) }}</pre>
              <span v-else>null</span>
            </dd>
          </div>

          <!-- Changes -->
          <div class="px-6 py-4 grid grid-cols-3 gap-4 border-b border-gray-200">
            <dt class="text-sm font-bold text-gray-900">Changes</dt>
            <dd class="text-sm text-green-600 font-mono col-span-2 font-medium">{{ log.changes === null ? 'null' : log.changes }}</dd>
          </div>

          <!-- Ip address -->
          <div class="px-6 py-4 grid grid-cols-3 gap-4 border-b border-gray-200 bg-gray-50/50">
            <dt class="text-sm font-bold text-gray-900">Ip address</dt>
            <dd class="text-sm text-gray-700 col-span-2">{{ log.ip_address || '-' }}</dd>
          </div>

          <!-- User agent -->
          <div class="px-6 py-4 grid grid-cols-3 gap-4 border-b border-gray-200">
            <dt class="text-sm font-bold text-gray-900">User agent</dt>
            <dd class="text-sm text-gray-700 col-span-2">{{ log.user_agent || '-' }}</dd>
          </div>
          
          <!-- Created at -->
          <div class="px-6 py-4 grid grid-cols-3 gap-4 bg-gray-50/50">
            <dt class="text-sm font-bold text-gray-900">Created at</dt>
            <dd class="text-sm text-gray-700 col-span-2">{{ formatDate(log.created_at) }}</dd>
          </div>
        </dl>
      </div>
      <div v-else class="flex justify-center items-center py-20 text-red-500">
        Failed to load audit log details.
      </div>
    </div>

    <!-- Bottom Actions -->
    <div class="px-8 py-4 bg-white border-t border-gray-200 flex justify-end items-center space-x-3">
      <button class="px-4 py-2 bg-white border border-gray-300 text-gray-700 text-sm font-medium rounded hover:bg-gray-50 transition">
        Save and continue editing
      </button>
      <button class="px-6 py-2 bg-green-600 text-white text-sm font-medium rounded hover:bg-green-700 transition">
        Save
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { adminAuditLogsAPI } from '@/apis/admin/adminAuditLogsAPI'

const route = useRoute()
const log = ref<any>(null)
const loading = ref(true)

const fetchLogDetail = async () => {
  loading.value = true
  try {
    const logId = route.params.id as string
    const res = await adminAuditLogsAPI.getById(logId)
    log.value = res.data
  } catch (error) {
    console.error('Failed to fetch audit log detail:', error)
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString: string | null) => {
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
  fetchLogDetail()
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
