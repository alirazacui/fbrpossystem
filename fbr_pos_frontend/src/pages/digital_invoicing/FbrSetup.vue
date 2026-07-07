<template>
  <div class="space-y-6 w-full mx-auto pb-10">
    <div class="mb-4">
      <h1 class="text-2xl font-bold text-gray-900 mb-1">FBR / PRAL setup</h1>
      <p class="text-sm text-gray-500">Connect your tenant to FBR's Digital Invoicing. Tokens are stored encrypted (Fernet) and never displayed back.</p>
    </div>

    <div class="space-y-4">
      <!-- Steps Card -->
      <div class="bg-white border border-gray-200 rounded-md p-6 shadow-sm">
        <h2 class="text-base font-bold text-gray-900 mb-4">Steps</h2>
        <ul class="space-y-4 text-sm text-gray-600">
          <li class="flex items-start">
            <svg class="w-5 h-5 text-green-500 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <span class="font-bold text-gray-900">1. Confirm IRIS account</span><br />
              Sign in to FBR's IRIS portal at least once with your NTN.
            </div>
          </li>
          <li class="flex items-start">
            <svg class="w-5 h-5 text-green-500 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <span class="font-bold text-gray-900">2. Choose integrator</span><br />
              PRAL (free) is the default. Other licensed integrators charge per invoice.
            </div>
          </li>
          <li class="flex items-start">
            <svg class="w-5 h-5 text-green-500 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <span class="font-bold text-gray-900">3. Business nature & sector</span><br />
              Set these on your tenant profile — they drive which scenarios apply.
            </div>
          </li>
          <li class="flex items-start">
            <svg class="w-5 h-5 text-green-500 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <span class="font-bold text-gray-900">4. Technical contact</span><br />
              Submit your tech contact to PRAL via the IRIS portal.
            </div>
          </li>
          <li class="flex items-start">
            <svg class="w-5 h-5 text-green-500 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <span class="font-bold text-gray-900">5. IP whitelisting</span><br />
              PRAL whitelists our static IPs. Tracked under FBR &rarr; IP whitelist.
            </div>
          </li>
          <li class="flex items-start">
            <svg class="w-5 h-5 text-green-500 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <span class="font-bold text-gray-900">6. Sandbox token</span><br />
              Paste the sandbox token + endpoint below, click Test, then Save.
            </div>
          </li>
        </ul>
      </div>

      <!-- Scenarios Box -->
      <div class="bg-white border border-gray-200 rounded-md p-6 shadow-sm">
        <h3 class="font-bold text-gray-900 mb-2">FBR sandbox scenarios for your tenant</h3>
        <p class="text-sm text-gray-600 mb-4">
          FBR assigns each Digital Invoicing tenant a specific list of scenarios that must pass in sandbox before production can be activated. The list shown here is what your IRIS profile says; the platform team configures it from that page when your tenant is set up. <span class="font-bold">{{ passedScenarios }} of {{ scenarios.length }}</span> runnable scenarios passed so far.
        </p>
        <div v-if="loading" class="text-sm text-gray-500 animate-pulse">Loading scenarios...</div>
        <div v-else-if="scenarios.length === 0" class="text-sm text-gray-500 italic">No scenarios assigned yet.</div>
        <ul v-else class="space-y-2 mb-4">
          <li v-for="scen in scenarios" :key="scen.code" class="flex items-center text-sm">
            <svg v-if="scen.passed" class="w-4 h-4 text-green-500 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <svg v-else class="w-4 h-4 text-gray-300 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span class="font-mono text-gray-900 mr-2">{{ scen.code }}</span> 
            <span class="text-gray-400 mr-2">·</span>
            <span class="font-bold text-gray-900">{{ scen.description }}</span>
          </li>
        </ul>
        <p class="text-xs text-gray-500">
          Once your sandbox token is saved, run the runnable scenarios from the scenario tests page. When every runnable row turns green, the production token field below unlocks. Rows marked "platform: not yet supported" don't block activation — they're work the platform team owes us.
        </p>
      </div>

      <!-- Sandbox Token Form -->
      <div class="bg-white border border-gray-200 rounded-md shadow-sm p-6">
        <h3 class="font-bold text-gray-900 mb-1">Sandbox token</h3>
        <p class="text-sm text-gray-600 mb-6">
          Paste the bearer token PRAL issued for the sandbox environment. The same token authenticates every endpoint (post / validate / edit / cancel) — PRAL's model is one bearer per (taxpayer &times; environment).
          <span v-if="hasProductionToken" class="text-orange-600 font-medium">Production is active — this sandbox token has been deactivated and is no longer used for submissions. Live invoices go to production only.</span>
        </p>
        
        <div class="space-y-6">
          <div>
            <label class="block text-sm font-bold text-gray-700 mb-1">API endpoint</label>
            <input 
              v-model="sandboxEndpoint"
              type="url" 
              class="block w-full rounded-md border-gray-300 shadow-sm focus:border-teal-500 focus:ring-teal-500 sm:text-sm"
              placeholder="https://gw.fbr.gov.pk"
            />
            <p class="mt-1 text-xs text-gray-500">Default <code>https://gw.fbr.gov.pk</code>. Paste only the gateway host (no <code>/di_data/...</code>path). The client appends the correct path for each endpoint (post / validate / etc.) at call time. If you accidentally paste the full submission URL we strip the path automatically before saving.</p>
          </div>
          
          <div>
            <label class="block text-sm font-bold text-gray-700 mb-1">Bearer token</label>
            <input 
              v-model="sandboxToken"
              type="text"
              class="block w-full rounded-md border-gray-300 shadow-sm focus:border-teal-500 focus:ring-teal-500 sm:text-sm font-mono"
              placeholder="Current: 7388...798f — paste a new token to rotate"
            />
            <p class="mt-1 text-xs text-gray-500">
              Token on file: {{ hasToken ? '7388...798f' : 'None' }}. The full bearer is encrypted at rest and never shown again — leave this field blank to keep it and only update the endpoint, or paste a new token to rotate.
            </p>
          </div>
          
          <div class="flex items-center space-x-3 pt-2">
            <button class="bg-white border border-gray-300 text-gray-700 px-4 py-2 rounded-md text-sm font-bold hover:bg-gray-50 shadow-sm">
              Test connection
            </button>
            <button 
              @click="saveSandbox"
              :disabled="saving"
              class="bg-green-600 text-white px-4 py-2 rounded-md text-sm font-bold hover:bg-green-700 shadow-sm disabled:opacity-50"
            >
              {{ saving ? 'Saving...' : 'Save (keep existing token)' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Production Token Box -->
      <div class="bg-white border border-gray-200 rounded-md shadow-sm p-6">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="font-bold text-gray-900 mb-1">Production token</h3>
            <p class="text-sm text-gray-600">
              Activate production once every eligible scenario passes in sandbox. 
              <router-link to="/invoicing/scenarios" class="text-green-600 hover:underline">Run scenarios &rarr;</router-link>
            </p>
          </div>
          <div>
            <span v-if="hasProductionToken" class="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold bg-green-100 text-green-800 border border-green-200">
              ENVIRONMENT: PRODUCTION
            </span>
            <span v-else class="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold bg-yellow-100 text-yellow-800 border border-yellow-200">
              ENVIRONMENT: SANDBOX
            </span>
          </div>
        </div>
        
        <div class="mt-6 border-t border-gray-100 pt-6">
          <div v-if="!allScenariosPassed && !hasProductionToken" class="bg-yellow-50 border border-yellow-200 rounded-md p-4 mb-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-yellow-800">Complete sandbox first</h3>
                <p class="text-sm text-yellow-700 mt-1">You must pass all {{ scenarios.length }} assigned scenarios in the sandbox before FBR will issue a production token. Currently passed: {{ passedScenarios }}.</p>
              </div>
            </div>
          </div>
          
          <div class="space-y-6">
            <!-- If token is saved and not editing -->
            <div v-if="hasProductionToken && !isEditingProductionToken" class="bg-gray-50 p-4 rounded-md border border-gray-200 flex justify-between items-center">
              <div>
                <p class="text-sm font-bold text-gray-900">Your production token is securely saved.</p>
                <p class="text-xs text-gray-500 mt-1">You are currently LIVE and submitting real invoices to FBR.</p>
              </div>
              <button 
                @click="isEditingProductionToken = true" 
                class="px-4 py-2 bg-white border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
              >
                Edit Token
              </button>
            </div>
            
            <!-- Token Form (shows if no token OR editing) -->
            <div v-if="!hasProductionToken || isEditingProductionToken">
              <label class="block text-sm font-bold text-gray-700 mb-1">Production Bearer Token</label>
              <input 
                v-model="productionToken"
                type="text"
                :disabled="!allScenariosPassed && !hasProductionToken"
                class="block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm font-mono disabled:bg-gray-100 disabled:text-gray-500"
                placeholder="Paste your live production token here..."
              />
              <p class="mt-1 text-xs text-gray-500">
                <span v-if="!allScenariosPassed && !hasProductionToken">This field is locked until sandbox testing is complete.</span>
                <span v-else>Paste the new bearer token to rotate it.</span>
              </p>
              
              <div class="flex items-center mt-4 space-x-3">
                <button 
                  @click="saveProduction"
                  :disabled="savingProduction || (!allScenariosPassed && !hasProductionToken) || !productionToken.trim()"
                  class="bg-green-600 text-white px-6 py-2 rounded-md text-sm font-bold hover:bg-green-700 shadow-sm disabled:opacity-50 transition-colors"
                >
                  {{ savingProduction ? 'Saving...' : 'Save & Go Live' }}
                </button>
                <button 
                  v-if="hasProductionToken && isEditingProductionToken"
                  @click="isEditingProductionToken = false; productionToken = ''" 
                  class="px-4 py-2 bg-white border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
                >
                  Cancel
                </button>
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
import companyAPI from '@/apis/admin/companyAPI'
import fbrAPI from '@/apis/digital_invoicing/fbrAPI'

const authStore = useAuthStore()
const loading = ref(true)
const saving = ref(false)

const scenarios = ref<{code: string, description: string, passed: boolean}[]>([])
const passedScenarios = ref(0)
const sandboxEndpoint = ref('')
const sandboxToken = ref('')
const hasToken = ref(false)

const productionToken = ref('')
const hasProductionToken = ref(false)
const savingProduction = ref(false)
const isEditingProductionToken = ref(false)

const allScenariosPassed = computed(() => {
  return scenarios.value.length > 0 && passedScenarios.value === scenarios.value.length
})

const FBR_SCENARIO_MAP: Record<string, string> = {
  'SN018': 'Services (FED in ST Mode)',
  'SN019': 'Services (ICT Ordinance)',
  'SN001': 'Standard Rate — Registered Buyer',
  'SN005': 'Reduced Rate — Registered Buyer',
}

const loadData = async () => {
  if (!authStore.user?.company_id) return
  try {
    const compId = authStore.user.company_id
    const res = await companyAPI.getCompanyDetail(compId)
    sandboxEndpoint.value = res.fbr_sandbox_endpoint || 'https://gw.fbr.gov.pk'
    hasToken.value = !!res.fbr_sandbox_token
    hasProductionToken.value = !!res.fbr_production_token
    
    // Fetch logs to see which passed
    const logs = await fbrAPI.getScenarioLogs(compId)
    const passedSet = new Set(logs.filter(l => l.status === 'success').map(l => l.scenario_code))

    const activeScenarios = []
    let passedCount = 0
    for (let i = 1; i <= 28; i++) {
      const fieldCode = `fbr_scenario_sn${String(i).padStart(3, '0')}`
      if (res[fieldCode]) {
        const code = `SN${String(i).padStart(3, '0')}`
        const passed = passedSet.has(code)
        if (passed) passedCount++
        activeScenarios.push({
          code,
          description: FBR_SCENARIO_MAP[code] || 'Assigned FBR Scenario',
          passed
        })
      }
    }
    scenarios.value = activeScenarios
    passedScenarios.value = passedCount
  } catch (error) {
    console.error('Failed to load company setup', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
})

const saveSandbox = async () => {
  if (!authStore.user?.company_id) return
  saving.value = true
  try {
    const payload: any = {}
    if (sandboxEndpoint.value) {
      // Strip path logic
      let url = sandboxEndpoint.value
      try {
        const urlObj = new URL(url)
        url = urlObj.origin
      } catch (e) {
        // Invalid URL ignore stripping
      }
      payload.fbr_sandbox_endpoint = url
    }
    if (sandboxToken.value.trim()) {
      payload.fbr_sandbox_token = sandboxToken.value.trim()
    }

    await companyAPI.patchCompany(authStore.user.company_id, payload)
    sandboxToken.value = '' // Clear on save since it's sensitive
    alert('Sandbox settings saved successfully!')
    await loadData() // Refresh to update "hasToken" status
  } catch (error) {
    console.error('Failed to save sandbox settings', error)
    alert('Failed to save sandbox settings')
  } finally {
    saving.value = false
  }
}

const saveProduction = async () => {
  if (!authStore.user?.company_id) return
  if (!productionToken.value.trim()) return
  
  savingProduction.value = true
  try {
    await companyAPI.patchCompany(authStore.user.company_id, {
      fbr_production_token: productionToken.value.trim(),
      fbr_sandbox_complete: true // Since they can only save if all passed
    })
    productionToken.value = ''
    isEditingProductionToken.value = false
    alert('Production token saved successfully! You are now LIVE.')
    await loadData()
  } catch (error) {
    console.error('Failed to save production token', error)
    alert('Failed to save production token')
  } finally {
    savingProduction.value = false
  }
}
</script>
