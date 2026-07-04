<template>
  <div class="h-full flex flex-col px-8 py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900">Products</h1>
      <div class="flex gap-3">
        <button class="px-4 py-2 border border-gray-300 text-gray-700 bg-white rounded-md text-sm font-semibold hover:bg-gray-50 transition-colors shadow-sm">
          Import CSV
        </button>
        <RouterLink to="/pos/products/create" class="px-4 py-2 bg-teal-600 text-white rounded-md text-sm font-semibold hover:bg-teal-700 transition-colors shadow-sm flex items-center">
          New product
        </RouterLink>
      </div>
    </div>

    <!-- Search & Filter -->
    <div class="mb-4 relative">
      <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
        </svg>
      </div>
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search by SKU, barcode, name…"
        class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:ring-teal-500 focus:border-teal-500 sm:text-sm"
        @input="handleSearch"
      />
    </div>

    <!-- Products Table -->
    <div class="bg-white shadow rounded-lg border border-gray-200 flex-1 flex flex-col overflow-hidden">
      <div class="overflow-x-auto flex-1">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">SKU</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Barcode</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">HS code</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Sale price</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="productsStore.loading">
              <td colspan="6" class="px-6 py-12 text-center text-gray-500">
                <div class="inline-flex items-center">
                  <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-teal-600" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Loading products...
                </div>
              </td>
            </tr>
            <tr v-else-if="productsStore.products.length === 0">
              <td colspan="6" class="px-6 py-12 text-center text-gray-500">
                No products found
              </td>
            </tr>
            <tr v-else v-for="product in productsStore.products" :key="product.id" class="hover:bg-gray-50 cursor-pointer" @click="$router.push(`/pos/products/${product.id}`)">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ product.sku || '—' }}</td>
              <td class="px-6 py-4 text-sm font-medium text-gray-900 max-w-xs truncate" :title="product.name">{{ product.name }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ product.barcode || '—' }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ product.hs_code || '—' }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ formatPrice(product.selling_price) }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm">
                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                  Active
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Pagination Footer -->
      <div class="bg-white px-4 py-3 border-t border-gray-200 flex items-center justify-between sm:px-6">
        <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
          <div>
            <p class="text-sm text-gray-700">
              Showing <span class="font-medium">{{ startIndex }}</span>–<span class="font-medium">{{ endIndex }}</span> of <span class="font-medium">{{ productsStore.pagination.count }}</span>
            </p>
          </div>
          <div class="flex items-center gap-4">
            <div class="flex items-center gap-2">
              <span class="text-sm text-gray-700">Rows</span>
              <select v-model="productsStore.pagination.pageSize" @change="handlePageSizeChange" class="border-gray-300 rounded-md text-sm py-1 pl-2 pr-6 focus:ring-teal-500 focus:border-teal-500">
                <option :value="20">20</option>
                <option :value="50">50</option>
                <option :value="100">100</option>
              </select>
            </div>
            <div>
              <p class="text-sm text-gray-700">Page {{ productsStore.pagination.page }} of {{ totalPages }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useProductsStore } from '@/stores/pos/productsStore'

const router = useRouter()
const productsStore = useProductsStore()
const searchQuery = ref('')
let searchTimeout: any = null

onMounted(async () => {
  await productsStore.fetchProducts()
})

const handleSearch = () => {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(async () => {
    if (searchQuery.value.trim()) {
      await productsStore.searchProducts(searchQuery.value)
    } else {
      await productsStore.fetchProducts()
    }
  }, 300)
}

const handlePageSizeChange = async () => {
  await productsStore.fetchProducts(1) // reset to first page
}

const formatPrice = (price: number) => {
  return Number(price).toFixed(2)
}

const totalPages = computed(() => {
  return Math.ceil(productsStore.pagination.count / productsStore.pagination.pageSize) || 1
})

const startIndex = computed(() => {
  if (productsStore.products.length === 0) return 0
  return (productsStore.pagination.page - 1) * productsStore.pagination.pageSize + 1
})

const endIndex = computed(() => {
  const end = productsStore.pagination.page * productsStore.pagination.pageSize
  return end > productsStore.pagination.count ? productsStore.pagination.count : end
})
</script>
