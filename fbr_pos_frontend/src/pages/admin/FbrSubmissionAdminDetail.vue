<template>
  <div class="h-full flex flex-col px-8 py-8" v-if="!loading && log">
    <div class="mb-6 flex items-center justify-between">
      <div>
        <div class="flex items-center text-sm text-gray-500 mb-2">
          <RouterLink to="/admin" class="hover:text-gray-900">Fbr</RouterLink>
          <span class="mx-2">&rsaquo;</span>
          <RouterLink to="/admin/fbr-submissions" class="hover:text-gray-900">Fbr submissions</RouterLink>
          <span class="mx-2">&rsaquo;</span>
          <span class="text-gray-900 font-medium truncate">FbrSubmission object ({{ log.id }})</span>
        </div>
        <h1 class="text-2xl font-bold text-gray-900 flex items-center gap-2">
          <RouterLink to="/admin/fbr-submissions" class="text-gray-400 hover:text-gray-600">
            &larr;
          </RouterLink>
          {{ log.local_invoice_id }}
        </h1>
      </div>
      <div class="flex items-center gap-3">
        <button v-if="log.sale_id" @click="viewInvoice" class="px-4 py-2 bg-indigo-600 text-white rounded-md text-sm font-semibold hover:bg-indigo-700 shadow-sm transition-colors">
          View invoice
        </button>
      </div>
    </div>

    <!-- Detail View -->
    <div class="bg-white shadow rounded-lg border border-gray-200 overflow-hidden flex-1 p-6 space-y-6 overflow-y-auto">
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label class="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1">Created at</label>
          <div class="text-sm text-gray-900">{{ log.created_at }}</div>
        </div>
        <div>
          <label class="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1">Updated at</label>
          <div class="text-sm text-gray-900">{{ log.created_at }}</div>
        </div>
        <div>
          <label class="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1">Tenant</label>
          <div class="text-sm text-gray-900 font-medium">{{ log.company_name }}</div>
        </div>
        <div>
          <label class="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1">Id</label>
          <div class="text-sm text-gray-900">{{ log.id }}</div>
        </div>
        <div>
          <label class="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1">Invoice</label>
          <div class="text-sm text-gray-900 font-mono">{{ log.local_invoice_id }}</div>
        </div>
        <div>
          <label class="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1">Return ref</label>
          <div class="text-sm text-gray-900">-</div>
        </div>
        <div>
          <label class="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1">Environment</label>
          <div class="text-sm text-gray-900 capitalize">{{ log.environment }}</div>
        </div>
        <div>
          <label class="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1">Endpoint</label>
          <div class="text-sm text-gray-900">{{ log.endpoint }}</div>
        </div>
      </div>

      <div class="border-t border-gray-200 pt-6">
        <label class="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">Request payload</label>
        <pre class="bg-gray-50 border border-gray-200 rounded-md p-4 text-xs font-mono text-gray-800 overflow-x-auto">{{ formatJSON(log.request_payload) }}</pre>
      </div>

      <div class="border-t border-gray-200 pt-6">
        <label class="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">Response payload</label>
        <pre class="bg-gray-50 border border-gray-200 rounded-md p-4 text-xs font-mono text-gray-800 overflow-x-auto">{{ formatJSON(log.response_payload) }}</pre>
      </div>

      <div class="border-t border-gray-200 pt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label class="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1">Http status</label>
          <div class="text-sm text-gray-900">{{ log.http_status }}</div>
        </div>
        <div>
          <label class="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1">Status code</label>
          <div class="text-sm text-gray-900 font-mono" :class="log.status_code === '00' ? 'text-green-600' : 'text-red-600'">{{ log.status_code }}</div>
        </div>
        <div>
          <label class="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1">Fbr invoice number</label>
          <div class="text-sm text-gray-900 font-mono">{{ log.fbr_invoice_id }}</div>
        </div>
        <div>
          <label class="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1">Attempt number</label>
          <div class="text-sm text-gray-900">{{ log.attempt }}</div>
        </div>
        <div>
          <label class="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1">Duration ms</label>
          <div class="text-sm text-gray-900">{{ log.latency_ms }}</div>
        </div>
        <div>
          <label class="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1">Error message</label>
          <div class="text-sm text-gray-900 text-red-600">{{ log.error_message }}</div>
        </div>
      </div>
    </div>
  </div>
  <div v-else class="h-full flex items-center justify-center">
    <div class="animate-spin rounded-full h-10 w-10 border-4 border-indigo-500 border-t-transparent"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axiosInstance from '@/apis/axiosInstance'

const route = useRoute()
const logId = route.params.id
const log = ref<any>(null)
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await axiosInstance.get(`/admin/fbr-submissions/${logId}/`)
    log.value = res.data
  } catch (err) {
    console.error('Failed to load submission detail', err)
    alert('Submission not found.')
  } finally {
    loading.value = false
  }
})

const formatJSON = (data: any) => {
  if (!data) return '-'
  try {
    return JSON.stringify(data, null, 4)
  } catch {
    return String(data)
  }
}

const viewInvoice = async () => {
  if (!log.value.sale_id) return
  try {
    const res = await axiosInstance.get(`/admin/fbr-submissions/${log.value.id}/invoice-pdf/`)
    const url = res.data?.url
    if (!url) {
      throw new Error('Invoice URL not available')
    }
    window.open(url, '_blank')
  } catch (error) {
    console.error('Failed to load invoice PDF:', error)
    alert('Failed to load PDF. Invoice might not exist or generation failed.')
  }
}
</script>
