<template>
  <div class="h-full flex flex-col px-8 py-8">
    <div class="mb-6 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">FBR submissions</h1>
        <p class="text-sm text-gray-500 mt-1">Live log of all PRAL API roundtrips (Sandbox & Production)</p>
      </div>
      <router-link to="/invoicing" class="text-sm text-teal-600 hover:text-teal-700 font-medium flex items-center">
        &larr; Back to Invoicing
      </router-link>
    </div>

    <!-- Controls -->
    <div class="flex items-center gap-4 mb-6">
      <div>
        <label class="block text-xs font-medium text-gray-500 uppercase tracking-wider mb-1">Status</label>
        <select v-model="statusFilter" class="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-teal-500 focus:border-teal-500 sm:text-sm rounded-md">
          <option value="all">All</option>
          <option value="00">Success (00)</option>
          <option value="error">Error</option>
        </select>
      </div>
    </div>

    <h2 class="text-lg font-bold text-gray-900 mb-4">Recent submissions</h2>

    <!-- Table -->
    <div class="bg-white shadow rounded-lg border border-gray-200 overflow-hidden flex-1">
      <div class="overflow-x-auto h-full">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">When</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Endpoint</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Env</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">FBR #</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Duration</th>
              <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Action</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="loading">
              <td colspan="7" class="px-6 py-12 text-center text-gray-500">
                <div class="inline-flex items-center">
                  <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-teal-600" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Loading submissions...
                </div>
              </td>
            </tr>
            <tr v-else-if="filteredLogs.length === 0">
              <td colspan="7" class="px-6 py-12 text-center text-gray-500">
                No submissions found.
              </td>
            </tr>
            <tr v-else v-for="(log, idx) in filteredLogs" :key="idx" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ formatDate(log.Submitted) }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-mono">{{ log.Endpoint }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm">
                <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium" :class="log.Env === 'production' ? 'bg-purple-100 text-purple-800' : 'bg-gray-100 text-gray-800'">
                  {{ log.Env }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-mono" :class="log.Code === '00' ? 'text-green-600' : 'text-red-600'">
                {{ log.Code }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-mono" :title="log['FBR invoice']">
                {{ log['FBR invoice'] ? truncate(log['FBR invoice']) : '—' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ log['Latency ms'] }} ms</td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <router-link v-if="log['Sale ID']" :to="`/pos/sales/${log['Sale ID']}`" class="text-teal-600 hover:text-teal-900">
                  View
                </router-link>
                <span v-else-if="log['Local invoice'] && log['Local invoice'].startsWith('SN')" class="text-gray-400" title="Sandbox Scenario">
                  Test
                </span>
                <span v-else class="text-gray-400">
                  —
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axiosInstance from '@/apis/axiosInstance'

const logs = ref<any[]>([])
const loading = ref(true)
const statusFilter = ref('all')

const fetchLogs = async () => {
  loading.value = true
  try {
    const res = await axiosInstance.get('/reports/fbr-submissions/')
    logs.value = res.data
  } catch (err) {
    console.error('Failed to fetch logs:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchLogs()
})

const filteredLogs = computed(() => {
  if (statusFilter.value === 'all') return logs.value
  if (statusFilter.value === '00') return logs.value.filter(l => l.Code === '00')
  if (statusFilter.value === 'error') return logs.value.filter(l => l.Code !== '00')
  return logs.value
})

const truncate = (str: string) => {
  if (str.length <= 15) return str
  return str.substring(0, 15) + '...'
}

const formatDate = (dateStr: string) => {
  const d = new Date(dateStr)
  if (isNaN(d.getTime())) return dateStr
  return d.toLocaleString()
}
</script>
