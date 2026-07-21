<template>
  <div class="p-8 max-w-3xl">
    <div class="flex items-center gap-3 mb-6">
      <router-link to="/school/exams" class="text-gray-400 hover:text-gray-700"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg></router-link>
      <div><h1 class="text-2xl font-bold text-gray-900">Edit Exam</h1><p class="text-sm text-gray-500">Update exam schedule details.</p></div>
    </div>
    <div v-if="pageLoading" class="flex items-center justify-center py-20"><div class="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div></div>
    <div v-else class="bg-white border border-gray-200 rounded-xl shadow-sm p-6 space-y-5">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Exam Name <span class="text-red-500">*</span></label>
        <input v-model="form.name" type="text" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
      </div>
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Exam Type</label>
          <select v-model="form.exam_type_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <option v-for="et in examTypes" :key="et.id" :value="et.id">{{ et.name }}</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Academic Session</label>
          <select v-model="form.academic_session_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <option v-for="ses in sessions" :key="ses.id" :value="ses.id">{{ ses.name }}</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Grade</label>
          <select v-model="form.grade_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <option v-for="g in grades" :key="g.id" :value="g.id">{{ g.name }}</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Section (Optional)</label>
          <select v-model="form.section_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <option value="">All Sections</option>
            <option v-for="sec in sections" :key="sec.id" :value="sec.id">{{ sec.name }}</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
          <input v-model="form.start_date" type="date" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
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
        <router-link :to="`/school/exams/${examId}`" class="px-4 py-2 text-sm font-medium text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50">Cancel</router-link>
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
import { examAPI } from '@/school/apis/examAPI'
import { examTypeAPI, type ExamType } from '@/school/apis/examTypeAPI'
import { gradeAPI, type Grade } from '@/school/apis/gradeAPI'
import { sectionAPI, type Section } from '@/school/apis/sectionAPI'
import { academicSessionAPI, type AcademicSession } from '@/school/apis/academicSessionAPI'

const router = useRouter()
const route = useRoute()
const examId = route.params.id as string
const pageLoading = ref(true)
const loading = ref(false)
const serverError = ref('')
const form = ref({ name: '', exam_type_id: '', academic_session_id: '', grade_id: '', section_id: '', start_date: '', end_date: '', is_active: true })
const examTypes = ref<ExamType[]>([])
const sessions = ref<AcademicSession[]>([])
const grades = ref<Grade[]>([])
const sections = ref<Section[]>([])

onMounted(async () => {
  try {
    const [exRes, etRes, sesRes, grRes, secRes] = await Promise.all([
      examAPI.retrieve(examId), examTypeAPI.list(), academicSessionAPI.list(), gradeAPI.list(), sectionAPI.list()
    ])
    const ex = exRes.data
    form.value = { name: ex.name, exam_type_id: ex.exam_type_id, academic_session_id: ex.academic_session_id, grade_id: ex.grade_id, section_id: ex.section_id || '', start_date: ex.start_date, end_date: ex.end_date || '', is_active: ex.is_active }
    examTypes.value = etRes.data.results || (etRes.data as any)
    sessions.value = sesRes.data.results || (sesRes.data as any)
    grades.value = grRes.data.results || (grRes.data as any)
    sections.value = secRes.data.results || (secRes.data as any)
  } catch { serverError.value = 'Failed to load exam.' }
  finally { pageLoading.value = false }
})

const handleSubmit = async () => {
  serverError.value = ''
  if (!form.value.name) { serverError.value = 'Name is required.'; return }
  loading.value = true
  try {
    const payload: any = { ...form.value }
    if (!payload.section_id) delete payload.section_id
    if (!payload.end_date) delete payload.end_date
    await examAPI.update(examId, payload)
    router.push(`/school/exams/${examId}`)
  } catch (err: any) {
    serverError.value = err.response?.data?.detail || 'Failed to update exam.'
  } finally { loading.value = false }
}
</script>
