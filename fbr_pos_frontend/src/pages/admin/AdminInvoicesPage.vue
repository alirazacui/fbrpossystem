<template>
  <div class="px-8 py-8 w-full flex flex-col h-[calc(100vh-64px)] overflow-hidden">
    <!-- Header -->
    <div class="mb-4 flex items-center text-sm text-gray-500">
      <span>Admin</span>
      <svg class="w-4 h-4 mx-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
      <span class="font-bold text-gray-900">Invoices</span>
      <span class="ml-2 text-gray-500">{{ filteredInvoices.length }} results ({{ invoices.length }} total)</span>
    </div>

    <!-- Search and Filters Bar -->
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
          placeholder="Search by Tenant or Invoice Number..." 
        />
      </div>
      
      <button @click="isFilterOpen = true" class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500">
        Filters
        <svg class="ml-2 -mr-1 h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
        </svg>
      </button>
    </div>

    <!-- Table -->
    <div class="flex-1 bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden flex flex-col">
      <div class="overflow-x-auto flex-1 custom-scrollbar">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50 sticky top-0 z-10">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Tenant</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Invoice No.</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">FBR Invoice No.</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Status</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">FBR Status</th>
              <th scope="col" class="px-6 py-3 text-right text-xs font-bold text-gray-700 uppercase tracking-wider">Amount</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Created at</th>
              <th scope="col" class="px-6 py-3 text-right text-xs font-bold text-gray-700 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="loading">
              <td colspan="8" class="px-6 py-10 text-center">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-teal-600 mx-auto"></div>
              </td>
            </tr>
            <tr v-else-if="filteredInvoices.length === 0">
              <td colspan="8" class="px-6 py-10 text-center text-sm text-gray-500">No invoices found matching your criteria.</td>
            </tr>
            <tr v-else v-for="invoice in filteredInvoices" :key="invoice.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ invoice.tenant_name }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ invoice.invoice_number }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                 {{ invoice.fbr_invoice_number || '-' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm">
                <span :class="{
                  'bg-yellow-100 text-yellow-800': invoice.status === 'DRAFT',
                  'bg-green-100 text-green-800': invoice.status === 'COMPLETED',
                  'bg-red-100 text-red-800': invoice.status === 'CANCELLED' || invoice.status === 'RETURNED',
                }" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
                  {{ invoice.status }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm">
                 <span :class="{
                  'bg-gray-100 text-gray-800': invoice.fbr_status === 'PENDING',
                  'bg-green-100 text-green-800': invoice.fbr_status === 'SUCCESS',
                  'bg-red-100 text-red-800': invoice.fbr_status === 'FAILED',
                }" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
                  {{ invoice.fbr_status }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right font-medium">Rs {{ Number(invoice.total_amount).toFixed(2) }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatDate(invoice.created_at) }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-right space-x-2">
                <button class="px-3 py-1.5 rounded-md bg-indigo-600 text-white hover:bg-indigo-700" @click="openInvoice(invoice)">
                  View
                </button>
                <button class="px-3 py-1.5 rounded-md border border-gray-300 text-gray-700 hover:bg-gray-50" @click="downloadInvoice(invoice)">
                  Download
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="px-6 py-3 bg-gray-50 border-t border-gray-200 text-sm text-gray-500">
        {{ filteredInvoices.length }} invoices
      </div>
    </div>

    <!-- Filter Slide-out Panel overlay -->
    <div v-if="isFilterOpen" class="fixed inset-0 bg-gray-600 bg-opacity-50 z-40" @click="isFilterOpen = false"></div>

    <!-- Filter Slide-out Panel -->
    <div 
      class="fixed inset-y-0 right-0 max-w-md w-full bg-white shadow-xl z-50 transform transition-transform duration-300 ease-in-out flex flex-col"
      :class="isFilterOpen ? 'translate-x-0' : 'translate-x-full'"
    >
      <div class="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
        <h2 class="text-lg font-medium text-gray-900">Filters</h2>
        <button @click="isFilterOpen = false" class="text-gray-400 hover:text-gray-500">
          <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      
      <div class="p-6 flex-1 overflow-y-auto">
        <!-- Status Filter -->
        <div class="mb-6">
          <h3 class="text-sm font-bold text-gray-900 mb-3">By status</h3>
          <div class="border border-gray-200 rounded-md overflow-hidden">
             <label class="flex items-center px-4 py-3 border-b border-gray-200 cursor-pointer hover:bg-gray-50 transition-colors" :class="{'bg-teal-50': filterStatus === 'All'}">
              <input type="radio" v-model="filterStatus" value="All" class="hidden">
              <span class="text-sm font-medium" :class="filterStatus === 'All' ? 'text-teal-700' : 'text-gray-700'">All</span>
            </label>
            <label class="flex items-center px-4 py-3 border-b border-gray-200 cursor-pointer hover:bg-gray-50 transition-colors" :class="{'bg-teal-50': filterStatus === 'DRAFT'}">
              <input type="radio" v-model="filterStatus" value="DRAFT" class="hidden">
              <span class="text-sm font-medium" :class="filterStatus === 'DRAFT' ? 'text-teal-700' : 'text-gray-700'">Draft</span>
            </label>
            <label class="flex items-center px-4 py-3 border-b border-gray-200 cursor-pointer hover:bg-gray-50 transition-colors" :class="{'bg-teal-50': filterStatus === 'COMPLETED'}">
              <input type="radio" v-model="filterStatus" value="COMPLETED" class="hidden">
              <span class="text-sm font-medium" :class="filterStatus === 'COMPLETED' ? 'text-teal-700' : 'text-gray-700'">Completed</span>
            </label>
             <label class="flex items-center px-4 py-3 cursor-pointer hover:bg-gray-50 transition-colors" :class="{'bg-teal-50': filterStatus === 'CANCELLED'}">
              <input type="radio" v-model="filterStatus" value="CANCELLED" class="hidden">
              <span class="text-sm font-medium" :class="filterStatus === 'CANCELLED' ? 'text-teal-700' : 'text-gray-700'">Cancelled</span>
            </label>
          </div>
        </div>

        <!-- FBR Status Filter -->
         <div class="mb-6">
          <h3 class="text-sm font-bold text-gray-900 mb-3">By fbr status</h3>
          <div class="border border-gray-200 rounded-md overflow-hidden">
             <label class="flex items-center px-4 py-3 border-b border-gray-200 cursor-pointer hover:bg-gray-50 transition-colors" :class="{'bg-teal-50': filterFbrStatus === 'All'}">
              <input type="radio" v-model="filterFbrStatus" value="All" class="hidden">
              <span class="text-sm font-medium" :class="filterFbrStatus === 'All' ? 'text-teal-700' : 'text-gray-700'">All</span>
            </label>
            <label class="flex items-center px-4 py-3 border-b border-gray-200 cursor-pointer hover:bg-gray-50 transition-colors" :class="{'bg-teal-50': filterFbrStatus === 'PENDING'}">
              <input type="radio" v-model="filterFbrStatus" value="PENDING" class="hidden">
              <span class="text-sm font-medium" :class="filterFbrStatus === 'PENDING' ? 'text-teal-700' : 'text-gray-700'">Pending</span>
            </label>
            <label class="flex items-center px-4 py-3 border-b border-gray-200 cursor-pointer hover:bg-gray-50 transition-colors" :class="{'bg-teal-50': filterFbrStatus === 'SUCCESS'}">
              <input type="radio" v-model="filterFbrStatus" value="SUCCESS" class="hidden">
              <span class="text-sm font-medium" :class="filterFbrStatus === 'SUCCESS' ? 'text-teal-700' : 'text-gray-700'">Success</span>
            </label>
             <label class="flex items-center px-4 py-3 cursor-pointer hover:bg-gray-50 transition-colors" :class="{'bg-teal-50': filterFbrStatus === 'FAILED'}">
              <input type="radio" v-model="filterFbrStatus" value="FAILED" class="hidden">
              <span class="text-sm font-medium" :class="filterFbrStatus === 'FAILED' ? 'text-teal-700' : 'text-gray-700'">Failed</span>
            </label>
          </div>
        </div>
      </div>

      <div class="p-4 border-t border-gray-200 bg-gray-50 flex justify-between items-center">
        <button @click="isFilterOpen = false" class="px-4 py-2 bg-gray-600 text-white text-sm font-medium rounded hover:bg-gray-700 transition">
          Show results
        </button>
        <button @click="clearFilters" class="px-4 py-2 bg-white border border-gray-300 text-gray-700 text-sm font-medium rounded hover:bg-gray-50 transition">
          Clear all filters
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { adminInvoicesAPI, type AdminInvoiceItem } from '@/apis/admin/adminInvoicesAPI'

const invoices = ref<AdminInvoiceItem[]>([])
const loading = ref(true)

const searchQuery = ref('')
const isFilterOpen = ref(false)

const filterStatus = ref<'All' | 'DRAFT' | 'COMPLETED' | 'CANCELLED'>('All')
const filterFbrStatus = ref<'All' | 'PENDING' | 'SUCCESS' | 'FAILED'>('All')

const fetchData = async () => {
  loading.value = true
  try {
    const res = await adminInvoicesAPI.getAll()
    invoices.value = res.data
  } catch (error) {
    console.error('Failed to fetch admin invoices:', error)
  } finally {
    loading.value = false
  }
}

const clearFilters = () => {
  filterStatus.value = 'All'
  filterFbrStatus.value = 'All'
  searchQuery.value = ''
}

const filteredInvoices = computed(() => {
  return invoices.value.filter(inv => {
    // Search 
    if (searchQuery.value) {
       const q = searchQuery.value.toLowerCase()
       const matchesTenant = inv.tenant_name.toLowerCase().includes(q)
       const matchesInvoiceNo = inv.invoice_number.toLowerCase().includes(q)
       if (!matchesTenant && !matchesInvoiceNo) return false
    }
    
    // Status Filter
    if (filterStatus.value !== 'All' && inv.status !== filterStatus.value) {
      return false
    }
    // FBR Status Filter
    if (filterFbrStatus.value !== 'All' && inv.fbr_status !== filterFbrStatus.value) {
        return false
    }

    return true
  })
})

const formatDate = (dateString: string) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  }).format(date)
}

const openInvoice = async (invoice: AdminInvoiceItem) => {
  try {
    const res = await adminInvoicesAPI.getDocumentUrl(invoice.id, false)
    const url = res.data?.url
    if (!url) throw new Error('Missing invoice URL')
    window.open(url, '_blank')
  } catch (error) {
    console.error('Failed to open invoice:', error)
    alert('Failed to open invoice PDF.')
  }
}

const downloadInvoice = async (invoice: AdminInvoiceItem) => {
  try {
    const res = await adminInvoicesAPI.getDocumentUrl(invoice.id, true)
    const url = res.data?.url
    if (!url) throw new Error('Missing invoice URL')
    window.open(url, '_blank')
  } catch (error) {
    console.error('Failed to download invoice:', error)
    alert('Failed to download invoice PDF.')
  }
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
