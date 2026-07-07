<template>
  <div class="h-full flex flex-col bg-gray-50 min-h-screen pb-24">
    <!-- Header -->
    <div class="px-8 py-4 border-b border-gray-200 bg-white sticky top-0 z-10 flex items-center justify-between">
      <div class="flex items-center gap-4">
        <button @click="goBack" class="p-2 hover:bg-gray-100 rounded-full transition-colors">
          <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
        </button>
        <div>
          <div class="flex items-center gap-2 text-sm text-gray-500 mb-1">
            <span>Platform_Admin</span>
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
            <router-link to="/admin/subscription-plans" class="hover:text-gray-900">Subscription plans</router-link>
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
            <span class="text-gray-900 font-medium">{{ isEdit ? 'Edit' : 'Add' }}</span>
          </div>
          <h1 class="text-2xl font-bold text-gray-900">{{ isEdit ? form.name : 'New Subscription Plan' }}</h1>
        </div>
      </div>
      
      <div class="flex items-center gap-3">
        <button @click="savePlan(false)" :disabled="isSubmitting" class="px-4 py-2 border border-gray-300 bg-white text-gray-700 rounded-md text-sm font-semibold hover:bg-gray-50 transition-colors shadow-sm">
          Save
        </button>
        <button @click="savePlan(true)" :disabled="isSubmitting" class="px-4 py-2 bg-teal-600 text-white rounded-md text-sm font-semibold hover:bg-teal-700 transition-colors shadow-sm">
          Save and continue editing
        </button>
      </div>
    </div>

    <!-- Content -->
    <div class="px-8 py-8 flex-1 w-full space-y-8">
      
      <!-- Basic Info -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div class="px-6 py-5 border-b border-gray-200 bg-gray-50">
          <h3 class="text-lg font-medium text-gray-900">Basic Details</h3>
        </div>
        <div class="p-6 space-y-6">
          <div class="grid grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Code*</label>
              <input type="text" v-model="form.code" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-teal-500 focus:border-teal-500 sm:text-sm" placeholder="e.g. starter" />
              <p class="mt-1 text-xs text-gray-500">Stable identifier (e.g. 'starter', 'pro', 'enterprise').</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Name*</label>
              <input type="text" v-model="form.name" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-teal-500 focus:border-teal-500 sm:text-sm" placeholder="e.g. Starter" />
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea v-model="form.description" rows="3" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-teal-500 focus:border-teal-500 sm:text-sm"></textarea>
          </div>

          <div class="grid grid-cols-2 gap-6">
            <div class="flex flex-col justify-center">
              <label class="flex items-center">
                <input type="checkbox" v-model="form.is_active" class="h-4 w-4 text-teal-600 focus:ring-teal-500 border-gray-300 rounded" />
                <span class="ml-2 block text-sm font-medium text-gray-700">Is active</span>
              </label>
              <p class="mt-1 text-xs text-gray-500 ml-6">Hide from new signups when false.</p>
            </div>
            <div class="flex flex-col justify-center">
              <label class="flex items-center">
                <input type="checkbox" v-model="form.is_trial" class="h-4 w-4 text-teal-600 focus:ring-teal-500 border-gray-300 rounded" />
                <span class="ml-2 block text-sm font-medium text-gray-700">Is trial</span>
              </label>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Sort order*</label>
            <input type="number" v-model.number="form.sort_order" class="w-32 px-3 py-2 border border-gray-300 rounded-md focus:ring-teal-500 focus:border-teal-500 sm:text-sm" />
          </div>
        </div>
      </div>

      <!-- Pricing -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div class="px-6 py-5 border-b border-gray-200 bg-gray-50">
          <h3 class="text-lg font-medium text-gray-900">Pricing</h3>
        </div>
        <div class="p-6 grid grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Monthly price (Rs)*</label>
            <input type="number" step="0.01" v-model.number="form.price_per_month" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-teal-500 focus:border-teal-500 sm:text-sm" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Yearly price (Rs)*</label>
            <input type="number" step="0.01" v-model.number="form.price_per_year" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-teal-500 focus:border-teal-500 sm:text-sm" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Duration Days (Default 30)*</label>
            <input type="number" v-model.number="form.duration_days" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-teal-500 focus:border-teal-500 sm:text-sm" />
          </div>
        </div>
      </div>

      <!-- Limits -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div class="px-6 py-5 border-b border-gray-200 bg-gray-50">
          <h3 class="text-lg font-medium text-gray-900">Limits (0 = unlimited)</h3>
        </div>
        <div class="p-6 grid grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Max products</label>
            <input type="number" v-model.number="form.max_products" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-teal-500 focus:border-teal-500 sm:text-sm" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Max users (Staff)</label>
            <input type="number" v-model.number="form.max_users" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-teal-500 focus:border-teal-500 sm:text-sm" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Max customers</label>
            <input type="number" v-model.number="form.max_customers" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-teal-500 focus:border-teal-500 sm:text-sm" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Max sales per month</label>
            <input type="number" v-model.number="form.max_sales_per_month" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-teal-500 focus:border-teal-500 sm:text-sm" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Max categories</label>
            <input type="number" v-model.number="form.max_categories" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-teal-500 focus:border-teal-500 sm:text-sm" />
          </div>
        </div>
      </div>

      <!-- Features -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div class="px-6 py-5 border-b border-gray-200 bg-gray-50">
          <h3 class="text-lg font-medium text-gray-900">Features</h3>
        </div>
        <div class="p-6 grid grid-cols-2 gap-4">
          <label class="flex items-center p-3 border border-gray-200 rounded-md hover:bg-gray-50 cursor-pointer">
            <input type="checkbox" v-model="form.includes_fbr_di" class="h-4 w-4 text-teal-600 focus:ring-teal-500 border-gray-300 rounded" />
            <span class="ml-3 block text-sm font-medium text-gray-700">FBR Digital Invoicing</span>
          </label>
          <label class="flex items-center p-3 border border-gray-200 rounded-md hover:bg-gray-50 cursor-pointer">
            <input type="checkbox" v-model="form.includes_inventory" class="h-4 w-4 text-teal-600 focus:ring-teal-500 border-gray-300 rounded" />
            <span class="ml-3 block text-sm font-medium text-gray-700">Inventory Tracking</span>
          </label>
          <label class="flex items-center p-3 border border-gray-200 rounded-md hover:bg-gray-50 cursor-pointer">
            <input type="checkbox" v-model="form.includes_warehousing" class="h-4 w-4 text-teal-600 focus:ring-teal-500 border-gray-300 rounded" />
            <span class="ml-3 block text-sm font-medium text-gray-700">Warehousing</span>
          </label>
          <label class="flex items-center p-3 border border-gray-200 rounded-md hover:bg-gray-50 cursor-pointer">
            <input type="checkbox" v-model="form.includes_advanced_reports" class="h-4 w-4 text-teal-600 focus:ring-teal-500 border-gray-300 rounded" />
            <span class="ml-3 block text-sm font-medium text-gray-700">Advanced Reports</span>
          </label>
          <label class="flex items-center p-3 border border-gray-200 rounded-md hover:bg-gray-50 cursor-pointer">
            <input type="checkbox" v-model="form.includes_audit_logs" class="h-4 w-4 text-teal-600 focus:ring-teal-500 border-gray-300 rounded" />
            <span class="ml-3 block text-sm font-medium text-gray-700">Audit Logs</span>
          </label>
          <label class="flex items-center p-3 border border-gray-200 rounded-md hover:bg-gray-50 cursor-pointer">
            <input type="checkbox" v-model="form.includes_hardware_integration" class="h-4 w-4 text-teal-600 focus:ring-teal-500 border-gray-300 rounded" />
            <span class="ml-3 block text-sm font-medium text-gray-700">Hardware Integration</span>
          </label>
          <label class="flex items-center p-3 border border-gray-200 rounded-md hover:bg-gray-50 cursor-pointer">
            <input type="checkbox" v-model="form.includes_restaurant_fnb" class="h-4 w-4 text-teal-600 focus:ring-teal-500 border-gray-300 rounded" />
            <span class="ml-3 block text-sm font-medium text-gray-700">Restaurant F&B</span>
          </label>
          <label class="flex items-center p-3 border border-gray-200 rounded-md hover:bg-gray-50 cursor-pointer">
            <input type="checkbox" v-model="form.includes_multi_branch" class="h-4 w-4 text-teal-600 focus:ring-teal-500 border-gray-300 rounded" />
            <span class="ml-3 block text-sm font-medium text-gray-700">Multi-Branch</span>
          </label>
          <label class="flex items-center p-3 border border-gray-200 rounded-md hover:bg-gray-50 cursor-pointer">
            <input type="checkbox" v-model="form.includes_debit_credit_notes" class="h-4 w-4 text-teal-600 focus:ring-teal-500 border-gray-300 rounded" />
            <span class="ml-3 block text-sm font-medium text-gray-700">Debit/Credit Notes</span>
          </label>
          <label class="flex items-center p-3 border border-gray-200 rounded-md hover:bg-gray-50 cursor-pointer">
            <input type="checkbox" v-model="form.includes_returns" class="h-4 w-4 text-teal-600 focus:ring-teal-500 border-gray-300 rounded" />
            <span class="ml-3 block text-sm font-medium text-gray-700">Returns</span>
          </label>
          <label class="flex items-center p-3 border border-gray-200 rounded-md hover:bg-gray-50 cursor-pointer">
            <input type="checkbox" v-model="form.includes_cheque_bank" class="h-4 w-4 text-teal-600 focus:ring-teal-500 border-gray-300 rounded" />
            <span class="ml-3 block text-sm font-medium text-gray-700">Cheque & Bank Transfer</span>
          </label>
        </div>
      </div>
      
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { subscriptionsAPI } from '@/apis/admin/subscriptionsAPI'

const router = useRouter()
const route = useRoute()

const isEdit = computed(() => route.params.id !== undefined)
const planId = computed(() => Number(route.params.id))
const isSubmitting = ref(false)

const form = ref({
  code: '',
  name: '',
  description: '',
  is_active: true,
  is_trial: false,
  sort_order: 0,
  price_per_month: 0,
  price_per_year: 0,
  duration_days: 30,
  max_products: 0,
  max_users: 0,
  max_customers: 0,
  max_sales_per_month: 0,
  max_categories: 0,
  includes_fbr_di: false,
  includes_inventory: false,
  includes_warehousing: false,
  includes_advanced_reports: false,
  includes_audit_logs: false,
  includes_hardware_integration: false,
  includes_restaurant_fnb: false,
  includes_multi_branch: false,
  includes_debit_credit_notes: true,
  includes_returns: true,
  includes_cheque_bank: false,
})

onMounted(async () => {
  if (isEdit.value) {
    try {
      const data = await subscriptionsAPI.getPlan(planId.value)
      // Merge fetched data into form
      Object.keys(form.value).forEach((key) => {
        if (data[key] !== undefined) {
          (form.value as any)[key] = data[key]
        }
      })
    } catch (err: any) {
      alert('Failed to load plan details')
      goBack()
    }
  }
})

const goBack = () => {
  router.push('/admin/subscription-plans')
}

const savePlan = async (continueEditing: boolean) => {
  if (!form.value.name || !form.value.code) {
    alert('Code and Name are required fields.')
    return
  }
  
  isSubmitting.value = true
  try {
    let savedPlan;
    if (isEdit.value) {
      savedPlan = await subscriptionsAPI.updatePlan(planId.value, form.value)
      alert('Plan updated successfully!')
    } else {
      savedPlan = await subscriptionsAPI.createPlan(form.value)
      alert('Plan created successfully!')
    }
    
    if (continueEditing) {
      if (!isEdit.value) {
        // Redirect to edit page of the newly created plan
        router.push(`/admin/subscription-plans/${savedPlan.id}/edit`)
      }
    } else {
      goBack()
    }
  } catch (err: any) {
    alert(err.response?.data?.message || 'Failed to save plan')
  } finally {
    isSubmitting.value = false
  }
}
</script>
