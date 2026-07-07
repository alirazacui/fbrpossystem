<template>
  <div class="p-6 w-full mx-auto font-sans">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">HS codes</h1>
      <p class="text-gray-500 text-sm">
        Full PRAL HS catalog — {{ totalCodes }} codes available. Source: FBR Master List.
      </p>
    </div>

    <div class="bg-white rounded-lg shadow border border-gray-200">
      <div class="p-4 border-b border-gray-200">
        <div class="relative max-w-md">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
            </svg>
          </div>
          <input
            v-model="searchQuery"
            @input="debouncedSearch"
            type="text"
            class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-teal-500 focus:border-teal-500 sm:text-sm"
            placeholder="Search by code or description..."
          />
        </div>
      </div>

      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Code</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Description</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Default rate</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">UoM</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="loading" class="animate-pulse">
              <td colspan="4" class="px-6 py-8 text-center text-gray-500">Loading...</td>
            </tr>
            <tr v-else-if="hsCodes.length === 0">
              <td colspan="4" class="px-6 py-8 text-center text-gray-500">No HS codes found matching your search.</td>
            </tr>
            <tr v-else v-for="item in hsCodes" :key="item.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ item.code }}</td>
              <td class="px-6 py-4 text-sm text-gray-500 max-w-xl">{{ item.description }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.default_rate || '—' }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.uom || '—' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Pagination controls -->
      <div class="bg-white px-4 py-3 border-t border-gray-200 flex items-center justify-between sm:px-6">
        <div class="flex-1 flex justify-between sm:hidden">
          <button @click="changePage(currentPage - 1)" :disabled="currentPage === 1" class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50">Previous</button>
          <button @click="changePage(currentPage + 1)" :disabled="currentPage === totalPages" class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50">Next</button>
        </div>
        <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
          <div>
            <p class="text-sm text-gray-700">
              Showing <span class="font-medium">{{ ((currentPage - 1) * 50) + 1 }}</span> to <span class="font-medium">{{ Math.min(currentPage * 50, totalCodes) }}</span> of <span class="font-medium">{{ totalCodes }}</span> results
            </p>
          </div>
          <div>
            <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
              <button @click="changePage(currentPage - 1)" :disabled="currentPage === 1" class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50">
                <span class="sr-only">Previous</span>
                &laquo;
              </button>
              <button class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700">
                Page {{ currentPage }} of {{ totalPages }}
              </button>
              <button @click="changePage(currentPage + 1)" :disabled="currentPage === totalPages" class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50">
                <span class="sr-only">Next</span>
                &raquo;
              </button>
            </nav>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { hsCodesAPI, type HSCode } from '@/apis/pos/hscodes/hsCodesAPI'

const hsCodes = ref<HSCode[]>([])
const loading = ref(true)
const searchQuery = ref('')
const currentPage = ref(1)
const totalCodes = ref(0)
const totalPages = ref(1)

let searchTimeout: any = null

const fetchCodes = async () => {
  loading.value = true
  try {
    const data = await hsCodesAPI.fetchHSCodes(currentPage.value, searchQuery.value)
    hsCodes.value = data.results
    totalCodes.value = data.count
    totalPages.value = Math.ceil(data.count / 50)
  } catch (error) {
    console.error('Failed to fetch HS Codes:', error)
  } finally {
    loading.value = false
  }
}

const debouncedSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    currentPage.value = 1
    fetchCodes()
  }, 400) // 400ms debounce
}

const changePage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    fetchCodes()
  }
}

onMounted(() => {
  fetchCodes()
})
</script>
