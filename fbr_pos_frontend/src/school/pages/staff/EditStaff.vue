<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <SchoolPageHeader
      title="Edit Staff Member"
      subtitle="Update teacher or administrative staff details."
      :backTo="`/school/staff/${staffId}`"
    />

    <div class="p-8 flex-1 max-w-4xl mx-auto w-full">
      <div v-if="pageLoading" class="flex items-center justify-center py-20">
        <div class="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
      </div>

      <SchoolFormCard v-else>
        <div class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="col-span-1 md:col-span-2">
              <label class="block text-sm font-semibold text-gray-700 mb-1">Full Name <span class="text-red-500">*</span></label>
              <input v-model="form.fullname" type="text" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-sm" />
              <p v-if="errors.fullname" class="text-red-500 text-xs mt-1">{{ errors.fullname }}</p>
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Email</label>
              <input v-model="form.email" type="email" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-sm" />
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Phone</label>
              <input v-model="form.phone_number" type="tel" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-sm" />
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">CNIC</label>
              <input v-model="form.cnic" type="text" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-sm" />
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Date of Birth</label>
              <input v-model="form.date_of_birth" type="date" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-sm bg-white" />
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Designation</label>
              <input v-model="form.designation" type="text" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-sm" />
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Date of Joining</label>
              <input v-model="form.date_of_joining" type="date" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-sm bg-white" />
            </div>
            
            <div class="col-span-1 md:col-span-2">
              <label class="block text-sm font-semibold text-gray-700 mb-1">Status</label>
              <select v-model="form.status" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-sm bg-white">
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
              </select>
            </div>

            <div class="col-span-1 md:col-span-2">
              <label class="block text-sm font-semibold text-gray-700 mb-1">Address</label>
              <textarea v-model="form.address" rows="3" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-sm resize-none"></textarea>
            </div>
          </div>

          <div v-if="serverError" class="bg-red-50 border border-red-200 text-red-700 text-sm rounded-xl px-4 py-3 flex items-start gap-3">
            <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            {{ serverError }}
          </div>

          <div class="flex justify-end gap-3 pt-6 border-t border-gray-100">
            <router-link :to="`/school/staff/${staffId}`" class="px-5 py-2.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 shadow-sm transition-colors">
              Cancel
            </router-link>
            <button @click="handleSubmit" :disabled="loading" class="px-6 py-2.5 text-sm font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 shadow-sm disabled:opacity-50 flex items-center gap-2 transition-colors">
              <div v-if="loading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              {{ loading ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </div>
      </SchoolFormCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import SchoolPageHeader from '@/school/components/SchoolPageHeader.vue'
import SchoolFormCard from '@/school/components/SchoolFormCard.vue'
import { staffAPI } from '@/school/apis/staffAPI'

const router = useRouter()
const route = useRoute()
const staffId = route.params.id as string

const pageLoading = ref(true)
const loading = ref(false)
const serverError = ref('')
const errors = ref<Record<string, string>>({})

const form = ref({
  fullname: '',
  email: '',
  phone_number: '',
  cnic: '',
  date_of_birth: '',
  designation: '',
  date_of_joining: '',
  address: '',
  status: 'active' as 'active' | 'inactive',
})

onMounted(async () => {
  try {
    const res = await staffAPI.retrieve(staffId)
    const s = res.data
    form.value = {
      fullname: s.fullname,
      email: s.email || '',
      phone_number: s.phone_number || '',
      cnic: s.cnic || '',
      date_of_birth: s.date_of_birth || '',
      designation: s.designation || '',
      date_of_joining: s.date_of_joining || '',
      address: s.address || '',
      status: s.status,
    }
  } catch {
    serverError.value = 'Failed to load staff member.'
  } finally {
    pageLoading.value = false
  }
})

const handleSubmit = async () => {
  errors.value = {}
  serverError.value = ''
  
  if (!form.value.fullname) {
    errors.value.fullname = 'Full name is required.'
    return
  }
  
  loading.value = true
  try {
    const payload = { ...form.value }
    if (!payload.date_of_birth) delete (payload as any).date_of_birth
    if (!payload.date_of_joining) delete (payload as any).date_of_joining
    
    await staffAPI.update(staffId, payload)
    router.push(`/school/staff/${staffId}`)
  } catch (err: any) {
    const data = err.response?.data
    if (data && typeof data === 'object') {
      Object.entries(data).forEach(([k, v]: any) => {
        errors.value[k] = Array.isArray(v) ? v.join(', ') : String(v)
      })
    }
    serverError.value = data?.detail || 'Failed to update staff member.'
  } finally {
    loading.value = false
  }
}
</script>
