<template>
  <div class="h-full flex flex-col px-8 py-8">
    <div class="mb-6 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Attendance</h1>
        <p class="text-sm text-gray-500 mt-1">Manage student daily attendance records.</p>
      </div>
      <router-link to="/school/attendance/create" class="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-indigo-700 shadow-sm flex items-center gap-2">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
        Mark Attendance
      </router-link>
    </div>

    <!-- Controls -->
    <div class="flex items-center gap-4 mb-6">
      <div class="relative flex-1 max-w-md">
        <input v-model="searchQuery" @keyup.enter="handleSearch" type="date" class="w-full pl-4 pr-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-sm" />
      </div>
      <button @click="handleSearch" class="px-4 py-2 text-sm font-medium text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50 shadow-sm">Filter</button>
      <button @click="resetFilters" v-if="searchQuery" class="px-4 py-2 text-sm font-medium text-red-600 hover:text-red-700">Clear</button>
    </div>

    <!-- Table -->
    <div class="bg-white shadow rounded-lg border border-gray-200 overflow-hidden flex-1 flex flex-col">
      <div class="overflow-x-auto flex-1">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50 sticky top-0 z-10">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Student</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Date</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Status</th>
              <th scope="col" class="px-6 py-3 text-right text-xs font-bold text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="loading">
              <td colspan="4" class="px-6 py-12 text-center text-gray-500">
                <div class="inline-flex items-center">
                  <div class="w-5 h-5 border-2 border-indigo-200 border-t-indigo-600 rounded-full animate-spin mr-3"></div>
                  Loading attendance...
                </div>
              </td>
            </tr>
            <tr v-else-if="items.length === 0">
              <td colspan="4" class="px-6 py-12 text-center text-gray-500">No records found.</td>
            </tr>
            <tr v-else v-for="item in items" :key="item.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-900">{{ item.student_name || '—' }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.date }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-bold">
                <span v-if="item.status === 'present'" class="text-green-600 bg-green-50 px-2 py-1 rounded">Present</span>
                <span v-else class="text-red-600 bg-red-50 px-2 py-1 rounded">Absent</span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <router-link :to="`/school/attendance/${item.id}/edit`" class="text-indigo-600 hover:text-indigo-900">Edit</router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="bg-white px-6 py-4 border-t border-gray-200 flex items-center justify-between">
        <div class="text-sm text-gray-500">Showing <span class="font-medium">{{ ((page - 1) * pageSize) + (items.length > 0 ? 1 : 0) }}</span> to <span class="font-medium">{{ ((page - 1) * pageSize) + items.length }}</span> of <span class="font-medium">{{ totalCount }}</span> results</div>
        <div class="flex gap-2">
          <button @click="page--" :disabled="page === 1" class="px-3 py-1 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50">Prev</button>
          <button @click="page++" :disabled="page * pageSize >= totalCount" class="px-3 py-1 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50">Next</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { attendanceAPI, type Attendance } from '@/school/apis/attendanceAPI'

const items = ref<Attendance[]>([])
const loading = ref(true)
const searchQuery = ref('')
const page = ref(1)
const pageSize = ref(10)
const totalCount = ref(0)

const fetchItems = async () => {
  loading.value = true
  try {
    const params = {
      page: page.value,
      page_size: pageSize.value,
      date: searchQuery.value || undefined
    }
    const res = await attendanceAPI.list(params)
    items.value = res.data.results
    totalCount.value = res.data.count
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchItems)
watch(page, fetchItems)

const handleSearch = () => {
  page.value = 1
  fetchItems()
}

const resetFilters = () => {
  searchQuery.value = ''
  page.value = 1
  fetchItems()
}
</script>
