<template>
  <div class="min-h-screen bg-gray-50">

    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center h-96">
      <div class="text-center">
        <div class="w-12 h-12 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin mx-auto mb-4"></div>
        <p class="text-sm text-gray-500">Loading student profile...</p>
      </div>
    </div>

    <div v-else-if="error" class="p-8">
      <div class="bg-red-50 border border-red-200 text-red-700 rounded-xl px-6 py-4 text-sm">{{ error }}</div>
    </div>

    <template v-else-if="student">
      <!-- Hero Header -->
      <div class="bg-white border-b border-gray-200">
        <div class="px-8 py-6">
          <div class="flex items-center gap-3 mb-6">
            <router-link to="/school/students" class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100 transition-colors text-gray-400 hover:text-gray-700">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
            </router-link>
            <span class="text-sm text-gray-400">All Students</span>
            <svg class="w-4 h-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
            <span class="text-sm font-medium text-gray-700">{{ student.fullname }}</span>
          </div>

          <div class="flex items-start justify-between">
            <div class="flex items-center gap-6">
              <!-- Avatar -->
              <div class="relative">
                <div v-if="student.photo" class="w-20 h-20 rounded-2xl overflow-hidden ring-4 ring-white shadow-lg">
                  <img :src="student.photo" :alt="student.fullname" class="w-full h-full object-cover" />
                </div>
                <div v-else class="w-20 h-20 rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold text-3xl shadow-lg ring-4 ring-white">
                  {{ student.fullname.charAt(0).toUpperCase() }}
                </div>
                <span :class="student.status === 'active' ? 'bg-green-500' : 'bg-gray-400'" class="absolute -bottom-1 -right-1 w-4 h-4 rounded-full border-2 border-white"></span>
              </div>

              <div>
                <div class="flex items-center gap-3 mb-1">
                  <h1 class="text-2xl font-bold text-gray-900">{{ student.fullname }}</h1>
                  <span :class="student.status === 'active' ? 'bg-green-50 text-green-700 border-green-200' : 'bg-gray-100 text-gray-500 border-gray-200'" class="px-2.5 py-0.5 rounded-full text-xs font-bold border">
                    {{ student.status === 'active' ? 'Active' : 'Inactive' }}
                  </span>
                </div>
                <div class="flex items-center gap-4 text-sm text-gray-500">
                  <span class="flex items-center gap-1.5">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/></svg>
                    {{ student.registration_number || 'No Reg. #' }}
                  </span>
                  <span v-if="student.section_name" class="flex items-center gap-1.5">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5"/></svg>
                    {{ student.section_name }}
                  </span>
                  <span v-if="student.gender" class="capitalize">{{ student.gender }}</span>
                  <span v-if="student.date_of_birth">DOB: {{ student.date_of_birth }}</span>
                </div>
              </div>
            </div>

            <div class="flex items-center gap-3">
              <button @click="printProfile" class="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 shadow-sm transition-colors">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"/></svg>
                Print
              </button>
              <router-link :to="`/school/students/${student.id}/edit`" class="flex items-center gap-2 px-4 py-2 text-sm font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 shadow-sm transition-colors">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
                Edit Student
              </router-link>
            </div>
          </div>

          <!-- Stat Cards -->
          <div class="grid grid-cols-4 gap-4 mt-6">
            <div class="bg-indigo-50 rounded-xl p-4 border border-indigo-100">
              <p class="text-xs font-semibold text-indigo-600 uppercase tracking-wider mb-1">Total Invoices</p>
              <p class="text-2xl font-bold text-indigo-900">{{ invoices.length }}</p>
            </div>
            <div class="bg-green-50 rounded-xl p-4 border border-green-100">
              <p class="text-xs font-semibold text-green-600 uppercase tracking-wider mb-1">Paid Invoices</p>
              <p class="text-2xl font-bold text-green-900">{{ invoices.filter(i => i.payment_status === 'paid').length }}</p>
            </div>
            <div class="bg-amber-50 rounded-xl p-4 border border-amber-100">
              <p class="text-xs font-semibold text-amber-600 uppercase tracking-wider mb-1">Attendance Days</p>
              <p class="text-2xl font-bold text-amber-900">{{ attendance.filter(a => a.status === 'present').length }}</p>
            </div>
            <div class="bg-purple-50 rounded-xl p-4 border border-purple-100">
              <p class="text-xs font-semibold text-purple-600 uppercase tracking-wider mb-1">Exam Results</p>
              <p class="text-2xl font-bold text-purple-900">{{ examResults.length }}</p>
            </div>
          </div>

          <!-- Tabs -->
          <div class="flex gap-1 mt-6 -mb-px">
            <button v-for="tab in tabs" :key="tab.id" @click="activeTab = tab.id"
              :class="activeTab === tab.id ? 'border-indigo-600 text-indigo-700 bg-white' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
              class="flex items-center gap-2 px-5 py-3 text-sm font-semibold border-b-2 transition-all">
              <span>{{ tab.label }}</span>
              <span v-if="tab.count !== undefined" :class="activeTab === tab.id ? 'bg-indigo-100 text-indigo-700' : 'bg-gray-100 text-gray-500'" class="text-xs font-bold px-2 py-0.5 rounded-full">{{ tab.count }}</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Tab Content -->
      <div class="px-8 py-6">

        <!-- ==================== OVERVIEW TAB ==================== -->
        <div v-if="activeTab === 'overview'" class="grid grid-cols-3 gap-6">
          <!-- Personal Info -->
          <div class="col-span-2 space-y-6">
            <div class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
              <div class="px-6 py-4 border-b border-gray-100 bg-gray-50 flex items-center justify-between">
                <h3 class="font-bold text-gray-900">Personal Information</h3>
              </div>
              <div class="p-6 grid grid-cols-2 gap-6">
                <InfoField label="Full Name" :value="student.fullname" />
                <InfoField label="Registration #" :value="student.registration_number" />
                <InfoField label="Gender" :value="student.gender" capitalize />
                <InfoField label="Date of Birth" :value="student.date_of_birth" />
                <InfoField label="CNIC / B-Form" :value="student.cnic" />
                <InfoField label="Admission Date" :value="student.admission_date" />
                <InfoField label="Phone" :value="student.phone_number" />
                <InfoField label="Email" :value="student.email" />
                <div class="col-span-2">
                  <InfoField label="Address" :value="student.address" />
                </div>
              </div>
            </div>
          </div>

          <!-- Guardian Sidebar -->
          <div class="space-y-6">
            <div class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
              <div class="px-6 py-4 border-b border-gray-100 bg-gray-50 flex items-center justify-between">
                <h3 class="font-bold text-gray-900">Guardians</h3>
                <router-link to="/school/student-guardians/create" class="text-xs text-indigo-600 font-semibold hover:text-indigo-800">+ Add</router-link>
              </div>
              <div class="p-4">
                <div v-if="loadingGuardians" class="py-4 text-center text-sm text-gray-400">Loading...</div>
                <div v-else-if="guardians.length === 0" class="py-6 text-center">
                  <svg class="w-8 h-8 text-gray-200 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a4 4 0 00-5-3.87M9 20H4v-2a4 4 0 015-3.87"/></svg>
                  <p class="text-xs text-gray-400">No guardians linked yet</p>
                </div>
                <div v-else class="space-y-3">
                  <div v-for="g in guardians" :key="g.id" class="flex items-center gap-3 p-3 rounded-lg bg-gray-50 border border-gray-100">
                    <div class="w-9 h-9 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-700 font-bold text-sm flex-shrink-0">
                      {{ g.guardian_name?.charAt(0) || '?' }}
                    </div>
                    <div class="min-w-0">
                      <p class="text-sm font-semibold text-gray-900 truncate">{{ g.guardian_name }}</p>
                      <p class="text-xs text-gray-500 capitalize">{{ g.relationship }}</p>
                    </div>
                    <span v-if="g.is_primary_billing_contact" class="ml-auto text-[10px] bg-blue-100 text-blue-700 px-1.5 py-0.5 rounded font-bold">Billing</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ==================== ATTENDANCE TAB ==================== -->
        <div v-if="activeTab === 'attendance'">
          <div class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-100 bg-gray-50 flex items-center justify-between">
              <h3 class="font-bold text-gray-900">Attendance Records</h3>
              <div class="flex items-center gap-4">
                <span class="text-sm text-gray-500">Present: <span class="font-bold text-green-600">{{ attendance.filter(a => a.status === 'present').length }}</span></span>
                <span class="text-sm text-gray-500">Absent: <span class="font-bold text-red-600">{{ attendance.filter(a => a.status === 'absent').length }}</span></span>
              </div>
            </div>
            <div v-if="loadingAttendance" class="py-12 text-center text-gray-400">Loading attendance...</div>
            <div v-else-if="attendance.length === 0" class="py-16 text-center">
              <svg class="w-10 h-10 text-gray-200 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10"/></svg>
              <p class="text-sm text-gray-400">No attendance records found</p>
            </div>
            <div v-else class="divide-y divide-gray-100">
              <div v-for="rec in attendance" :key="rec.id" class="flex items-center justify-between px-6 py-4 hover:bg-gray-50">
                <span class="text-sm font-medium text-gray-900">{{ rec.date }}</span>
                <span :class="rec.status === 'present' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'" class="px-3 py-1 rounded-full text-xs font-bold capitalize">{{ rec.status }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- ==================== INVOICES TAB ==================== -->
        <div v-if="activeTab === 'invoices'">
          <div class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-100 bg-gray-50 flex items-center justify-between">
              <h3 class="font-bold text-gray-900">Fee Invoices</h3>
              <router-link to="/school/invoices/create" class="text-xs font-semibold text-indigo-600 hover:text-indigo-800 flex items-center gap-1">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
                New Invoice
              </router-link>
            </div>
            <div v-if="loadingInvoices" class="py-12 text-center text-gray-400">Loading invoices...</div>
            <div v-else-if="invoices.length === 0" class="py-16 text-center">
              <p class="text-sm text-gray-400">No invoices generated yet</p>
            </div>
            <table v-else class="min-w-full divide-y divide-gray-100">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase">Invoice #</th>
                  <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase">Date</th>
                  <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase">Amount</th>
                  <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase">Status</th>
                  <th class="px-6 py-3 text-right text-xs font-bold text-gray-500 uppercase">Action</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-for="inv in invoices" :key="inv.id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 text-sm font-mono text-gray-900">{{ inv.invoice_number || inv.id.slice(0,8) }}</td>
                  <td class="px-6 py-4 text-sm text-gray-600">{{ inv.invoice_date }}</td>
                  <td class="px-6 py-4 text-sm font-bold text-gray-900">Rs {{ Number(inv.total_payable_amount || 0).toLocaleString() }}</td>
                  <td class="px-6 py-4">
                    <span :class="{
                      'bg-green-100 text-green-700': inv.payment_status === 'paid',
                      'bg-yellow-100 text-yellow-700': inv.payment_status === 'partial',
                      'bg-red-100 text-red-700': inv.payment_status === 'unpaid'
                    }" class="px-2.5 py-1 rounded-full text-xs font-bold capitalize">{{ inv.payment_status }}</span>
                  </td>
                  <td class="px-6 py-4 text-right">
                    <router-link :to="`/school/invoices/${inv.id}`" class="text-indigo-600 hover:text-indigo-900 text-sm font-medium">View</router-link>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- ==================== EXAM RESULTS TAB ==================== -->
        <div v-if="activeTab === 'results'">
          <div class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-100 bg-gray-50">
              <h3 class="font-bold text-gray-900">Exam Results</h3>
            </div>
            <div v-if="loadingResults" class="py-12 text-center text-gray-400">Loading results...</div>
            <div v-else-if="examResults.length === 0" class="py-16 text-center">
              <p class="text-sm text-gray-400">No exam results recorded yet</p>
            </div>
            <table v-else class="min-w-full divide-y divide-gray-100">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase">Exam</th>
                  <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase">Subject</th>
                  <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase">Marks</th>
                  <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase">Grade</th>
                  <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase">Remarks</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-for="res in examResults" :key="res.id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 text-sm font-medium text-gray-900">{{ res.exam_name || '—' }}</td>
                  <td class="px-6 py-4 text-sm text-gray-600">{{ res.subject_name || '—' }}</td>
                  <td class="px-6 py-4 text-sm font-bold text-indigo-700">{{ res.marks_obtained }}</td>
                  <td class="px-6 py-4">
                    <span v-if="res.grade" class="px-2.5 py-1 rounded-lg text-xs font-bold bg-indigo-50 text-indigo-700 border border-indigo-100">{{ res.grade }}</span>
                    <span v-else class="text-gray-300">—</span>
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-500">{{ res.remarks || '—' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, defineComponent, h } from 'vue'
import { useRoute } from 'vue-router'
import { studentAPI, type Student } from '@/school/apis/studentAPI'
import { studentGuardianAPI } from '@/school/apis/studentGuardianAPI'
import { attendanceAPI } from '@/school/apis/attendanceAPI'
import { feeInvoiceAPI } from '@/school/apis/feeInvoiceAPI'
import { studentExamResultAPI } from '@/school/apis/studentExamResultAPI'

// ---- InfoField helper component ----
const InfoField = defineComponent({
  props: { label: String, value: String, capitalize: Boolean },
  setup(props) {
    return () => h('div', {}, [
      h('p', { class: 'text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1' }, props.label),
      h('p', { class: `text-sm font-medium text-gray-900 ${props.capitalize ? 'capitalize' : ''}` }, props.value || '—'),
    ])
  }
})

const route = useRoute()
const studentId = route.params.id as string
const activeTab = ref('overview')

const student = ref<Student | null>(null)
const loading = ref(true)
const error = ref('')

const guardians = ref<any[]>([])
const loadingGuardians = ref(false)

const attendance = ref<any[]>([])
const loadingAttendance = ref(false)

const invoices = ref<any[]>([])
const loadingInvoices = ref(false)

const examResults = ref<any[]>([])
const loadingResults = ref(false)

const tabs = computed(() => [
  { id: 'overview', label: 'Overview' },
  { id: 'attendance', label: 'Attendance', count: attendance.value.length },
  { id: 'invoices', label: 'Fee Invoices', count: invoices.value.length },
  { id: 'results', label: 'Exam Results', count: examResults.value.length },
])

onMounted(async () => {
  try {
    const res = await studentAPI.retrieve(studentId)
    student.value = res.data
  } catch {
    error.value = 'Failed to load student.'
  } finally {
    loading.value = false
  }

  // Load all related data in parallel
  loadingGuardians.value = true
  loadingAttendance.value = true
  loadingInvoices.value = true
  loadingResults.value = true

  const [guardRes, attRes, invRes, resRes] = await Promise.allSettled([
    studentGuardianAPI.list({ student_id: studentId, page_size: 50 }),
    attendanceAPI.list({ student_id: studentId, page_size: 200 }),
    feeInvoiceAPI.list({ student_id: studentId, page_size: 100 }),
    studentExamResultAPI.list({ student_id: studentId, page_size: 100 }),
  ])

  if (guardRes.status === 'fulfilled') guardians.value = guardRes.value.data.results || []
  if (attRes.status === 'fulfilled') attendance.value = attRes.value.data.results || []
  if (invRes.status === 'fulfilled') invoices.value = invRes.value.data.results || []
  if (resRes.status === 'fulfilled') examResults.value = resRes.value.data.results || []

  loadingGuardians.value = false
  loadingAttendance.value = false
  loadingInvoices.value = false
  loadingResults.value = false
})

const printProfile = () => window.print()
</script>
