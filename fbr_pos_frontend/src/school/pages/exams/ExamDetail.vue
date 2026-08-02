<template>
  <div class="p-8 space-y-6 max-w-4xl">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-3">
        <router-link to="/school/exams" class="text-gray-400 hover:text-gray-700"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg></router-link>
        <h1 class="text-2xl font-bold text-gray-900">Exam Detail</h1>
      </div>
      <div class="flex gap-2" v-if="exam">
        <router-link :to="`/school/exams/${exam.id}/edit`" class="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-semibold text-indigo-700 bg-indigo-50 rounded-lg hover:bg-indigo-100 transition-colors">Edit</router-link>
        <router-link :to="`/school/exam-results/create?exam_id=${exam.id}`" class="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white text-sm font-semibold rounded-lg hover:bg-indigo-700">Enter Results</router-link>
      </div>
    </div>
    <div v-if="loading" class="flex items-center justify-center py-20"><div class="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div></div>
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 rounded-lg px-4 py-3 text-sm">{{ error }}</div>
    <template v-else-if="exam">
      <div class="bg-white border border-gray-200 rounded-xl shadow-sm p-6">
        <div class="flex items-start justify-between mb-6">
          <div>
            <h2 class="text-xl font-bold text-gray-900">{{ exam.name }}</h2>
            <p class="text-sm text-indigo-600 font-semibold mt-1">{{ exam.exam_type_name || 'N/A' }}</p>
          </div>
          <span :class="exam.is_active ? 'bg-green-50 text-green-700 border-green-200' : 'bg-gray-100 text-gray-500 border-gray-200'" class="px-3 py-1 rounded-full text-xs font-bold border">{{ exam.is_active ? 'Active' : 'Inactive' }}</span>
        </div>
        <div class="grid grid-cols-2 gap-6 border-t border-gray-100 pt-5">
          <div><p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Session</p><p class="text-sm font-medium text-gray-800">{{ exam.session_name || '—' }}</p></div>
          <div><p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Grade</p><p class="text-sm font-medium text-gray-800">{{ exam.grade_name || '—' }}</p></div>
          <div><p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Section</p><p class="text-sm font-medium text-gray-800">{{ exam.section_name || 'All Sections' }}</p></div>
          <div><p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Start Date</p><p class="text-sm font-medium text-gray-800">{{ exam.start_date }}</p></div>
          <div><p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">End Date</p><p class="text-sm font-medium text-gray-800">{{ exam.end_date || '—' }}</p></div>
        </div>
      </div>
      <!-- Results List -->
      <div>
        <h3 class="text-lg font-bold text-gray-900 mb-4">Results</h3>
        <div v-if="results.length === 0" class="bg-gray-50 border border-dashed border-gray-200 rounded-xl p-10 text-center text-sm text-gray-500">No results entered yet.</div>
        <div v-else class="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
          <table class="w-full text-sm">
            <thead class="bg-gray-50 border-b border-gray-200">
              <tr>
                <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Student</th>
                <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Subject</th>
                <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Marks</th>
                <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Grade</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-for="r in results" :key="r.id" class="hover:bg-gray-50">
                <td class="px-6 py-4 font-semibold text-gray-900">{{ r.student_name }}</td>
                <td class="px-6 py-4 text-gray-600">{{ r.subject_name }}</td>
                <td class="px-6 py-4 text-gray-800 font-medium">{{ r.marks_obtained }} / {{ r.max_marks }}</td>
                <td class="px-6 py-4 text-indigo-600 font-bold">{{ r.grade_letter || '—' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { examAPI, type Exam } from '@/school/apis/examAPI'
import { studentExamResultAPI, type StudentExamResult } from '@/school/apis/studentExamResultAPI'

const route = useRoute()
const examId = route.params.id as string
const exam = ref<Exam | null>(null)
const results = ref<StudentExamResult[]>([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const [exRes, resRes] = await Promise.all([
      examAPI.retrieve(examId),
      studentExamResultAPI.list({ exam_id: examId })
    ])
    exam.value = exRes.data
    results.value = resRes.data.results || (resRes.data as any)
  } catch { error.value = 'Failed to load exam details.' }
  finally { loading.value = false }
})
</script>
