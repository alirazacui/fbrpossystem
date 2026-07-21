<template>
  <div class="space-y-6 w-full mx-auto pb-10 max-w-7xl">
    <div class="mb-4 flex items-start justify-between">
      <div class="max-w-4xl">
        <h1 class="text-2xl font-bold text-gray-900 mb-2">Sandbox scenarios</h1>
        <p class="text-sm text-gray-500">
          Each scenario submits a synthetic invoice to PRAL's sandbox (the exact saleType, rate, and SRO schedule each scenarioId requires) and reports PRAL's response. Run them one at a time to iterate on a failing scenario, or "Run all" to verify the whole list. All eligible scenarios must pass before the production token activates.
        </p>
      </div>
      <button 
        @click="runAll" 
        :disabled="isRunningAll"
        class="bg-green-600 text-white px-4 py-2.5 rounded-md font-bold text-sm hover:bg-green-700 shadow-sm flex items-center whitespace-nowrap ml-4 disabled:opacity-50"
      >
        <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        {{ isRunningAll ? 'Running...' : 'Run all eligible' }}
      </button>
    </div>

    <!-- Legend -->
    <div class="bg-white border border-gray-200 rounded-md p-4 flex items-center space-x-6 text-sm shadow-sm">
      <span class="font-bold text-gray-900">Legend:</span>
      <div class="flex items-center text-gray-600">
        <span class="bg-gray-100 text-gray-800 font-medium px-2 py-0.5 rounded-full text-xs mr-2 border border-gray-200">Pending</span> Not yet run
      </div>
      <div class="flex items-center text-gray-600">
        <span class="bg-green-600 text-white font-medium px-2 py-0.5 rounded-full text-xs mr-2">Success</span> PRAL accepted
      </div>
      <div class="flex items-center text-gray-600">
        <span class="bg-red-50 text-red-700 font-medium px-2 py-0.5 rounded-full text-xs mr-2 border border-red-200">Failed</span> PRAL rejected
      </div>
      <div class="flex items-center text-gray-600">
        <span class="bg-yellow-50 text-yellow-700 font-medium px-2 py-0.5 rounded-full text-xs mr-2 border border-yellow-200">Not yet supported</span> Platform doesn't ship a builder for this code yet
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-10 text-gray-500 animate-pulse">
      Loading scenarios...
    </div>

    <!-- Empty State -->
    <div v-else-if="scenariosList.length === 0" class="bg-gray-50 border border-gray-200 rounded-md p-8 text-center shadow-sm">
      <svg class="w-12 h-12 text-gray-400 mx-auto mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
      </svg>
      <h3 class="text-lg font-bold text-gray-900 mb-1">No scenarios assigned</h3>
      <p class="text-sm text-gray-500">
        FBR has not assigned any sandbox scenarios to your tenant yet. If you believe this is an error, please check the Setup Wizard or contact the platform team to enable scenarios for your account.
      </p>
    </div>

    <!-- Scenarios Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div 
        v-for="scen in scenariosList" 
        :key="scen.code" 
        class="bg-white border border-gray-200 rounded-md shadow-sm overflow-hidden flex flex-col"
      >
        <!-- Card Header & Body -->
        <div class="p-5 flex-grow">
          <div class="flex items-center justify-between mb-4">
            <h3 class="font-bold text-gray-900">{{ scen.code }}</h3>
            <span 
              class="px-2.5 py-0.5 rounded-full text-xs font-bold"
              :class="{
                'bg-green-600 text-white': scen.status === 'success',
                'bg-red-50 text-red-700 border border-red-200': scen.status === 'failed',
                'bg-gray-100 text-gray-800 border border-gray-200': scen.status === 'pending'
              }"
            >
              {{ scen.status === 'success' ? 'Success' : scen.status === 'failed' ? 'Failed' : 'Pending' }}
            </span>
          </div>
          
          <div class="space-y-1 mb-4">
            <p class="text-sm text-gray-700">{{ scen.description }}</p>
            <p class="text-xs text-gray-500 font-mono" v-if="scen.log?.fbr_invoice_number">FBR # {{ scen.log.fbr_invoice_number }}</p>
            <p class="text-xs text-gray-400">Last attempt: {{ scen.log?.created_at ? new Date(scen.log.created_at).toLocaleString() : 'Never' }}</p>
            <p v-if="scen.log?.error_message" class="text-xs text-red-600 mt-2 line-clamp-2" :title="scen.log.error_message">{{ scen.log.error_message }}</p>
          </div>

          <button 
            @click="toggleExpand(scen.code)"
            class="text-sm text-green-700 font-medium hover:underline flex items-center focus:outline-none"
          >
            <svg class="w-4 h-4 mr-1 transition-transform" :class="{'rotate-90': expandedId === scen.code}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
            Show / edit request & response
          </button>
        </div>

        <!-- Expanded JSON View -->
        <div v-if="expandedId === scen.code" class="border-t border-gray-200 bg-gray-50 p-4">
          <div class="space-y-4">
            <!-- Request -->
            <div>
              <div class="flex justify-between items-center mb-2">
                <h4 class="font-bold text-gray-700 text-xs uppercase tracking-wider">Request Payload</h4>
                <div class="flex space-x-2">
                  <button 
                    @click="resetToTemplate(scen.code)"
                    class="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded hover:bg-gray-200 font-medium border border-gray-300"
                  >
                    Reset
                  </button>
                  <button 
                    @click="sendEdited(scen)"
                    class="text-xs bg-green-100 text-green-800 px-2 py-1 rounded hover:bg-green-200 font-bold border border-green-200"
                  >
                    Send edited request
                  </button>
                </div>
              </div>
              <textarea 
                v-model="editPayloads[scen.code]"
                class="w-full h-48 font-mono text-xs bg-white text-gray-800 p-2 rounded border border-gray-300 focus:ring-green-500 focus:border-green-500 shadow-inner"
              ></textarea>
            </div>
            
            <!-- Response -->
            <div>
              <h4 class="font-bold text-gray-700 text-xs uppercase tracking-wider mb-2">FBR Response</h4>
              <div class="w-full h-32 overflow-y-auto font-mono text-xs bg-gray-100 text-gray-700 p-2 rounded border border-gray-300 whitespace-pre shadow-inner">
{{ scen.log?.response_payload ? JSON.stringify(scen.log.response_payload, null, 2) : 'No response data yet.' }}
              </div>
            </div>
          </div>
        </div>

        <!-- Card Footer (Buttons) -->
        <div class="p-4 border-t border-gray-100 bg-gray-50 flex items-center space-x-2">
          <button 
            @click="runSingle(scen.code)"
            class="flex-grow bg-white border border-gray-300 text-gray-700 py-1.5 rounded text-sm font-bold hover:bg-gray-100 flex items-center justify-center focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-green-500 shadow-sm"
          >
            <svg class="w-4 h-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {{ scen.status === 'pending' ? 'Run' : 'Re-run' }}
          </button>
          <button class="bg-white border border-gray-300 text-gray-700 p-1.5 rounded hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-green-500 shadow-sm" title="Export Log">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Success Alert (only if all passed) -->
    <div v-if="allPassed && !loading" class="bg-green-50 border border-green-200 text-green-800 rounded-md p-4 flex items-center shadow-sm">
      <svg class="w-5 h-5 mr-3 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <span class="text-sm font-medium">All scenarios passed. You can activate production from FBR &rarr; Setup.</span>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth/authStore'
import fbrAPI from '@/apis/digital_invoicing/fbrAPI'
import companyAPI from '@/apis/admin/companyAPI'

const authStore = useAuthStore()
const loading = ref(false)
const isRunningAll = ref(false)

const scenariosList = ref<any[]>([])
const expandedId = ref<string | null>(null)
const editPayloads = ref<Record<string, string>>({})
const templates = ref<Record<string, any>>({})

const allPassed = computed(() => {
  return scenariosList.value.length > 0 && scenariosList.value.every(s => s.status === 'success')
})

const FBR_SCENARIO_MAP: Record<string, string> = {
  'SN018': 'Services (FED in ST Mode)',
  'SN019': 'Services (ICT Ordinance)',
  'SN001': 'Standard Rate — Registered Buyer',
  'SN005': 'Reduced Rate — Registered Buyer',
}

const loadData = async () => {
  if (!authStore.user?.company_id) return
  loading.value = true
  try {
    const compId = authStore.user.company_id
    const comp = await companyAPI.getCompanyDetail(compId)
    const logs = await fbrAPI.getScenarioLogs(compId)
    
    // Fetch scenario templates
    try {
      templates.value = await fbrAPI.getScenarioTemplates(compId)
    } catch (e) {
      console.error('Failed to load scenario templates:', e)
    }
    
    const logsByCode = new Map()
    logs.forEach((l: any) => logsByCode.set(l.scenario_code, l))

    const activeScenarios = []
    for (let i = 1; i <= 28; i++) {
      const fieldCode = `fbr_scenario_sn${String(i).padStart(3, '0')}`
      if (comp[fieldCode]) {
        const code = `SN${String(i).padStart(3, '0')}`
        const log = logsByCode.get(code)
        
        activeScenarios.push({
          code,
          description: FBR_SCENARIO_MAP[code] || 'Assigned FBR Scenario',
          status: log ? log.status.toLowerCase() : 'pending',
          log: log || null
        })
      }
    }
    
    scenariosList.value = activeScenarios
  } catch (error) {
    console.error('Failed to load scenario data:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
})

const toggleExpand = (code: string) => {
  if (expandedId.value === code) {
    expandedId.value = null
  } else {
    expandedId.value = code
    // Initialize edit buffer if missing
    if (!editPayloads.value[code]) {
      const scen = scenariosList.value.find(s => s.code === code)
      if (scen?.log?.request_payload) {
        editPayloads.value[code] = JSON.stringify(scen.log.request_payload, null, 2)
      } else if (templates.value[code]) {
        editPayloads.value[code] = JSON.stringify(templates.value[code], null, 2)
      } else {
        editPayloads.value[code] = '{}'
      }
    }
  }
}

const resetToTemplate = (code: string) => {
  if (templates.value[code]) {
    editPayloads.value[code] = JSON.stringify(templates.value[code], null, 2)
  } else {
    editPayloads.value[code] = '{}'
  }
}

const runAll = async () => {
  if (!authStore.user?.company_id) return
  isRunningAll.value = true
  try {
    await fbrAPI.clearAllScenarios(authStore.user.company_id)
    alert('Started running all scenarios in the background. Refreshing in a few moments.')
    setTimeout(() => {
      loadData()
      isRunningAll.value = false
    }, 4000)
  } catch (err: any) {
    alert(err.response?.data?.error || 'Failed to start run all')
    isRunningAll.value = false
  }
}

const runSingle = async (code: string) => {
  if (!authStore.user?.company_id) return
  try {
    await fbrAPI.clearSingleScenario(authStore.user.company_id, code)
    alert(`Started re-running ${code} in the background.`)
    setTimeout(loadData, 2000)
  } catch (err: any) {
    alert(err.response?.data?.error || 'Failed to start run single')
  }
}

const sendEdited = async (scen: any) => {
  if (!authStore.user?.company_id) return
  try {
    const rawStr = editPayloads.value[scen.code]
    const parsedPayload = JSON.parse(rawStr)
    
    await fbrAPI.submitEditedScenario(authStore.user.company_id, scen.code, parsedPayload)
    alert('Edited request sent successfully!')
    await loadData()
  } catch (err: any) {
    alert('Failed to send edited request: ' + (err.response?.data?.error || err.message))
  }
}
</script>
