<template>
  <div class="h-full flex flex-col px-8 py-8">
    <div class="mb-6 flex items-center justify-between">
      <div>
        <div class="flex items-center text-sm text-gray-500 mb-2">
          <RouterLink to="/admin" class="hover:text-gray-900">Fbr</RouterLink>
          <span class="mx-2">&rsaquo;</span>
          <span class="text-gray-900 font-medium">Fbr submissions</span>
        </div>
        <h1 class="text-2xl font-bold text-gray-900 flex items-center gap-2">
          <RouterLink to="/admin" class="text-gray-400 hover:text-gray-600">
            &larr;
          </RouterLink>
          {{ total }} Total Submissions
        </h1>
      </div>
    </div>

    <!-- Search & Filters -->
    <div class="flex flex-col sm:flex-row gap-4 mb-6">
      <div class="relative flex-1 max-w-md">
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Type to search (Invoice #, Tenant, FBR #)..."
          class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          @input="handleSearch"
        />
      </div>
      <button class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 flex items-center gap-2">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
        </svg>
        Filters
      </button>
    </div>

    <!-- Table -->
    <div class="bg-white shadow rounded-lg border border-gray-200 overflow-hidden flex-1 flex flex-col">
      <div class="overflow-x-auto flex-1">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Invoice</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tenant</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Endpoint</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">HTTP</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status code</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fbr invoice number</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Attempt number</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Submitted at</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="loading">
              <td colspan="8" class="px-6 py-12 text-center text-gray-500">
                <div class="inline-flex items-center">
                  <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-indigo-600" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Loading submissions...
                </div>
              </td>
            </tr>
            <tr v-else-if="submissions.length === 0">
              <td colspan="8" class="px-6 py-12 text-center text-gray-500">
                No submissions found.
              </td>
            </tr>
            <tr v-else v-for="log in submissions" :key="log.id" class="hover:bg-gray-50 cursor-pointer" @click="$router.push(`/admin/fbr-submissions/${log.id}`)">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-mono text-indigo-600">{{ log.local_invoice_id }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-medium">{{ log.company_name }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ log.endpoint }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ log.http_status }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm" :class="log.status_code === '00' ? 'text-green-600' : 'text-red-600'">
                {{ log.status_code }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-500">{{ truncate(log.fbr_invoice_id) }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ log.attempt }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ log.created_at }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <!-- Pagination (Basic) -->
      <div class="bg-white px-4 py-3 border-t border-gray-200 flex items-center justify-between sm:px-6">
        <span class="text-sm text-gray-700">Showing <strong>{{ submissions.length }}</strong> of <strong>{{ total }}</strong></span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axiosInstance from '@/apis/axiosInstance'

const submissions = ref<any[]>([])
const loading = ref(true)
const searchQuery = ref('')
const total = ref(0)
let searchTimeout: any = null

const fetchSubmissions = async () => {
  loading.value = true
  try {
    const res = await axiosInstance.get('/admin/fbr-submissions/', {
      params: { search: searchQuery.value }
    })
    submissions.value = res.data.results
    total.value = res.data.count
  } catch (err) {
    console.error('Failed to fetch FBR submissions:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchSubmissions()
})

const handleSearch = () => {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    fetchSubmissions()
  }, 400)
}

const truncate = (str: string) => {
  if (!str || str === '-') return '-'
  if (str.length <= 20) return str
  return str.substring(0, 20) + '...'
}
</script>
