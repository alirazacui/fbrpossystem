<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <!-- Header -->
    <div class="bg-white border-b border-gray-200 px-8 py-6 flex-shrink-0">
      <div class="flex items-center gap-3 mb-1">
        <router-link to="/school/attendance" class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100 transition-colors text-gray-400 hover:text-gray-700">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
        </router-link>
        <span class="text-sm text-gray-400">Attendance</span>
        <svg class="w-4 h-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
        <span class="text-sm font-medium text-gray-700">Class Register</span>
      </div>
      <div class="flex items-center justify-between mt-4">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Daily Class Register</h1>
          <p class="text-sm text-gray-500 mt-0.5">Quickly mark attendance for an entire class section.</p>
        </div>
        <div class="flex items-center gap-3">
          <router-link to="/school/attendance" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 shadow-sm transition-colors">
            Cancel
          </router-link>
          <button @click="handleSubmit" :disabled="loading || students.length === 0" class="px-6 py-2 text-sm font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 shadow-sm disabled:opacity-50 flex items-center gap-2 transition-colors">
            <div v-if="loading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
            {{ loading ? 'Saving...' : 'Save Register' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="flex-1 p-8">
      <div class="max-w-5xl mx-auto space-y-6">
        
        <!-- Filters -->
        <div class="bg-white border border-gray-200 rounded-xl shadow-sm p-6 grid grid-cols-3 gap-6">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Select Date <span class="text-red-500">*</span></label>
            <input v-model="form.date" type="date" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500" />
          </div>
          <div class="col-span-2">
            <label class="block text-sm font-semibold text-gray-700 mb-2">Select Class Section <span class="text-red-500">*</span></label>
            <select v-model="form.section_id" @change="fetchStudents" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 bg-white">
              <option value="">-- Choose a Section --</option>
              <option v-for="sec in sections" :key="sec.id" :value="sec.id">{{ sec.name }} {{ sec.grade_name ? `(${sec.grade_name})` : '' }}</option>
            </select>
          </div>
        </div>

        <div v-if="serverError" class="bg-red-50 border border-red-200 text-red-700 text-sm rounded-xl px-5 py-4 flex items-start gap-3 shadow-sm">
          <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          {{ serverError }}
        </div>

        <!-- Student Grid -->
        <div v-if="form.section_id" class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-100 bg-gray-50 flex items-center justify-between">
            <h2 class="font-bold text-gray-900">Student Roster</h2>
            
            <!-- Bulk Actions -->
            <div class="flex gap-2" v-if="students.length > 0">
              <button @click="markAll('present')" class="px-3 py-1.5 text-xs font-semibold text-green-700 bg-green-100 rounded-lg hover:bg-green-200 transition-colors">Mark All Present</button>
              <button @click="markAll('absent')" class="px-3 py-1.5 text-xs font-semibold text-red-700 bg-red-100 rounded-lg hover:bg-red-200 transition-colors">Mark All Absent</button>
            </div>
          </div>

          <!-- Loading State -->
          <div v-if="fetchingStudents" class="p-12 text-center">
            <div class="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin mx-auto mb-4"></div>
            <p class="text-sm text-gray-500">Loading roster...</p>
          </div>

          <!-- Empty State -->
          <div v-else-if="students.length === 0" class="p-16 text-center">
             <svg class="w-12 h-12 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/></svg>
            <h3 class="text-base font-semibold text-gray-700 mb-1">No active enrollments</h3>
            <p class="text-sm text-gray-400">There are no students actively enrolled in this section.</p>
          </div>

          <!-- Table -->
          <div v-else>
            <table class="w-full text-sm">
              <thead class="bg-gray-50 border-b border-gray-100">
                <tr>
                  <th class="text-left px-6 py-3 font-bold text-gray-500 uppercase tracking-wider text-xs">Student Name</th>
                  <th class="text-left px-6 py-3 font-bold text-gray-500 uppercase tracking-wider text-xs">Registration #</th>
                  <th class="text-center px-6 py-3 font-bold text-gray-500 uppercase tracking-wider text-xs">Attendance Status</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-for="(student, index) in students" :key="student.id" class="hover:bg-gray-50 transition-colors">
                  <td class="px-6 py-4">
                    <div class="flex items-center gap-3">
                      <div class="w-8 h-8 rounded-full bg-indigo-100 text-indigo-700 flex items-center justify-center font-bold text-xs">
                        {{ student.student_name ? student.student_name.charAt(0).toUpperCase() : '?' }}
                      </div>
                      <span class="font-semibold text-gray-900">{{ student.student_name || 'Unknown Student' }}</span>
                    </div>
                  </td>
                  <td class="px-6 py-4 text-gray-500 font-mono text-xs">
                    {{ student.student_registration_number || '—' }}
                  </td>
                  <td class="px-6 py-4">
                    <div class="flex items-center justify-center gap-2">
                      <label class="cursor-pointer relative">
                        <input type="radio" :name="`status-${index}`" value="present" v-model="student.attendance_status" class="peer sr-only" />
                        <div class="px-4 py-1.5 rounded-l-lg border border-gray-200 text-sm font-medium text-gray-600 peer-checked:bg-green-500 peer-checked:text-white peer-checked:border-green-600 transition-all">Present</div>
                      </label>
                      <label class="cursor-pointer relative -ml-3">
                        <input type="radio" :name="`status-${index}`" value="absent" v-model="student.attendance_status" class="peer sr-only" />
                        <div class="px-4 py-1.5 rounded-r-lg border border-gray-200 border-l-0 text-sm font-medium text-gray-600 peer-checked:bg-red-500 peer-checked:text-white peer-checked:border-red-600 peer-checked:border-l peer-checked:-ml-px transition-all">Absent</div>
                      </label>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { attendanceAPI } from '@/school/apis/attendanceAPI'
import { sectionAPI, type Section } from '@/school/apis/sectionAPI'
import { enrollmentAPI, type Enrollment } from '@/school/apis/enrollmentAPI'

interface GridStudent extends Enrollment {
  attendance_status: 'present' | 'absent'
}

const router = useRouter()
const loading = ref(false)
const fetchingStudents = ref(false)
const serverError = ref('')

const form = ref({
  date: new Date().toISOString().split('T')[0],
  section_id: '',
})

const sections = ref<Section[]>([])
const students = ref<GridStudent[]>([])

onMounted(async () => {
  try {
    const secRes = await sectionAPI.list({ page_size: 100 })
    sections.value = secRes.data.results || (secRes.data as any)
  } catch {
    serverError.value = 'Failed to load sections.'
  }
})

const fetchStudents = async () => {
  if (!form.value.section_id) {
    students.value = []
    return
  }
  
  fetchingStudents.value = true
  serverError.value = ''
  try {
    const res = await enrollmentAPI.list({ 
      section_id: form.value.section_id, 
      status: 'ongoing',
      page_size: 500 
    })
    
    const enrollments = res.data.results || (res.data as any)
    
    // Map enrollments to our grid model, defaulting to present
    students.value = enrollments.map((e: Enrollment) => ({
      ...e,
      attendance_status: 'present'
    }))
    
  } catch (err) {
    serverError.value = 'Failed to fetch student roster.'
  } finally {
    fetchingStudents.value = false
  }
}

const markAll = (status: 'present' | 'absent') => {
  students.value.forEach(s => s.attendance_status = status)
}

const handleSubmit = async () => {
  if (!form.value.date || !form.value.section_id) {
    serverError.value = 'Date and Section are required.'
    return
  }
  
  if (students.value.length === 0) return
  
  loading.value = true
  serverError.value = ''
  
  try {
    const payload = {
      date: form.value.date,
      section_id: form.value.section_id,
      attendances: students.value.map(s => ({
        student_id: s.student_id,
        enrollment_id: s.id,
        status: s.attendance_status
      }))
    }
    
    await attendanceAPI.bulkMark(payload)
    router.push('/school/attendance')
  } catch (err: any) {
    serverError.value = err.response?.data?.detail || 'Failed to save attendance.'
  } finally {
    loading.value = false
  }
}
</script>
