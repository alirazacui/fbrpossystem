<template>
  <div class="h-full flex flex-col bg-gray-50 pb-12">
    <!-- Header -->
    <div class="px-8 py-6 border-b border-gray-200 bg-white sticky top-0 z-10 flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-900">Product Details</h1>
      <div class="flex gap-3">
        <button @click="deleteProduct" class="px-4 py-2 border border-red-300 text-red-700 bg-white rounded-md text-sm font-semibold hover:bg-red-50 transition-colors">
          Delete
        </button>
        <button @click="$router.back()" class="px-4 py-2 border border-gray-300 text-gray-700 bg-white rounded-md text-sm font-semibold hover:bg-gray-50 transition-colors">
          Back
        </button>
        <button @click="handleUpdate" class="px-6 py-2 bg-teal-600 text-white rounded-md text-sm font-semibold hover:bg-teal-700 transition-colors shadow-sm disabled:opacity-50" :disabled="loading">
          {{ loading ? 'Updating...' : 'Update product' }}
        </button>
      </div>
    </div>

    <div v-if="loadingInit" class="p-12 text-center text-gray-500">
      Loading product details...
    </div>
    <div v-else class="flex-1 overflow-auto px-8 py-8">
      <div class="w-full">
        <!-- Flex/Grid Layout -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
          
          <!-- LEFT COLUMN -->
          <div class="space-y-8 flex flex-col">
            <!-- Basic Section -->
            <section class="bg-white shadow-sm rounded-lg border border-gray-200 p-6">
              <h2 class="text-lg font-bold text-gray-900 mb-6">Basic</h2>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="col-span-2 md:col-span-1">
                  <label class="block text-sm font-medium text-gray-700 mb-1">Name <span class="text-red-500">*</span></label>
                  <input v-model="form.name" type="text" class="block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring-teal-500 focus:border-teal-500 sm:text-sm" />
                </div>
                
                <div class="col-span-2 md:col-span-1">
                  <label class="block text-sm font-medium text-gray-700 mb-1">SKU <span class="text-red-500">*</span></label>
                  <input v-model="form.sku" type="text" class="block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring-teal-500 focus:border-teal-500 sm:text-sm uppercase" />
                </div>
                <div class="col-span-2 md:col-span-1">
                  <label class="block text-sm font-medium text-gray-700 mb-1">Barcode</label>
                  <input v-model="form.barcode" type="text" class="block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring-teal-500 focus:border-teal-500 sm:text-sm" />
                </div>

                <div class="col-span-2 md:col-span-1">
                  <label class="block text-sm font-medium text-gray-700 mb-1">Category</label>
                  <select v-model="form.category_id" class="block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring-teal-500 focus:border-teal-500 sm:text-sm">
                    <option value="">— None —</option>
                    <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
                  </select>
                </div>
              </div>
            </section>

            <!-- Tax & FBR Section -->
            <section class="bg-white shadow-sm rounded-lg border border-gray-200 p-6">
              <h2 class="text-lg font-bold text-gray-900 mb-6">Tax & FBR</h2>
              <div class="space-y-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">HS code <span class="text-red-500">*</span></label>
                  <input v-model="form.hs_code" type="text" class="block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring-teal-500 focus:border-teal-500 sm:text-sm uppercase" />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Tax rate</label>
                  <select v-model="form.tax_rate_percent" class="block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring-teal-500 focus:border-teal-500 sm:text-sm">
                    <option value="">— None —</option>
                    <option value="18%">Standard 18%</option>
                    <option value="8%">Reduced 8%</option>
                    <option value="0%">Zero Rated / Exempt</option>
                  </select>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">FBR sale type</label>
                  <input v-model="form.fbr_sale_type" type="text" class="block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring-teal-500 focus:border-teal-500 sm:text-sm" />
                </div>
              </div>
            </section>
          </div>
          
          <!-- RIGHT COLUMN -->
          <div class="space-y-8 flex flex-col">
            <!-- Pricing Section -->
            <section class="bg-white shadow-sm rounded-lg border border-gray-200 p-6">
              <h2 class="text-lg font-bold text-gray-900 mb-6">Pricing & Inventory</h2>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Cost price</label>
                  <div class="relative rounded-md shadow-sm">
                    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <span class="text-gray-500 sm:text-sm">Rs</span>
                    </div>
                    <input v-model="form.cost_price" type="number" step="0.01" class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:ring-teal-500 focus:border-teal-500 sm:text-sm" />
                  </div>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Sale price <span class="text-red-500">*</span></label>
                  <div class="relative rounded-md shadow-sm">
                    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <span class="text-gray-500 sm:text-sm">Rs</span>
                    </div>
                    <input v-model="form.price" type="number" step="0.01" class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:ring-teal-500 focus:border-teal-500 sm:text-sm" />
                  </div>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Retail price</label>
                  <div class="relative rounded-md shadow-sm">
                    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <span class="text-gray-500 sm:text-sm">Rs</span>
                    </div>
                    <input v-model="form.retail_price" type="number" step="0.01" class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:ring-teal-500 focus:border-teal-500 sm:text-sm" />
                  </div>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Min sale price</label>
                  <div class="relative rounded-md shadow-sm">
                    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <span class="text-gray-500 sm:text-sm">Rs</span>
                    </div>
                    <input v-model="form.min_sale_price" type="number" step="0.01" class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:ring-teal-500 focus:border-teal-500 sm:text-sm" />
                  </div>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Current Stock</label>
                  <div class="relative rounded-md shadow-sm">
                    <input v-model="form.current_stock" type="number" class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-teal-500 focus:border-teal-500 sm:text-sm bg-gray-50 font-bold" />
                  </div>
                </div>
              </div>
            </section>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { productsAPI } from '@/apis/pos/products/productsAPI'
import { categoriesAPI } from '@/apis/pos/categories/categoriesAPI'

const router = useRouter()
const route = useRoute()
const loading = ref(false)
const loadingInit = ref(true)
const categories = ref<any[]>([])

const productId = Number(route.params.id)

const form = reactive({
  name: '',
  sku: '',
  barcode: '',
  category_id: '',
  price: 0,
  cost_price: 0,
  retail_price: 0,
  min_sale_price: 0,
  current_stock: 0,
  hs_code: '',
  tax_rate_percent: '18%',
  fbr_sale_type: 'Goods at standard rate (default)',
})

onMounted(async () => {
  try {
    const [catRes, prodRes] = await Promise.all([
      categoriesAPI.fetchCategories(),
      productsAPI.retrieve(productId)
    ])
    
    categories.value = catRes
    const product = prodRes.data
    
    form.name = product.name || ''
    form.sku = product.sku || ''
    form.barcode = product.barcode || ''
    form.category_id = product.category_id ? String(product.category_id) : ''
    form.price = Number(product.selling_price || product.price) || 0
    form.cost_price = Number(product.cost_price) || 0
    form.retail_price = Number(product.fbr_fixed_retail_price) || 0
    form.min_sale_price = Number(product.min_sale_price) || 0
    form.current_stock = Number(product.current_stock) || 0
    form.hs_code = product.hs_code || ''
    form.fbr_sale_type = product.fbr_sale_type || ''
    form.tax_rate_percent = product.tax_rate_percent + '%'
  } catch (error) {
    console.error('Failed to load product details', error)
    alert('Failed to load product details.')
    router.back()
  } finally {
    loadingInit.value = false
  }
})

const handleUpdate = async () => {
  loading.value = true
  try {
    const payload: Record<string, any> = {}
    if (form.name) payload.name = form.name
    if (form.sku) payload.sku = form.sku
    if (form.barcode) payload.barcode = form.barcode
    if (form.category_id) payload.category_id = Number(form.category_id)
    if (form.price !== null) payload.selling_price = Number(form.price)
    if (form.cost_price !== null) payload.cost_price = Number(form.cost_price)
    if (form.retail_price !== null) payload.fbr_fixed_retail_price = Number(form.retail_price)
    if (form.min_sale_price !== null) payload.min_sale_price = Number(form.min_sale_price)
    if (form.current_stock !== null) payload.current_stock = Number(form.current_stock)
    if (form.hs_code) payload.hs_code = form.hs_code
    if (form.fbr_sale_type) payload.fbr_sale_type = form.fbr_sale_type
    if (form.tax_rate_percent) payload.tax_rate_percent = form.tax_rate_percent
    
    await productsAPI.update(productId, payload)
    alert('Product updated successfully!')
  } catch (error) {
    console.error(error)
    alert('Failed to update product.')
  } finally {
    loading.value = false
  }
}

const deleteProduct = async () => {
  const confirmed = await (window as any).$confirm('Are you sure you want to delete this product? This action cannot be undone.')
  if (!confirmed) return
  
  try {
    await productsAPI.delete(productId)
    router.push('/pos/products')
  } catch (error) {
    console.error(error)
    alert('Failed to delete product.')
  }
}
</script>
