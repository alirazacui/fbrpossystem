<template>
  <div class="p-8 max-w-3xl">
    <div class="flex items-center gap-3 mb-6">
      <router-link to="/school/enrollments" class="text-gray-400 hover:text-gray-700"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg></router-link>
      <div><h1 class="text-2xl font-bold text-gray-900">New Enrollment</h1><p class="text-sm text-gray-500">Enroll a student in a session and section.</p></div>
    </div>

    <div class="bg-white border border-gray-200 rounded-xl shadow-sm p-6 space-y-6">
      <div class="grid grid-cols-2 gap-5">
        <div class="col-span-2">
          <label class="block text-sm font-medium text-gray-700 mb-1">Student <span class="text-red-500">*</span></label>
          <select v-model="form.student_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <option value="" disabled>Select Student</option>
            <option v-for="stu in students" :key="stu.id" :value="stu.id">{{ stu.fullname }}</option>
          </select>
          <p v-if="errors.student_id" class="text-red-500 text-xs mt-1">{{ errors.student_id }}</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Academic Session <span class="text-red-500">*</span></label>
          <select v-model="form.academic_session_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <option value="" disabled>Select Session</option>
            <option v-for="ses in sessions" :key="ses.id" :value="ses.id">{{ ses.name }}</option>
          </select>
          <p v-if="errors.academic_session_id" class="text-red-500 text-xs mt-1">{{ errors.academic_session_id }}</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Grade <span class="text-red-500">*</span></label>
          <select v-model="form.grade_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <option value="" disabled>Select Grade</option>
            <option v-for="g in grades" :key="g.id" :value="g.id">{{ g.name }}</option>
          </select>
          <p v-if="errors.grade_id" class="text-red-500 text-xs mt-1">{{ errors.grade_id }}</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Section <span class="text-red-500">*</span></label>
          <select v-model="form.section_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <option value="" disabled>Select Section</option>
            <option v-for="sec in sections" :key="sec.id" :value="sec.id">{{ sec.name }}</option>
          </select>
          <p v-if="errors.section_id" class="text-red-500 text-xs mt-1">{{ errors.section_id }}</p>
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
          {{ loading ? 'Saving...' : 'Enroll Student' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { enrollmentAPI } from '@/school/apis/enrollmentAPI'
import { studentAPI, type Student } from '@/school/apis/studentAPI'
import { sectionAPI, type Section } from '@/school/apis/sectionAPI'
import { gradeAPI, type Grade } from '@/school/apis/gradeAPI'
import { academicSessionAPI, type AcademicSession } from '@/school/apis/academicSessionAPI'

const router = useRouter()
const loading = ref(false)
const serverError = ref('')
const errors = ref<Record<string, string>>({})

const form = ref({
  student_id: '',
  academic_session_id: '',
  grade_id: '',
  section_id: '',
  status: 'ongoing' as 'ongoing' | 'promoted' | 'repeated' | 'left',
  enrollment_date: new Date().toISOString().split('T')[0],
  student_registration_number: ''
})

const students = ref<Student[]>([])
const sessions = ref<AcademicSession[]>([])
const grades = ref<Grade[]>([])
const sections = ref<Section[]>([])

onMounted(async () => {
  try {
    const [stuRes, sesRes, grRes, secRes] = await Promise.all([
      studentAPI.list(),
      academicSessionAPI.list(),
      gradeAPI.list(),
      sectionAPI.list()
    ])
    students.value = stuRes.data.results || (stuRes.data as any)
    sessions.value = sesRes.data.results || (sesRes.data as any)
    grades.value = grRes.data.results || (grRes.data as any)
    sections.value = secRes.data.results || (secRes.data as any)

    const activeSes = sessions.value.find(s => s.is_active)
    if (activeSes) form.value.academic_session_id = activeSes.id
  } catch {
    serverError.value = 'Failed to load form data.'
  }
})

const handleSubmit = async () => {
  errors.value = {}
  serverError.value = ''
  if (!form.value.student_id) errors.value.student_id = 'Required.'
  if (!form.value.academic_session_id) errors.value.academic_session_id = 'Required.'
  if (!form.value.grade_id) errors.value.grade_id = 'Required.'
  if (!form.value.section_id) errors.value.section_id = 'Required.'
  if (Object.keys(errors.value).length > 0) return

  loading.value = true
  try {
    await enrollmentAPI.create(form.value)
    router.push('/school/enrollments')
  } catch (err: any) {
    const data = err.response?.data
    if (data && typeof data === 'object') Object.entries(data).forEach(([k, v]: any) => { errors.value[k] = Array.isArray(v) ? v.join(', ') : v })
    serverError.value = data?.detail || 'Failed to create enrollment.'
  } finally { loading.value = false }
}
</script>
