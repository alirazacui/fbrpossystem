<template>
  <div class="p-8 space-y-6 max-w-4xl">

    <!-- Header -->
    <div class="flex items-center justify-between mb-2">
      <div class="flex items-center gap-3">
        <router-link to="/school/invoices" class="text-gray-400 hover:text-gray-700">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
        </router-link>
        <h1 class="text-2xl font-bold text-gray-900">Invoice Details</h1>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
    </div>
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 rounded-lg px-4 py-3 text-sm">{{ error }}</div>

    <template v-else-if="invoice">

      <!-- ⚠️ CNIC Warning Banner -->
      <div
        v-if="needsCnicWarning"
        class="flex items-start gap-3 bg-amber-50 border border-amber-300 rounded-xl px-5 py-4"
      >
        <svg class="w-5 h-5 text-amber-500 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
        </svg>
        <div>
          <p class="text-sm font-bold text-amber-800">CNIC Required — Invoice exceeds PKR 20,000</p>
          <p class="text-xs text-amber-700 mt-0.5">FBR requires guardian CNIC for invoices ≥ PKR 20,000. Please link a guardian with a valid CNIC before generating the FBR invoice.</p>
        </div>
      </div>

      <!-- Invoice Card -->
      <div class="bg-white border border-gray-200 rounded-xl shadow-sm p-8">

        <!-- Invoice Header -->
        <div class="flex items-start justify-between border-b border-gray-100 pb-6 mb-6">
          <div>
            <h2 class="text-2xl font-bold text-gray-900 mb-1">Fee Voucher</h2>
            <p class="text-sm font-semibold text-gray-500">Student: <span class="text-gray-800">{{ invoice.student_name || '—' }}</span></p>
          </div>
          <div class="text-right flex flex-col items-end gap-2">
            <!-- Payment Status -->
            <span :class="{
              'bg-red-50 text-red-700 border-red-200': invoice.status === 'unpaid',
              'bg-green-50 text-green-700 border-green-200': invoice.status === 'paid',
              'bg-yellow-50 text-yellow-700 border-yellow-200': invoice.status === 'partial'
            }" class="px-3 py-1 rounded-full text-xs font-bold border uppercase tracking-wider">
              {{ invoice.status }}
            </span>
            <!-- FBR Status -->
            <span :class="{
              'bg-gray-100 text-gray-600 border-gray-200': invoice.invoice_status_fbr === 'draft',
              'bg-indigo-50 text-indigo-700 border-indigo-200': invoice.invoice_status_fbr === 'sent_to_fbr',
              'bg-red-50 text-red-700 border-red-200': invoice.invoice_status_fbr === 'failed',
            }" class="px-3 py-1 rounded-full text-xs font-bold border uppercase tracking-wider">
              FBR: {{ invoice.invoice_status_fbr?.replace('_', ' ') }}
            </span>
          </div>
        </div>

        <!-- Meta Grid -->
        <div class="grid grid-cols-2 gap-8 mb-8">
          <div>
            <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Academic Details</p>
            <p class="text-sm text-gray-800">Session: <span class="font-semibold">{{ invoice.session_name || '—' }}</span></p>
            <p class="text-sm text-gray-800">Grade: <span class="font-semibold">{{ invoice.grade_name || '—' }}</span></p>
            <p class="text-sm text-gray-800 mt-1">Invoice Date: <span class="font-semibold">{{ invoice.invoice_date }}</span></p>
            <p v-if="invoice.due_date" class="text-sm text-gray-800">Due: <span class="font-semibold text-red-600">{{ invoice.due_date }}</span></p>
          </div>
          <div class="text-right">
            <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">FBR Integration</p>
            <p v-if="invoice.fbr_invoice_number" class="text-sm text-gray-800">
              FBR Invoice #: <span class="font-semibold font-mono text-indigo-700">{{ invoice.fbr_invoice_number }}</span>
            </p>
            <p v-else class="text-sm text-gray-400 italic">Not submitted to FBR yet</p>
          </div>
        </div>

        <!-- Fee Items Table -->
        <div v-if="invoice.items && invoice.items.length > 0" class="mb-8">
          <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">Fee Items</p>
          <div class="border border-gray-200 rounded-lg overflow-hidden">
            <table class="w-full text-sm">
              <thead class="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th class="text-left px-4 py-2.5 text-xs font-bold text-gray-500 uppercase tracking-wider">Description</th>
                  <th class="text-left px-4 py-2.5 text-xs font-bold text-gray-500 uppercase tracking-wider">PCT Code</th>
                  <th class="text-right px-4 py-2.5 text-xs font-bold text-gray-500 uppercase tracking-wider">Qty</th>
                  <th class="text-right px-4 py-2.5 text-xs font-bold text-gray-500 uppercase tracking-wider">Unit Price</th>
                  <th class="text-right px-4 py-2.5 text-xs font-bold text-gray-500 uppercase tracking-wider">Discount</th>
                  <th class="text-right px-4 py-2.5 text-xs font-bold text-gray-500 uppercase tracking-wider">Tax</th>
                  <th class="text-right px-4 py-2.5 text-xs font-bold text-gray-500 uppercase tracking-wider">Total</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-for="item in invoice.items" :key="item.id" class="hover:bg-gray-50">
                  <td class="px-4 py-3 text-gray-800 font-medium">{{ item.description || '—' }}</td>
                  <td class="px-4 py-3 text-gray-500 font-mono text-xs">{{ item.pct_code || '—' }}</td>
                  <td class="px-4 py-3 text-right text-gray-600">{{ item.quantity }}</td>
                  <td class="px-4 py-3 text-right text-gray-800">Rs {{ item.unit_price }}</td>
                  <td class="px-4 py-3 text-right text-red-600">{{ parseFloat(item.discount_amount) > 0 ? `- Rs ${item.discount_amount}` : '—' }}</td>
                  <td class="px-4 py-3 text-right text-gray-600">{{ parseFloat(item.tax_amount) > 0 ? `Rs ${item.tax_amount}` : '—' }}</td>
                  <td class="px-4 py-3 text-right font-bold text-gray-900">Rs {{ item.total_amount }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Totals -->
        <div class="bg-gray-50 rounded-lg p-6 flex flex-col gap-2 border border-gray-100">
          <div class="flex justify-between text-sm">
            <span class="text-gray-600">Total Amount</span>
            <span class="font-semibold text-gray-900">Rs {{ invoice.total_amount }}</span>
          </div>
          <div class="flex justify-between text-sm">
            <span class="text-gray-600">Concession</span>
            <span class="font-semibold text-red-600">- Rs {{ invoice.total_concession_amount }}</span>
          </div>
          <hr class="border-gray-200 my-2" />
          <div class="flex justify-between text-lg font-bold">
            <span class="text-gray-900">Net Payable</span>
            <span class="text-indigo-700">Rs {{ invoice.total_payable_amount }}</span>
          </div>
        </div>

        <!-- FBR Action Section -->
        <div class="mt-6 pt-6 border-t border-gray-100">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-bold text-gray-800">FBR Digital Invoice</p>
              <p class="text-xs text-gray-500 mt-0.5">Submit this fee voucher to PRAL for FBR compliance</p>
            </div>

            <!-- Already sent -->
            <div v-if="invoice.invoice_status_fbr === 'sent_to_fbr'" class="flex items-center gap-2 text-sm font-semibold text-indigo-700">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
              Submitted to FBR
            </div>

            <!-- Failed — can retry -->
            <button
              v-else-if="invoice.invoice_status_fbr === 'failed'"
              @click="handleGenerateFbr"
              :disabled="generatingFbr || needsCnicWarning"
              class="flex items-center gap-2 px-4 py-2 text-sm font-semibold text-white bg-red-600 rounded-lg hover:bg-red-700 disabled:opacity-50 transition-colors"
            >
              <div v-if="generatingFbr" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
              {{ generatingFbr ? 'Retrying...' : 'Retry FBR Submit' }}
            </button>

            <!-- Draft — generate -->
            <button
              v-else
              @click="handleGenerateFbr"
              :disabled="generatingFbr || needsCnicWarning"
              class="flex items-center gap-2 px-5 py-2 text-sm font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 disabled:opacity-50 transition-colors"
            >
              <div v-if="generatingFbr" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
              {{ generatingFbr ? 'Generating...' : 'Generate FBR Invoice' }}
            </button>
          </div>

          <!-- FBR Error -->
          <div v-if="fbrError" class="mt-3 bg-red-50 border border-red-200 text-red-700 text-xs rounded-lg px-4 py-2">
            {{ fbrError }}
          </div>

          <!-- FBR Success: QR Code -->
          <div v-if="invoice.invoice_status_fbr === 'sent_to_fbr' && invoice.fbr_invoice_number" class="mt-5 flex items-start gap-6 bg-indigo-50 border border-indigo-100 rounded-xl p-5">
            <div class="flex-1">
              <p class="text-xs font-bold text-indigo-700 uppercase tracking-wider mb-1">FBR Invoice Reference</p>
              <p class="font-mono text-sm font-bold text-indigo-900">{{ invoice.fbr_invoice_number }}</p>
              <p class="text-xs text-indigo-500 mt-2">Parents can verify this invoice on the FBR Tax Asaan Mobile App by scanning the QR code.</p>
            </div>
            <div class="flex-shrink-0">
              <p class="text-xs font-bold text-indigo-700 uppercase tracking-wider mb-2 text-center">QR Code</p>
              <img
                :src="`https://api.qrserver.com/v1/create-qr-code/?size=120x120&data=${encodeURIComponent(invoice.fbr_invoice_number)}`"
                alt="FBR QR Code"
                class="w-28 h-28 border-2 border-indigo-200 rounded-lg"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Payments Section -->
      <div class="mt-4">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-bold text-gray-900">Payments</h3>
          <button v-if="invoice.status !== 'paid'" @click="showAddPayment = true" class="text-sm font-semibold text-indigo-600 hover:text-indigo-800 flex items-center gap-1">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
            Record Payment
          </button>
        </div>

        <div v-if="!payments.length" class="bg-gray-50 border border-gray-200 border-dashed rounded-xl p-10 text-center">
          <p class="text-gray-500 text-sm">No payments recorded yet.</p>
        </div>

        <div v-else class="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
          <table class="w-full text-sm">
            <thead class="bg-gray-50 border-b border-gray-200">
              <tr>
                <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Date</th>
                <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Mode</th>
                <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Reference</th>
                <th class="text-right px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Amount</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-for="pay in payments" :key="pay.id" class="hover:bg-gray-50">
                <td class="px-6 py-4 text-gray-600">{{ pay.payment_date }}</td>
                <td class="px-6 py-4 font-semibold text-gray-900 capitalize">{{ pay.payment_mode }}</td>
                <td class="px-6 py-4 text-gray-500">{{ pay.reference_no || '—' }}</td>
                <td class="px-6 py-4 text-right font-bold text-green-600">Rs {{ pay.amount_paid }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>

    <!-- Record Payment Modal -->
    <div v-if="showAddPayment" class="fixed inset-0 z-50 flex items-center justify-center bg-black/30 backdrop-blur-sm">
      <div class="bg-white rounded-xl shadow-xl p-6 w-full max-w-md mx-4">
        <h3 class="text-lg font-bold text-gray-900 mb-4">Record Payment</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Amount Paid <span class="text-red-500">*</span></label>
            <input v-model.number="paymentForm.amount_paid" type="number" class="w-full px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Payment Date <span class="text-red-500">*</span></label>
            <input v-model="paymentForm.payment_date" type="date" class="w-full px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Payment Mode</label>
            <select v-model="paymentForm.payment_mode" class="w-full px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
              <option value="cash">Cash</option>
              <option value="bank">Bank</option>
              <option value="online">Online</option>
              <option value="cheque">Cheque</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Reference No.</label>
            <input v-model="paymentForm.reference_no" type="text" class="w-full px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          </div>
        </div>
        <div class="flex gap-3 justify-end mt-6">
          <button @click="showAddPayment = false" class="px-4 py-2 text-sm font-medium text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50">Cancel</button>
          <button @click="handleRecordPayment" :disabled="savingPayment" class="px-4 py-2 text-sm font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 disabled:opacity-50">
            {{ savingPayment ? 'Saving...' : 'Record Payment' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { feeInvoiceAPI, type FeeInvoice } from '@/school/apis/feeInvoiceAPI'
import { feePaymentAPI, type FeePayment } from '@/school/apis/feePaymentAPI'

const route = useRoute()
const invoiceId = route.params.id as string

const invoice = ref<FeeInvoice | null>(null)
const payments = ref<FeePayment[]>([])

const loading = ref(true)
const error = ref('')
const fbrError = ref('')
const generatingFbr = ref(false)

const showAddPayment = ref(false)
const savingPayment = ref(false)
const paymentForm = ref({
  amount_paid: 0,
  payment_date: new Date().toISOString().split('T')[0],
  payment_mode: 'cash' as 'cash' | 'bank' | 'online' | 'cheque',
  reference_no: ''
})

// FBR compliance: warn if >= 20,000 and no guardian linked
const needsCnicWarning = computed(() => {
  if (!invoice.value) return false
  const payable = parseFloat(invoice.value.total_payable_amount || '0')
  return payable >= 20000 && !invoice.value.guardian_id
})

const fetchDetails = async () => {
  loading.value = true
  error.value = ''
  try {
    const [invRes, payRes] = await Promise.all([
      feeInvoiceAPI.retrieve(invoiceId),
      feePaymentAPI.list({ fee_invoice_id: invoiceId })
    ])
    invoice.value = invRes.data
    payments.value = payRes.data.results || (payRes.data as any)
  } catch {
    error.value = 'Failed to load invoice details.'
  } finally {
    loading.value = false
  }
}

onMounted(fetchDetails)

const handleGenerateFbr = async () => {
  if (!invoice.value || needsCnicWarning.value) return
  fbrError.value = ''
  generatingFbr.value = true
  try {
    await feeInvoiceAPI.generateFbr(invoiceId)
    // Refresh the invoice to get updated status and fbr_invoice_number
    await fetchDetails()
  } catch (err: any) {
    const msg = err.response?.data?.error || err.response?.data?.detail || 'Failed to generate FBR invoice. Please check token configuration.'
    fbrError.value = msg
  } finally {
    generatingFbr.value = false
  }
}

const handleRecordPayment = async () => {
  if (!paymentForm.value.amount_paid) return
  savingPayment.value = true
  try {
    await feePaymentAPI.create({
      fee_invoice_id: invoiceId,
      ...paymentForm.value
    })
    showAddPayment.value = false
    await fetchDetails()
  } catch {
    alert('Failed to record payment')
  } finally {
    savingPayment.value = false
  }
}
</script>
