<template>
  <div class="p-8 max-w-3xl">
    <div class="flex items-center gap-3 mb-6">
      <router-link to="/school/enrollments" class="text-gray-400 hover:text-gray-700"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg></router-link>
      <div><h1 class="text-2xl font-bold text-gray-900">Edit Enrollment</h1><p class="text-sm text-gray-500">Update enrollment details.</p></div>
    </div>

    <div v-if="pageLoading" class="flex items-center justify-center py-20"><div class="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div></div>

    <div v-else class="bg-white border border-gray-200 rounded-xl shadow-sm p-6 space-y-6">
      <div class="grid grid-cols-2 gap-5">
        <div class="col-span-2">
          <label class="block text-sm font-medium text-gray-700 mb-1">Student <span class="text-red-500">*</span></label>
          <select v-model="form.student_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <option v-for="stu in students" :key="stu.id" :value="stu.id">{{ stu.fullname }}</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Academic Session <span class="text-red-500">*</span></label>
          <select v-model="form.academic_session_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <option v-for="ses in sessions" :key="ses.id" :value="ses.id">{{ ses.name }}</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Grade <span class="text-red-500">*</span></label>
          <select v-model="form.grade_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <option v-for="g in grades" :key="g.id" :value="g.id">{{ g.name }}</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Section <span class="text-red-500">*</span></label>
          <select v-model="form.section_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <option v-for="sec in sections" :key="sec.id" :value="sec.id">{{ sec.name }}</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Status</label>
          <select v-model="form.status" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <option value="ongoing">Ongoing</option>
            <option value="promoted">Promoted</option>
            <option value="repeated">Repeated</option>
            <option value="left">Left</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Enrollment Date</label>
          <input v-model="form.enrollment_date" type="date" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Student Reg No (Optional)</label>
          <input v-model="form.student_registration_number" type="text" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>
      </div>

      <div v-if="serverError" class="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-4 py-3">{{ serverError }}</div>

      <div class="flex justify-end gap-3 pt-4">
        <router-link to="/school/enrollments" class="px-4 py-2 text-sm font-medium text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50">Cancel</router-link>
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
import { enrollmentAPI } from '@/school/apis/enrollmentAPI'
import { studentAPI, type Student } from '@/school/apis/studentAPI'
import { sectionAPI, type Section } from '@/school/apis/sectionAPI'
import { gradeAPI, type Grade } from '@/school/apis/gradeAPI'
import { academicSessionAPI, type AcademicSession } from '@/school/apis/academicSessionAPI'

const router = useRouter()
const route = useRoute()
const enrollmentId = route.params.id as string

const pageLoading = ref(true)
const loading = ref(false)
const serverError = ref('')
const errors = ref<Record<string, string>>({})

const form = ref({
  student_id: '',
  academic_session_id: '',
  grade_id: '',
  section_id: '',
  status: 'ongoing' as 'ongoing' | 'promoted' | 'repeated' | 'left',
  enrollment_date: '',
  student_registration_number: ''
})

const students = ref<Student[]>([])
const sessions = ref<AcademicSession[]>([])
const grades = ref<Grade[]>([])
const sections = ref<Section[]>([])

onMounted(async () => {
  try {
    const [enRes, stuRes, sesRes, grRes, secRes] = await Promise.all([
      enrollmentAPI.retrieve(enrollmentId),
      studentAPI.list(),
      academicSessionAPI.list(),
      gradeAPI.list(),
      sectionAPI.list()
    ])
    
    const e = enRes.data
    form.value = {
      student_id: e.student_id,
      academic_session_id: e.academic_session_id,
      grade_id: e.grade_id,
      section_id: e.section_id,
      status: e.status,
      enrollment_date: e.enrollment_date || '',
      student_registration_number: e.student_registration_number || ''
    }

    students.value = stuRes.data.results || (stuRes.data as any)
    sessions.value = sesRes.data.results || (sesRes.data as any)
    grades.value = grRes.data.results || (grRes.data as any)
    sections.value = secRes.data.results || (secRes.data as any)
  } catch {
    serverError.value = 'Failed to load enrollment data.'
  } finally {
    pageLoading.value = false
  }
})

const handleSubmit = async () => {
  errors.value = {}
  serverError.value = ''
  loading.value = true
  try {
    await enrollmentAPI.update(enrollmentId, form.value)
    router.push('/school/enrollments')
  } catch (err: any) {
    const data = err.response?.data
    if (data && typeof data === 'object') Object.entries(data).forEach(([k, v]: any) => { errors.value[k] = Array.isArray(v) ? v.join(', ') : v })
    serverError.value = data?.detail || 'Failed to update.'
  } finally { loading.value = false }
}
</script>
