<template>
  <div class="h-full flex flex-col bg-gray-50 pb-12">
    <!-- Header -->
    <div class="px-8 py-6 border-b border-gray-200 bg-white sticky top-0 z-10 flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-900">New product</h1>
      <div class="flex gap-3">
        <button @click="$router.back()" class="px-4 py-2 border border-gray-300 text-gray-700 bg-white rounded-md text-sm font-semibold hover:bg-gray-50 transition-colors">
          Discard
        </button>
        <button @click="handleSave" class="px-6 py-2 bg-teal-600 text-white rounded-md text-sm font-semibold hover:bg-teal-700 transition-colors shadow-sm disabled:opacity-50" :disabled="loading">
          {{ loading ? 'Saving...' : 'Save product' }}
        </button>
      </div>
    </div>

    <div class="flex-1 overflow-auto px-8 py-8">
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
                  <label class="block text-sm font-medium text-gray-700 mb-1">Name (Urdu)</label>
                  <input v-model="form.nameUrdu" type="text" dir="rtl" class="block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring-teal-500 focus:border-teal-500 sm:text-sm font-urdu" />
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

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">SRO schedule (optional)</label>
                    <input v-model="form.sro_schedule" type="text" placeholder="e.g. EIGHTH SCHEDULE Table 1" class="block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring-teal-500 focus:border-teal-500 sm:text-sm" />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">SRO item serial no (optional)</label>
                    <input v-model="form.sro_serial" type="text" placeholder="e.g. 70" class="block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring-teal-500 focus:border-teal-500 sm:text-sm" />
                  </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Unit of measure <span class="text-red-500">*</span></label>
                    <select v-model="form.uom" class="block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring-teal-500 focus:border-teal-500 sm:text-sm">
                      <option value="Numbers, pieces, units">Numbers, pieces, units</option>
                      <option value="1000 kWh">1000 kWh</option>
                      <option value="40 KG">40 KG</option>
                      <option value="Bag">Bag</option>
                      <option value="Barrels">Barrels</option>
                      <option value="Bill of Lading">Bill of Lading</option>
                      <option value="Bottle">Bottle</option>
                      <option value="Box">Box</option>
                      <option value="Bundle">Bundle</option>
                      <option value="Carat">Carat</option>
                      <option value="Carton">Carton</option>
                      <option value="Case">Case</option>
                      <option value="Cubic Metre">Cubic Metre</option>
                      <option value="Dozen">Dozen</option>
                      <option value="Drum">Drum</option>
                      <option value="Foot">Foot</option>
                      <option value="Gallon">Gallon</option>
                      <option value="Gram">Gram</option>
                      <option value="Inch">Inch</option>
                      <option value="KG">Kilogram</option>
                      <option value="KWH">Kilowatt Hour (KWH)</option>
                      <option value="Litre">Litre</option>
                      <option value="Mega Watt (MW)">Mega Watt (MW)</option>
                      <option value="Metre">Metre</option>
                      <option value="Metric Ton">Metric Ton</option>
                      <option value="Million BTU (MMBTU)">Million BTU (MMBTU)</option>
                      <option value="Pack">Pack / Packet</option>
                      <option value="Pair">Pair</option>
                      <option value="Pallet">Pallet</option>
                      <option value="Piece">Piece</option>
                      <option value="Roll">Roll</option>
                      <option value="Set">Set</option>
                      <option value="Sheet">Sheet</option>
                      <option value="Square Foot">Square Foot</option>
                      <option value="Square Metre">Square Metre</option>
                      <option value="Ton">Ton</option>
                      <option value="Tube">Tube</option>
                      <option value="Yard">Yard</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Tax rate</label>
                    <select v-model="form.tax_rate_percent" class="block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring-teal-500 focus:border-teal-500 sm:text-sm">
                      <option value="">— None —</option>
                      <option value="18%">Standard 18%</option>
                      <option value="5%">Reduced 5%</option>
                      <option value="0%">Zero Rated</option>
                      <option value="0%">Exempt</option>
                    </select>
                  </div>
                </div>

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

                <div class="flex items-center pt-2">
                  <input id="taxable" v-model="form.taxable" type="checkbox" class="h-4 w-4 text-teal-600 focus:ring-teal-500 border-gray-300 rounded" />
                  <label for="taxable" class="ml-2 block text-sm font-medium text-gray-900">Taxable</label>
                </div>
              </div>
            </section>
          </div>
          
          <!-- RIGHT COLUMN -->
          <div class="space-y-8 flex flex-col">
            <!-- Pricing Section -->
            <section class="bg-white shadow-sm rounded-lg border border-gray-200 p-6">
              <h2 class="text-lg font-bold text-gray-900 mb-6">Pricing</h2>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Cost price</label>
                  <div class="relative rounded-md shadow-sm">
                    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <span class="text-gray-500 sm:text-sm">Rs</span>
                    </div>
                    <input v-model="form.cost_price" type="number" step="0.01" class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:ring-teal-500 focus:border-teal-500 sm:text-sm" placeholder="0.00" />
                  </div>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Sale price <span class="text-red-500">*</span></label>
                  <div class="relative rounded-md shadow-sm">
                    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <span class="text-gray-500 sm:text-sm">Rs</span>
                    </div>
                    <input v-model="form.price" type="number" step="0.01" class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:ring-teal-500 focus:border-teal-500 sm:text-sm" placeholder="0.00" />
                  </div>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Retail price</label>
                  <div class="relative rounded-md shadow-sm">
                    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <span class="text-gray-500 sm:text-sm">Rs</span>
                    </div>
                    <input v-model="form.retail_price" type="number" step="0.01" class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:ring-teal-500 focus:border-teal-500 sm:text-sm" placeholder="0.00" />
                  </div>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Min sale price</label>
                  <div class="relative rounded-md shadow-sm">
                    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <span class="text-gray-500 sm:text-sm">Rs</span>
                    </div>
                    <input v-model="form.min_sale_price" type="number" step="0.01" class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:ring-teal-500 focus:border-teal-500 sm:text-sm" placeholder="0.00" />
                  </div>
                </div>
              </div>
            </section>
            
            <!-- Inventory Section -->
            <section class="bg-white shadow-sm rounded-lg border border-gray-200 p-6">
              <h2 class="text-lg font-bold text-gray-900 mb-6">Inventory</h2>
              <div class="space-y-6">
                <div class="grid grid-cols-2 gap-4 max-w-sm">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Current Stock</label>
                    <input v-model="form.current_stock" type="number" class="block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring-teal-500 focus:border-teal-500 sm:text-sm" placeholder="0" />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Reorder level</label>
                    <input v-model="form.reorder_level" type="number" class="block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring-teal-500 focus:border-teal-500 sm:text-sm" placeholder="0" />
                  </div>
                </div>
                
                <div class="flex items-center pt-2">
                  <input id="active" v-model="form.active" type="checkbox" class="h-4 w-4 text-teal-600 focus:ring-teal-500 border-gray-300 rounded" />
                  <label for="active" class="ml-2 block text-sm font-medium text-gray-900">Active</label>
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
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useProductsStore } from '@/stores/pos/productsStore'
import { hsCodesAPI, type HSCode } from '@/apis/pos/hscodes/hsCodesAPI'
import { categoriesAPI } from '@/apis/pos/categories/categoriesAPI'

const router = useRouter()
const productsStore = useProductsStore()
const loading = ref(false)
const dropdownOpen = ref(false)
const hsSearch = ref('')
const dropdownRef = ref<HTMLElement | null>(null)
const hsCodesList = ref<HSCode[]>([])
const searchingHS = ref(false)
const categories = ref<any[]>([])

const form = reactive({
  name: '',
  nameUrdu: '',
  sku: '',
  barcode: '',
  category_id: '',
  cost_price: null,
  price: null,
  retail_price: null,
  min_sale_price: null,
  hs_code: '',
  sro_schedule: '',
  sro_serial: '',
  uom: 'Numbers, pieces, units',
  tax_rate_percent: '18%',
  fbr_sale_type: 'Goods at standard rate (default)',
  taxable: true,
  current_stock: 0,
  reorder_level: 0,
  active: true,
})

// Close dropdown when clicking outside
const handleClickOutside = (event: MouseEvent) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target as Node)) {
    dropdownOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('mousedown', handleClickOutside)
  searchHSCodes() // Initial fetch
  loadCategories()
})

const loadCategories = async () => {
  try {
    const res = await categoriesAPI.fetchCategories()
    categories.value = res
  } catch (error) {
    console.error('Failed to load categories', error)
  }
}

onUnmounted(() => {
  document.removeEventListener('mousedown', handleClickOutside)
})

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

const normalizeTaxRatePercent = (value: string) => {
  return value === '8%' ? '5%' : value
}

const handleSave = async () => {
  if (!form.name || !form.sku || !form.price || !form.hs_code) {
    alert('Please fill all required fields (Name, SKU, Sale Price, HS Code)')
    return
  }

  loading.value = true
  try {
    const payload = {
      name: form.name,
      sku: form.sku,
      barcode: form.barcode,
      category_id: form.category_id ? Number(form.category_id) : undefined,
      selling_price: Number(form.price),
      cost_price: form.cost_price ? Number(form.cost_price) : 0,
      fbr_fixed_retail_price: form.retail_price ? Number(form.retail_price) : 0,
      current_stock: Number(form.current_stock) || 0, 
      hs_code: form.hs_code,
      fbr_sale_type: form.fbr_sale_type,
      tax_rate_percent: normalizeTaxRatePercent(form.tax_rate_percent) || "0%",
      unit_of_measure: form.uom,
      fbr_sro_schedule_no: form.sro_schedule,
      fbr_sro_item_serial_no: form.sro_serial,
    }
    
    await productsStore.createProduct(payload as any)
    router.push('/pos/products')
  } catch (error) {
    console.error(error)
    alert('Failed to save product. Please check network logs.')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jameel+Noori+Nastaleeq&display=swap');

.font-urdu {
  font-family: 'Jameel Noori Nastaleeq', 'Noto Nastaliq Urdu', serif;
}
</style>
