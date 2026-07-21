<template>
  <div class="p-8 max-w-2xl mx-auto">
    <div class="flex items-center gap-3 mb-6">
      <router-link to="/school/attendance" class="text-gray-400 hover:text-gray-700"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg></router-link>
      <div><h1 class="text-2xl font-bold text-gray-900">Mark Attendance</h1><p class="text-sm text-gray-500">Record a student's daily attendance.</p></div>
    </div>

    <div class="bg-white border border-gray-200 rounded-xl shadow-sm p-6 space-y-5">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Student <span class="text-red-500">*</span></label>
        <select v-model="form.student_id" @change="autoSelectEnrollment" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
          <option value="">Select a student...</option>
          <option v-for="st in students" :key="st.id" :value="st.id">{{ st.first_name }} {{ st.last_name }} ({{ st.registration_number }})</option>
        </select>
        <p v-if="errors.student_id" class="text-red-500 text-xs mt-1">{{ errors.student_id }}</p>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Date <span class="text-red-500">*</span></label>
          <input v-model="form.date" type="date" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          <p v-if="errors.date" class="text-red-500 text-xs mt-1">{{ errors.date }}</p>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Status <span class="text-red-500">*</span></label>
          <select v-model="form.status" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <option value="present">Present</option>
            <option value="absent">Absent</option>
          </select>
        </div>
      </div>

      <div v-if="serverError" class="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-4 py-3">{{ serverError }}</div>

      <div class="flex justify-end gap-3 pt-2">
        <router-link to="/school/attendance" class="px-4 py-2 text-sm font-medium text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50">Cancel</router-link>
        <button @click="handleSubmit" :disabled="loading" class="px-5 py-2 text-sm font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 disabled:opacity-50 flex items-center gap-2">
          <div v-if="loading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          {{ loading ? 'Saving...' : 'Save Record' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { attendanceAPI } from '@/school/apis/attendanceAPI'
import { studentAPI } from '@/school/apis/studentAPI'
import { enrollmentAPI } from '@/school/apis/enrollmentAPI'

const router = useRouter()
const loading = ref(false)
const serverError = ref('')
const errors = ref<Record<string, string>>({})

const today = new Date().toISOString().split('T')[0]

const form = ref({
  student_id: '',
  date: today,
  status: 'present' as 'present' | 'absent',
  enrollement_id: ''
})

const students = ref<any[]>([])
const enrollments = ref<any[]>([])

onMounted(async () => {
  try {
    const [stRes, enRes] = await Promise.all([
      studentAPI.list({ page_size: 200 }),
      enrollmentAPI.list({ page_size: 500 })
    ])
    students.value = stRes.data.results
    enrollments.value = enRes.data.results
  } catch {
    serverError.value = 'Failed to load options.'
  }
})

const autoSelectEnrollment = () => {
  const enrollment = enrollments.value.find(e => e.student_id === form.value.student_id && e.status === 'active')
  if (enrollment) {
    form.value.enrollement_id = enrollment.id
  } else {
    form.value.enrollement_id = ''
  }
}

const handleSubmit = async () => {
  errors.value = {}
  serverError.value = ''
  if (!form.value.student_id) errors.value.student_id = 'Required'
  if (!form.value.date) errors.value.date = 'Required'
  
  if (!form.value.enrollement_id) {
    serverError.value = 'Student must have an active enrollment to mark attendance.'
    return
  }

  if (Object.keys(errors.value).length > 0) return

  loading.value = true
  try {
    await attendanceAPI.create(form.value)
    router.push('/school/attendance')
  } catch (err: any) {
    serverError.value = err.response?.data?.detail || 'Failed to save.'
  } finally {
    loading.value = false
  }
}
</script>
