<template>
  <div class="p-8 space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Fee Invoices</h1>
        <p class="text-sm text-gray-500 mt-1">Manage student billing and generated invoices.</p>
      </div>
      <router-link to="/school/invoices/create" class="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white text-sm font-semibold rounded-lg hover:bg-indigo-700 transition-colors">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
        Generate Invoice
      </router-link>
    </div>

    <div v-if="loading" class="flex items-center justify-center py-20"><div class="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div></div>
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 rounded-lg px-4 py-3 text-sm">{{ error }}</div>
    
    <div v-else-if="invoices.length === 0" class="bg-white border border-gray-200 rounded-xl p-16 text-center">
      <svg class="w-12 h-12 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
      <h3 class="text-base font-semibold text-gray-700 mb-1">No invoices generated</h3>
      <router-link to="/school/invoices/create" class="text-sm text-indigo-600 font-semibold hover:underline">Generate Invoice →</router-link>
    </div>
    
    <div v-else class="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
      <table class="w-full text-sm">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Student</th>
            <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Date</th>
            <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Amount</th>
            <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Status</th>
            <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">FBR Status</th>
            <th class="text-right px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="inv in invoices" :key="inv.id" class="hover:bg-gray-50 transition-colors">
            <td class="px-6 py-4 font-semibold text-gray-900">{{ inv.student_name || 'Unknown' }}</td>
            <td class="px-6 py-4 text-gray-600">{{ inv.invoice_date }}</td>
            <td class="px-6 py-4 font-bold text-gray-900">Rs {{ inv.total_payable_amount }}</td>
            <td class="px-6 py-4">
              <span :class="{
                'bg-red-50 text-red-700': inv.status === 'unpaid',
                'bg-green-50 text-green-700': inv.status === 'paid',
                'bg-yellow-50 text-yellow-700': inv.status === 'partial'
              }" class="px-2 py-0.5 rounded-full text-xs font-semibold uppercase">{{ inv.status }}</span>
            </td>
            <td class="px-6 py-4 text-gray-500 text-xs">
              <span v-if="inv.invoice_status_fbr === 'sent_to_fbr'" class="text-green-600 font-bold">Synced</span>
              <span v-else-if="inv.invoice_status_fbr === 'failed'" class="text-red-600 font-bold">Failed</span>
              <span v-else>Draft</span>
            </td>
            <td class="px-6 py-4 text-right">
              <div class="flex items-center justify-end gap-2">
                <router-link :to="`/school/invoices/${inv.id}`" class="text-xs text-indigo-600 hover:text-indigo-800 font-semibold">View</router-link>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { feeInvoiceAPI, type FeeInvoice } from '@/school/apis/feeInvoiceAPI'

const invoices = ref<FeeInvoice[]>([])
const loading = ref(true)
const error = ref('')

const fetchInvoices = async () => {
  loading.value = true
  try {
    const res = await feeInvoiceAPI.list()
    invoices.value = res.data.results || (res.data as any)
  } catch { error.value = 'Failed to load invoices.' }
  finally { loading.value = false }
}

onMounted(fetchInvoices)
</script>
