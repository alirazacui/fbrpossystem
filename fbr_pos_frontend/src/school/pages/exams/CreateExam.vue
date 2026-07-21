<template>
  <div class="p-8 max-w-3xl">
    <div class="flex items-center gap-3 mb-6">
      <router-link to="/school/exams" class="text-gray-400 hover:text-gray-700"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg></router-link>
      <div><h1 class="text-2xl font-bold text-gray-900">Schedule Exam</h1><p class="text-sm text-gray-500">Set up a new exam for a grade or section.</p></div>
    </div>

    <div class="bg-white border border-gray-200 rounded-xl shadow-sm p-6 space-y-5">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Exam Name <span class="text-red-500">*</span></label>
        <input v-model="form.name" type="text" placeholder="e.g. Midterm 2026 - Grade 5" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        <p v-if="errors.name" class="text-red-500 text-xs mt-1">{{ errors.name }}</p>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Exam Type <span class="text-red-500">*</span></label>
          <select v-model="form.exam_type_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <option value="" disabled>Select Exam Type</option>
            <option v-for="et in examTypes" :key="et.id" :value="et.id">{{ et.name }}</option>
          </select>
          <p v-if="errors.exam_type_id" class="text-red-500 text-xs mt-1">{{ errors.exam_type_id }}</p>
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
          <label class="block text-sm font-medium text-gray-700 mb-1">Section (Optional)</label>
          <select v-model="form.section_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <option value="">All Sections</option>
            <option v-for="sec in sections" :key="sec.id" :value="sec.id">{{ sec.name }}</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Start Date <span class="text-red-500">*</span></label>
          <input v-model="form.start_date" type="date" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          <p v-if="errors.start_date" class="text-red-500 text-xs mt-1">{{ errors.start_date }}</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">End Date</label>
          <input v-model="form.end_date" type="date" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>
      </div>

      <div class="flex items-center gap-2">
        <input type="checkbox" id="active" v-model="form.is_active" class="w-4 h-4 accent-indigo-600 rounded" />
        <label for="active" class="text-sm text-gray-700 cursor-pointer">Active</label>
      </div>

      <div v-if="serverError" class="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-4 py-3">{{ serverError }}</div>

      <div class="flex justify-end gap-3 pt-4">
        <router-link to="/school/exams" class="px-4 py-2 text-sm font-medium text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50">Cancel</router-link>
        <button @click="handleSubmit" :disabled="loading" class="px-5 py-2 text-sm font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 disabled:opacity-50 flex items-center gap-2">
          <div v-if="loading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          {{ loading ? 'Saving...' : 'Schedule Exam' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { examAPI } from '@/school/apis/examAPI'
import { examTypeAPI, type ExamType } from '@/school/apis/examTypeAPI'
import { gradeAPI, type Grade } from '@/school/apis/gradeAPI'
import { sectionAPI, type Section } from '@/school/apis/sectionAPI'
import { academicSessionAPI, type AcademicSession } from '@/school/apis/academicSessionAPI'

const router = useRouter()
const loading = ref(false)
const serverError = ref('')
const errors = ref<Record<string, string>>({})

const form = ref({ name: '', exam_type_id: '', academic_session_id: '', grade_id: '', section_id: '', start_date: '', end_date: '', is_active: true })

const examTypes = ref<ExamType[]>([])
const sessions = ref<AcademicSession[]>([])
const grades = ref<Grade[]>([])
const sections = ref<Section[]>([])

onMounted(async () => {
  try {
    const [etRes, sesRes, grRes, secRes] = await Promise.all([
      examTypeAPI.list(), academicSessionAPI.list(), gradeAPI.list(), sectionAPI.list()
    ])
    examTypes.value = etRes.data.results || (etRes.data as any)
    sessions.value = sesRes.data.results || (sesRes.data as any)
    grades.value = grRes.data.results || (grRes.data as any)
    sections.value = secRes.data.results || (secRes.data as any)

    const active = sessions.value.find(s => s.is_active)
    if (active) form.value.academic_session_id = active.id
  } catch { serverError.value = 'Failed to load form data.' }
})

const handleSubmit = async () => {
  errors.value = {}
  serverError.value = ''
  if (!form.value.name) errors.value.name = 'Required.'
  if (!form.value.exam_type_id) errors.value.exam_type_id = 'Required.'
  if (!form.value.academic_session_id) errors.value.academic_session_id = 'Required.'
  if (!form.value.grade_id) errors.value.grade_id = 'Required.'
  if (!form.value.start_date) errors.value.start_date = 'Required.'
  if (Object.keys(errors.value).length > 0) return

  loading.value = true
  try {
    const payload: any = { ...form.value }
    if (!payload.section_id) delete payload.section_id
    if (!payload.end_date) delete payload.end_date
    const res = await examAPI.create(payload)
    router.push(`/school/exams/${res.data.id}`)
  } catch (err: any) {
    const data = err.response?.data
    if (data && typeof data === 'object') Object.entries(data).forEach(([k, v]: any) => { errors.value[k] = Array.isArray(v) ? v.join(', ') : v })
    serverError.value = data?.detail || 'Failed to create exam.'
  } finally { loading.value = false }
}
</script>
