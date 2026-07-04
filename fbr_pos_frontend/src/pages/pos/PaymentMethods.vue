<template>
  <div class="flex flex-col pb-12 h-full bg-gray-50/50 min-h-screen">
    <!-- Header -->
    <div class="px-8 pt-8 pb-6 border-b border-gray-200 bg-white">
      <h1 class="text-2xl font-bold text-gray-900">Payment methods</h1>
      <p class="text-sm text-gray-500 mt-1">
        Configure your accepted payment gateways. Fill in details and upload QR codes, then enable the method.
      </p>
    </div>

    <div v-if="loading" class="flex justify-center items-center py-20">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-teal-600"></div>
    </div>

    <div v-else class="px-8 py-8 w-full space-y-6">
      <!-- Enabled Methods Toggle Row -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-1">Enabled methods</h2>
        <p class="text-xs text-gray-500 mb-4">Cashiers only see methods enabled here on the POS checkout screen.</p>
        
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
          <label class="flex items-center space-x-2 cursor-pointer">
            <input type="checkbox" v-model="settings.is_cash_enabled" class="rounded border-gray-300 text-teal-600 focus:ring-teal-500" />
            <span class="text-sm text-gray-700 font-medium">Cash</span>
          </label>
          <label class="flex items-center space-x-2 cursor-pointer">
            <input type="checkbox" v-model="settings.is_card_enabled" class="rounded border-gray-300 text-teal-600 focus:ring-teal-500" />
            <span class="text-sm text-gray-700 font-medium">Card</span>
          </label>
          <label class="flex items-center space-x-2 cursor-pointer">
            <input type="checkbox" :checked="settings.is_easypaisa_enabled" @change="toggleEasyPaisa" class="rounded border-gray-300 text-teal-600 focus:ring-teal-500" />
            <span class="text-sm text-gray-700 font-medium">EasyPaisa</span>
          </label>
          <label class="flex items-center space-x-2 cursor-pointer">
            <input type="checkbox" :checked="settings.is_jazzcash_enabled" @change="toggleJazzCash" class="rounded border-gray-300 text-teal-600 focus:ring-teal-500" />
            <span class="text-sm text-gray-700 font-medium">JazzCash</span>
          </label>
          <label class="flex items-center space-x-2 cursor-pointer">
            <input type="checkbox" :checked="settings.is_raast_enabled" @change="toggleRaast" class="rounded border-gray-300 text-teal-600 focus:ring-teal-500" />
            <span class="text-sm text-gray-700 font-medium">Raast</span>
          </label>
          <label class="flex items-center space-x-2 cursor-pointer">
            <input type="checkbox" :checked="settings.is_bank_transfer_enabled" @change="toggleBankTransfer" class="rounded border-gray-300 text-teal-600 focus:ring-teal-500" />
            <span class="text-sm text-gray-700 font-medium">Bank Transfer</span>
          </label>
        </div>

        <!-- Save toggles button -->
        <div class="mt-4 pt-4 border-t border-gray-100 flex justify-end">
          <button @click="saveToggles" :disabled="saving" class="px-4 py-2 text-sm font-medium bg-teal-600 text-white rounded-lg hover:bg-teal-700 disabled:opacity-50 transition">
            <span v-if="saving">Saving...</span>
            <span v-else>Save Toggles</span>
          </button>
        </div>
      </div>

      <!-- Config Cards -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        <!-- EasyPaisa -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div class="px-6 py-4 bg-green-50 border-b border-green-100 flex items-center justify-between">
            <h3 class="text-sm font-bold text-green-800 uppercase tracking-wide">EasyPaisa</h3>
            <span v-if="settings.is_easypaisa_enabled" class="text-xs font-semibold bg-green-200 text-green-800 px-2 py-0.5 rounded-full">Enabled</span>
            <span v-else class="text-xs font-semibold bg-gray-200 text-gray-600 px-2 py-0.5 rounded-full">Disabled</span>
          </div>
          <div class="p-6 space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Merchant ID</label>
              <input type="text" v-model="settings.easypaisa_merchant_id" placeholder="e.g. EP-123456" class="w-full rounded-lg border-gray-300 shadow-sm focus:border-teal-500 focus:ring-teal-500 text-sm" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">QR Code Image</label>
              <input type="file" @change="(e) => handleFileChange(e, 'easypaisa_qr_image')" accept="image/*" class="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100 cursor-pointer" />
              <div v-if="settings.easypaisa_qr_image && typeof settings.easypaisa_qr_image === 'string'" class="mt-3">
                <img :src="settings.easypaisa_qr_image" alt="EasyPaisa QR" class="h-24 w-24 object-cover rounded-lg border border-gray-200 shadow-sm" />
              </div>
            </div>
            <div class="pt-2 border-t border-gray-100 flex justify-end">
              <button @click="saveCard('easypaisa')" :disabled="savingCard === 'easypaisa'" class="px-4 py-2 text-sm font-medium bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 transition">
                <span v-if="savingCard === 'easypaisa'">Saving...</span>
                <span v-else>Save EasyPaisa</span>
              </button>
            </div>
          </div>
        </div>

        <!-- JazzCash -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div class="px-6 py-4 bg-red-50 border-b border-red-100 flex items-center justify-between">
            <h3 class="text-sm font-bold text-red-800 uppercase tracking-wide">JazzCash</h3>
            <span v-if="settings.is_jazzcash_enabled" class="text-xs font-semibold bg-red-200 text-red-800 px-2 py-0.5 rounded-full">Enabled</span>
            <span v-else class="text-xs font-semibold bg-gray-200 text-gray-600 px-2 py-0.5 rounded-full">Disabled</span>
          </div>
          <div class="p-6 space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Merchant ID</label>
              <input type="text" v-model="settings.jazzcash_merchant_id" placeholder="e.g. JC-789012" class="w-full rounded-lg border-gray-300 shadow-sm focus:border-teal-500 focus:ring-teal-500 text-sm" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">QR Code Image</label>
              <input type="file" @change="(e) => handleFileChange(e, 'jazzcash_qr_image')" accept="image/*" class="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-red-50 file:text-red-700 hover:file:bg-red-100 cursor-pointer" />
              <div v-if="settings.jazzcash_qr_image && typeof settings.jazzcash_qr_image === 'string'" class="mt-3">
                <img :src="settings.jazzcash_qr_image" alt="JazzCash QR" class="h-24 w-24 object-cover rounded-lg border border-gray-200 shadow-sm" />
              </div>
            </div>
            <div class="pt-2 border-t border-gray-100 flex justify-end">
              <button @click="saveCard('jazzcash')" :disabled="savingCard === 'jazzcash'" class="px-4 py-2 text-sm font-medium bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 transition">
                <span v-if="savingCard === 'jazzcash'">Saving...</span>
                <span v-else>Save JazzCash</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Raast -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div class="px-6 py-4 bg-blue-50 border-b border-blue-100 flex items-center justify-between">
            <h3 class="text-sm font-bold text-blue-800 uppercase tracking-wide">Raast</h3>
            <span v-if="settings.is_raast_enabled" class="text-xs font-semibold bg-blue-200 text-blue-800 px-2 py-0.5 rounded-full">Enabled</span>
            <span v-else class="text-xs font-semibold bg-gray-200 text-gray-600 px-2 py-0.5 rounded-full">Disabled</span>
          </div>
          <div class="p-6 space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">IBAN (Receiver)</label>
              <input type="text" v-model="settings.raast_iban" placeholder="PK36SCBL0000001123456702" class="w-full rounded-lg border-gray-300 shadow-sm focus:border-teal-500 focus:ring-teal-500 text-sm font-mono" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">QR Code Image</label>
              <input type="file" @change="(e) => handleFileChange(e, 'raast_qr_image')" accept="image/*" class="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 cursor-pointer" />
              <div v-if="settings.raast_qr_image && typeof settings.raast_qr_image === 'string'" class="mt-3">
                <img :src="settings.raast_qr_image" alt="Raast QR" class="h-24 w-24 object-cover rounded-lg border border-gray-200 shadow-sm" />
              </div>
            </div>
            <div class="pt-2 border-t border-gray-100 flex justify-end">
              <button @click="saveCard('raast')" :disabled="savingCard === 'raast'" class="px-4 py-2 text-sm font-medium bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition">
                <span v-if="savingCard === 'raast'">Saving...</span>
                <span v-else>Save Raast</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Bank Transfer -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div class="px-6 py-4 bg-purple-50 border-b border-purple-100 flex items-center justify-between">
            <h3 class="text-sm font-bold text-purple-800 uppercase tracking-wide">Bank Transfer</h3>
            <span v-if="settings.is_bank_transfer_enabled" class="text-xs font-semibold bg-purple-200 text-purple-800 px-2 py-0.5 rounded-full">Enabled</span>
            <span v-else class="text-xs font-semibold bg-gray-200 text-gray-600 px-2 py-0.5 rounded-full">Disabled</span>
          </div>
          <div class="p-6 space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Bank Name</label>
              <input type="text" v-model="settings.bank_name" placeholder="HBL / MCB / UBL ..." class="w-full rounded-lg border-gray-300 shadow-sm focus:border-teal-500 focus:ring-teal-500 text-sm" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Account Name</label>
              <input type="text" v-model="settings.bank_account_name" placeholder="Account holder name" class="w-full rounded-lg border-gray-300 shadow-sm focus:border-teal-500 focus:ring-teal-500 text-sm" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">IBAN</label>
              <input type="text" v-model="settings.bank_iban" placeholder="PK..." class="w-full rounded-lg border-gray-300 shadow-sm focus:border-teal-500 focus:ring-teal-500 text-sm font-mono" />
            </div>
            <div class="pt-2 border-t border-gray-100 flex justify-end">
              <button @click="saveCard('bank')" :disabled="savingCard === 'bank'" class="px-4 py-2 text-sm font-medium bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 transition">
                <span v-if="savingCard === 'bank'">Saving...</span>
                <span v-else>Save Bank Details</span>
              </button>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from "@/stores/auth/authStore"
import companyAPI from '@/apis/admin/companyAPI'

const authStore = useAuthStore()
const loading = ref(true)
const saving = ref(false)
const savingCard = ref('')

const settings = ref({
  is_cash_enabled: true,
  is_card_enabled: false,
  is_easypaisa_enabled: false,
  is_jazzcash_enabled: false,
  is_raast_enabled: false,
  is_bank_transfer_enabled: false,
  
  easypaisa_merchant_id: '',
  easypaisa_qr_image: null as File | string | null,
  
  jazzcash_merchant_id: '',
  jazzcash_qr_image: null as File | string | null,
  
  raast_iban: '',
  raast_qr_image: null as File | string | null,
  
  bank_name: '',
  bank_account_name: '',
  bank_iban: '',
})

const filesToUpload = ref<{ [key: string]: File }>({})

const fetchSettings = async () => {
  if (!authStore.user?.company_id) return
  try {
    const res = await companyAPI.getPaymentSettings(authStore.user.company_id)
    Object.assign(settings.value, res)
  } catch (err) {
    console.error('Failed to fetch payment settings', err)
  } finally {
    loading.value = false
  }
}

const handleFileChange = (e: Event, field: string) => {
  const target = e.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    filesToUpload.value[field] = target.files[0]
  }
}

// Toggles with validation
const toggleEasyPaisa = (e: Event) => {
  const isChecked = (e.target as HTMLInputElement).checked
  if (isChecked) {
    if (!settings.value.easypaisa_merchant_id || (!settings.value.easypaisa_qr_image && !filesToUpload.value['easypaisa_qr_image'])) {
      alert("Please save Merchant ID and upload a QR image before enabling EasyPaisa.")
      ;(e.target as HTMLInputElement).checked = false
      return
    }
  }
  settings.value.is_easypaisa_enabled = isChecked
}

const toggleJazzCash = (e: Event) => {
  const isChecked = (e.target as HTMLInputElement).checked
  if (isChecked) {
    if (!settings.value.jazzcash_merchant_id || (!settings.value.jazzcash_qr_image && !filesToUpload.value['jazzcash_qr_image'])) {
      alert("Please save Merchant ID and upload a QR image before enabling JazzCash.")
      ;(e.target as HTMLInputElement).checked = false
      return
    }
  }
  settings.value.is_jazzcash_enabled = isChecked
}

const toggleRaast = (e: Event) => {
  const isChecked = (e.target as HTMLInputElement).checked
  if (isChecked) {
    if (!settings.value.raast_iban || (!settings.value.raast_qr_image && !filesToUpload.value['raast_qr_image'])) {
      alert("Please save IBAN and upload a QR image before enabling Raast.")
      ;(e.target as HTMLInputElement).checked = false
      return
    }
  }
  settings.value.is_raast_enabled = isChecked
}

const toggleBankTransfer = (e: Event) => {
  const isChecked = (e.target as HTMLInputElement).checked
  if (isChecked) {
    if (!settings.value.bank_name || !settings.value.bank_account_name || !settings.value.bank_iban) {
      alert("Please save Bank Name, Account Name, and IBAN before enabling Bank Transfer.")
      ;(e.target as HTMLInputElement).checked = false
      return
    }
  }
  settings.value.is_bank_transfer_enabled = isChecked
}

// Save only toggles
const saveToggles = async () => {
  if (!authStore.user?.company_id) return
  saving.value = true
  try {
    const res = await companyAPI.patchPaymentSettings(authStore.user.company_id, {
      is_cash_enabled: settings.value.is_cash_enabled,
      is_card_enabled: settings.value.is_card_enabled,
      is_easypaisa_enabled: settings.value.is_easypaisa_enabled,
      is_jazzcash_enabled: settings.value.is_jazzcash_enabled,
      is_raast_enabled: settings.value.is_raast_enabled,
      is_bank_transfer_enabled: settings.value.is_bank_transfer_enabled,
    })
    Object.assign(settings.value, res)
    alert("Payment toggles saved!")
  } catch (err: any) {
    alert(err.response?.data?.is_easypaisa_enabled?.[0] || err.response?.data?.is_jazzcash_enabled?.[0] || err.response?.data?.is_raast_enabled?.[0] || err.response?.data?.is_bank_transfer_enabled?.[0] || err.response?.data?.detail || 'Failed to save toggles.')
  } finally {
    saving.value = false
  }
}

// Save individual card
const saveCard = async (card: string) => {
  if (!authStore.user?.company_id) return
  savingCard.value = card
  try {
    const formData = new FormData()
    
    if (card === 'easypaisa') {
      formData.append('easypaisa_merchant_id', settings.value.easypaisa_merchant_id)
      if (filesToUpload.value['easypaisa_qr_image']) {
        formData.append('easypaisa_qr_image', filesToUpload.value['easypaisa_qr_image'])
      }
    } else if (card === 'jazzcash') {
      formData.append('jazzcash_merchant_id', settings.value.jazzcash_merchant_id)
      if (filesToUpload.value['jazzcash_qr_image']) {
        formData.append('jazzcash_qr_image', filesToUpload.value['jazzcash_qr_image'])
      }
    } else if (card === 'raast') {
      formData.append('raast_iban', settings.value.raast_iban)
      if (filesToUpload.value['raast_qr_image']) {
        formData.append('raast_qr_image', filesToUpload.value['raast_qr_image'])
      }
    } else if (card === 'bank') {
      formData.append('bank_name', settings.value.bank_name)
      formData.append('bank_account_name', settings.value.bank_account_name)
      formData.append('bank_iban', settings.value.bank_iban)
    }

    const res = await companyAPI.patchPaymentSettings(authStore.user.company_id, formData)
    Object.assign(settings.value, res)
    // Clear the file input for this card
    if (card === 'easypaisa') delete filesToUpload.value['easypaisa_qr_image']
    if (card === 'jazzcash') delete filesToUpload.value['jazzcash_qr_image']
    if (card === 'raast') delete filesToUpload.value['raast_qr_image']
    
    alert(`${card.charAt(0).toUpperCase() + card.slice(1)} details saved!`)
  } catch (err: any) {
    console.error(err)
    alert(err.response?.data?.detail || 'Failed to save. Check all required fields.')
  } finally {
    savingCard.value = ''
  }
}

onMounted(() => {
  fetchSettings()
})
</script>
