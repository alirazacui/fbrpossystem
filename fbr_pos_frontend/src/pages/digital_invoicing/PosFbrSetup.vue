<template>
  <div class="space-y-6 w-full mx-auto pb-10">
    <div class="mb-4">
      <h1 class="text-2xl font-bold text-gray-900 mb-1">FBR Retail POS Setup</h1>
      <p class="text-sm text-gray-500">Connect your POS to FBR Retail POS Cloud API. Enter your POS credentials below.</p>
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
              <span class="font-bold text-gray-900">1. Register as POS Client</span><br />
              Register your business as a POS Client on FBR's eFBR portal.
            </div>
          </li>
          <li class="flex items-start">
            <svg class="w-5 h-5 text-green-500 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <span class="font-bold text-gray-900">2. Get POS ID</span><br />
              After registration, FBR will issue a POS ID for your business.
            </div>
          </li>
          <li class="flex items-start">
            <svg class="w-5 h-5 text-green-500 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <span class="font-bold text-gray-900">3. Get Token</span><br />
              FBR issues a single Bearer Token (UUID) for your POS integration. Enter it below.
            </div>
          </li>
          <li class="flex items-start">
            <svg class="w-5 h-5 text-green-500 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <span class="font-bold text-gray-900">4. Test & Save</span><br />
              Use "Test Connection" to verify your credentials, then save.
            </div>
          </li>
        </ul>
      </div>

      <!-- Info Banner -->
      <div class="bg-blue-50 border border-blue-200 rounded-md p-4 flex items-start space-x-3">
        <svg class="w-5 h-5 text-blue-500 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div class="text-sm text-blue-800">
          <p class="font-semibold mb-1">FBR POS V2.1 — One Token for Everything</p>
          <p>FBR issues a single Bearer Token (UUID) for POS integration. This same token is used for both sandbox testing and production. The "Code" (e.g. 3364862B) is a registration reference only — enter the UUID token here.</p>
        </div>
      </div>

      <!-- POS Credentials Form -->
      <div class="bg-white border border-gray-200 rounded-md shadow-sm p-6">
        <h3 class="font-bold text-gray-900 mb-1">POS Credentials</h3>
        <p class="text-sm text-gray-600 mb-6">
          Enter your POS ID and Token from FBR. These are required for invoice submission.
        </p>

        <div class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">POS ID *</label>
              <input
                v-model="form.pos_id"
                type="text"
                placeholder="e.g., 194444"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
              />
              <p class="text-xs text-gray-500 mt-1">POS Registration Number issued by FBR</p>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Registration Code</label>
              <input
                v-model="form.pos_access_code"
                type="text"
                placeholder="e.g., 3364862B"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
              />
              <p class="text-xs text-gray-500 mt-1">Registration reference code from FBR portal (not used for API calls)</p>
            </div>
          </div>

          <!-- Single Token Field -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Bearer Token (UUID) *</label>
            <textarea
              v-model="form.pos_sandbox_token"
              rows="2"
              placeholder="e.g., 840a2665-e8b2-34ac-87b3-bee52e7dff57"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent font-mono text-sm"
            ></textarea>
            <p class="text-xs text-gray-500 mt-1">
              The UUID token from FBR. Used as the Bearer token for all API calls (sandbox and production).
            </p>
          </div>

          <!-- Endpoint -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">API Endpoint</label>
            <input
              v-model="form.pos_sandbox_endpoint"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent font-mono text-sm"
            />
            <div class="mt-2 space-y-1 text-xs text-gray-500">
              <p>Common FBR endpoints — copy the one that works for your registration:</p>
              <button type="button" @click="form.pos_sandbox_endpoint = 'https://fbr.gov.pk'"
                class="block text-blue-600 hover:underline text-left">
                → https://fbr.gov.pk &nbsp;<span class="text-purple-600 font-semibold">(Suggested PRAL Cloud IMS endpoint)</span>
              </button>
              <button type="button" @click="form.pos_sandbox_endpoint = 'https://gw.fbr.gov.pk/imsp/v1/api/Live/PostData'"
                class="block text-blue-600 hover:underline text-left">
                → https://gw.fbr.gov.pk/imsp/v1/api/Live/PostData &nbsp;<span class="text-green-600 font-semibold">(DI/Production gateway)</span>
              </button>
              <button type="button" @click="form.pos_sandbox_endpoint = 'https://esp.fbr.gov.pk:8244/FBR/v1/api/Live/PostData'"
                class="block text-blue-600 hover:underline text-left">
                → https://esp.fbr.gov.pk:8244/FBR/v1/api/Live/PostData &nbsp;<span class="text-gray-400">(Legacy Retail POS sandbox)</span>
              </button>
            </div>
          </div>

          <!-- Test Connection -->
          <div class="flex items-center gap-3 pt-2">
            <button
              @click="testConnection"
              :disabled="testing || !form.pos_id || !form.pos_sandbox_token"
              class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 transition-colors disabled:opacity-50"
            >
              <svg v-if="testing" class="animate-spin h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <svg v-else class="w-4 h-4 mr-2 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {{ testing ? 'Testing...' : 'Test Connection' }}
            </button>

            <!-- Save Button (inline with Test) -->
            <button
              @click="saveSettings"
              :disabled="saving"
              class="inline-flex items-center px-5 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 transition-colors disabled:opacity-50"
            >
              <svg v-if="saving" class="animate-spin h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <svg v-else class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              {{ saving ? 'Saving...' : 'Save Settings' }}
            </button>

            <!-- Result Badge -->
            <span
              v-if="testResult"
              :class="testResult.success
                ? 'bg-green-100 text-green-800 border-green-300'
                : 'bg-red-100 text-red-800 border-red-300'"
              class="inline-flex items-center px-3 py-1.5 rounded-md text-sm font-medium border"
            >
              {{ testResult.success ? '✅' : '❌' }} {{ testResult.message }}
            </span>
          </div>
        </div>
      </div>


    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axiosInstance from '@/apis/axiosInstance'

// NOTE: axiosInstance has baseURL = 'http://localhost:8000/api'
// Actual backend URL resolves to: /api/pos-fbr-settings/
// (companies router is mounted at api/ not api/companies/)
const API_PATH = 'pos-fbr-settings/'

const form = ref({
  pos_id: '',
  pos_access_code: '',
  pos_sandbox_token: '',          // This is the single FBR bearer token
  pos_sandbox_endpoint: 'https://esp.fbr.gov.pk:8244/FBR/v1/api/Live/PostData',
  pos_production_token: '',
  pos_production_endpoint: 'https://gw.fbr.gov.pk/imsp/v1/api/Live/PostData',
})

const loading = ref(false)
const saving = ref(false)
const testing = ref(false)
const testResult = ref<{ success: boolean; message: string } | null>(null)

const fetchSettings = async () => {
  loading.value = true
  try {
    console.log('[POS Setup] Fetching settings from:', API_PATH)
    const res = await axiosInstance.get(API_PATH)
    console.log('[POS Setup] Fetched settings:', res.data)
    form.value = { ...form.value, ...res.data }
  } catch (error: any) {
    console.error('[POS Setup] Error fetching settings:', error.response?.status, error.response?.data || error.message)
  } finally {
    loading.value = false
  }
}

const saveSettings = async () => {
  saving.value = true
  testResult.value = null
  try {
    const payload = {
      pos_id: form.value.pos_id,
      pos_access_code: form.value.pos_access_code,
      pos_sandbox_token: form.value.pos_sandbox_token,
      pos_sandbox_endpoint: form.value.pos_sandbox_endpoint,
      // Mirror single token to production field as well
      pos_production_token: form.value.pos_sandbox_token,
      pos_production_endpoint: form.value.pos_production_endpoint,
    }
    console.log('[POS Setup] Saving settings:', payload)
    await axiosInstance.post(`${API_PATH}save/`, payload)
    testResult.value = { success: true, message: 'Settings saved successfully!' }
  } catch (error: any) {
    console.error('[POS Setup] Error saving:', error.response?.status, error.response?.data || error.message)
    const msg = error.response?.data?.detail || error.response?.data?.error || 'Failed to save settings'
    testResult.value = { success: false, message: msg }
  } finally {
    saving.value = false
  }
}

const testConnection = async () => {
  if (!form.value.pos_id || !form.value.pos_sandbox_token) {
    testResult.value = { success: false, message: 'Enter POS ID and Token first.' }
    return
  }

  testing.value = true
  testResult.value = null

  // Send current form values so the backend can test WITHOUT requiring a save first
  const requestPayload = {
    pos_id: form.value.pos_id,
    token: form.value.pos_sandbox_token,
    endpoint: form.value.pos_sandbox_endpoint,
  }
  const url = `${API_PATH}test_connection/`

  console.group('[POS Setup] Test Connection')
  console.log('URL:', url)
  console.log('Request payload:', requestPayload)

  try {
    const res = await axiosInstance.post(url, requestPayload)
    console.log('HTTP status:', res.status)
    console.log('Response data:', res.data)
    console.log('FBR http_status:', res.data.http_status)
    console.log('FBR raw response:', res.data.fbr_response)
    console.log('What we sent (headers):', res.data.sent_headers)
    console.log('What we sent (payload):', res.data.sent_payload)
    console.groupEnd()

    testResult.value = {
      success: res.data.success,
      message: res.data.message || (res.data.success ? 'Connection OK' : 'Failed'),
    }
  } catch (error: any) {
    const httpStatus = error.response?.status
    const data = error.response?.data
    console.error('HTTP status:', httpStatus)
    console.error('Response data:', data)
    console.error('FBR raw response:', data?.fbr_response)
    console.error('Full error:', error)
    console.groupEnd()

    const msg = data?.message || data?.error || data?.detail || `HTTP ${httpStatus} error`
    testResult.value = { success: false, message: msg }
  } finally {
    testing.value = false
  }
}

onMounted(() => {
  fetchSettings()
})
</script>
