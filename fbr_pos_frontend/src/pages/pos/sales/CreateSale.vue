<template>
  <div class="w-full space-y-6 pb-24 px-2 sm:px-4 lg:px-6 mt-4">
    <!-- Header -->
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 tracking-tight">New invoice</h1>
        <p class="text-sm text-gray-500 mt-2">Manual entry — For wholesalers, service providers, or office staff issuing tax invoices outside the POS.</p>
      </div>
    </div>

    <!-- Main Grid -->
    <div class="flex flex-col xl:flex-row gap-6">
      
      <!-- Left Column (Buyer & Details) -->
      <div class="flex-1 space-y-6">
        
        <!-- Buyer Card -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-100 bg-gray-50/50">
            <h2 class="text-base font-semibold text-gray-800">Header</h2>
          </div>
          <div class="p-6">
            <label class="block text-sm font-medium text-gray-700 mb-2">Buyer</label>
            <div class="relative">
              <select v-model="selectedCustomerId" class="block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm pl-3 pr-10 py-2.5 bg-white border appearance-none">
                <option :value="null">Walk-in (unregistered)</option>
                <option v-for="customer in customers" :key="customer.id" :value="customer.id">
                  {{ customer.name }} <span v-if="customer.ntn_cnic">({{ customer.ntn_cnic }})</span>
                </option>
              </select>
              <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-500">
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
              </div>
            </div>
          </div>
        </div>

        <!-- Items Card -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-100 bg-gray-50/50 flex justify-between items-center">
            <h2 class="text-base font-semibold text-gray-800">Items</h2>
            <button @click="showProductSelector = !showProductSelector" class="inline-flex items-center px-3 py-1.5 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors">
              <svg class="-ml-1 mr-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path></svg>
              Add Products
            </button>
          </div>
          
          <div class="p-6">
            <!-- Product Search -->
            <div v-if="showProductSelector" class="mb-6 p-4 bg-gray-50 rounded-lg border border-gray-200 animate-fade-in-down">
              <div class="flex items-center gap-3 mb-4">
                <div class="relative flex-1">
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" /></svg>
                  </div>
                  <input 
                    type="text" 
                    v-model="productSearchQuery" 
                    placeholder="Search by SKU, barcode, name..." 
                    class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
                  >
                </div>
                <div class="text-sm font-medium text-gray-700 whitespace-nowrap">
                  {{ saleLines.length }} item added
                </div>
                <button @click="showProductSelector = false" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700">
                  Done
                </button>
              </div>
              <p class="text-xs text-gray-500 mb-2">Click a product to add it. Click again to add another of the same item. Press 'Done' when finished.</p>
              
              <div class="bg-white border border-gray-200 rounded-md overflow-hidden max-h-60 overflow-y-auto">
                <div v-for="product in filteredProducts" :key="product.id" @click="addProduct(product)" class="flex justify-between items-center p-3 hover:bg-green-50 cursor-pointer border-b border-gray-100 last:border-0 group">
                  <div>
                    <p class="text-sm font-bold text-gray-900 group-hover:text-green-700">{{ product.name }}</p>
                    <p class="text-xs text-gray-500">SKU: {{ product.sku || 'N/A' }} | HS Code: {{ product.hs_code || 'N/A' }}</p>
                  </div>
                  <div class="text-right">
                    <p class="text-sm font-bold text-gray-900">{{ product.selling_price !== null && product.selling_price !== undefined ? 'Rs ' + formatMoney(Number(product.selling_price)) : 'N/A' }}</p>
                    <span :class="product.current_stock < 0 ? 'text-red-500' : 'text-gray-500'" class="text-xs font-medium">{{ product.current_stock }} in stock</span>
                  </div>
                </div>
                <div v-if="filteredProducts.length === 0" class="p-4 text-center text-sm text-gray-500">
                  No products found matching "{{ productSearchQuery }}"
                </div>
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="saleLines.length === 0" class="text-center py-8 text-sm text-gray-500">
              No products yet. Click "Add Products" to pick one.
            </div>

            <!-- Items Table -->
            <div v-else class="overflow-x-auto overflow-y-visible">
              <table class="min-w-full divide-y divide-gray-200 text-left">
                <thead>
                  <tr class="text-xs font-bold text-gray-900 uppercase tracking-wide">
                    <th scope="col" class="pb-3 w-1/4">SKU / name</th>
                    <th scope="col" class="pb-3 w-32">HS code</th>
                    <th scope="col" class="pb-3 w-24">UoM</th>
                    <th scope="col" class="pb-3 text-right w-20">Avail.</th>
                    <th scope="col" class="pb-3 text-right w-24">Qty</th>
                    <th scope="col" class="pb-3 text-right w-28">Rate (Rs)</th>
                    <th scope="col" class="pb-3 text-right w-20">Tax %</th>
                    <th scope="col" class="pb-3 text-right w-28">Discount</th>
                    <th scope="col" class="pb-3 text-right w-28">Line total</th>
                    <th scope="col" class="w-10"></th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100">
                  <tr v-for="(line, index) in saleLines" :key="index" class="group align-top">
                    <td class="py-4">
                      <p class="text-xs text-gray-500 font-medium">{{ line.product.sku || 'N/A' }}</p>
                      <p class="text-sm text-gray-900 font-bold uppercase truncate max-w-[200px]" :title="line.product.name">{{ line.product.name }}</p>
                    </td>
                    <td class="py-4">
                      <input type="text" :value="line.product.hs_code || 'N/A'" disabled class="w-full text-sm bg-gray-50 border border-gray-200 rounded px-2 py-1 text-gray-500 font-mono">
                    </td>
                    <td class="py-4">
                      <input type="text" value="Kilogram" disabled class="w-full text-sm bg-gray-50 border border-gray-200 rounded px-2 py-1 text-gray-500">
                    </td>
                    <td class="py-4 text-right">
                      <span :class="line.product.current_stock < line.quantity ? 'text-red-500 font-bold' : 'text-gray-900 font-medium'">{{ line.product.current_stock }}</span>
                    </td>
                    <td class="py-4 text-right">
                      <input type="number" v-model.number="line.quantity" min="1" :max="line.product.current_stock > 0 ? line.product.current_stock : undefined" class="w-20 text-right text-sm border-gray-300 rounded shadow-sm focus:ring-green-500 focus:border-green-500">
                    </td>
                    <td class="py-4 text-right">
                      <input type="number" v-model.number="line.unit_price" step="0.01" class="w-24 text-right text-sm border-gray-300 rounded shadow-sm focus:ring-green-500 focus:border-green-500">
                    </td>
                    <td class="py-4 text-right">
                      <input type="number" v-model.number="line.tax_rate_percent" step="0.1" class="w-16 text-right text-sm border-gray-300 rounded shadow-sm focus:ring-green-500 focus:border-green-500">
                    </td>
                    <td class="py-4 text-right">
                      <input type="number" v-model.number="line.line_discount" step="0.01" class="w-24 text-right text-sm border-gray-300 rounded shadow-sm focus:ring-green-500 focus:border-green-500">
                    </td>
                    <td class="py-4 text-right font-bold text-gray-900 flex items-center justify-end h-full mt-2">
                      Rs. {{ formatMoney(calculateLineTotal(line)) }}
                    </td>
                    <td class="py-4 text-right pl-2 mt-2">
                      <button @click="removeLine(index)" class="text-gray-400 hover:text-red-500 transition-colors">
                        <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Notes Card -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-100 bg-gray-50/50">
            <h2 class="text-base font-semibold text-gray-800">Notes</h2>
          </div>
          <div class="p-6">
            <textarea v-model="notes" rows="3" placeholder="Any notes for this invoice (visible in admin only)..." class="block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm resize-none"></textarea>
            <p class="mt-3 text-xs text-gray-500 flex items-center">
              <span class="bg-gray-100 text-gray-600 px-2 py-0.5 rounded mr-2 font-medium">Buyer: {{ selectedCustomerName }}</span>
              Saved as a draft locally. On the next screen you can "Validate with FBR" (free dry-run) and then "Submit to FBR" when ready.
            </p>
          </div>
        </div>

        <!-- Warnings -->
        <div v-if="outOfStockLines.length > 0" class="bg-yellow-50 border border-yellow-200 rounded-xl p-4 flex items-start">
          <svg class="h-5 w-5 text-yellow-500 mt-0.5 mr-3 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
          </svg>
          <div>
            <h3 class="text-sm font-bold text-yellow-800">Selling more than you have on hand</h3>
            <ul class="list-disc pl-5 mt-1 space-y-1">
              <li v-for="line in outOfStockLines" :key="line.product_id" class="text-xs text-yellow-700">
                <span class="font-bold">{{ line.product.name }}</span>: on hand {{ line.product.current_stock }}, invoicing {{ line.quantity }} (short {{ line.quantity - line.product.current_stock }})
              </li>
            </ul>
            <p class="text-xs text-yellow-600 mt-2">You can still create this invoice — stock will go negative. Check the count or restock if this looks wrong.</p>
          </div>
        </div>

      </div>

      <!-- Right Column (Live Totals) -->
      <div class="w-full xl:w-96 space-y-6">
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden sticky top-6">
          <div class="px-6 py-4 border-b border-gray-100 bg-gray-50/50">
            <h2 class="text-base font-semibold text-gray-800">Live totals</h2>
          </div>
          <div class="p-6 space-y-4">
            <div class="flex justify-between text-sm">
              <span class="text-gray-500">Subtotal</span>
              <span class="font-medium text-gray-900">Rs. {{ formatMoney(subtotal) }}</span>
            </div>
            
            <div class="flex items-center justify-between text-sm group">
              <span class="text-gray-500">Invoice discount</span>
              <div class="flex items-center w-24">
                <input type="number" v-model.number="globalDiscount" min="0" max="100" class="block w-16 text-right rounded-l-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm z-10 transition-colors">
                <span class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-500 sm:text-sm">%</span>
              </div>
            </div>

            <div class="flex justify-between text-sm">
              <span class="text-gray-500">Tax</span>
              <span class="font-medium text-gray-900">Rs. {{ formatMoney(totalTax) }}</span>
            </div>

            <div class="pt-4 border-t border-gray-100 flex justify-between items-center">
              <span class="text-base font-bold text-gray-900">Grand total</span>
              <span class="text-xl font-bold text-green-600">Rs. {{ formatMoney(grandTotal) }}</span>
            </div>
          </div>
          
          <!-- By rate band -->
          <div v-if="Object.keys(taxesByRate).length > 0" class="px-6 pb-6 pt-2 border-t border-gray-50 bg-gray-50/30">
            <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3">By rate band</h3>
            <div class="space-y-3">
              <div v-for="(data, rate) in taxesByRate" :key="rate" class="flex flex-col text-xs text-gray-600 bg-white p-3 rounded-md border border-gray-100 shadow-sm">
                <span class="font-bold text-gray-800 mb-1">{{ rate }}%</span>
                <span class="text-gray-500">Rs. {{ formatMoney(data.subtotal) }} &rarr; tax <span class="font-semibold text-gray-900">Rs. {{ formatMoney(data.tax) }}</span></span>
              </div>
            </div>
          </div>
          
        </div>
      </div>

    </div>

    <!-- Preview Section -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden mt-8">
      <div class="px-6 py-4 border-b border-gray-100 bg-gray-50/50 flex justify-between items-center">
        <h2 class="text-base font-semibold text-gray-800">Preview</h2>
        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
          Sale invoice
        </span>
      </div>
      <div class="p-8 bg-gray-100 flex justify-center w-full">
        <!-- Receipt Mockup -->
        <div class="bg-white w-full p-10 rounded-sm shadow-md border border-gray-200">
          <div class="flex justify-between items-start border-b-2 border-gray-800 pb-8 mb-8">
            <div class="space-y-1">
              <h3 class="text-3xl font-black text-gray-900 tracking-tight uppercase">{{ authStore.company?.name || 'Your Company' }}</h3>
              <p class="text-sm font-medium text-gray-600">NTN: <span class="text-gray-900">{{ authStore.company?.ntn || 'N/A' }}</span></p>
              <p class="text-sm font-medium text-gray-600">Sector: All Other Sectors</p>
            </div>
            <div class="text-right">
              <div class="text-4xl font-black text-gray-200 uppercase tracking-widest">INVOICE</div>
              <div class="text-sm font-bold text-gray-500 mt-2">DRAFT — (assigned on save)</div>
            </div>
          </div>

          <div class="mb-10 grid grid-cols-2 gap-8">
            <div>
              <p class="text-xs text-gray-400 uppercase tracking-widest font-bold mb-2">Billed To</p>
              <p class="text-lg font-bold text-gray-900">{{ selectedCustomerName }}</p>
              <p class="text-sm font-medium text-gray-500">{{ selectedCustomerId ? 'Registered Customer' : 'Unregistered / Walk-in' }}</p>
            </div>
            <div class="text-right">
              <p class="text-xs text-gray-400 uppercase tracking-widest font-bold mb-2">Date</p>
              <p class="text-sm font-bold text-gray-900">{{ new Date().toLocaleDateString('en-PK', { year: 'numeric', month: 'long', day: 'numeric' }) }}</p>
            </div>
          </div>

          <table class="w-full text-sm mb-10">
            <thead>
              <tr class="text-gray-900 border-b-2 border-gray-800">
                <th class="pb-3 text-left font-bold uppercase text-xs tracking-wider">Description</th>
                <th class="pb-3 text-right font-bold uppercase text-xs tracking-wider w-24">Qty</th>
                <th class="pb-3 text-right font-bold uppercase text-xs tracking-wider w-32">Rate</th>
                <th class="pb-3 text-right font-bold uppercase text-xs tracking-wider w-32">Tax</th>
                <th class="pb-3 text-right font-bold uppercase text-xs tracking-wider w-32">Amount</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-if="saleLines.length === 0">
                <td colspan="5" class="py-8 text-center text-gray-400 font-medium italic">No items added to invoice</td>
              </tr>
              <tr v-for="(line, index) in saleLines" :key="index">
                <td class="py-4 text-gray-900 font-medium">
                  <p class="text-sm font-medium text-gray-900">{{ line.product.name }}</p>
                  <p class="text-xs text-gray-500">{{ line.product.sku }}</p>
                </td>
                <td class="py-4 text-right text-gray-700">{{ line.quantity }}</td>
                <td class="py-4 text-right text-gray-700">{{ formatMoney(line.unit_price) }}</td>
                <td class="py-4 text-right text-gray-700">{{ formatMoney(calculateLineTax(line)) }}</td>
                <td class="py-4 text-right text-gray-900 font-bold">{{ formatMoney(calculateLineTotal(line)) }}</td>
              </tr>
            </tbody>
          </table>

          <div class="flex justify-end border-t-2 border-gray-800 pt-8">
            <div class="w-80 space-y-3 text-sm">
              <div class="flex justify-between items-center">
                <span class="text-gray-600 font-medium">Subtotal</span>
                <span class="text-gray-900 font-medium">Rs. {{ formatMoney(subtotal) }}</span>
              </div>
              <div v-if="globalDiscount > 0" class="flex justify-between items-center">
                <span class="text-gray-600 font-medium">Discount ({{ globalDiscount }}%)</span>
                <span class="text-red-600 font-medium">- Rs. {{ formatMoney(totalDiscountValue) }}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-gray-600 font-medium">Sales Tax</span>
                <span class="text-gray-900 font-medium">Rs. {{ formatMoney(totalTax) }}</span>
              </div>
              <div class="flex justify-between items-center pt-4 border-t border-gray-200">
                <span class="text-gray-900 font-black text-lg uppercase tracking-wider">Total</span>
                <span class="text-gray-900 font-black text-xl">Rs. {{ formatMoney(grandTotal) }}</span>
              </div>
            </div>
          </div>
          
          <div class="mt-16 pt-8 border-t border-gray-200 flex justify-between items-center">
            <p class="text-xs text-gray-500 font-medium">Notes: {{ notes || 'None' }}</p>
            <p class="text-xs text-gray-400 italic">This is a preview. Official PDF generated after FBR submission.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Fixed Bottom Actions -->
    <div class="fixed bottom-0 left-0 right-0 lg:left-64 bg-white border-t border-gray-200 p-4 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)] z-40">
      <div class="w-full px-2 sm:px-4 lg:px-6 flex items-center justify-between">
        <p class="text-sm text-gray-500">
          The invoice will be saved locally as a draft. You can validate + submit it to FBR from the invoice detail page.
        </p>
        <div class="flex space-x-3">
          <button @click="$router.back()" class="px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
            Cancel
          </button>
          <button @click="submitInvoice" :disabled="isSubmitting || saleLines.length === 0" class="inline-flex items-center px-6 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed">
            <svg v-if="isSubmitting" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
            Create invoice
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth/authStore'
import { productsAPI, type Product } from '@/apis/pos/products/productsAPI'
import { customersAPI, type Customer } from '@/apis/pos/customers/customersAPI'
import { salesAPI } from '@/apis/pos/sales/salesAPI'
import axiosInstance from '@/apis/axiosInstance'

const router = useRouter()
const authStore = useAuthStore()

// State
const customers = ref<Customer[]>([])
const products = ref<Product[]>([])
const selectedCustomerId = ref<number | null>(null)
const showProductSelector = ref(false)
const productSearchQuery = ref('')
const isSubmitting = ref(false)
const notes = ref('')

interface LocalSaleLine {
  product_id: number;
  product: Product;
  quantity: number;
  unit_price: number;
  tax_rate_percent: number;
  line_discount: number;
}

const saleLines = ref<LocalSaleLine[]>([])
const globalDiscount = ref<number>(0)

// Fetch Data
const fetchData = async () => {
  try {
    const [custRes, prodRes] = await Promise.all([
      customersAPI.list({ limit: 100 }),
      productsAPI.list({ limit: 100 })
    ])
    customers.value = custRes.data.results || custRes.data
    products.value = prodRes.data.results || prodRes.data
  } catch (error) {
    console.error('Error fetching data:', error)
    alert('Failed to load products and customers')
  }
}

onMounted(() => {
  fetchData()
})

const filteredProducts = computed(() => {
  const query = productSearchQuery.value.toLowerCase().trim()
  if (!query) return products.value
  return products.value.filter(p => 
    p.name.toLowerCase().includes(query) || 
    (p.sku && p.sku.toLowerCase().includes(query)) ||
    (p.barcode && p.barcode.toLowerCase().includes(query))
  )
})

const outOfStockLines = computed(() => {
  return saleLines.value.filter(l => l.quantity > l.product.current_stock)
})

const selectedCustomerName = computed(() => {
  if (!selectedCustomerId.value) return 'Walk-in'
  const c = customers.value.find(c => c.id === selectedCustomerId.value)
  return c ? c.name : 'Walk-in'
})

const subtotal = computed(() => {
  return saleLines.value.reduce((sum, line) => sum + (line.unit_price * line.quantity), 0)
})

const totalDiscountValue = computed(() => {
  if (!globalDiscount.value) return 0
  return (subtotal.value * globalDiscount.value) / 100
})

const totalTax = computed(() => {
  return saleLines.value.reduce((sum, line) => sum + calculateLineTax(line), 0)
})

const grandTotal = computed(() => {
  return (subtotal.value - totalDiscountValue.value) + totalTax.value
})

const taxesByRate = computed(() => {
  const bands: Record<string, { subtotal: number, tax: number }> = {}
  saleLines.value.forEach(line => {
    const rate = Number(line.tax_rate_percent) || 0
    if (rate > 0) {
      const lineTax = calculateLineTax(line)
      const lineSub = calculateLineTotal(line) - lineTax
      if (!bands[rate]) bands[rate] = { subtotal: 0, tax: 0 }
      bands[rate].subtotal += lineSub
      bands[rate].tax += lineTax
    }
  })
  return bands
})

// Actions
const getProductName = (id: number) => {
  return products.value.find(p => p.id === id)?.name || 'Unknown Product'
}

const addProduct = (prod: Product) => {
  // Check if already in list
  const existing = saleLines.value.find(l => l.product_id === prod.id)
  if (existing) {
    existing.quantity += 1
  } else {
    saleLines.value.push({
      product_id: prod.id,
      product: prod,
      quantity: 1,
      unit_price: Number(prod.selling_price ?? prod.price) || 0,
      tax_rate_percent: normalizeTaxRatePercent(prod.tax_rate_percent),
      line_discount: 0
    })
  }
  
  productSearchQuery.value = ''
}

const removeLine = (index: number) => {
  saleLines.value.splice(index, 1)
}

const calculateLineTax = (line: LocalSaleLine) => {
  const lineSubtotal = (line.unit_price * line.quantity) - line.line_discount
  // Apply proportional global discount before calculating tax
  const proportionalDiscount = (lineSubtotal / subtotal.value) * totalDiscountValue.value || 0
  const taxableValue = lineSubtotal - proportionalDiscount
  return (taxableValue * line.tax_rate_percent) / 100
}

const calculateLineTotal = (line: LocalSaleLine) => {
  const lineSubtotal = (line.unit_price * line.quantity) - line.line_discount
  const proportionalDiscount = (lineSubtotal / subtotal.value) * totalDiscountValue.value || 0
  return (lineSubtotal - proportionalDiscount) + calculateLineTax(line)
}

const normalizeTaxRatePercent = (value: string | number) => {
  const normalized = String(value)
  if (normalized === '8%' || normalized === '8') return 5
  return parseFloat(normalized.replace('%', '')) || 0
}

const formatMoney = (val: number) => {
  return val.toFixed(2)
}

const submitInvoice = async () => {
  if (saleLines.value.length === 0) return
  
  isSubmitting.value = true
  try {
    const payload = {
      customer: selectedCustomerId.value || undefined,
      notes: notes.value || '',
      sale_type: 'Sale Invoice',
      // cash_session if applicable
    }
    
    // 1. Create Draft Sale
    const response = await salesAPI.create(payload as any)
    const saleId = response.data.id
    
    // 2. Add Lines
    for (const line of saleLines.value) {
      const lineSubtotal = (line.unit_price * line.quantity) - line.line_discount
      const proportionalDiscount = (lineSubtotal / subtotal.value) * totalDiscountValue.value || 0
      await axiosInstance.post(`/sales/${saleId}/add-line/`, {
        product_id: line.product_id,
        quantity: line.quantity,
        unit_price: line.unit_price,
        discount_amount: line.line_discount + proportionalDiscount,
      })
    }
    
    // 3. (Optional) We skip adding payment and completing the sale here
    // because the user wants this to be saved purely as a DRAFT.
    // They will validate and submit on the details screen.

    alert('Draft invoice created successfully!')
    // Navigate to sale list page
    router.push(`/pos/sales/`)
  } catch (error: any) {
    console.error('Submit error:', error)
    alert(error.response?.data?.message || 'Failed to create invoice')
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.animate-fade-in-down {
  animation: fadeInDown 0.3s ease-out;
}

@keyframes fadeInDown {
  0% {
    opacity: 0;
    transform: translateY(-10px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
