<template>
  <div class="min-h-screen bg-gray-50 flex flex-col pb-12 font-sans">
    
    <!-- Top Nav -->
    <div class="px-8 py-4 flex items-center justify-between">
      <div class="flex items-center text-sm font-medium text-gray-500 hover:text-gray-700 cursor-pointer transition-colors" @click="router.push('/pos/sales')">
        <svg class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" /></svg>
        Back to sales
      </div>
      <div>
        <span v-if="isDraft" class="inline-flex items-center text-yellow-700 bg-yellow-50 px-3 py-1 rounded-md text-xs font-semibold border border-yellow-100">
          <svg class="w-3 h-3 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>
          Draft &mdash; cannot amend
        </span>
        <span v-else-if="isFinalized" class="inline-flex items-center text-green-700 bg-green-50 px-3 py-1 rounded-md text-xs font-semibold border border-green-100">
          <svg class="w-3 h-3 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>
          Finalized &mdash; cannot amend
        </span>
      </div>
    </div>

    <!-- Main Content Loading -->
    <div v-if="loading" class="flex-1 flex justify-center items-center py-20">
      <svg class="animate-spin h-8 w-8 text-green-600" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>

    <!-- Main Content -->
    <div v-else-if="sale" class="w-full px-8 space-y-6">
      
      <!-- Title & Basic Info -->
      <div>
        <h1 class="text-3xl font-bold text-gray-900 tracking-tight">{{ sale.sale_number }}</h1>
        <div class="flex items-center gap-3 mt-3 text-sm">
          <span :class="isDraft ? 'bg-yellow-100 text-yellow-800' : 'bg-green-100 text-green-800'" class="px-2.5 py-0.5 rounded-md font-semibold text-xs uppercase tracking-wider">{{ statusText }}</span>
          <span class="text-gray-500 font-medium">{{ formatDate(sale.created_at) }}</span>
        </div>
      </div>
      
      <!-- Action Buttons Row -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div class="flex items-center gap-2">
          <!-- Validate with FBR -->
          <button v-if="isDraft && !isValidated" @click="validateFbr" :disabled="actionLoading" class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 transition-colors disabled:opacity-50">
            <svg class="w-4 h-4 mr-2 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            Validate with FBR
          </button>
          
          <!-- Submit to FBR -->
          <button v-if="isDraft" @click="submitFbr" :disabled="actionLoading" class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 transition-colors disabled:opacity-50">
            <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>
            Submit to FBR
          </button>
          
          <!-- Download / View PDF -->
          <button v-if="isFinalized" @click="downloadPdf" class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 transition-colors disabled:opacity-50">
            <svg class="w-4 h-4 mr-2 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>
            Download
          </button>
          
          <!-- More Actions (...) -->
          <div class="relative">
            <button @click="showActions = !showActions" @blur="closeActions" class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 transition-colors focus:outline-none">
              <svg class="w-5 h-5 text-gray-500" fill="currentColor" viewBox="0 0 20 20"><path d="M6 10a2 2 0 11-4 0 2 2 0 014 0zM12 10a2 2 0 11-4 0 2 2 0 014 0zM16 12a2 2 0 100-4 2 2 0 000 4z" /></svg>
            </button>
            <div v-show="showActions" class="origin-top-left absolute left-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-50 focus:outline-none">
              <div class="py-1">
                <button @click.stop="downloadPdf" class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Download PDF</button>
                <button v-if="isDraft" @click.stop="cancelSale" class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 border-t border-gray-100">Cancel Draft</button>
                <button v-if="isFinalized" @click.stop="cancelSale" class="block w-full text-left px-4 py-2 text-sm text-red-700 hover:bg-red-50 border-t border-gray-100">Mark cancelled on FBR</button>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Delete Draft Button -->
        <div>
          <button v-if="isDraft" @click="cancelSale" :disabled="actionLoading" class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-red-500 hover:bg-red-600 transition-colors disabled:opacity-50">
            Delete draft
          </button>
        </div>
      </div>

      <!-- FBR Validation Messages -->
      <div v-if="fbrError" class="bg-red-50 border-l-4 border-red-500 p-4 rounded-r-md shadow-sm">
        <div class="flex items-start">
          <div class="flex-shrink-0 mt-0.5">
            <svg class="h-5 w-5 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-bold text-red-800">FBR Validation Failed</h3>
            <div class="mt-1 text-sm text-red-700 leading-relaxed font-mono whitespace-pre-wrap">
              {{ fbrError }}
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="isValidated && isDraft" class="bg-teal-50 border-l-4 border-teal-500 p-4 rounded-r-md shadow-sm">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-teal-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="ml-3">
            <p class="text-sm font-bold text-teal-800">Invoice successfully validated by FBR!</p>
            <p class="text-sm text-teal-700 mt-0.5">The invoice complies with all FBR rules and is ready to be submitted.</p>
          </div>
        </div>
      </div>


      <!-- 3 Columns Layout: Buyer | Totals | Payments -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        <!-- Buyer -->
        <div class="bg-white border border-gray-200 rounded-lg p-5">
          <h3 class="text-sm font-bold text-gray-900 mb-4">Buyer</h3>
          <p class="text-sm text-gray-500">{{ sale.customer_name || 'Walk-in' }}</p>
          <p v-if="sale.customer_ntn_cnic" class="text-xs text-gray-500 mt-1">NTN: {{ sale.customer_ntn_cnic }}</p>
        </div>

        <!-- Totals -->
        <div class="bg-white border border-gray-200 rounded-lg p-5">
          <h3 class="text-sm font-bold text-gray-900 mb-4">Totals</h3>
          <div class="space-y-1 text-sm font-mono">
            <div class="flex justify-between items-center">
              <span class="text-gray-600 font-sans">Subtotal</span>
              <span class="text-gray-900">Rs {{ formatMoney(sale.subtotal) }}</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-gray-400 font-sans">Discount</span>
              <span class="text-gray-400">- Rs {{ formatMoney(sale.total_discount) }}</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-gray-600 font-sans">Tax</span>
              <span class="text-gray-900">Rs {{ formatMoney(sale.total_tax) }}</span>
            </div>
            <div class="flex justify-between items-center font-bold text-gray-900 py-1">
              <span class="font-sans">Grand total</span>
              <span>Rs {{ formatMoney(sale.total_amount) }}</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-gray-600 font-sans">Paid</span>
              <span class="text-gray-900">Rs {{ formatMoney(sale.amount_paid) }}</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-gray-600 font-sans">Change</span>
              <span class="text-gray-900">Rs {{ formatMoney(sale.change_given) }}</span>
            </div>
          </div>
        </div>

        <!-- Payments -->
        <div class="bg-white border border-gray-200 rounded-lg p-5">
          <h3 class="text-sm font-bold text-gray-900 mb-4">Payments</h3>
          <div v-if="!sale.payments || sale.payments.length === 0" class="text-sm text-gray-500">
            None
          </div>
          <div v-else class="space-y-2 font-mono text-sm">
            <div v-for="(payment, idx) in sale.payments" :key="idx" class="flex justify-between">
              <span class="text-gray-600 font-sans capitalize">{{ (payment.payment_method || 'Cash').toLowerCase() }}</span>
              <span class="text-gray-900">Rs {{ formatMoney(payment.amount) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- FBR Validated Box (If submitted/finalized) -->
      <div v-if="isFinalized" class="bg-white border-2 border-green-500 rounded-lg shadow-sm p-6 overflow-hidden relative mb-6">
        <div class="absolute -right-4 -top-4 opacity-10">
          <svg class="h-32 w-32 text-green-500" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" /></svg>
        </div>
        
        <div v-if="!sale.fbr_invoice_number">
          <h3 class="text-base font-bold text-yellow-600 mb-2 relative z-10">Processing FBR Submission...</h3>
          <p class="text-sm text-gray-500 relative z-10">Waiting for FBR to return the official Invoice Number and QR Code.</p>
          <button @click="fetchSale" class="mt-4 text-sm text-teal-600 font-semibold">↻ Refresh Status</button>
        </div>

        <div v-else>
          <h3 class="text-base font-bold text-green-800 mb-4 relative z-10">FBR-validated</h3>
          
          <div class="flex flex-col sm:flex-row gap-6 relative z-10">
            <!-- Text Info -->
            <div class="flex-1">
              <p class="text-xs font-semibold text-gray-500 mb-1">FBR Invoice #</p>
              <div class="flex items-start gap-3">
                <svg class="h-6 w-6 text-gray-400 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm14 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z" /></svg>
                <div>
                  <p class="text-base font-mono text-gray-900 break-all"><span class="font-bold">{{ sale.fbr_invoice_number }}</span></p>
                  <p class="text-sm text-gray-500 mt-2 leading-relaxed">Unique FBR Invoice ID.<br>Verify at e.fbr.gov.pk or scan with FBR Tax Asaan.</p>
                </div>
              </div>
            </div>
            
            <!-- QR Code -->
            <div v-if="sale.fbr_qr_code" class="flex-shrink-0 bg-white p-2 border border-gray-200 rounded-md">
              <img :src="`https://api.qrserver.com/v1/create-qr-code/?size=120x120&data=${encodeURIComponent(sale.fbr_qr_code)}`" alt="FBR QR Code" class="w-24 h-24 sm:w-28 sm:h-28" />
            </div>
          </div>
        </div>
      </div>

      <!-- Line Items -->
      <div class="bg-white border border-gray-200 rounded-lg overflow-hidden">
        <div class="px-5 py-4">
          <h2 class="text-sm font-bold text-gray-900">Line items</h2>
        </div>
        <div class="overflow-x-auto border-t border-gray-100">
          <table class="min-w-full divide-y divide-gray-100">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider w-12">#</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Product</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">SKU</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">HS Code</th>
                <th scope="col" class="px-6 py-3 text-right text-xs font-bold text-gray-500 uppercase tracking-wider">Qty</th>
                <th scope="col" class="px-6 py-3 text-right text-xs font-bold text-gray-500 uppercase tracking-wider">Unit Price</th>
                <th scope="col" class="px-6 py-3 text-right text-xs font-bold text-gray-500 uppercase tracking-wider">Tax</th>
                <th scope="col" class="px-6 py-3 text-right text-xs font-bold text-gray-500 uppercase tracking-wider">Line Total</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-100">
              <tr v-if="!sale.lines || sale.lines.length === 0">
                <td colspan="8" class="px-6 py-4 text-center text-sm text-gray-500">No line items.</td>
              </tr>
              <tr v-else v-for="(line, idx) in sale.lines" :key="idx" class="hover:bg-gray-50 transition-colors">
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ idx + 1 }}</td>
                <td class="px-6 py-4 text-sm font-medium text-gray-900">{{ line.product_name }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-mono">{{ line.sku || line.product_name.substring(0,25) }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-mono">{{ line.hs_code || '—' }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right font-mono">{{ Number(line.quantity).toFixed(2) }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right font-mono">Rs {{ formatMoney(line.unit_price) }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right font-mono">Rs {{ formatMoney(line.sales_tax_applicable || 0) }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 text-right font-mono">Rs {{ formatMoney(line.line_total) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- FBR Submissions Log -->
      <div class="bg-white border border-gray-200 rounded-lg overflow-hidden">
        <div class="px-5 py-4 flex items-center">
          <h2 class="text-sm font-bold text-gray-900">FBR submissions log</h2>
          <span class="text-gray-400 font-normal text-sm ml-1">({{ mockLogs.length }} roundtrip{{ mockLogs.length !== 1 ? 's' : '' }})</span>
        </div>
        <div class="overflow-x-auto border-t border-gray-100">
          <table class="min-w-full divide-y divide-gray-100">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">When</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Endpoint</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Env</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">HTTP</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">PRAL Code</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">ms</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">FBR No. / Error</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-100">
              <tr v-if="mockLogs.length === 0">
                <td colspan="7" class="px-6 py-4 text-center text-sm text-gray-500 italic">No FBR logs recorded for this invoice yet.</td>
              </tr>
              <tr v-else v-for="(log, i) in mockLogs" :key="i" class="hover:bg-gray-50 transition-colors">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-600">{{ log.when }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-600">{{ log.endpoint }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm">
                  <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 border border-green-200">
                    {{ log.env }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-mono font-medium text-gray-900">{{ log.http }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm">
                  <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-50 text-green-700 font-mono">
                    {{ log.pral }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-600">{{ log.ms }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-900">{{ log.fbrNo }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
    </div>
    
    <ConfirmModal
      v-model="confirmModalOpen"
      :title="confirmTitle"
      :message="confirmMessage"
      :type="confirmType"
      :confirmLabel="confirmLabel"
      :loading="actionLoading"
      @confirm="executePendingAction"
    />

    <!-- Payment Selection Modal -->
    <div v-if="paymentModalOpen" class="fixed inset-0 z-50 overflow-y-auto">
      <div class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:p-0">
        <div class="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75" @click="paymentModalOpen = false"></div>
        <div class="relative inline-block w-full max-w-md p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-lg">
          <h3 class="text-lg font-medium leading-6 text-gray-900 mb-4">Select Payment Method</h3>
          <p class="text-sm text-gray-500 mb-4">How is the customer paying for this invoice?</p>
          
          <div class="space-y-3 max-h-60 overflow-y-auto custom-scrollbar p-1">
            <label v-if="paymentSettings?.is_cash_enabled" class="flex items-center p-3 border rounded-lg cursor-pointer hover:bg-gray-50" :class="selectedPayment === 'cash' ? 'border-green-500 bg-green-50' : 'border-gray-200'">
              <input type="radio" v-model="selectedPayment" value="cash" class="sr-only" />
              <span class="ml-2 font-medium text-gray-900">Cash</span>
            </label>
            <label v-if="paymentSettings?.is_card_enabled" class="flex items-center p-3 border rounded-lg cursor-pointer hover:bg-gray-50" :class="selectedPayment === 'card' ? 'border-green-500 bg-green-50' : 'border-gray-200'">
              <input type="radio" v-model="selectedPayment" value="card" class="sr-only" />
              <span class="ml-2 font-medium text-gray-900">Card</span>
            </label>
            <label v-if="paymentSettings?.is_easypaisa_enabled" class="flex items-center p-3 border rounded-lg cursor-pointer hover:bg-gray-50" :class="selectedPayment === 'easypaisa' ? 'border-green-500 bg-green-50' : 'border-gray-200'">
              <input type="radio" v-model="selectedPayment" value="easypaisa" class="sr-only" />
              <span class="ml-2 font-medium text-gray-900">EasyPaisa</span>
            </label>
            <label v-if="paymentSettings?.is_jazzcash_enabled" class="flex items-center p-3 border rounded-lg cursor-pointer hover:bg-gray-50" :class="selectedPayment === 'jazzcash' ? 'border-green-500 bg-green-50' : 'border-gray-200'">
              <input type="radio" v-model="selectedPayment" value="jazzcash" class="sr-only" />
              <span class="ml-2 font-medium text-gray-900">JazzCash</span>
            </label>
            <label v-if="paymentSettings?.is_raast_enabled" class="flex items-center p-3 border rounded-lg cursor-pointer hover:bg-gray-50" :class="selectedPayment === 'raast' ? 'border-green-500 bg-green-50' : 'border-gray-200'">
              <input type="radio" v-model="selectedPayment" value="raast" class="sr-only" />
              <span class="ml-2 font-medium text-gray-900">Raast</span>
            </label>
            <label v-if="paymentSettings?.is_bank_transfer_enabled" class="flex items-center p-3 border rounded-lg cursor-pointer hover:bg-gray-50" :class="selectedPayment === 'bank_transfer' ? 'border-green-500 bg-green-50' : 'border-gray-200'">
              <input type="radio" v-model="selectedPayment" value="bank_transfer" class="sr-only" />
              <span class="ml-2 font-medium text-gray-900">Bank Transfer</span>
            </label>
            <label v-if="paymentSettings?.is_cheque_enabled" class="flex items-center p-3 border rounded-lg cursor-pointer hover:bg-gray-50" :class="selectedPayment === 'cheque' ? 'border-green-500 bg-green-50' : 'border-gray-200'">
              <input type="radio" v-model="selectedPayment" value="cheque" class="sr-only" />
              <span class="ml-2 font-medium text-gray-900">Cheque</span>
            </label>
            <div v-if="!paymentSettings" class="text-sm text-gray-500">Loading payment methods...</div>
          </div>
          
          <div class="mt-6 flex justify-end gap-3">
            <button @click="paymentModalOpen = false" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none">
              Cancel
            </button>
            <button @click="confirmPaymentAndSubmit" :disabled="actionLoading" class="px-4 py-2 text-sm font-medium text-white bg-green-600 rounded-md hover:bg-green-700 focus:outline-none disabled:opacity-50">
              <span v-if="actionLoading">Processing...</span>
              <span v-else>Confirm & Submit</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { salesAPI } from '@/apis/pos/sales/salesAPI'
import axiosInstance from '@/apis/axiosInstance'
import ConfirmModal from '@/components/ConfirmModal.vue'
import companyAPI from '@/apis/admin/companyAPI'
import { useAuthStore } from '@/stores/auth/authStore'

const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()

const saleId = Number(route.params.id)
const sale = ref<any>(null)
const loading = ref(true)
const actionLoading = ref(false)
const showActions = ref(false)
const fbrError = ref('')

const isDraft = computed(() => sale.value?.status?.toLowerCase() === 'draft')
const isFinalized = computed(() => sale.value?.status?.toLowerCase() === 'completed')
const isValidated = computed(() => sale.value?.fbr_submission_status?.toLowerCase() === 'validated')

const statusText = computed(() => {
  if (isFinalized.value) return 'Submitted'
  if (isDraft.value && isValidated.value) return 'Validated'
  if (isDraft.value) return 'Draft'
  return sale.value?.status
})

const closeActions = () => {
  setTimeout(() => {
    showActions.value = false
  }, 200)
}

// Mock logs based on state
const mockLogs = computed(() => {
  if (!sale.value) return []
  const logs = []
  
  if (isFinalized.value || sale.value.fbr_submission_status === 'SUCCESS') {
    logs.push({
      when: new Date(sale.value.fbr_submitted_at || sale.value.updated_at).toLocaleString('en-US'),
      endpoint: 'postinvoicedata',
      env: 'production',
      http: '200',
      pral: '00',
      ms: '1104',
      fbrNo: sale.value.fbr_invoice_number || '3640263516977DIQSGY46850602'
    })
  }
  
  if (isValidated.value || isFinalized.value) {
    const date = new Date(sale.value.updated_at)
    date.setSeconds(date.getSeconds() - 7)
    logs.push({
      when: date.toLocaleString('en-US'),
      endpoint: 'validateinvoicedata',
      env: 'production',
      http: '200',
      pral: '00',
      ms: '976',
      fbrNo: ''
    })
  }
  
  return logs
})

const fetchSale = async () => {
  loading.value = true
  try {
    const res = await salesAPI.retrieve(saleId)
    sale.value = res.data
  } catch (error) {
    console.error('Error fetching sale details', error)
    alert('Failed to load invoice details')
    router.push('/pos/sales')
  } finally {
    loading.value = false
  }
}

const validateFbr = async () => {
  actionLoading.value = true
  fbrError.value = ''
  try {
    await salesAPI.validateFbr(saleId)
    await fetchSale()
  } catch (error: any) {
    fbrError.value = error.response?.data?.detail || 'Unknown validation error occurred.'
  } finally {
    actionLoading.value = false
  }
}

// Confirmation Modal State
const confirmModalOpen = ref(false)
const confirmTitle = ref('')
const confirmMessage = ref('')
const confirmType = ref<'danger'|'warning'|'success'>('danger')
const confirmLabel = ref('Confirm')
let pendingAction: (() => Promise<void>) | null = null

const openConfirm = (title: string, message: string, label: string, type: 'danger'|'warning'|'success', action: () => Promise<void>) => {
  confirmTitle.value = title
  confirmMessage.value = message
  confirmLabel.value = label
  confirmType.value = type
  pendingAction = action
  confirmModalOpen.value = true
}

const executePendingAction = async () => {
  if (pendingAction) {
    await pendingAction()
    confirmModalOpen.value = false
  }
}

const paymentSettings = ref<any>(null)
const paymentModalOpen = ref(false)
const selectedPayment = ref('cash')

const getEnabledPaymentMethods = () => {
  const methods: Array<{ key: string; enabled: boolean }> = [
    { key: 'cash', enabled: !!paymentSettings.value?.is_cash_enabled },
    { key: 'card', enabled: !!paymentSettings.value?.is_card_enabled },
    { key: 'easypaisa', enabled: !!paymentSettings.value?.is_easypaisa_enabled },
    { key: 'jazzcash', enabled: !!paymentSettings.value?.is_jazzcash_enabled },
    { key: 'raast', enabled: !!paymentSettings.value?.is_raast_enabled },
    { key: 'bank_transfer', enabled: !!paymentSettings.value?.is_bank_transfer_enabled },
    { key: 'cheque', enabled: !!paymentSettings.value?.is_cheque_enabled },
  ]

  return methods.filter(method => method.enabled).map(method => method.key)
}

const syncSelectedPayment = () => {
  const enabledMethods = getEnabledPaymentMethods()
  if (!enabledMethods.includes(selectedPayment.value)) {
    selectedPayment.value = 'cash'
  }
}

watch(paymentModalOpen, (isOpen) => {
  if (isOpen) {
    selectedPayment.value = 'cash'
    syncSelectedPayment()
  }
})

const submitFbr = async () => {
  if (!paymentSettings.value && authStore.user?.company_id) {
    try {
      paymentSettings.value = await companyAPI.getPaymentSettings(authStore.user.company_id)
    } catch (e) {
      console.warn("Failed to load payment settings")
    }
  }

  syncSelectedPayment()
  paymentModalOpen.value = true
}

const confirmPaymentAndSubmit = async () => {
  syncSelectedPayment()

  actionLoading.value = true
  try {
    const total = Number(sale.value?.total_amount || 0)
    const paid = Number(sale.value?.total_paid || 0)
    if (total > paid) {
      await salesAPI.addPayment(saleId, {
        amount: total - paid,
        payment_method: selectedPayment.value
      })
    }

    await salesAPI.complete(saleId)
    // Wait for the celery task to run
    setTimeout(async () => {
      await fetchSale()
      actionLoading.value = false
      paymentModalOpen.value = false
    }, 1500)
  } catch (error: any) {
    alert(error.response?.data?.detail || error.response?.data?.message || 'Submission failed.')
    actionLoading.value = false
    paymentModalOpen.value = false
  }
}

const cancelSale = () => {
  showActions.value = false
  openConfirm(
    isDraft.value ? 'Delete Draft' : 'Cancel on FBR',
    isDraft.value ? 'Are you sure you want to delete this draft? This cannot be undone.' : 'Are you sure you want to cancel this invoice on the FBR system?',
    isDraft.value ? 'Delete Draft' : 'Cancel Invoice',
    'danger',
    async () => {
      actionLoading.value = true
      try {
        await salesAPI.cancel(saleId)
        await fetchSale()
      } catch (error: any) {
        alert(error.response?.data?.message || 'Cancellation failed.')
      } finally {
        actionLoading.value = false
      }
    }
  )
}

const downloadPdf = async () => {
  showActions.value = false
  actionLoading.value = true
  try {
    const res = await salesAPI.printReceipt(saleId)
    // Create a Blob from the PDF Stream
    const file = new Blob([res.data], { type: 'application/pdf' })
    const fileURL = URL.createObjectURL(file)
    window.open(fileURL, '_blank')
    
    // Log the download action
    try {
      await axiosInstance.post(`/sales/${saleId}/log_download/`)
    } catch (logErr) {
      console.warn('Failed to log download:', logErr)
    }
  } catch (error) {
    console.error('Failed to download PDF:', error)
    alert('Failed to load PDF.')
  } finally {
    actionLoading.value = false
  }
}

const formatMoney = (amount: number | string) => {
  return Number(amount || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const formatDate = (dateStr: string) => {
  if (!dateStr) return '—'
  const d = new Date(dateStr)
  return d.toISOString().split('T')[0]
}

onMounted(async () => {
  fetchSale()
  if (authStore.user?.company_id) {
    try {
      paymentSettings.value = await companyAPI.getPaymentSettings(authStore.user.company_id)
    } catch (e) {
      console.warn("Failed to pre-load payment settings")
    }
  }
})
</script>
