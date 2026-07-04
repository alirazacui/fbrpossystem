<template>
  <div class="space-y-6 pb-12" v-if="company">

    <!-- ── Confirm Modal ───────────────────────────────── -->
    <ConfirmModal
      v-model="modal.show"
      :title="modal.title"
      :message="modal.message"
      :type="modal.type"
      :confirm-label="modal.confirmLabel"
      :loading="modal.loading"
      @confirm="modal.onConfirm"
    />

    <!-- Assign Plan Modal -->
    <div v-if="assignModalOpen" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="assignModalOpen = false"></div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">Assign Subscription Plan</h3>
            <div class="mt-4">
              <label class="block text-sm font-medium text-gray-700 mb-2">Select Plan</label>
              <select v-model="selectedPlanId" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-teal-500 focus:border-teal-500">
                <option value="">-- Choose a plan --</option>
                <option v-for="plan in subscriptionPlans" :key="plan.id" :value="plan.id">
                  {{ plan.name }} ({{ plan.price_per_month === 0 ? 'Free' : `Rs ${plan.price_per_month}/mo` }})
                </option>
              </select>
            </div>
            <div class="mt-4">
              <label class="block text-sm font-medium text-gray-700 mb-2">Notes (Optional)</label>
              <input type="text" v-model="assignNotes" placeholder="Reason for assigning..." class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-teal-500 focus:border-teal-500" />
            </div>
          </div>
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button @click="submitAssignPlan" :disabled="!selectedPlanId || isAssigning" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-teal-600 text-base font-medium text-white hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500 sm:ml-3 sm:w-auto sm:text-sm">
              {{ isAssigning ? 'Assigning...' : 'Assign Plan' }}
            </button>
            <button @click="assignModalOpen = false" type="button" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">{{ company.business_name }}</h1>
        <p class="text-gray-600 mt-1">Tenant Details & FBR Integration</p>
      </div>
      <div class="flex items-center space-x-4">
        <button
          @click="goBack"
          class="px-4 py-2 text-gray-600 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition"
        >
          Back
        </button>
        <button
          @click="editCompany"
          class="px-4 py-2 text-teal-700 bg-teal-50 border border-teal-200 rounded-lg hover:bg-teal-100 transition"
        >
          Edit
        </button>
        <button
          @click="openPermissions"
          class="px-4 py-2 text-purple-700 bg-purple-50 border border-purple-200 rounded-lg hover:bg-purple-100 transition flex items-center space-x-1.5"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/>
          </svg>
          <span>Permissions</span>
        </button>
        <button
          v-if="['admin', 'admin_staff'].includes(authStore.user?.role || '')"
          @click="passwordModalOpen = true"
          class="px-4 py-2 text-indigo-700 bg-indigo-50 border border-indigo-200 rounded-lg hover:bg-indigo-100 transition"
        >
          Change Password
        </button>
        <button
          @click="toggleCompanyStatus"
          :class="company.is_active 
            ? 'text-red-700 bg-red-50 border border-red-200 hover:bg-red-100' 
            : 'text-green-700 bg-green-50 border border-green-200 hover:bg-green-100'"
          class="px-4 py-2 border rounded-lg transition"
        >
          {{ company.is_active ? 'Deactivate' : 'Activate' }}
        </button>
      </div>
    </div>

    <div class="max-w-4xl space-y-6">
      <!-- Company Info -->
      <div class="space-y-6">
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-lg font-bold text-gray-900 mb-4 pb-2 border-b border-gray-100">Business Information</h2>
          <div class="space-y-4 text-sm">
            <div>
              <p class="text-gray-500 mb-1">NTN</p>
              <p class="font-medium text-gray-900">{{ company.ntn || 'N/A' }}</p>
            </div>
            <div>
              <p class="text-gray-500 mb-1">Address</p>
              <p class="font-medium text-gray-900">{{ company.address || 'N/A' }}</p>
            </div>
            <div>
              <p class="text-gray-500 mb-1">FBR Sector</p>
              <p class="font-medium text-gray-900 capitalize">{{ company.fbr_sector?.replace('_', ' ') || 'N/A' }}</p>
            </div>
            <div>
              <p class="text-gray-500 mb-1">Status</p>
              <span :class="company.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'" class="px-2 py-1 rounded text-xs font-semibold uppercase tracking-wide">
                {{ company.is_active ? 'Active' : 'Inactive' }}
              </span>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex justify-between items-center mb-4 pb-2 border-b border-gray-100">
            <h2 class="text-lg font-bold text-gray-900">Subscription Information</h2>
            <button @click="openAssignModal" class="text-sm px-3 py-1 bg-teal-50 text-teal-700 border border-teal-200 rounded hover:bg-teal-100 transition">
              Assign Plan
            </button>
          </div>
          <div class="space-y-4 text-sm">
            <div>
              <p class="text-gray-500 mb-1">Current Plan</p>
              <p class="font-medium text-gray-900 capitalize">{{ company.subscription_plan || 'No Plan Assigned' }}</p>
            </div>
            <div>
              <p class="text-gray-500 mb-1">Subscription Status</p>
              <span :class="company.subscription_status === 'active' ? 'bg-green-100 text-green-800' : (company.subscription_status === 'expired' ? 'bg-red-100 text-red-800' : 'bg-gray-100 text-gray-800')" class="px-2 py-1 rounded text-xs font-semibold uppercase tracking-wide">
                {{ company.subscription_status || 'None' }}
              </span>
            </div>
            <div v-if="company.subscription_expiry_date">
              <p class="text-gray-500 mb-1">Expiry Date</p>
              <p class="font-medium text-gray-900">{{ company.subscription_expiry_date }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

    <!-- Change Owner Password Modal -->
    <div v-if="passwordModalOpen" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="password-modal-title" role="dialog" aria-modal="true">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="closePasswordModal"></div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <h3 class="text-lg leading-6 font-medium text-gray-900" id="password-modal-title">Change Owner Password</h3>
            <div class="mt-4 space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">New Password</label>
                <input v-model="passwordForm.new_password" type="password" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-teal-500 focus:border-teal-500" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Confirm Password</label>
                <input v-model="passwordForm.confirm_password" type="password" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-teal-500 focus:border-teal-500" />
              </div>
              <p v-if="passwordError" class="text-sm text-red-600">{{ passwordError }}</p>
            </div>
          </div>
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button @click="submitOwnerPasswordChange" :disabled="passwordSaving" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-indigo-600 text-base font-medium text-white hover:bg-indigo-700 sm:ml-3 sm:w-auto sm:text-sm">
              {{ passwordSaving ? 'Saving...' : 'Save Password' }}
            </button>
            <button @click="closePasswordModal" type="button" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  
  <!-- Loading State -->
  <div v-else class="flex justify-center items-center h-64">
    <div class="w-8 h-8 border-4 border-teal-600 border-t-transparent rounded-full animate-spin"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import companyAPI from '@/apis/admin/companyAPI'
import { subscriptionsAPI } from '@/apis/admin/subscriptionsAPI'
import ConfirmModal from '@/components/ConfirmModal.vue'
import type { Company } from '@/types'
import { useAuthStore } from '@/stores/auth/authStore'

const route = useRoute()
const router = useRouter()
const companyId = Number(route.params.id)
const authStore = useAuthStore()

const company = ref<Company | null>(null)

// Modal state
const modal = reactive<{
  show: boolean
  title: string
  message: string
  type: 'danger' | 'warning' | 'success'
  confirmLabel: string
  loading: boolean
  onConfirm: () => void
}>({
  show: false,
  title: '',
  message: '',
  type: 'danger',
  confirmLabel: 'Confirm',
  loading: false,
  onConfirm: () => {},
})

const openModal = (opts: Partial<typeof modal> & { onConfirm: () => void }) => {
  Object.assign(modal, { show: true, loading: false, type: 'danger', confirmLabel: 'Confirm', ...opts })
}


const fetchCompany = async () => {
  try {
    company.value = await companyAPI.getCompanyDetail(companyId)
  } catch (error) {
    console.error('Error fetching company:', error)
    openModal({
      show: true,
      title: 'Load Error',
      message: 'Failed to load company details. Please try again.',
      type: 'warning',
      confirmLabel: 'Retry',
      onConfirm: () => { modal.show = false; fetchCompany() },
    })
  }
}

// Subscription Assign Logic
const subscriptionPlans = ref<any[]>([])
const assignModalOpen = ref(false)
const selectedPlanId = ref<number | ''>('')
const assignNotes = ref('')
const isAssigning = ref(false)
const passwordModalOpen = ref(false)
const passwordSaving = ref(false)
const passwordError = ref('')
const passwordForm = reactive({
  new_password: '',
  confirm_password: '',
})

const openAssignModal = async () => {
  assignModalOpen.value = true
  if (subscriptionPlans.value.length === 0) {
    try {
      subscriptionPlans.value = await subscriptionsAPI.getPlans()
    } catch (e) {
      console.error('Failed to load plans', e)
    }
  }
}

const submitAssignPlan = async () => {
  if (!selectedPlanId.value) return
  isAssigning.value = true
  try {
    await subscriptionsAPI.assignPlan({
      company_id: companyId,
      plan_id: Number(selectedPlanId.value),
      notes: assignNotes.value
    })
    assignModalOpen.value = false
    alert('Subscription assigned successfully!')
    await fetchCompany() // Refresh company details to show new plan
  } catch (err: any) {
    console.error(err)
    alert(err.response?.data?.message || 'Failed to assign plan')
  } finally {
    isAssigning.value = false
  }
}

const closePasswordModal = () => {
  passwordModalOpen.value = false
  passwordError.value = ''
  passwordForm.new_password = ''
  passwordForm.confirm_password = ''
}

const submitOwnerPasswordChange = async () => {
  passwordError.value = ''
  if (!passwordForm.new_password || !passwordForm.confirm_password) {
    passwordError.value = 'Both password fields are required.'
    return
  }
  if (passwordForm.new_password !== passwordForm.confirm_password) {
    passwordError.value = 'Passwords do not match.'
    return
  }

  passwordSaving.value = true
  try {
    await companyAPI.changeOwnerPassword(companyId, {
      new_password: passwordForm.new_password,
      confirm_password: passwordForm.confirm_password,
    })
    closePasswordModal()
    alert('Owner password changed successfully!')
  } catch (err: any) {
    passwordError.value = err.response?.data?.detail || err.response?.data?.confirm_password || 'Failed to change password.'
  } finally {
    passwordSaving.value = false
  }
}

onMounted(() => {
  if (!isNaN(companyId)) {
    fetchCompany()
  }
})


const goBack = () => {
  router.back()
}

const editCompany = () => {
  router.push(`/admin/tenants/${companyId}/edit`)
}

const openPermissions = () => {
  router.push(`/admin/tenants/${companyId}/permissions`)
}

const toggleCompanyStatus = () => {
  const isCurrentlyActive = company.value?.is_active
  const actionText = isCurrentlyActive ? 'Deactivate' : 'Activate'

  openModal({
    title: `${actionText} Company`,
    message: `Are you sure you want to ${actionText.toLowerCase()} "${company.value?.business_name}"? ${isCurrentlyActive ? 'They will lose access to the platform.' : 'They will regain access to the platform.'}`,
    type: isCurrentlyActive ? 'danger' : 'success',
    confirmLabel: actionText,
    onConfirm: async () => {
      modal.loading = true
      try {
        if (isCurrentlyActive) {
          await companyAPI.deactivateCompany(companyId)
        } else {
          await companyAPI.activateCompany(companyId)
        }
        modal.show = false
        await fetchCompany()
      } catch (err) {
        console.error(`Error ${actionText.toLowerCase()}ing:`, err)
        modal.loading = false
        modal.title = 'Action Failed'
        modal.message = `Failed to ${actionText.toLowerCase()} the company. Please try again.`
        modal.type = 'warning'
        modal.confirmLabel = 'Close'
        modal.onConfirm = () => { modal.show = false }
      }
    },
  })
}
</script>
