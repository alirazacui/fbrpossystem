<template>
  <div class="px-8 py-8 w-full flex flex-col h-[calc(100vh-64px)] overflow-hidden">
    <!-- Header -->
    <div class="mb-4 flex items-center text-sm text-gray-500">
      <span>Fbr</span>
      <svg class="w-4 h-4 mx-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
      <span class="font-bold text-gray-900">Fbr tokens</span>
      <span class="ml-2 text-gray-500">{{ filteredTokens.length }} results ({{ tokens.length }} total)</span>
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
          placeholder="Type to search" 
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
              <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Environment</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Is active</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Created at</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Updated at</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="loading">
              <td colspan="5" class="px-6 py-10 text-center">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-teal-600 mx-auto"></div>
              </td>
            </tr>
            <tr v-else-if="filteredTokens.length === 0">
              <td colspan="5" class="px-6 py-10 text-center text-sm text-gray-500">No FBR tokens found matching your criteria.</td>
            </tr>
            <tr v-else v-for="token in filteredTokens" :key="token.id" @click="$router.push(`/admin/fbr-tokens/${token.id}`)" class="hover:bg-gray-50 cursor-pointer">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ token.tenant_name }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ token.environment }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm">
                <div v-if="token.is_active" class="flex items-center justify-center w-6 h-6 bg-green-100 text-green-600 rounded-full">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
                </div>
                <div v-else class="flex items-center justify-center w-6 h-6 bg-red-100 text-red-500 rounded-full">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatDate(token.created_at) }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatDate(token.updated_at) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="px-6 py-3 bg-gray-50 border-t border-gray-200 text-sm text-gray-500">
        {{ filteredTokens.length }} fbr tokens
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
        <!-- Environment Filter -->
        <div class="mb-6">
          <h3 class="text-sm font-bold text-gray-900 mb-3">By environment</h3>
          <div class="border border-gray-200 rounded-md overflow-hidden">
            <label class="flex items-center px-4 py-3 border-b border-gray-200 cursor-pointer hover:bg-gray-50 transition-colors" :class="{'bg-green-50': filterEnvironment === 'All'}">
              <input type="radio" v-model="filterEnvironment" value="All" class="hidden">
              <span class="text-sm font-medium" :class="filterEnvironment === 'All' ? 'text-green-700' : 'text-gray-700'">All</span>
            </label>
            <label class="flex items-center px-4 py-3 border-b border-gray-200 cursor-pointer hover:bg-gray-50 transition-colors" :class="{'bg-green-50': filterEnvironment === 'Sandbox'}">
              <input type="radio" v-model="filterEnvironment" value="Sandbox" class="hidden">
              <span class="text-sm font-medium" :class="filterEnvironment === 'Sandbox' ? 'text-green-700' : 'text-gray-700'">Sandbox</span>
            </label>
            <label class="flex items-center px-4 py-3 cursor-pointer hover:bg-gray-50 transition-colors" :class="{'bg-green-50': filterEnvironment === 'Production'}">
              <input type="radio" v-model="filterEnvironment" value="Production" class="hidden">
              <span class="text-sm font-medium" :class="filterEnvironment === 'Production' ? 'text-green-700' : 'text-gray-700'">Production</span>
            </label>
          </div>
        </div>

        <!-- Is Active Filter -->
        <div>
          <h3 class="text-sm font-bold text-gray-900 mb-3">By is active</h3>
          <div class="flex rounded-md shadow-sm">
            <button @click="filterActive = 'All'" type="button" class="flex-1 px-4 py-2 text-sm font-medium rounded-l-md border border-gray-300 focus:z-10 focus:ring-2 focus:ring-teal-500" :class="filterActive === 'All' ? 'bg-gray-100 text-gray-900' : 'bg-white text-gray-700 hover:bg-gray-50'">
              All
            </button>
            <button @click="filterActive = 'Yes'" type="button" class="flex-1 px-4 py-2 text-sm font-medium border-t border-b border-gray-300 focus:z-10 focus:ring-2 focus:ring-teal-500" :class="filterActive === 'Yes' ? 'bg-green-50 text-green-700' : 'bg-white text-gray-700 hover:bg-gray-50'">
              Yes
            </button>
            <button @click="filterActive = 'No'" type="button" class="flex-1 px-4 py-2 text-sm font-medium rounded-r-md border border-l-0 border-gray-300 focus:z-10 focus:ring-2 focus:ring-teal-500" :class="filterActive === 'No' ? 'bg-gray-100 text-gray-900' : 'bg-white text-gray-700 hover:bg-gray-50'">
              No
            </button>
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
import { fbrTokensAPI, type FbrTokenItem } from '@/apis/admin/fbrTokensAPI'

const tokens = ref<FbrTokenItem[]>([])
const loading = ref(true)

const searchQuery = ref('')
const isFilterOpen = ref(false)

const filterEnvironment = ref<'All' | 'Sandbox' | 'Production'>('All')
const filterActive = ref<'All' | 'Yes' | 'No'>('All')

const fetchData = async () => {
  loading.value = true
  try {
    const res = await fbrTokensAPI.getAll()
    tokens.value = res.data
  } catch (error) {
    console.error('Failed to fetch FBR tokens:', error)
  } finally {
    loading.value = false
  }
}

const clearFilters = () => {
  filterEnvironment.value = 'All'
  filterActive.value = 'All'
  searchQuery.value = ''
}

const filteredTokens = computed(() => {
  return tokens.value.filter(t => {
    // Search 
    if (searchQuery.value && !t.tenant_name.toLowerCase().includes(searchQuery.value.toLowerCase())) {
      return false
    }
    // Env Filter
    if (filterEnvironment.value !== 'All' && t.environment !== filterEnvironment.value) {
      return false
    }
    // Active Filter
    if (filterActive.value === 'Yes' && !t.is_active) return false
    if (filterActive.value === 'No' && t.is_active) return false

    return true
  })
})

const formatDate = (dateString: string) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
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
