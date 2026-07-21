<template>
  <div class="p-8 max-w-2xl">
    <div class="flex items-center gap-3 mb-6">
      <router-link to="/school/exams" class="text-gray-400 hover:text-gray-700"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg></router-link>
      <div><h1 class="text-2xl font-bold text-gray-900">Enter Exam Result</h1><p class="text-sm text-gray-500">Record marks for a student.</p></div>
    </div>
    <div class="bg-white border border-gray-200 rounded-xl shadow-sm p-6 space-y-5">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Exam <span class="text-red-500">*</span></label>
        <select v-model="form.exam_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
          <option value="" disabled>Select Exam</option>
          <option v-for="e in exams" :key="e.id" :value="e.id">{{ e.name }}</option>
        </select>
        <p v-if="errors.exam_id" class="text-red-500 text-xs mt-1">{{ errors.exam_id }}</p>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Student <span class="text-red-500">*</span></label>
        <select v-model="form.student_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
          <option value="" disabled>Select Student</option>
          <option v-for="stu in students" :key="stu.id" :value="stu.id">{{ stu.fullname }}</option>
        </select>
        <p v-if="errors.student_id" class="text-red-500 text-xs mt-1">{{ errors.student_id }}</p>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Subject <span class="text-red-500">*</span></label>
        <select v-model="form.subject_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
          <option value="" disabled>Select Subject</option>
          <option v-for="sub in subjects" :key="sub.id" :value="sub.id">{{ sub.name }}</option>
        </select>
        <p v-if="errors.subject_id" class="text-red-500 text-xs mt-1">{{ errors.subject_id }}</p>
      </div>
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Marks Obtained <span class="text-red-500">*</span></label>
          <input v-model.number="form.marks_obtained" type="number" min="0" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Max Marks <span class="text-red-500">*</span></label>
          <input v-model.number="form.max_marks" type="number" min="0" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>
      </div>
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Grade Letter</label>
          <input v-model="form.grade_letter" type="text" placeholder="A, B+, etc." class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Remarks</label>
          <input v-model="form.remarks" type="text" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>
      </div>
      <div v-if="serverError" class="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-4 py-3">{{ serverError }}</div>
      <div class="flex justify-end gap-3 pt-4">
        <router-link to="/school/exams" class="px-4 py-2 text-sm font-medium text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50">Cancel</router-link>
        <button @click="handleSubmit" :disabled="loading" class="px-5 py-2 text-sm font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 disabled:opacity-50 flex items-center gap-2">
          <div v-if="loading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          {{ loading ? 'Saving...' : 'Save Result' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { studentExamResultAPI } from '@/school/apis/studentExamResultAPI'
import { examAPI, type Exam } from '@/school/apis/examAPI'
import { studentAPI, type Student } from '@/school/apis/studentAPI'
import { subjectAPI, type Subject } from '@/school/apis/subjectAPI'

const router = useRouter()
const route = useRoute()
const loading = ref(false)
const serverError = ref('')
const errors = ref<Record<string, string>>({})
const form = ref({ exam_id: (route.query.exam_id as string) || '', student_id: '', subject_id: '', marks_obtained: 0, max_marks: 100, grade_letter: '', remarks: '' })
const exams = ref<Exam[]>([])
const students = ref<Student[]>([])
const subjects = ref<Subject[]>([])

onMounted(async () => {
  try {
    const [exRes, stuRes, subRes] = await Promise.all([examAPI.list(), studentAPI.list(), subjectAPI.list()])
    exams.value = exRes.data.results || (exRes.data as any)
    students.value = stuRes.data.results || (stuRes.data as any)
    subjects.value = subRes.data.results || (subRes.data as any)
  } catch { serverError.value = 'Failed to load form data.' }
})

const handleSubmit = async () => {
  errors.value = {}
  serverError.value = ''
  if (!form.value.exam_id) errors.value.exam_id = 'Required.'
  if (!form.value.student_id) errors.value.student_id = 'Required.'
  if (!form.value.subject_id) errors.value.subject_id = 'Required.'
  if (Object.keys(errors.value).length > 0) return
  loading.value = true
  try {
    const payload: any = { ...form.value }
    if (!payload.grade_letter) delete payload.grade_letter
    if (!payload.remarks) delete payload.remarks
    await studentExamResultAPI.create(payload)
    router.push(`/school/exams/${form.value.exam_id}`)
  } catch (err: any) {
    const data = err.response?.data
    if (data && typeof data === 'object') Object.entries(data).forEach(([k, v]: any) => { errors.value[k] = Array.isArray(v) ? v.join(', ') : v })
    serverError.value = data?.detail || 'Failed to save result.'
  } finally { loading.value = false }
}
</script>
