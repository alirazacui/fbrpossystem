<template>
  <div class="px-8 py-8 w-full">
    <!-- Header -->
    <div class="mb-6 flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-900">Warehouse Stock Levels</h1>
      <router-link to="/pos/warehouses" class="px-4 py-2 bg-gray-100 text-gray-700 border border-gray-300 rounded shadow-sm text-sm hover:bg-gray-200 transition">
        &larr; Back to Warehouses
      </router-link>
    </div>

    <!-- Filters -->
    <div class="mb-6 flex gap-4">
      <select v-model="selectedWarehouse" @change="fetchStock" class="px-3 py-2 border border-gray-300 rounded shadow-sm focus:ring-teal-500 focus:border-teal-500 text-sm">
        <option value="">All Warehouses</option>
        <option v-for="wh in warehouses" :key="wh.id" :value="wh.id">{{ wh.name }}</option>
      </select>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="mb-6 bg-red-50 border-l-4 border-red-500 p-4 rounded-md">
      <p class="text-sm font-medium text-red-800">{{ error }}</p>
    </div>

    <!-- Stock List -->
    <div class="bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Product</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">SKU / Barcode</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Warehouse</th>
              <th scope="col" class="px-6 py-3 text-right text-xs font-bold text-gray-500 uppercase tracking-wider">Qty in Stock</th>
              <th scope="col" class="px-6 py-3 text-right text-xs font-bold text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="loading">
              <td colspan="5" class="px-6 py-10 text-center">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-teal-600 mx-auto"></div>
              </td>
            </tr>
            <tr v-else-if="stocks.length === 0">
              <td colspan="5" class="px-6 py-10 text-center text-sm text-gray-500 italic">No stock records found. Make sure you have products and warehouses created.</td>
            </tr>
            <tr v-else v-for="stock in stocks" :key="stock.id" class="hover:bg-gray-50 transition-colors" :class="{'bg-red-50': stock.is_low}">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {{ stock.product_name }}
                <span v-if="stock.is_low" class="ml-2 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-red-100 text-red-800">Low Stock</span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                <div>{{ stock.product_sku || '-' }}</div>
                <div class="text-xs text-gray-400">{{ stock.product_barcode || '-' }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ stock.warehouse_name }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-bold" :class="stock.is_low ? 'text-red-600' : 'text-gray-900'">
                {{ stock.quantity }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button @click="openAdjustModal(stock)" class="text-blue-600 hover:text-blue-900 focus:outline-none bg-blue-50 px-3 py-1 rounded border border-blue-100">
                  Adjust Qty
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Adjust Stock Modal -->
    <div v-if="isModalOpen" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="closeAdjustModal"></div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
                <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">Adjust Stock Level</h3>
                <div class="mt-4">
                  <p class="text-sm text-gray-500 mb-4">
                    Product: <strong class="text-gray-900">{{ activeStock?.product_name }}</strong><br>
                    Warehouse: <strong class="text-gray-900">{{ activeStock?.warehouse_name }}</strong>
                  </p>
                  
                  <label class="block text-sm font-medium text-gray-700 mb-1">New Quantity</label>
                  <input type="number" step="0.001" v-model="adjustQuantity" class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-teal-500 focus:border-teal-500 sm:text-sm" />
                </div>
              </div>
            </div>
          </div>
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button type="button" @click="saveAdjustment" :disabled="saving" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50">
              {{ saving ? 'Saving...' : 'Save Adjustment' }}
            </button>
            <button type="button" @click="closeAdjustModal" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { warehouseStockAPI, type WarehouseStock } from '@/apis/tenant/warehouseStockAPI'
import { warehousesAPI, type Warehouse } from '@/apis/tenant/warehousesAPI'

const loading = ref(true)
const saving = ref(false)
const error = ref('')
const stocks = ref<WarehouseStock[]>([])
const warehouses = ref<Warehouse[]>([])
const selectedWarehouse = ref('')

const isModalOpen = ref(false)
const activeStock = ref<WarehouseStock | null>(null)
const adjustQuantity = ref<number | string>(0)

const fetchStock = async () => {
  loading.value = true
  error.value = ''
  try {
    const params = selectedWarehouse.value ? { warehouse: selectedWarehouse.value } : {}
    // Filter on frontend for simplicity if backend doesn't support ?warehouse= filter out of the box
    const res = await warehouseStockAPI.getAll()
    let data = res.data.results || res.data
    if (selectedWarehouse.value) {
      data = data.filter((s: WarehouseStock) => s.warehouse.toString() === selectedWarehouse.value.toString())
    }
    stocks.value = data
  } catch (err: any) {
    console.error("Failed to fetch stock", err)
    error.value = err.response?.data?.detail || 'Failed to load stock data.'
  } finally {
    loading.value = false
  }
}

const fetchWarehouses = async () => {
  try {
    const res = await warehousesAPI.getAll()
    warehouses.value = res.data.results || res.data
  } catch (err) {
    console.error("Failed to fetch warehouses", err)
  }
}

const openAdjustModal = (stock: WarehouseStock) => {
  activeStock.value = stock
  adjustQuantity.value = stock.quantity
  isModalOpen.value = true
}

const closeAdjustModal = () => {
  isModalOpen.value = false
  activeStock.value = null
  adjustQuantity.value = 0
}

const saveAdjustment = async () => {
  if (!activeStock.value) return
  saving.value = true
  try {
    await warehouseStockAPI.update(activeStock.value.id!, {
      quantity: adjustQuantity.value
    })
    await fetchStock()
    closeAdjustModal()
  } catch (err: any) {
    console.error("Failed to adjust stock", err)
    alert(err.response?.data?.detail || 'Failed to adjust stock.')
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  await fetchWarehouses()
  await fetchStock()
})
</script>
