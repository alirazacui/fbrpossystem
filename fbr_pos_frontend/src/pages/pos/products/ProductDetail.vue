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

                <!-- HS code — searchable dropdown (same as Create page) -->
                <div class="relative" ref="dropdownRef">
                  <label class="block text-sm font-medium text-gray-700 mb-1">HS code <span class="text-red-500">*</span></label>

                  <div
                    class="block w-full border rounded-md py-2 px-3 bg-white cursor-pointer flex justify-between items-center sm:text-sm"
                    :class="dropdownOpen ? 'border-teal-500 ring-1 ring-teal-500' : 'border-gray-300 text-gray-500'"
                    @click="dropdownOpen = !dropdownOpen"
                  >
                    <span :class="{'text-gray-900': form.hs_code}">{{ form.hs_code || '— pick HS code —' }}</span>
                    <svg class="h-4 w-4 text-gray-400" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" /></svg>
                  </div>

                  <div v-if="dropdownOpen" class="absolute z-20 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg max-h-60 overflow-auto">
                    <div class="sticky top-0 bg-white p-2 border-b border-gray-200">
                      <div class="relative rounded-md shadow-sm border border-green-500">
                        <div class="absolute inset-y-0 left-0 pl-2 flex items-center pointer-events-none">
                          <svg class="h-4 w-4 text-gray-400" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" /></svg>
                        </div>
                        <input type="text" v-model="hsSearch" @input="searchHSCodes" class="block w-full pl-8 pr-3 py-1.5 focus:outline-none sm:text-sm" placeholder="Search HS code or description..." />
                      </div>
                    </div>
                    <ul class="py-1">
                      <li v-if="searchingHS" class="px-3 py-4 text-center text-sm text-gray-500 animate-pulse">
                        Searching FBR catalog...
                      </li>
                      <template v-else>
                        <li v-for="item in hsCodesList" :key="item.code" @click="selectHS(item.code)" class="cursor-pointer hover:bg-gray-100 px-3 py-2">
                          <div class="font-bold text-sm text-gray-900">{{ item.code }}</div>
                          <div class="text-xs text-gray-500 uppercase truncate">{{ item.description }}</div>
                        </li>
                        <li v-if="hsCodesList.length === 0" class="px-3 py-4 text-center text-sm text-gray-500">
                          No HS codes found matching "{{ hsSearch }}"
                        </li>
                      </template>
                    </ul>
                  </div>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Tax rate</label>
                  <select v-model="form.tax_rate_percent" class="block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring-teal-500 focus:border-teal-500 sm:text-sm">
                    <option value="">— None —</option>
                    <option value="18%">Standard 18%</option>
                    <option value="17%">17%</option>
                    <option value="15%">15%</option>
                    <option value="16%">16%</option>
                    <option value="5%">Reduced 5%</option>
                    <option value="0%">Zero Rated</option>
                    <option value="Exempt">Exempt</option>
                  </select>
                </div>

                <!-- FBR sale type — grouped select (same as Create page) -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">FBR sale type</label>
                  <select v-model="form.fbr_sale_type" class="block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring-teal-500 focus:border-teal-500 sm:text-sm">
                    <optgroup label="Common">
                      <option value="Goods at standard rate (default)">Standard rate (general goods)</option>
                      <option value="3rd Schedule Goods">3rd Schedule (taxed on retail price)</option>
                      <option value="Goods at Reduced Rate">Reduced rate (8th Schedule)</option>
                      <option value="Goods at zero-rate">Zero-rated (5th Schedule)</option>
                      <option value="Exempt Goods">Exempt (6th Schedule)</option>
                      <option value="Electric Vehicle">Electric Vehicle</option>
                      <option value="Mobile Phones">Mobile Phones (9th Schedule)</option>
                    </optgroup>
                    <optgroup label="Specialised / sector-specific">
                      <option value="CNG Sales">CNG Sales</option>
                      <option value="Cement /Concrete Block">Cement /Concrete Block</option>
                      <option value="Cotton Ginners">Cotton ginners</option>
                      <option value="Electricity Supply to Retailers">Electricity Supply to Retailers</option>
                      <option value="Gas to CNG stations">Gas to CNG stations</option>
                      <option value="Goods as per SRO.297(|)/2023">Goods per SRO.297(|)/2023</option>
                      <option value="Goods (FED in ST Mode)">Goods — FED in ST mode</option>
                      <option value="Non-Adjustable Supplies">Non-Adjustable Supplies</option>
                      <option value="Petroleum Products">Petroleum Products</option>
                      <option value="Potassium Chlorate">Potassium Chlorate</option>
                      <option value="Processing/ Conversion of Goods">Processing/Conversion of Goods</option>
                      <option value="Services">Services</option>
                      <option value="Services (FED in ST Mode)">Services — FED in ST mode</option>
                      <option value="Ship breaking">Ship breaking</option>
                      <option value="Steel Melting and re-rolling">Steel melting and re-rolling</option>
                      <option value="Telecommunication services">Telecommunication services</option>
                      <option value="Toll Manufacturing">Toll Manufacturing</option>
                    </optgroup>
                  </select>
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
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { productsAPI } from '@/apis/pos/products/productsAPI'
import { categoriesAPI } from '@/apis/pos/categories/categoriesAPI'
import { hsCodesAPI, type HSCode } from '@/apis/pos/hscodes/hsCodesAPI'

const router = useRouter()
const route = useRoute()
const loading = ref(false)
const loadingInit = ref(true)
const categories = ref<any[]>([])

// HS code dropdown state (same pattern as Create page)
const dropdownOpen = ref(false)
const dropdownRef = ref<HTMLElement | null>(null)
const hsSearch = ref('')
const hsCodesList = ref<HSCode[]>([])
const searchingHS = ref(false)

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

// Close HS code dropdown when clicking outside
const handleClickOutside = (event: MouseEvent) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target as Node)) {
    dropdownOpen.value = false
  }
}

onMounted(async () => {
  document.addEventListener('mousedown', handleClickOutside)
  searchHSCodes() // initial fetch, same as Create page

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
    form.tax_rate_percent = normalizeTaxRatePercent(product.tax_rate_percent)
  } catch (error) {
    console.error('Failed to load product details', error)
    alert('Failed to load product details.')
    router.back()
  } finally {
    loadingInit.value = false
  }
})

onUnmounted(() => {
  document.removeEventListener('mousedown', handleClickOutside)
})

// HS code search — identical logic to Create page
let searchTimeout: any = null
const searchHSCodes = () => {
  searchingHS.value = true
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(async () => {
    try {
      const data = await hsCodesAPI.fetchHSCodes(1, hsSearch.value)
      hsCodesList.value = data.results
    } catch (e) {
      console.error(e)
    } finally {
      searchingHS.value = false
    }
  }, 400)
}

const selectHS = (code: string) => {
  form.hs_code = code
  dropdownOpen.value = false
}

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

const normalizeTaxRatePercent = (value: string | number) => {
  const normalized = String(value || '').trim()
  if (!normalized) {
    return ''
  }
  if (normalized === '8%' || normalized === '8') {
    return '5%'
  }
  if (normalized === 'Exempt') {
    return 'Exempt'
  }
  return normalized.endsWith('%') ? normalized : `${normalized}%`
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