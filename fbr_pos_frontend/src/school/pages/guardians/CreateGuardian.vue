<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <SchoolPageHeader
      title="Add Guardian"
      subtitle="Create a new parent or guardian record."
      backTo="/school/guardians"
    />

    <div class="p-8 flex-1 max-w-4xl mx-auto w-full">
      <SchoolFormCard>
        <div class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">First Name <span class="text-red-500">*</span></label>
              <input v-model="form.first_name" type="text" placeholder="e.g. John" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-sm" />
              <p v-if="errors.first_name" class="text-red-500 text-xs mt-1">{{ errors.first_name }}</p>
            </div>
            
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Last Name <span class="text-red-500">*</span></label>
              <input v-model="form.last_name" type="text" placeholder="e.g. Doe" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-sm" />
              <p v-if="errors.last_name" class="text-red-500 text-xs mt-1">{{ errors.last_name }}</p>
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Email</label>
              <input v-model="form.email" type="email" placeholder="guardian@example.com" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-sm" />
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Phone Number</label>
              <input v-model="form.phone_number" type="tel" placeholder="03XX-XXXXXXX" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-sm" />
            </div>

            <div class="col-span-1 md:col-span-2">
              <label class="block text-sm font-semibold text-gray-700 mb-1">CNIC</label>
              <input v-model="form.cnic" type="text" placeholder="00000-0000000-0" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-sm font-mono" />
            </div>

            <div class="col-span-1 md:col-span-2">
              <label class="block text-sm font-semibold text-gray-700 mb-1">Address</label>
              <textarea v-model="form.address" rows="3" placeholder="Residential address..." class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-sm resize-none"></textarea>
            </div>
          </div>

          <div v-if="serverError" class="bg-red-50 border border-red-200 text-red-700 text-sm rounded-xl px-4 py-3 flex items-start gap-3">
            <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            {{ serverError }}
          </div>

          <div class="flex justify-end gap-3 pt-6 border-t border-gray-100">
            <router-link to="/school/guardians" class="px-5 py-2.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 shadow-sm transition-colors">
              Cancel
            </router-link>
            <button @click="handleSubmit" :disabled="loading" class="px-6 py-2.5 text-sm font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 shadow-sm disabled:opacity-50 flex items-center gap-2 transition-colors">
              <div v-if="loading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              {{ loading ? 'Saving...' : 'Add Guardian' }}
            </button>
          </div>
        </div>
      </SchoolFormCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import SchoolPageHeader from '@/school/components/SchoolPageHeader.vue'
import SchoolFormCard from '@/school/components/SchoolFormCard.vue'
import { guardianAPI } from '@/school/apis/guardianAPI'

const router = useRouter()
const loading = ref(false)
const serverError = ref('')
const errors = ref<Record<string, string>>({})

const form = ref({ first_name: '', last_name: '', email: '', phone_number: '', cnic: '', address: '' })

const handleSubmit = async () => {
  errors.value = {}
  serverError.value = ''
  
  if (!form.value.first_name) errors.value.first_name = 'Required.'
  if (!form.value.last_name) errors.value.last_name = 'Required.'
  if (Object.keys(errors.value).length > 0) return

  loading.value = true
  try {
    await guardianAPI.create(form.value)
    router.push('/school/guardians')
  } catch (err: any) {
    const data = err.response?.data
    if (data && typeof data === 'object') {
      Object.entries(data).forEach(([k, v]: any) => { 
        errors.value[k] = Array.isArray(v) ? v.join(', ') : String(v) 
      })
    }
    serverError.value = data?.detail || 'Failed to create guardian.'
  } finally { 
    loading.value = false 
  }
}
</script>
