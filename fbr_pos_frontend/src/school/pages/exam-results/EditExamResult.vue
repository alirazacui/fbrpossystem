<template>
  <div class="p-8 max-w-2xl mx-auto">
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center gap-3">
        <router-link to="/school/exam-results" class="text-gray-400 hover:text-gray-700"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg></router-link>
        <div><h1 class="text-2xl font-bold text-gray-900">Edit Exam Result</h1><p class="text-sm text-gray-500">Update a student's exam score.</p></div>
      </div>
      <button @click="handleDelete" class="px-4 py-2 text-sm font-semibold text-red-600 bg-red-50 rounded-lg hover:bg-red-100 transition-colors">Delete</button>
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
      
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Subject</label>
        <div class="px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700">
          {{ initialData?.subject_name }}
        </div>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Marks Obtained <span class="text-red-500">*</span></label>
          <input v-model.number="form.marks_obtained" type="number" min="0" step="0.5" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Grade</label>
          <input v-model="form.grade" type="text" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Remarks</label>
        <textarea v-model="form.remarks" rows="2" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none"></textarea>
      </div>

      <div v-if="serverError" class="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-4 py-3">{{ serverError }}</div>

      <div class="flex justify-end gap-3 pt-2">
        <router-link to="/school/exam-results" class="px-4 py-2 text-sm font-medium text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50">Cancel</router-link>
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
import { studentExamResultAPI } from '@/school/apis/studentExamResultAPI'

const router = useRouter()
const route = useRoute()
const loadingInitial = ref(true)
const loading = ref(false)
const serverError = ref('')
const initialData = ref<any>(null)

const form = ref({
  marks_obtained: 0,
  grade: '',
  remarks: ''
})

onMounted(async () => {
  try {
    const res = await studentExamResultAPI.retrieve(route.params.id as string)
    initialData.value = res.data
    form.value = {
      marks_obtained: parseFloat(res.data.marks_obtained || '0'),
      grade: res.data.grade || '',
      remarks: res.data.remarks || ''
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
    await studentExamResultAPI.update(route.params.id as string, form.value)
    router.push('/school/exam-results')
  } catch (err: any) {
    serverError.value = err.response?.data?.detail || 'Failed to update.'
  } finally {
    loading.value = false
  }
}

const handleDelete = async () => {
  if (confirm('Are you sure you want to delete this result?')) {
    try {
      await studentExamResultAPI.delete(route.params.id as string)
      router.push('/school/exam-results')
    } catch (err) {
      console.error(err)
      alert('Failed to delete.')
    }
  }
}
</script>
