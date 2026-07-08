<template>
  <div class="flex flex-col pb-12 h-full bg-gray-50/50 min-h-screen">
    <!-- Welcome Section -->
    <div class="px-8 pt-8 pb-6 flex justify-between items-end border-b border-gray-200 bg-white">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 mb-1">Welcome, {{ userFullName }}.</h1>
        <p class="text-sm text-gray-500">Signed in to <span class="font-medium text-gray-700">{{ companyName }}</span>.</p>
        <p class="text-xs text-gray-400 mt-1">NTN: <span class="font-medium text-gray-600">{{ companyNtn }}</span></p>
      </div>
      <p class="text-xs text-gray-400 font-medium tracking-wide">Updated {{ timeAgo }}</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="px-8 mt-10 flex justify-center">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600"></div>
    </div>

    <!-- Dashboard Content -->
    <div v-else class="px-8 py-8 w-full space-y-6">
      
      <!-- Top KPIs (2 rows of 4) -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        
        <!-- Products -->
        <div class="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-4">
            <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider">Products</h3>
            <div class="p-1.5 bg-green-50 rounded text-green-600">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path></svg>
            </div>
          </div>
          <div class="text-2xl font-bold text-gray-900 mb-1">{{ stats?.products.active || 0 }}</div>
          <p class="text-xs text-gray-500">Active products</p>
        </div>

        <!-- Customers -->
        <div class="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-4">
            <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider">Customers</h3>
            <div class="p-1.5 bg-gray-50 rounded text-gray-500">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
            </div>
          </div>
          <div class="text-2xl font-bold text-gray-900 mb-1">{{ stats?.customers.total || 0 }}</div>
          <p class="text-xs text-gray-500">On file</p>
        </div>

        <!-- Invoices -->
        <div class="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-4">
            <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider">Invoices</h3>
            <div class="p-1.5 bg-green-50 rounded text-green-600">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
            </div>
          </div>
          <div class="text-2xl font-bold text-gray-900 mb-1">{{ stats?.invoices.this_month_count || 0 }}</div>
          <p class="text-xs text-gray-500">{{ stats?.invoices.this_month_count || 0 }} this month · Rs {{ formatMoney(stats?.invoices.this_month_total || 0) }}</p>
        </div>

        <!-- Stock -->
        <div class="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-4">
            <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider">Stock</h3>
            <div class="p-1.5 bg-gray-50 rounded text-gray-500">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
            </div>
          </div>
          <div class="text-2xl font-bold text-gray-900 mb-1">{{ stats?.products.active || 0 }}</div> <!-- Using active count as stock items count approximation -->
          <p class="text-xs text-gray-500">Rs {{ formatMoney(stats?.stock.value || 0) }} value</p>
        </div>

        <!-- Invoices today -->
        <div class="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
          <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider mb-4">Invoices Today</h3>
          <div class="text-2xl font-bold text-gray-900 mb-1">Rs. {{ formatMoney(stats?.sales_today || 0) }}</div>
          <!-- Sparkline placeholder -->
          <div class="h-6 mt-3 relative">
            <svg class="absolute inset-0 h-full w-full" preserveAspectRatio="none" viewBox="0 0 100 20">
              <polyline points="0,20 20,5 100,5" fill="none" stroke="#16a34a" stroke-width="2" />
            </svg>
          </div>
        </div>

        <!-- Sent to FBR -->
        <div class="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
          <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider mb-4">Sent to FBR</h3>
          <div class="text-2xl font-bold text-gray-900 mb-1">{{ stats?.fbr.sent || 0 }}</div>
        </div>

        <!-- Avg Invoice -->
        <div class="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
          <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider mb-4">Avg Invoice</h3>
          <div class="text-2xl font-bold text-gray-900 mb-1">Rs. {{ formatMoney(stats?.avg_invoice || 0) }}</div>
        </div>

        <!-- Pending Validation -->
        <div class="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
          <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider mb-4">Pending Validation</h3>
          <div class="text-2xl font-bold text-gray-900 mb-1">{{ stats?.fbr.pending || 0 }}</div>
        </div>

      </div>

      <!-- Chart Section -->
      <div class="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
        <div class="flex justify-between items-start mb-6">
          <div>
            <h2 class="text-sm font-bold text-gray-900">Sales over time</h2>
            <p class="text-xs text-gray-500 mt-1">{{ totalChartInvoices }} invoices · Rs {{ formatMoney(totalChartSales) }} total</p>
          </div>
          <div class="flex bg-gray-100 rounded-md p-1">
            <button class="px-3 py-1 text-xs font-medium bg-white shadow-sm rounded">Daily</button>
            <button class="px-3 py-1 text-xs font-medium text-gray-500">Sale invoice</button>
          </div>
        </div>

        <!-- CSS Bar Chart -->
        <div class="h-64 mt-4 relative flex items-end pt-4" v-if="stats && stats.chart_data">
          <!-- Y-Axis Grid Lines -->
          <div class="absolute inset-0 flex flex-col justify-between pointer-events-none pb-6">
            <div v-for="tick in yAxisTicks" :key="tick" class="border-b border-gray-100 w-full flex items-center relative">
              <span class="absolute -top-3 -left-12 text-xs text-gray-400 font-mono w-10 text-right pr-2">
                Rs {{ tick }}
              </span>
            </div>
            <!-- Zero line -->
            <div class="border-b-2 border-gray-200 w-full relative">
              <span class="absolute -top-3 -left-12 text-xs text-gray-400 font-mono w-10 text-right pr-2">
                Rs 0
              </span>
            </div>
          </div>
          
          <!-- Bars -->
          <div class="w-full flex justify-around items-end h-full ml-2 relative z-10 pb-1">
            <div v-for="day in sortedChartData" :key="day.date" class="flex flex-col items-center group w-full px-2" :style="{ height: getBarHeight(day.total) + '%' }">
              <!-- Tooltip -->
              <div class="opacity-0 group-hover:opacity-100 transition-opacity absolute -top-8 bg-gray-800 text-white text-xs py-1 px-2 rounded pointer-events-none whitespace-nowrap z-20">
                Rs {{ formatMoney(day.total) }}<br>{{ day.date }}
              </div>
              <div class="w-full max-w-[60px] bg-green-500 hover:bg-green-600 rounded-t-sm w-full h-full transition-colors cursor-pointer relative group">
              </div>
              <!-- X-Axis Label -->
              <div class="text-[10px] text-gray-500 mt-3 absolute -bottom-6 w-20 text-center -ml-10 font-mono">
                {{ day.date }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 3 Columns Bottom Section -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <!-- Recent Invoices -->
        <div class="lg:col-span-1 bg-white border border-gray-200 rounded-xl p-5 shadow-sm flex flex-col">
          <h3 class="text-sm font-bold text-gray-900 mb-4 flex items-center gap-2">
            <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
            Recent invoices
          </h3>
          <div class="space-y-4 flex-1">
            <div v-if="!stats?.recent_invoices?.length" class="text-sm text-gray-500 py-4 text-center">No recent invoices</div>
            <div v-for="inv in stats?.recent_invoices" :key="inv.id" class="flex justify-between items-center pb-3 border-b border-gray-50 last:border-0 text-sm font-mono">
              <span class="text-gray-900 truncate w-1/3">{{ inv.sale_number }}</span>
              <span class="text-gray-500 truncate w-1/3 text-center text-xs font-sans uppercase">{{ inv.customer__name }}</span>
              <span class="text-gray-900 font-bold text-right w-1/3">Rs. {{ formatMoney(inv.total_amount) }}</span>
            </div>
          </div>
          <div class="mt-4 text-right">
            <router-link to="/pos/sales" class="text-xs text-gray-500 hover:text-gray-700">All sales →</router-link>
          </div>
        </div>

        <!-- Right Side: Low Stock & Failed FBR -->
        <div class="lg:col-span-2 flex flex-col gap-6">
          
          <!-- Low Stock -->
          <div class="bg-white border border-gray-200 rounded-xl p-5 shadow-sm flex-1">
            <h3 class="text-sm font-bold text-gray-900 mb-4 flex items-center gap-2">
              <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path></svg>
              Low stock
            </h3>
            <div v-if="!stats?.low_stock?.length" class="text-sm text-gray-500 py-4">
              All stock levels healthy.
            </div>
            <div v-else class="space-y-2">
              <div v-for="item in stats.low_stock" :key="item.id" class="flex justify-between items-center pb-2 border-b border-gray-50 text-sm">
                <span class="text-gray-900">{{ item.name }}</span>
                <span class="text-red-600 font-bold">{{ item.current_stock }} left</span>
              </div>
            </div>
            <div class="mt-4 text-right">
              <router-link to="/pos/products" class="text-xs text-gray-500 hover:text-gray-700">Manage stock →</router-link>
            </div>
          </div>

          <!-- Failed FBR -->
          <div class="bg-white border border-orange-200 rounded-xl p-5 shadow-sm">
            <h3 class="text-sm font-bold text-orange-600 mb-4 flex items-center gap-2">
              <svg class="w-4 h-4 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              Failed FBR submissions
            </h3>
            <div v-if="!stats?.failed_fbr?.length" class="text-sm text-gray-500">
              No failed submissions.
            </div>
            <div v-else class="space-y-3">
              <div v-for="fail in stats.failed_fbr" :key="fail.id" class="flex gap-4 items-start pb-3 border-b border-gray-50 last:border-0 text-sm">
                <span class="font-mono text-gray-900 w-1/4 break-all">{{ fail.sale_number }}</span>
                <span class="text-gray-500 text-xs flex-1">{{ fail.fbr_error_message || 'Unknown error' }}</span>
              </div>
              <div class="mt-2 text-right">
                <router-link to="/pos/sales" class="text-xs text-gray-500 hover:text-gray-700">View all →</router-link>
              </div>
            </div>
          </div>
          
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth/authStore'
import { dashboardAPI, type DashboardStats } from '@/apis/pos/dashboard/dashboardAPI'

const authStore = useAuthStore()
const loading = ref(true)
const stats = ref<DashboardStats | null>(null)

const fetchStats = async () => {
  loading.value = true
  try {
    stats.value = await dashboardAPI.getStats()
  } catch (err) {
    console.error('Failed to fetch dashboard stats', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchStats()
})

// UI formatting
const formatMoney = (val: number | string) => {
  const num = typeof val === 'string' ? parseFloat(val) : val
  return num.toLocaleString('en-PK', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const timeAgo = computed(() => {
  return "just now" // To make it perfect we could use date-fns here, but keeping it simple for the demo
})

// User text
const companyName = computed(() => authStore.user?.company_name || 'My Company')
const companyNtn = computed(() => authStore.user?.company_ntn || 'N/A')
const userFullName = computed(() => {
  if (authStore.user?.first_name || authStore.user?.last_name) {
    return `${authStore.user.first_name} ${authStore.user.last_name}`.trim().toUpperCase()
  }
  return authStore.user?.username?.toUpperCase() || 'USER'
})

// Chart Logic
const sortedChartData = computed(() => {
  if (!stats.value?.chart_data) return []
  // Sort ascending by date for chart
  return [...stats.value.chart_data].sort((a, b) => a.date.localeCompare(b.date))
})

const maxChartValue = computed(() => {
  if (!sortedChartData.value.length) return 100
  const max = Math.max(...sortedChartData.value.map(d => d.total))
  return max > 0 ? max : 100 // Prevent division by zero
})

const getBarHeight = (val: number) => {
  // Return percentage relative to max height (cap at 100%)
  return Math.min(100, Math.max(0, (val / maxChartValue.value) * 100))
}

const yAxisTicks = computed(() => {
  const max = maxChartValue.value
  // Create 4 ticks (25%, 50%, 75%, 100%)
  return [
    Math.round(max).toLocaleString(),
    Math.round(max * 0.75).toLocaleString(),
    Math.round(max * 0.5).toLocaleString(),
    Math.round(max * 0.25).toLocaleString(),
  ]
})

const totalChartSales = computed(() => {
  return sortedChartData.value.reduce((sum, d) => sum + d.total, 0)
})

const totalChartInvoices = computed(() => {
  // Note: API returns totals, not invoice count per day, so this is just an approximation for UI matching
  return stats.value?.invoices.this_month_count || 0 
})

</script>

