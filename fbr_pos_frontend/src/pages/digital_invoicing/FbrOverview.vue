<template>
  <div class="space-y-6 max-w-4xl">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">FBR / Compliance</h1>
      <p class="text-gray-500">Manage your connection to FBR PRAL Digital Invoicing</p>
    </div>

    <!-- Environment Status -->
    <div class="bg-white rounded-lg shadow p-6 border border-gray-100 flex items-center justify-between">
      <div>
        <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-1">Environment</h2>
        <div class="flex items-center space-x-2">
          <div class="w-3 h-3 rounded-full bg-green-500"></div>
          <span class="text-xl font-bold text-gray-900 capitalize">{{ environment }}</span>
        </div>
        <p class="text-sm text-gray-500 mt-1">Last success: {{ lastSuccessDate }}</p>
      </div>
      <div class="text-right">
        <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-1">Scenarios</h2>
        <div class="text-xl font-bold text-gray-900">{{ passedScenarios }} / {{ totalScenarios }}</div>
        <router-link to="/invoicing/scenarios" class="text-sm text-teal-600 hover:text-teal-700 font-medium">
          Run sandbox tests &rarr;
        </router-link>
      </div>
      <div class="text-right">
        <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-1">Cancel budget</h2>
        <div class="text-xl font-bold text-gray-900">Rs {{ cancelBudget }}</div>
        <a href="#" class="text-sm text-teal-600 hover:text-teal-700 font-medium">
          View tracker &rarr;
        </a>
      </div>
    </div>

    <!-- Quick Links Grid -->
    <div>
      <h2 class="text-lg font-bold text-gray-900 mb-4">Quick links</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        <!-- Setup wizard -->
        <router-link to="/invoicing/setup" class="bg-white rounded-lg shadow p-4 border border-gray-100 hover:shadow-md transition-shadow group flex items-start space-x-3">
          <div class="bg-teal-50 text-teal-600 p-2 rounded-lg group-hover:bg-teal-100 transition-colors">
            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </div>
          <div>
            <h3 class="font-medium text-gray-900">Setup wizard</h3>
            <p class="text-sm text-gray-500">Configure tokens and endpoints</p>
          </div>
        </router-link>

        <!-- Scenario tests -->
        <router-link to="/invoicing/scenarios" class="bg-white rounded-lg shadow p-4 border border-gray-100 hover:shadow-md transition-shadow group flex items-start space-x-3">
          <div class="bg-indigo-50 text-indigo-600 p-2 rounded-lg group-hover:bg-indigo-100 transition-colors">
            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <h3 class="font-medium text-gray-900">Scenario tests</h3>
            <p class="text-sm text-gray-500">Run required sandbox cases</p>
          </div>
        </router-link>

        <!-- Submission log -->
        <router-link to="/invoicing/logs" class="bg-white rounded-lg shadow p-4 border border-gray-100 hover:shadow-md transition-shadow group flex items-start space-x-3">
          <div class="bg-blue-50 text-blue-600 p-2 rounded-lg group-hover:bg-blue-100 transition-colors">
            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <div>
            <h3 class="font-medium text-gray-900">Submission log</h3>
            <p class="text-sm text-gray-500">View live invoice history</p>
          </div>
        </router-link>

        <!-- Cancel budget -->
        <a href="#" class="bg-white rounded-lg shadow p-4 border border-gray-100 hover:shadow-md transition-shadow group flex items-start space-x-3 opacity-70 cursor-not-allowed">
          <div class="bg-red-50 text-red-600 p-2 rounded-lg group-hover:bg-red-100 transition-colors">
            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <h3 class="font-medium text-gray-900">Cancel budget</h3>
            <p class="text-sm text-gray-500">Manage cancellation limits</p>
          </div>
        </a>

        <!-- Manual amendment -->
        <a href="#" class="bg-white rounded-lg shadow p-4 border border-gray-100 hover:shadow-md transition-shadow group flex items-start space-x-3 opacity-70 cursor-not-allowed">
          <div class="bg-yellow-50 text-yellow-600 p-2 rounded-lg group-hover:bg-yellow-100 transition-colors">
            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </div>
          <div>
            <h3 class="font-medium text-gray-900">Manual amendment</h3>
            <p class="text-sm text-gray-500">Fix FBR rejected invoices</p>
          </div>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth/authStore'
import companyAPI from '@/apis/admin/companyAPI'
import fbrAPI from '@/apis/digital_invoicing/fbrAPI'

const authStore = useAuthStore()

const loading = ref(true)
const environment = ref('sandbox')
const lastSuccessDate = ref('No success yet')
const passedScenarios = ref(0)
const totalScenarios = ref(0)
const cancelBudget = ref('0')

const loadData = async () => {
  if (!authStore.user?.company_id) return
  loading.value = true
  
  try {
    const compId = authStore.user.company_id
    
    // Fetch company info
    const comp = await companyAPI.getCompanyDetail(compId)
    environment.value = comp.fbr_production_token ? 'production' : 'sandbox'
    
    // Count assigned scenarios
    let assigned = 0
    for (let i = 1; i <= 28; i++) {
      const code = `fbr_scenario_sn${String(i).padStart(3, '0')}`
      if (comp[code]) assigned++
    }
    totalScenarios.value = assigned
    
    // Fetch logs to count successes
    const logs = await fbrAPI.getScenarioLogs(compId)
    
    let passed = 0
    let mostRecentSuccess = 0
    
    logs.forEach((log: any) => {
      if (log.status === 'success') {
        passed++
        const dateVal = new Date(log.created_at).getTime()
        if (dateVal > mostRecentSuccess) {
          mostRecentSuccess = dateVal
        }
      }
    })
    
    passedScenarios.value = passed
    
    if (mostRecentSuccess > 0) {
      lastSuccessDate.value = new Date(mostRecentSuccess).toLocaleString()
    }
    
  } catch (err) {
    console.error('Failed to load FBR overview stats', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>
