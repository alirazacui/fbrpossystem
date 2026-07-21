<template>
  <div class="p-8 max-w-3xl">
    <div class="flex items-center gap-3 mb-6">
      <router-link to="/school/invoices" class="text-gray-400 hover:text-gray-700"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg></router-link>
      <div><h1 class="text-2xl font-bold text-gray-900">Generate Invoice</h1><p class="text-sm text-gray-500">Create a manual fee invoice for a student.</p></div>
    </div>

    <div class="bg-white border border-gray-200 rounded-xl shadow-sm p-6 space-y-6">
      <div class="grid grid-cols-2 gap-5">
        <div class="col-span-2">
          <label class="block text-sm font-medium text-gray-700 mb-1">Student <span class="text-red-500">*</span></label>
          <select v-model="form.student_id" @change="onStudentChange" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <option value="" disabled>Select Student</option>
            <option v-for="stu in students" :key="stu.id" :value="stu.id">{{ stu.fullname }}</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Fee Structure <span class="text-red-500">*</span></label>
          <select v-model="form.fee_structure_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <option value="" disabled>Select Fee Structure</option>
            <option v-for="fs in feeStructures" :key="fs.id" :value="fs.id">{{ fs.name }}</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Enrollment Record <span class="text-red-500">*</span></label>
          <select v-model="form.enrollement_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <option value="" disabled>Select Enrollment</option>
            <option v-for="e in enrollments" :key="e.id" :value="e.id">{{ e.session_name }} - {{ e.grade_name }}</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Invoice Date</label>
          <input v-model="form.invoice_date" type="date" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Due Date</label>
          <input v-model="form.due_date" type="date" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Total Amount <span class="text-red-500">*</span></label>
          <input v-model.number="form.total_amount" type="number" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Concession Amount</label>
          <input v-model.number="form.total_concession_amount" type="number" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>

        <div class="col-span-2">
          <label class="block text-sm font-medium text-gray-700 mb-1">Total Payable Amount <span class="text-red-500">*</span></label>
          <input v-model.number="form.total_payable_amount" type="number" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-gray-50" readonly />
          <p class="text-xs text-gray-500 mt-1">Calculated automatically (Total - Concession)</p>
        </div>
      </div>

      <div v-if="serverError" class="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-4 py-3">{{ serverError }}</div>

      <div class="flex justify-end gap-3 pt-4">
        <router-link to="/school/invoices" class="px-4 py-2 text-sm font-medium text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50">Cancel</router-link>
        <button @click="handleSubmit" :disabled="loading" class="px-5 py-2 text-sm font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 disabled:opacity-50 flex items-center gap-2">
          <div v-if="loading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          {{ loading ? 'Generating...' : 'Generate Invoice' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { feeInvoiceAPI } from '@/school/apis/feeInvoiceAPI'
import { studentAPI, type Student } from '@/school/apis/studentAPI'
import { feeStructureAPI, type FeeStructure } from '@/school/apis/feeStructureAPI'
import { enrollmentAPI, type Enrollment } from '@/school/apis/enrollmentAPI'

const router = useRouter()
const loading = ref(false)
const serverError = ref('')

const form = ref({
  student_id: '',
  fee_structure_id: '',
  enrollement_id: '',
  academic_session_id: '',
  grade_id: '',
  invoice_date: new Date().toISOString().split('T')[0],
  due_date: '',
  total_amount: 0,
  total_concession_amount: 0,
  total_payable_amount: 0
})

const students = ref<Student[]>([])
const feeStructures = ref<FeeStructure[]>([])
const allEnrollments = ref<Enrollment[]>([])
const enrollments = ref<Enrollment[]>([])

onMounted(async () => {
  try {
    const [stuRes, fsRes, enRes] = await Promise.all([
      studentAPI.list(),
      feeStructureAPI.list(),
      enrollmentAPI.list()
    ])
    students.value = stuRes.data.results || (stuRes.data as any)
    feeStructures.value = fsRes.data.results || (fsRes.data as any)
    allEnrollments.value = enRes.data.results || (enRes.data as any)
  } catch {
    serverError.value = 'Failed to load form data.'
  }
})

const onStudentChange = () => {
  enrollments.value = allEnrollments.value.filter(e => e.student_id === form.value.student_id)
  form.value.enrollement_id = ''
}

watch(() => [form.value.total_amount, form.value.total_concession_amount], ([tot, con]) => {
  form.value.total_payable_amount = Math.max(0, Number(tot) - Number(con))
})

const handleSubmit = async () => {
  serverError.value = ''
  if (!form.value.student_id || !form.value.fee_structure_id || !form.value.enrollement_id) {
    serverError.value = 'Please fill all required fields.'
    return
  }

  // Find enrollment to extract session and grade
  const selectedEnrollment = enrollments.value.find(e => e.id === form.value.enrollement_id)
  if (selectedEnrollment) {
    form.value.academic_session_id = selectedEnrollment.academic_session_id
    form.value.grade_id = selectedEnrollment.grade_id
  }

  loading.value = true
  try {
    const payload = { ...form.value }
    if (!payload.due_date) delete (payload as any).due_date
    const res = await feeInvoiceAPI.create(payload)
    router.push(`/school/invoices/${res.data.id}`)
  } catch (err: any) {
    serverError.value = err.response?.data?.detail || 'Failed to generate invoice.'
  } finally { loading.value = false }
}
</script>
