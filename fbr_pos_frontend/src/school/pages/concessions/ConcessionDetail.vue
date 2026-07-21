<template>
  <div class="p-8 max-w-3xl mx-auto">
    <div class="flex items-center justify-between mb-8">
      <div class="flex items-center gap-3">
        <router-link to="/school/concessions" class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-200 transition-colors">
          <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
        </router-link>
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Concession Detail</h1>
          <p class="text-sm text-gray-500">View detailed information about this fee concession</p>
        </div>
      </div>
      <div class="flex gap-3">
        <button @click="handleDelete" class="px-4 py-2 text-sm font-semibold text-red-600 bg-red-50 rounded-lg hover:bg-red-100 transition-colors">Delete</button>
        <router-link :to="`/school/concessions/${route.params.id}/edit`" class="px-4 py-2 text-sm font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors shadow-sm">Edit Concession</router-link>
      </div>
    </div>

    <div v-if="loading" class="flex justify-center py-20">
      <div class="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
    </div>

    <div v-else-if="item" class="space-y-6">
      <div class="bg-white shadow-sm border border-gray-200 rounded-xl overflow-hidden">
        <div class="px-6 py-5 border-b border-gray-100 bg-gray-50">
          <h3 class="text-lg font-semibold text-gray-900">Concession Overview</h3>
        </div>
        <div class="p-6 grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <p class="text-sm font-medium text-gray-500 mb-1">Student</p>
            <p class="text-base font-semibold text-gray-900">{{ item.student_name || '—' }}</p>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-500 mb-1">Session</p>
            <p class="text-base text-gray-900">{{ item.session_name || '—' }}</p>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-500 mb-1">Fee Head</p>
            <p class="text-base font-semibold text-indigo-600">{{ item.fee_head_name || 'Global (All Heads)' }}</p>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-500 mb-1">Concession Type</p>
            <p class="text-base text-gray-900 capitalize">{{ item.concession_type.replace('_', ' ') }}</p>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-500 mb-1">Value</p>
            <p class="text-2xl font-bold text-gray-900">
              <span v-if="item.concession_type === 'percentage'">{{ item.percentage }}%</span>
              <span v-else>Rs {{ item.amount }}</span>
            </p>
          </div>
          <div class="md:col-span-2">
            <p class="text-sm font-medium text-gray-500 mb-1">Reason / Notes</p>
            <p class="text-base text-gray-900 bg-gray-50 p-4 rounded-lg">{{ item.reason || 'No reason provided.' }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { studentFeeConcessionAPI, type StudentFeeConcession } from '@/school/apis/studentFeeConcessionAPI'

const route = useRoute()
const router = useRouter()
const item = ref<StudentFeeConcession | null>(null)
const loading = ref(true)

const fetchItem = async () => {
  try {
    const res = await studentFeeConcessionAPI.retrieve(route.params.id as string)
    item.value = res.data
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchItem)

const handleDelete = async () => {
  if (confirm('Are you sure you want to delete this concession?')) {
    try {
      await studentFeeConcessionAPI.delete(route.params.id as string)
      router.push('/school/concessions')
    } catch (err) {
      console.error(err)
      alert('Failed to delete.')
    }
  }
}
</script>
