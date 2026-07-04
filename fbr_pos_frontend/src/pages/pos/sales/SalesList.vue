<template>
  <div class="min-h-screen bg-gray-50 flex flex-col p-4 sm:p-8">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between mb-8">
      <div>
        <h1 class="text-3xl font-black text-gray-900 tracking-tight">Invoices</h1>
        <p class="text-sm text-gray-500 mt-1">FBR Digital Invoicing &mdash; track every invoice across its lifecycle.</p>
      </div>
      <div class="mt-4 sm:mt-0 flex justify-end w-full sm:w-auto">
        <RouterLink to="/pos/sales/new" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-semibold rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
          <svg class="-ml-1 mr-2 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          New invoice
        </RouterLink>
      </div>
    </div>

    <!-- Dashboard Stat Cards -->
    <div class="grid grid-cols-6 gap-4 mb-8">
      <!-- All Invoices -->
      <div class="bg-white rounded-lg p-4 border-2 border-green-600 shadow-sm flex flex-col justify-between cursor-pointer animate-spring-up" style="animation-delay: 0.1s">
        <div class="flex justify-between items-start mb-2">
          <span class="text-xs font-semibold text-gray-700">All invoices</span>
          <svg class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
        </div>
        <span class="text-2xl font-bold text-gray-900">{{ stats.all }}</span>
      </div>

      <!-- Validated by FBR -->
      <div class="bg-white rounded-lg p-4 border border-green-200 shadow-sm flex flex-col justify-between cursor-pointer hover:border-green-400 transition-colors animate-spring-up" style="animation-delay: 0.15s">
        <div class="flex justify-between items-start mb-2">
          <span class="text-xs font-semibold text-gray-700">Validated by FBR</span>
          <svg class="h-4 w-4 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
        </div>
        <span class="text-2xl font-bold text-gray-900">{{ stats.validated }}</span>
      </div>

      <!-- Submitted -->
      <div class="bg-white rounded-lg p-4 border border-blue-200 shadow-sm flex flex-col justify-between cursor-pointer hover:border-blue-400 transition-colors animate-spring-up" style="animation-delay: 0.2s">
        <div class="flex justify-between items-start mb-2">
          <span class="text-xs font-semibold text-gray-700">Submitted</span>
          <svg class="h-4 w-4 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
        </div>
        <span class="text-2xl font-bold text-gray-900">{{ stats.submitted }}</span>
      </div>

      <!-- Failed -->
      <div class="bg-white rounded-lg p-4 border border-red-200 bg-red-50/20 shadow-sm flex flex-col justify-between cursor-pointer hover:border-red-400 transition-colors animate-spring-up" style="animation-delay: 0.25s">
        <div class="flex justify-between items-start mb-2">
          <span class="text-xs font-semibold text-gray-700">Failed</span>
          <svg class="h-4 w-4 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
        </div>
        <span class="text-2xl font-bold text-gray-900">{{ stats.failed }}</span>
      </div>

      <!-- Drafts -->
      <div class="bg-white rounded-lg p-4 border border-yellow-200 shadow-sm flex flex-col justify-between cursor-pointer hover:border-yellow-400 transition-colors animate-spring-up" style="animation-delay: 0.3s">
        <div class="flex justify-between items-start mb-2">
          <span class="text-xs font-semibold text-gray-700">Drafts (not submitted)</span>
          <svg class="h-4 w-4 text-yellow-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg>
        </div>
        <span class="text-2xl font-bold text-gray-900">{{ stats.drafts }}</span>
      </div>

      <!-- Cancelled -->
      <div class="bg-white rounded-lg p-4 border border-gray-200 shadow-sm flex flex-col justify-between cursor-pointer hover:border-gray-400 transition-colors animate-spring-up" style="animation-delay: 0.35s">
        <div class="flex justify-between items-start mb-2">
          <span class="text-xs font-semibold text-gray-700">Edited / cancelled</span>
          <svg class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
        </div>
        <span class="text-2xl font-bold text-gray-900">{{ stats.cancelled }}</span>
      </div>
    </div>

    <!-- Filters Area -->
    <div class="bg-white rounded-t-lg border border-gray-200 border-b-0 p-4 grid grid-cols-5 gap-4 items-end shadow-sm">
      <div class="col-span-1">
        <label class="block text-xs font-medium text-gray-700 mb-1">Search</label>
        <div class="relative rounded-md shadow-sm">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
          </div>
          <input type="text" v-model="filters.search" @input="fetchSales" placeholder="Invoice #, FBR #, or buyer name" class="block w-full pl-9 py-2 sm:text-sm border-gray-300 rounded-md focus:ring-green-500 focus:border-green-500">
        </div>
      </div>
      
      <div class="col-span-1">
        <label class="block text-xs font-medium text-gray-700 mb-1">Status</label>
        <select v-model="filters.status" @change="fetchSales" class="block w-full py-2 px-3 border border-gray-300 bg-gray-50 rounded-md shadow-sm focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm">
          <option value="">All statuses</option>
          <option value="DRAFT">Draft</option>
          <option value="COMPLETED">Finalized</option>
          <option value="CANCELLED">Cancelled</option>
        </select>
      </div>

      <div class="col-span-1">
        <label class="block text-xs font-medium text-gray-700 mb-1">Branch</label>
        <select v-model="filters.branch" @change="fetchSales" class="block w-full py-2 px-3 border border-gray-300 bg-gray-50 rounded-md shadow-sm focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm text-gray-500">
          <option value="">All branches</option>
        </select>
      </div>

      <div class="col-span-1">
        <label class="block text-xs font-medium text-gray-700 mb-1">From</label>
        <input type="date" v-model="filters.dateFrom" @change="fetchSales" class="block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm">
      </div>
      
      <div class="col-span-1">
        <label class="block text-xs font-medium text-gray-700 mb-1">To</label>
        <input type="date" v-model="filters.dateTo" @change="fetchSales" class="block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm">
      </div>
    </div>

    <!-- Table -->
    <div class="bg-white border border-gray-200 rounded-b-lg shadow-sm flex-1 flex flex-col overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50/80">
            <tr>
              <th scope="col" class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider whitespace-nowrap">Invoice #</th>
              <th scope="col" class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider whitespace-nowrap">FBR #</th>
              <th scope="col" class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider whitespace-nowrap">Date</th>
              <th scope="col" class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider whitespace-nowrap">Buyer</th>
              <th scope="col" class="px-6 py-4 text-center text-xs font-bold text-gray-500 uppercase tracking-wider whitespace-nowrap">Items</th>
              <th scope="col" class="px-6 py-4 text-right text-xs font-bold text-gray-500 uppercase tracking-wider whitespace-nowrap">Total</th>
              <th scope="col" class="px-6 py-4 text-center text-xs font-bold text-gray-500 uppercase tracking-wider whitespace-nowrap">Status</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-100">
            <tr v-if="loading">
              <td colspan="7" class="px-6 py-12 text-center text-gray-500">
                <div class="inline-flex items-center">
                  <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-green-600" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Loading invoices...
                </div>
              </td>
            </tr>
            <tr v-else-if="sales.length === 0">
              <td colspan="7" class="px-6 py-12 text-center text-gray-500">
                No invoices found.
              </td>
            </tr>
            <tr v-else v-for="sale in sales" :key="sale.id" @click="router.push(`/pos/sales/${sale.id}`)" class="hover:bg-gray-50 cursor-pointer transition-colors">
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="sale.status === 'draft' ? 'text-green-600' : 'text-gray-900'" class="text-sm font-medium">{{ sale.sale_number || '—' }}</span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div v-if="sale.fbr_invoice_number" class="flex items-center space-x-2 text-sm text-gray-900 font-mono">
                  <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm14 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z" /></svg>
                  <span>{{ sale.fbr_invoice_number }}</span>
                </div>
                <span v-else class="text-gray-400 text-sm">&mdash;</span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(sale.created_at) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                {{ sale.customer_name || 'Walk-in' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700 text-center">
                {{ sale.items_count || 1 }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-medium text-right">
                Rs {{ formatMoney(sale.total_amount) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-center">
                <span v-if="sale.status === 'completed'" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-green-100 text-green-800">
                  Submitted
                </span>
                <span v-else-if="sale.status === 'draft' && sale.fbr_submission_status === 'validated'" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-100 text-blue-800">
                  Validated
                </span>
                <span v-else-if="sale.status === 'draft'" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-yellow-100 text-yellow-800">
                  Draft
                </span>
                <span v-else class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-gray-100 text-gray-800 capitalize">
                  {{ sale.status }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Footer -->
      <div class="px-6 py-4 border-t border-gray-100 bg-white flex items-center justify-between">
        <span class="text-sm text-gray-500">
          Showing {{ sales.length }} of {{ totalCount }} invoices.
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { salesAPI, type Sale } from '@/apis/pos/sales/salesAPI'

const router = useRouter()
const sales = ref<any[]>([])
const loading = ref(true)
const totalCount = ref(0)

const filters = reactive({
  search: '',
  status: '',
  branch: '',
  dateFrom: '',
  dateTo: '',
})

const stats = reactive({
  all: 0,
  validated: 0,
  submitted: 0,
  failed: 0,
  drafts: 0,
  cancelled: 0,
})

let searchTimeout: any = null

const fetchSales = () => {
  if (searchTimeout) clearTimeout(searchTimeout)
  
  searchTimeout = setTimeout(async () => {
    loading.value = true
    try {
      const params: Record<string, any> = { limit: 100 }
      if (filters.search) params.search = filters.search
      if (filters.status) params.status = filters.status
      // NOTE: backend needs support for these specific filters if used
      
      const res = await salesAPI.list(params)
      sales.value = res.data.results || res.data || []
      totalCount.value = res.data.count || sales.value.length
      
      // Calculate dashboard stats based on loaded data (for now)
      calculateStats()
      
    } catch (error) {
      console.error('Failed to fetch sales:', error)
    } finally {
      loading.value = false
    }
  }, 300)
}

const calculateStats = () => {
  let drafts = 0
  let finalized = 0
  let cancelled = 0
  let fbr_success = 0
  let fbr_failed = 0
  
  sales.value.forEach(s => {
    if (s.status === 'draft') drafts++
    if (s.status === 'completed') finalized++
    if (s.status === 'cancelled') cancelled++
    if (s.fbr_submission_status === 'success') fbr_success++
    if (s.fbr_submission_status === 'failed') fbr_failed++
  })
  
  stats.all = sales.value.length
  stats.drafts = drafts
  stats.validated = finalized // Assuming validated is basically completed/finalized for this UI
  stats.submitted = fbr_success
  stats.failed = fbr_failed
  stats.cancelled = cancelled
}

const formatMoney = (amount: number | string) => {
  return Number(amount).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const formatDate = (dateStr: string) => {
  if (!dateStr) return '—'
  const d = new Date(dateStr)
  return d.toISOString().split('T')[0] // Returns YYYY-MM-DD
}

onMounted(() => {
  fetchSales()
})
</script>

<style scoped>
@keyframes spring-up {
  0% {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  60% {
    opacity: 1;
    transform: translateY(-2px) scale(1.02);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.animate-spring-up {
  animation: spring-up 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) both;
}
</style>
