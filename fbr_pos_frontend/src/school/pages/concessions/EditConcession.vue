<template>
  <div class="p-8 max-w-2xl">
    <div class="flex items-center gap-3 mb-6">
      <router-link to="/school/concessions" class="text-gray-400 hover:text-gray-700"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg></router-link>
      <div><h1 class="text-2xl font-bold text-gray-900">Edit Concession</h1><p class="text-sm text-gray-500">Update fee discount details.</p></div>
    </div>

    <div v-if="loadingInitial" class="bg-white border border-gray-200 rounded-xl shadow-sm p-12 text-center text-gray-500">
      Loading...
    </div>

    <div v-else class="bg-white border border-gray-200 rounded-xl shadow-sm p-6 space-y-5">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Student</label>
        <div class="px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700">
          {{ initialData?.student_name }}
        </div>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Academic Session</label>
          <select v-model="form.academic_session_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <option v-for="s in sessions" :key="s.id" :value="s.id">{{ s.name }}</option>
          </select>
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
          {{ loading ? 'Saving...' : 'Save Changes' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { studentFeeConcessionAPI } from '@/school/apis/studentFeeConcessionAPI'
import { academicSessionAPI } from '@/school/apis/academicSessionAPI'
import { feeHeadAPI } from '@/school/apis/feeHeadAPI'

const router = useRouter()
const route = useRoute()
const loadingInitial = ref(true)
const loading = ref(false)
const serverError = ref('')
const initialData = ref<any>(null)

const form = ref({
  academic_session_id: '',
  fee_head_id: '',
  concession_type: 'percentage' as 'percentage' | 'fixed_amount',
  percentage: 0,
  amount: 0,
  reason: ''
})

const sessions = ref<any[]>([])
const feeHeads = ref<any[]>([])

onMounted(async () => {
  try {
    const [sessRes, fhRes, itemRes] = await Promise.all([
      academicSessionAPI.list({ page_size: 100 }),
      feeHeadAPI.list({ page_size: 100 }),
      studentFeeConcessionAPI.retrieve(route.params.id as string)
    ])
    sessions.value = sessRes.data.results
    feeHeads.value = fhRes.data.results
    initialData.value = itemRes.data
    
    form.value = {
      academic_session_id: itemRes.data.academic_session_id,
      fee_head_id: itemRes.data.fee_head_id || '',
      concession_type: itemRes.data.concession_type,
      percentage: parseFloat(itemRes.data.percentage || '0'),
      amount: parseFloat(itemRes.data.amount || '0'),
      reason: itemRes.data.reason || ''
    }
  } catch {
    serverError.value = 'Failed to load data.'
  } finally {
    loadingInitial.value = false
  }
})

const handleSubmit = async () => {
  serverError.value = ''
  loading.value = true
  try {
    const payload: any = { ...form.value }
    if (!payload.fee_head_id) payload.fee_head_id = null
    if (payload.concession_type === 'percentage') {
      payload.amount = 0
    } else {
      payload.percentage = 0
    }
    
    await studentFeeConcessionAPI.update(route.params.id as string, payload)
    router.push('/school/concessions')
  } catch (err: any) {
    serverError.value = err.response?.data?.detail || 'Failed to update.'
  } finally {
    loading.value = false
  }
}
</script>
