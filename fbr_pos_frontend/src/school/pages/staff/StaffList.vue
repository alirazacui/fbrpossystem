<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <SchoolPageHeader
      title="Staff Directory"
      subtitle="Manage teachers, administrators, and support staff."
    >
      <template #actions>
        <router-link
          to="/school/staff/create"
          class="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white text-sm font-semibold rounded-lg hover:bg-indigo-700 shadow-sm transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
          Add Staff Member
        </router-link>
      </template>
    </SchoolPageHeader>

    <div class="p-8 flex-1">
      <div v-if="loading" class="flex items-center justify-center py-20">
        <div class="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
      </div>
      
      <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 rounded-xl px-4 py-3 text-sm flex items-start gap-3">
        <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
        {{ error }}
      </div>
      
      <div v-else-if="staffList.length === 0" class="bg-white border border-gray-200 rounded-xl p-16 text-center shadow-sm">
        <svg class="w-12 h-12 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
        <h3 class="text-base font-semibold text-gray-700 mb-1">No staff members</h3>
        <p class="text-sm text-gray-400 mb-4">Add teachers or admins to manage your school operations.</p>
        <router-link to="/school/staff/create" class="text-sm text-indigo-600 font-semibold hover:underline">Add Staff →</router-link>
      </div>
      
      <div v-else class="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Staff Member</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Designation</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Contact</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Status</th>
              <th class="text-right px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="member in staffList" :key="member.id" class="hover:bg-gray-50 transition-colors">
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="w-9 h-9 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-700 font-bold text-sm shadow-inner">
                    {{ member.fullname.charAt(0).toUpperCase() }}
                  </div>
                  <div>
                    <div class="font-semibold text-gray-900">{{ member.fullname }}</div>
                    <div class="text-xs text-gray-500">{{ member.cnic || 'No CNIC' }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 text-gray-600 font-medium">{{ member.designation || '—' }}</td>
              <td class="px-6 py-4">
                <div class="text-gray-900">{{ member.phone_number || '—' }}</div>
                <div class="text-xs text-gray-500">{{ member.email || '—' }}</div>
              </td>
              <td class="px-6 py-4">
                <span :class="member.status === 'active' ? 'bg-green-50 text-green-700 border-green-200' : 'bg-gray-100 text-gray-500 border-gray-200'" class="px-2.5 py-0.5 rounded-full text-xs font-bold border">
                  {{ member.status === 'active' ? 'Active' : 'Inactive' }}
                </span>
              </td>
              <td class="px-6 py-4 text-right">
                <div class="flex items-center justify-end gap-3">
                  <router-link :to="`/school/staff/${member.id}`" class="text-indigo-600 hover:text-indigo-900 font-medium text-sm">Profile</router-link>
                  <router-link :to="`/school/staff/${member.id}/edit`" class="text-gray-500 hover:text-gray-900 font-medium text-sm">Edit</router-link>
                  <button @click="confirmDelete(member)" class="text-red-500 hover:text-red-700 font-medium text-sm">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Delete Confirm Modal -->
    <SchoolModal
      :isOpen="!!deleteTarget"
      title="Delete Staff Member"
      submitLabel="Delete"
      :loading="deleting"
      maxWidth="sm"
      @close="deleteTarget = null"
      @submit="handleDelete"
    >
      <template v-if="deleteTarget">
        <p class="text-sm text-gray-600">
          Are you sure you want to remove <strong>{{ deleteTarget.fullname }}</strong>?<br>
          <span class="text-red-600 mt-2 block font-medium">This action cannot be undone.</span>
        </p>
      </template>
    </SchoolModal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import SchoolPageHeader from '@/school/components/SchoolPageHeader.vue'
import SchoolModal from '@/school/components/SchoolModal.vue'
import { staffAPI, type Staff } from '@/school/apis/staffAPI'

const staffList = ref<Staff[]>([])
const loading = ref(true)
const error = ref('')
const deleteTarget = ref<Staff | null>(null)
const deleting = ref(false)

const fetchStaff = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await staffAPI.list()
    staffList.value = res.data.results || (res.data as any)
  } catch {
    error.value = 'Failed to load staff.'
  } finally {
    loading.value = false
  }
}

const confirmDelete = (s: Staff) => { deleteTarget.value = s }

const handleDelete = async () => {
  if (!deleteTarget.value) return
  deleting.value = true
  try {
    await staffAPI.delete(deleteTarget.value.id)
    staffList.value = staffList.value.filter(s => s.id !== deleteTarget.value!.id)
    deleteTarget.value = null
  } catch {
    error.value = 'Failed to delete staff member.'
  } finally {
    deleting.value = false
  }
}

onMounted(fetchStaff)
</script>
