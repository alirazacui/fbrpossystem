<template>
  <div class="p-8 max-w-3xl mx-auto">
    <div class="flex items-center justify-between mb-8">
      <div class="flex items-center gap-3">
        <router-link to="/school/enrollments" class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-200 transition-colors">
          <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
        </router-link>
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Enrollment Detail</h1>
          <p class="text-sm text-gray-500">View detailed enrollment information</p>
        </div>
      </div>
      <div class="flex gap-3">
        <button @click="handleDelete" class="px-4 py-2 text-sm font-semibold text-red-600 bg-red-50 rounded-lg hover:bg-red-100 transition-colors">Delete</button>
        <router-link :to="`/school/enrollments/${route.params.id}/edit`" class="px-4 py-2 text-sm font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors shadow-sm">Edit</router-link>
      </div>
    </div>

    <div v-if="loading" class="flex justify-center py-20">
      <div class="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
    </div>

    <div v-else-if="item" class="space-y-6">
      <div class="bg-white shadow-sm border border-gray-200 rounded-xl overflow-hidden">
        <div class="px-6 py-5 border-b border-gray-100 bg-gray-50">
          <h3 class="text-lg font-semibold text-gray-900">Enrollment Overview</h3>
        </div>
        <div class="p-6 grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <p class="text-sm font-medium text-gray-500 mb-1">Student</p>
            <p class="text-base font-semibold text-gray-900">{{ item.student_name || '—' }}</p>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-500 mb-1">Academic Session</p>
            <p class="text-base text-gray-900">{{ item.session_name || '—' }}</p>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-500 mb-1">Grade</p>
            <p class="text-base text-gray-900">{{ item.grade_name || '—' }}</p>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-500 mb-1">Section</p>
            <p class="text-base text-gray-900">{{ item.section_name || '—' }}</p>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-500 mb-1">Enrollment Date</p>
            <p class="text-base text-gray-900">{{ item.enrollment_date }}</p>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-500 mb-1">Status</p>
            <p class="text-base font-bold capitalize" :class="item.status === 'active' ? 'text-green-600' : 'text-red-600'">
              {{ item.status }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { enrollmentAPI, type Enrollment } from '@/school/apis/enrollmentAPI'

const route = useRoute()
const router = useRouter()
const item = ref<Enrollment | null>(null)
const loading = ref(true)

const fetchItem = async () => {
  try {
    const res = await enrollmentAPI.retrieve(route.params.id as string)
    item.value = res.data
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchItem)

const handleDelete = async () => {
  if (confirm('Are you sure you want to delete this enrollment?')) {
    try {
      await enrollmentAPI.delete(route.params.id as string)
      router.push('/school/enrollments')
    } catch (err) {
      console.error(err)
      alert('Failed to delete.')
    }
  }
}
</script>
