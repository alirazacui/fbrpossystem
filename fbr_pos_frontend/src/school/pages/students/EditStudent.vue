<template>
  <div class="p-8 max-w-3xl">
    <div class="flex items-center gap-3 mb-6">
      <router-link to="/school/students" class="text-gray-400 hover:text-gray-700"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg></router-link>
      <div><h1 class="text-2xl font-bold text-gray-900">Edit Student</h1><p class="text-sm text-gray-500">Update student information.</p></div>
    </div>

    <div v-if="pageLoading" class="flex items-center justify-center py-20"><div class="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div></div>

    <div v-else class="bg-white border border-gray-200 rounded-xl shadow-sm p-6 space-y-6">
      <div class="grid grid-cols-2 gap-5">
        <div class="col-span-2">
          <label class="block text-sm font-medium text-gray-700 mb-1">Full Name <span class="text-red-500">*</span></label>
          <input v-model="form.fullname" type="text" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          <p v-if="errors.fullname" class="text-red-500 text-xs mt-1">{{ errors.fullname }}</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Registration Number</label>
          <input v-model="form.registration_number" type="text" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Current Section</label>
          <select v-model="form.current_section_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <option value="">Unassigned</option>
            <option v-for="sec in sections" :key="sec.id" :value="sec.id">{{ sec.name }} ({{ sec.grade_name || 'N/A' }})</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Gender</label>
          <select v-model="form.gender" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <option value="">Select Gender</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Date of Birth</label>
          <input v-model="form.date_of_birth" type="date" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Admission Date</label>
          <input v-model="form.admission_date" type="date" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Status</label>
          <select v-model="form.status" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
          </select>
        </div>
      </div>

      <hr class="border-gray-100" />

      <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider">Contact Info</h3>
      
      <div class="grid grid-cols-2 gap-5">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input v-model="form.email" type="email" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Phone Number</label>
          <input v-model="form.phone_number" type="tel" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">CNIC (B-Form)</label>
          <input v-model="form.cnic" type="text" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>

        <div class="col-span-2">
          <label class="block text-sm font-medium text-gray-700 mb-1">Address</label>
          <textarea v-model="form.address" rows="2" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none"></textarea>
        </div>
      </div>

      <div v-if="serverError" class="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-4 py-3">{{ serverError }}</div>

      <div class="flex justify-end gap-3 pt-4">
        <router-link :to="`/school/students/${studentId}`" class="px-4 py-2 text-sm font-medium text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50">Cancel</router-link>
        <button @click="handleSubmit" :disabled="loading" class="px-5 py-2 text-sm font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 disabled:opacity-50 flex items-center gap-2">
          <div v-if="loading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          {{ loading ? 'Saving...' : 'Save Changes' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { studentAPI } from '@/school/apis/studentAPI'
import { sectionAPI, type Section } from '@/school/apis/sectionAPI'

const router = useRouter()
const route = useRoute()
const studentId = route.params.id as string

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
  gender: '' as 'male' | 'female' | '',
  registration_number: '',
  admission_date: '',
  current_section_id: '',
  address: '',
  status: 'active' as 'active' | 'inactive'
})

const sections = ref<Section[]>([])

onMounted(async () => {
  try {
    const [stuRes, secRes] = await Promise.all([
      studentAPI.retrieve(studentId),
      sectionAPI.list()
    ])
    
    const s = stuRes.data
    form.value = {
      fullname: s.fullname,
      email: s.email || '',
      phone_number: s.phone_number || '',
      cnic: s.cnic || '',
      date_of_birth: s.date_of_birth || '',
      gender: s.gender || '',
      registration_number: s.registration_number || '',
      admission_date: s.admission_date || '',
      current_section_id: s.current_section_id || '',
      address: s.address || '',
      status: s.status
    }
    
    sections.value = secRes.data.results || (secRes.data as any)
  } catch {
    serverError.value = 'Failed to load data.'
  } finally {
    pageLoading.value = false
  }
})

const handleSubmit = async () => {
  errors.value = {}
  serverError.value = ''
  if (!form.value.fullname) errors.value.fullname = 'Required.'
  if (Object.keys(errors.value).length > 0) return

  loading.value = true
  try {
    const payload = { ...form.value }
    if (!payload.current_section_id) delete (payload as any).current_section_id
    if (!payload.gender) delete (payload as any).gender
    if (!payload.date_of_birth) delete (payload as any).date_of_birth
    if (!payload.admission_date) delete (payload as any).admission_date

    await studentAPI.update(studentId, payload as any)
    router.push(`/school/students/${studentId}`)
  } catch (err: any) {
    const data = err.response?.data
    if (data && typeof data === 'object') Object.entries(data).forEach(([k, v]: any) => { errors.value[k] = Array.isArray(v) ? v.join(', ') : v })
    serverError.value = data?.detail || 'Failed to update student.'
  } finally { loading.value = false }
}
</script>
