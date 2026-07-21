<template>
  <div class="p-8 max-w-2xl">
    <div class="flex items-center gap-3 mb-6">
      <router-link to="/school/concessions" class="text-gray-400 hover:text-gray-700"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg></router-link>
      <div><h1 class="text-2xl font-bold text-gray-900">Add Concession</h1><p class="text-sm text-gray-500">Apply a fee discount to a student.</p></div>
    </div>

    <div class="bg-white border border-gray-200 rounded-xl shadow-sm p-6 space-y-5">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Student <span class="text-red-500">*</span></label>
        <select v-model="form.student_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
          <option value="">Select a student...</option>
          <option v-for="st in students" :key="st.id" :value="st.id">{{ st.first_name }} {{ st.last_name }} ({{ st.registration_number }})</option>
        </select>
        <p v-if="errors.student_id" class="text-red-500 text-xs mt-1">{{ errors.student_id }}</p>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Academic Session <span class="text-red-500">*</span></label>
          <select v-model="form.academic_session_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <option value="">Select session...</option>
            <option v-for="s in sessions" :key="s.id" :value="s.id">{{ s.name }}</option>
          </select>
          <p v-if="errors.academic_session_id" class="text-red-500 text-xs mt-1">{{ errors.academic_session_id }}</p>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Fee Head</label>
          <select v-model="form.fee_head_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <option value="">Global (All Heads)</option>
            <option v-for="fh in feeHeads" :key="fh.id" :value="fh.id">{{ fh.name }}</option>
          </select>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Concession Type <span class="text-red-500">*</span></label>
          <select v-model="form.concession_type" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <option value="percentage">Percentage (%)</option>
            <option value="fixed_amount">Fixed Amount (Rs)</option>
          </select>
        </div>
        <div v-if="form.concession_type === 'percentage'">
          <label class="block text-sm font-medium text-gray-700 mb-1">Percentage <span class="text-red-500">*</span></label>
          <input v-model.number="form.percentage" type="number" min="0" max="100" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>
        <div v-else>
          <label class="block text-sm font-medium text-gray-700 mb-1">Amount (Rs) <span class="text-red-500">*</span></label>
          <input v-model.number="form.amount" type="number" min="0" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Reason</label>
        <textarea v-model="form.reason" rows="2" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none"></textarea>
      </div>

      <div v-if="serverError" class="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-4 py-3">{{ serverError }}</div>

      <div class="flex justify-end gap-3 pt-2">
        <router-link to="/school/concessions" class="px-4 py-2 text-sm font-medium text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50">Cancel</router-link>
        <button @click="handleSubmit" :disabled="loading" class="px-5 py-2 text-sm font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 disabled:opacity-50 flex items-center gap-2">
          <div v-if="loading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          {{ loading ? 'Saving...' : 'Save Concession' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { studentFeeConcessionAPI } from '@/school/apis/studentFeeConcessionAPI'
import { studentAPI } from '@/school/apis/studentAPI'
import { academicSessionAPI } from '@/school/apis/academicSessionAPI'
import { feeHeadAPI } from '@/school/apis/feeHeadAPI'

const router = useRouter()
const loading = ref(false)
const serverError = ref('')
const errors = ref<Record<string, string>>({})

const form = ref({
  student_id: '',
  academic_session_id: '',
  fee_head_id: '',
  concession_type: 'percentage' as 'percentage' | 'fixed_amount',
  percentage: 0,
  amount: 0,
  reason: ''
})

const students = ref<any[]>([])
const sessions = ref<any[]>([])
const feeHeads = ref<any[]>([])

onMounted(async () => {
  try {
    const [stRes, sessRes, fhRes] = await Promise.all([
      studentAPI.list({ page_size: 100 }),
      academicSessionAPI.list({ page_size: 100 }),
      feeHeadAPI.list({ page_size: 100 })
    ])
    students.value = stRes.data.results
    sessions.value = sessRes.data.results
    feeHeads.value = fhRes.data.results
  } catch {
    serverError.value = 'Failed to load options.'
  }
})

const handleSubmit = async () => {
  errors.value = {}
  serverError.value = ''
  if (!form.value.student_id) errors.value.student_id = 'Required'
  if (!form.value.academic_session_id) errors.value.academic_session_id = 'Required'
  if (Object.keys(errors.value).length > 0) return

  loading.value = true
  try {
    const payload: any = { ...form.value }
    if (!payload.fee_head_id) delete payload.fee_head_id
    if (payload.concession_type === 'percentage') {
      payload.amount = 0
    } else {
      payload.percentage = 0
    }
    
    await studentFeeConcessionAPI.create(payload)
    router.push('/school/concessions')
  } catch (err: any) {
    serverError.value = err.response?.data?.detail || 'Failed to save.'
  } finally {
    loading.value = false
  }
}
</script>
