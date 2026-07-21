<template>
  <div class="p-8 max-w-2xl">
    <div class="flex items-center gap-3 mb-6">
      <router-link to="/school/student-guardians" class="text-gray-400 hover:text-gray-700"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg></router-link>
      <div><h1 class="text-2xl font-bold text-gray-900">Link Guardian</h1><p class="text-sm text-gray-500">Associate a student with a guardian.</p></div>
    </div>

    <div class="bg-white border border-gray-200 rounded-xl shadow-sm p-6 space-y-5">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Student <span class="text-red-500">*</span></label>
        <select v-model="form.student_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
          <option value="" disabled>Select Student</option>
          <option v-for="stu in students" :key="stu.id" :value="stu.id">{{ stu.fullname }} ({{ stu.registration_number || 'No Reg' }})</option>
        </select>
        <p v-if="errors.student_id" class="text-red-500 text-xs mt-1">{{ errors.student_id }}</p>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Guardian <span class="text-red-500">*</span></label>
        <select v-model="form.guardian_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
          <option value="" disabled>Select Guardian</option>
          <option v-for="g in guardians" :key="g.id" :value="g.id">{{ g.first_name }} {{ g.last_name }} ({{ g.phone_number || 'No Phone' }})</option>
        </select>
        <p v-if="errors.guardian_id" class="text-red-500 text-xs mt-1">{{ errors.guardian_id }}</p>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Relationship</label>
        <input v-model="form.relation" type="text" placeholder="e.g. Father, Mother, Uncle" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
      </div>

      <div class="flex items-center gap-2 mt-2">
        <input type="checkbox" id="billing" v-model="form.is_primary_billing_contact" class="w-4 h-4 accent-indigo-600 rounded border-gray-300" />
        <label for="billing" class="text-sm text-gray-700 cursor-pointer">Primary Billing Contact</label>
      </div>

      <div v-if="serverError" class="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-4 py-3">{{ serverError }}</div>

      <div class="flex justify-end gap-3 pt-4">
        <router-link to="/school/student-guardians" class="px-4 py-2 text-sm font-medium text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50">Cancel</router-link>
        <button @click="handleSubmit" :disabled="loading" class="px-5 py-2 text-sm font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 disabled:opacity-50 flex items-center gap-2">
          <div v-if="loading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          {{ loading ? 'Saving...' : 'Link Guardian' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { studentGuardianAPI } from '@/school/apis/studentGuardianAPI'
import { studentAPI, type Student } from '@/school/apis/studentAPI'
import { guardianAPI, type Guardian } from '@/school/apis/guardianAPI'

const router = useRouter()
const loading = ref(false)
const serverError = ref('')
const errors = ref<Record<string, string>>({})

const form = ref({ student_id: '', guardian_id: '', relation: '', is_primary_billing_contact: false })

const students = ref<Student[]>([])
const guardians = ref<Guardian[]>([])

onMounted(async () => {
  try {
    const [stuRes, grdRes] = await Promise.all([
      studentAPI.list(),
      guardianAPI.list()
    ])
    students.value = stuRes.data.results || (stuRes.data as any)
    guardians.value = grdRes.data.results || (grdRes.data as any)
  } catch {
    serverError.value = 'Failed to load form data.'
  }
})

const handleSubmit = async () => {
  errors.value = {}
  serverError.value = ''
  if (!form.value.student_id) errors.value.student_id = 'Required.'
  if (!form.value.guardian_id) errors.value.guardian_id = 'Required.'
  if (Object.keys(errors.value).length > 0) return

  loading.value = true
  try {
    await studentGuardianAPI.create(form.value)
    router.push('/school/student-guardians')
  } catch (err: any) {
    const data = err.response?.data
    if (data && typeof data === 'object') Object.entries(data).forEach(([k, v]: any) => { errors.value[k] = Array.isArray(v) ? v.join(', ') : v })
    serverError.value = data?.detail || 'Failed to create link.'
  } finally { loading.value = false }
}
</script>
