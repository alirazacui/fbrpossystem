<template>
  <div class="flex flex-col pb-12 h-full bg-gray-50/50 min-h-screen">
    
    <div v-if="loading" class="flex justify-center items-center py-20">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-teal-600"></div>
    </div>
    
    <div v-else-if="error" class="px-8 py-8 w-full">
      <div class="bg-red-50 border border-red-200 rounded-lg p-6">
        <h2 class="text-lg font-bold text-red-800">Failed to load dashboard</h2>
        <p class="text-sm text-red-600 mt-2">{{ error }}</p>
        <button @click="fetchStats" class="mt-4 px-4 py-2 bg-red-600 text-white text-sm rounded hover:bg-red-700">Retry</button>
      </div>
    </div>

    <div v-else-if="stats" class="px-8 py-8 w-full space-y-6">
      <div class="flex items-center justify-between mb-2">
        <h1 class="text-2xl font-bold text-gray-900">Platform Overview</h1>
        <p class="text-xs text-gray-400 font-medium">Last refreshed: just now</p>
      </div>

      <!-- Stat Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <!-- Total Tenants -->
        <router-link to="/admin/tenants" class="bg-white border border-gray-200 rounded-xl p-5 shadow-sm hover:shadow-md hover:border-teal-300 transition-all cursor-pointer group">
          <div class="flex justify-between items-start mb-4">
            <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider group-hover:text-teal-700 transition-colors">Tenants</h3>
            <div class="p-1.5 bg-teal-50 rounded text-teal-600 group-hover:bg-teal-100 transition-colors">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>
            </div>
          </div>
          <div class="text-2xl font-bold text-gray-900 mb-1 group-hover:text-teal-700 transition-colors">{{ stats.metrics.total_tenants }}</div>
          <p class="text-xs text-gray-500"><span class="text-teal-600 font-semibold">{{ stats.metrics.active_tenants }}</span> active</p>
        </router-link>
        
        <!-- Total Users -->
        <router-link to="/admin/users" class="bg-white border border-gray-200 rounded-xl p-5 shadow-sm hover:shadow-md hover:border-blue-300 transition-all cursor-pointer group">
          <div class="flex justify-between items-start mb-4">
            <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider group-hover:text-blue-700 transition-colors">Users</h3>
            <div class="p-1.5 bg-blue-50 rounded text-blue-600 group-hover:bg-blue-100 transition-colors">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
            </div>
          </div>
          <div class="text-2xl font-bold text-gray-900 mb-1 group-hover:text-blue-700 transition-colors">{{ stats.metrics.total_users }}</div>
          <p class="text-xs text-gray-500">Across all tenants</p>
        </router-link>

        <router-link to="/admin/cashiers?role=manager" class="bg-white border border-gray-200 rounded-xl p-5 shadow-sm hover:shadow-md hover:border-orange-300 transition-all cursor-pointer group">
          <div class="flex justify-between items-start mb-4">
            <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider group-hover:text-orange-700 transition-colors">Managers</h3>
            <div class="p-1.5 bg-orange-50 rounded text-orange-600 group-hover:bg-orange-100 transition-colors">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 8.048M12 4.354L8.646 7.708M12 4.354l3.354 3.354M9 12a4 4 0 11-8 0 4 4 0 018 0zm12 0a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
            </div>
          </div>
          <div class="text-2xl font-bold text-gray-900 mb-1 group-hover:text-orange-700 transition-colors">{{ stats.metrics.total_managers }}</div>
          <p class="text-xs text-gray-500">Click to view all managers</p>
        </router-link>

        <router-link to="/admin/cashiers?role=cashier" class="bg-white border border-gray-200 rounded-xl p-5 shadow-sm hover:shadow-md hover:border-yellow-300 transition-all cursor-pointer group">
          <div class="flex justify-between items-start mb-4">
            <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider group-hover:text-yellow-700 transition-colors">Cashiers</h3>
            <div class="p-1.5 bg-yellow-50 rounded text-yellow-600 group-hover:bg-yellow-100 transition-colors">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            </div>
          </div>
          <div class="text-2xl font-bold text-gray-900 mb-1 group-hover:text-yellow-700 transition-colors">{{ stats.metrics.total_cashiers }}</div>
          <p class="text-xs text-gray-500">Click to view all cashiers</p>
        </router-link>

        <router-link to="/admin/cashiers?role=salesperson" class="bg-white border border-gray-200 rounded-xl p-5 shadow-sm hover:shadow-md hover:border-indigo-300 transition-all cursor-pointer group">
          <div class="flex justify-between items-start mb-4">
            <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider group-hover:text-indigo-700 transition-colors">Salespersons</h3>
            <div class="p-1.5 bg-indigo-50 rounded text-indigo-600 group-hover:bg-indigo-100 transition-colors">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            </div>
          </div>
          <div class="text-2xl font-bold text-gray-900 mb-1 group-hover:text-indigo-700 transition-colors">{{ stats.metrics.total_salespersons }}</div>
          <p class="text-xs text-gray-500">Click to view all salespersons</p>
        </router-link>

        <!-- FBR Submissions -->
        <RouterLink to="/admin/fbr-submissions" class="bg-white border border-gray-200 rounded-xl p-5 shadow-sm hover:shadow-md hover:border-green-300 transition-all cursor-pointer group">
          <div class="flex justify-between items-start mb-4">
            <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider group-hover:text-green-700 transition-colors">FBR Submissions</h3>
            <div class="p-1.5 bg-green-50 rounded text-green-600 group-hover:bg-green-100 transition-colors">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            </div>
          </div>
          <div class="text-2xl font-bold text-gray-900 mb-1 group-hover:text-green-700 transition-colors">{{ stats.metrics.total_fbr_submissions }}</div>
          <p class="text-xs text-gray-500">All PRAL submissions</p>
        </RouterLink>

        <!-- Active Subscriptions -->
        <router-link to="/admin/tenants" class="bg-white border border-gray-200 rounded-xl p-5 shadow-sm hover:shadow-md hover:border-purple-300 transition-all cursor-pointer group">
          <div class="flex justify-between items-start mb-4">
            <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider group-hover:text-purple-700 transition-colors">Active Subs</h3>
            <div class="p-1.5 bg-purple-50 rounded text-purple-600 group-hover:bg-purple-100 transition-colors">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"></path></svg>
            </div>
          </div>
          <div class="text-2xl font-bold text-gray-900 mb-1 group-hover:text-purple-700 transition-colors">{{ stats.metrics.active_subscriptions }}</div>
          <p class="text-xs text-gray-500">Currently billed</p>
        </router-link>
      </div>

      <!-- Chart -->
      <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
        <h2 class="text-sm font-bold text-gray-900 mb-1">FBR Submissions (Last 30 Days)</h2>
        <p class="text-xs text-gray-500 mb-4">Daily count of all PRAL submission attempts across all tenants.</p>
        <div v-if="stats.chart_data.labels.length === 0" class="text-sm text-gray-400 italic py-10 text-center">No FBR submissions in the last 30 days.</div>
        <div v-else class="relative rounded-2xl border border-gray-100 bg-gradient-to-b from-white to-gray-50/80 p-4">
          <div class="h-72 w-full">
            <canvas ref="submissionChartCanvas"></canvas>
          </div>
        </div>
        <div v-if="stats.chart_data.labels.length > 0" class="mt-2 flex items-center justify-between text-[10px] text-gray-400">
          <span>Oldest</span>
          <span>Newest</span>
        </div>
      </div>

    <!-- Bottom Lists -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      
      <!-- FBR Failures -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden col-span-1 lg:col-span-2">
        <div class="px-5 py-4 border-b border-gray-100 flex justify-between items-center bg-gray-50">
          <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wide">Recent FBR Failures</h2>
          <span class="text-xs font-semibold px-2 py-1 bg-red-100 text-red-700 rounded-full">Needs Attention</span>
        </div>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-100">
            <thead class="bg-white">
              <tr>
                <th class="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Sale ID</th>
                <th class="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Endpoint</th>
                <th class="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Status</th>
                <th class="px-5 py-3 text-right text-xs font-semibold text-gray-500 uppercase tracking-wider">Time</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-100">
              <tr v-if="stats.failed_fbr.length === 0">
                <td colspan="4" class="px-5 py-4 text-sm text-gray-500 text-center italic">No recent failures. All clear! ✓</td>
              </tr>
              <tr v-for="log in stats.failed_fbr" :key="log.sale_id + log.attempted_at" class="hover:bg-gray-50">
                <td class="px-5 py-3 whitespace-nowrap text-sm font-medium text-gray-900">#{{ log.sale_id }}</td>
                <td class="px-5 py-3 whitespace-nowrap text-sm font-mono text-gray-600">{{ log.endpoint }}</td>
                <td class="px-5 py-3 whitespace-nowrap text-sm text-red-600 font-medium">{{ log.status_code }}</td>
                <td class="px-5 py-3 whitespace-nowrap text-sm text-gray-500 text-right">{{ log.attempted_at }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Right Column -->
      <div class="space-y-6">
        <!-- Expiring Subs -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div class="px-5 py-4 border-b border-gray-100 bg-gray-50">
            <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wide">Expiring Subscriptions</h2>
          </div>
          <div class="p-5 space-y-4">
            <div v-if="stats.expiring_subscriptions.length === 0" class="text-sm text-gray-500 italic">No subscriptions expiring soon.</div>
            <div v-for="sub in stats.expiring_subscriptions" :key="sub.company_name" class="flex justify-between items-center">
              <div>
                <p class="text-sm font-medium text-gray-900">{{ sub.company_name }}</p>
                <p class="text-xs text-gray-500">{{ sub.plan }}</p>
              </div>
              <span class="text-xs font-semibold text-orange-600 bg-orange-50 px-2 py-1 rounded">{{ sub.expires_on }}</span>
            </div>
          </div>
        </div>

        <!-- Recent Activity -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div class="px-5 py-4 border-b border-gray-100 bg-gray-50">
            <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wide">Recent Activity</h2>
          </div>
          <div class="p-5 space-y-4">
            <div v-if="stats.recent_activity.length === 0" class="text-sm text-gray-500 italic">No recent activity.</div>
            <div v-for="act in stats.recent_activity" :key="act.date" class="border-l-2 border-teal-500 pl-3">
              <p class="text-sm text-gray-800">{{ act.message }}</p>
              <p class="text-xs text-gray-400 mt-1">{{ act.date }}</p>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, nextTick, watch } from 'vue'
import { Chart, registerables } from 'chart.js'
import adminDashboardAPI, { type DashboardStats } from '@/apis/admin/dashboardAPI'

Chart.register(...registerables)

const loading = ref(true)
const error = ref('')
const stats = ref<DashboardStats | null>(null)
const submissionChartCanvas = ref<HTMLCanvasElement | null>(null)
let submissionChart: Chart | null = null

const destroyChart = () => {
  if (submissionChart) {
    submissionChart.destroy()
    submissionChart = null
  }
}

const renderSubmissionChart = async () => {
  await nextTick()

  const canvas = submissionChartCanvas.value
  if (!canvas || !stats.value) return

  destroyChart()

  const context = canvas.getContext('2d')
  if (!context) return

  const gradient = context.createLinearGradient(0, 0, 0, 280)
  gradient.addColorStop(0, 'rgba(20, 184, 166, 0.32)')
  gradient.addColorStop(1, 'rgba(20, 184, 166, 0.02)')

  submissionChart = new Chart(context, {
    type: 'line',
    data: {
      labels: stats.value.chart_data.labels,
      datasets: [
        {
          label: 'Submissions',
          data: stats.value.chart_data.values,
          borderColor: '#0f766e',
          backgroundColor: gradient,
          fill: true,
          tension: 0.35,
          pointRadius: 3,
          pointHoverRadius: 5,
          pointBackgroundColor: '#14b8a6',
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          borderWidth: 3,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      layout: {
        padding: {
          top: 12,
          right: 8,
          bottom: 0,
          left: 4,
        },
      },
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          backgroundColor: '#111827',
          titleColor: '#ffffff',
          bodyColor: '#ffffff',
          padding: 10,
          displayColors: false,
          callbacks: {
            label: (context) => `${context.parsed.y} submissions`,
          },
        },
      },
      scales: {
        x: {
          grid: {
            display: false,
          },
          ticks: {
            color: '#6b7280',
            maxRotation: 0,
            autoSkip: true,
            maxTicksLimit: 10,
          },
        },
        y: {
          beginAtZero: true,
          grid: {
            color: 'rgba(229, 231, 235, 0.9)',
          },
          ticks: {
            precision: 0,
            color: '#6b7280',
          },
        },
      },
    },
  })
}

const fetchStats = async () => {
  loading.value = true
  error.value = ''
  try {
    const data = await adminDashboardAPI.getStats()
    stats.value = data
  } catch (err: any) {
    console.error("Failed to load dashboard stats", err)
    error.value = err.response?.data?.detail || err.message || 'Unknown error'
  } finally {
    loading.value = false
  }

  if (!error.value && stats.value) {
    await renderSubmissionChart()
  }
}

onMounted(() => {
  fetchStats()
})

onBeforeUnmount(() => {
  destroyChart()
})
</script>
