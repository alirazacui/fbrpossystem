<template>
  <div class="h-full flex flex-col bg-gray-50 pb-12">
    <!-- Header -->
    <div class="px-8 py-6 border-b border-gray-200 bg-white sticky top-0 z-10 flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Subscription plans</h1>
        <p class="text-sm text-gray-500 mt-1">Manage pricing plans and their limits for tenants.</p>
      </div>
      <router-link to="/admin/subscription-plans/create" class="px-4 py-2 bg-teal-600 text-white rounded-md text-sm font-semibold hover:bg-teal-700 transition-colors shadow-sm flex items-center gap-2">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
        Add plan
      </router-link>
    </div>

    <!-- Content -->
    <div class="px-8 py-8 flex-1 w-full">
      <div v-if="loading" class="flex justify-center p-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-teal-600"></div>
      </div>
      
      <div v-else class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div class="p-4 border-b border-gray-200 flex justify-between items-center bg-gray-50/50">
          <div class="relative w-72">
            <input type="text" v-model="searchQuery" placeholder="Type to search..." class="w-full pl-9 pr-4 py-2 border border-gray-300 rounded-md focus:ring-teal-500 focus:border-teal-500 sm:text-sm" />
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
            </div>
          </div>
          <button class="flex items-center gap-2 text-sm text-gray-600 hover:text-gray-900">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"></path></svg>
            Filters
          </button>
        </div>
        
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Code</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Monthly</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Yearly</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Max products</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Max users</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Sort order</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Is active</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="plan in filteredPlans" :key="plan.id" class="hover:bg-gray-50 cursor-pointer" @click="goToEdit(plan.id)">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-teal-600">{{ plan.code || '-' }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ plan.name }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatMoney(plan.price_per_month) }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatMoney(plan.price_per_year) }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ plan.max_products_display }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ plan.max_users_display }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ plan.sort_order }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm">
                  <span v-if="plan.is_active" class="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                    Yes
                  </span>
                  <span v-else class="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">
                    No
                  </span>
                </td>
              </tr>
              <tr v-if="filteredPlans.length === 0">
                <td colspan="8" class="px-6 py-12 text-center text-sm text-gray-500">
                  No subscription plans found.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { subscriptionsAPI } from '@/apis/admin/subscriptionsAPI'

const router = useRouter()
const plans = ref<any[]>([])
const loading = ref(true)
const searchQuery = ref('')

onMounted(async () => {
  await loadPlans()
})

const loadPlans = async () => {
  loading.value = true
  try {
    const data = await subscriptionsAPI.getPlans()
    plans.value = data
  } catch (error) {
    console.error('Failed to load subscription plans:', error)
    alert('Failed to load plans.')
  } finally {
    loading.value = false
  }
}

const filteredPlans = computed(() => {
  if (!searchQuery.value) return plans.value
  const lowerQuery = searchQuery.value.toLowerCase()
  return plans.value.filter(plan => 
    plan.name.toLowerCase().includes(lowerQuery) || 
    (plan.code && plan.code.toLowerCase().includes(lowerQuery))
  )
})

const formatMoney = (amount: string | number) => {
  const val = Number(amount)
  if (val === 0) return 'Free'
  return `Rs ${val.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
}

const goToEdit = (id: number) => {
  router.push(`/admin/subscription-plans/${id}/edit`)
}
</script>
