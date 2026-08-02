<template>
  <div class="p-8 max-w-3xl mx-auto">
    <div class="flex items-center justify-between mb-8">
      <div class="flex items-center gap-3">
        <router-link to="/school/exam-types" class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-200 transition-colors">
          <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
        </router-link>
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Exam Type Detail</h1>
          <p class="text-sm text-gray-500">View information about this exam category</p>
        </div>
      </div>
      <div class="flex gap-3">
        <button @click="handleDelete" class="px-4 py-2 text-sm font-semibold text-red-600 bg-red-50 rounded-lg hover:bg-red-100 transition-colors">Delete</button>
        <router-link :to="`/school/exam-types/${route.params.id}/edit`" class="px-4 py-2 text-sm font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors shadow-sm">Edit</router-link>
      </div>
    </div>

    <div v-if="loading" class="flex justify-center py-20">
      <div class="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
    </div>

    <div v-else-if="item" class="space-y-6">
      <div class="bg-white shadow-sm border border-gray-200 rounded-xl overflow-hidden">
        <div class="px-6 py-5 border-b border-gray-100 bg-gray-50">
          <h3 class="text-lg font-semibold text-gray-900">Overview</h3>
        </div>
        <div class="p-6">
          <p class="text-sm font-medium text-gray-500 mb-1">Name</p>
          <p class="text-xl font-bold text-gray-900">{{ item.name }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { examTypeAPI, type ExamType } from '@/school/apis/examTypeAPI'

const route = useRoute()
const router = useRouter()
const item = ref<ExamType | null>(null)
const loading = ref(true)

const fetchItem = async () => {
  try {
    const res = await examTypeAPI.retrieve(route.params.id as string)
    item.value = res.data
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchItem)

const handleDelete = async () => {
  if (confirm('Are you sure you want to delete this exam type?')) {
    try {
      await examTypeAPI.delete(route.params.id as string)
      router.push('/school/exam-types')
    } catch (err) {
      console.error(err)
      alert('Failed to delete.')
    }
  }
}
</script>
