<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <SchoolPageHeader
      title="Guardians"
      subtitle="Manage parents and guardians of your students."
    >
      <template #actions>
        <router-link
          to="/school/guardians/create"
          class="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white text-sm font-semibold rounded-lg hover:bg-indigo-700 shadow-sm transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
          Add Guardian
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
      
      <div v-else-if="guardians.length === 0" class="bg-white border border-gray-200 rounded-xl p-16 text-center shadow-sm">
        <svg class="w-12 h-12 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a4 4 0 00-5-3.87M9 20H4v-2a4 4 0 015-3.87m4-9a4 4 0 110 8 4 4 0 010-8zM15 7a4 4 0 11-8 0 4 4 0 018 0z"/></svg>
        <h3 class="text-base font-semibold text-gray-700 mb-1">No guardians yet</h3>
        <p class="text-sm text-gray-400 mb-4">Add parents or guardians to associate them with students.</p>
        <router-link to="/school/guardians/create" class="text-sm text-indigo-600 font-semibold hover:underline">Add Guardian →</router-link>
      </div>
      
      <div v-else class="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Guardian Name</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Contact Details</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">CNIC</th>
              <th class="text-right px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="g in guardians" :key="g.id" class="hover:bg-gray-50 transition-colors">
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="w-9 h-9 rounded-full bg-blue-100 flex items-center justify-center text-blue-700 font-bold text-sm shadow-inner">
                    {{ g.first_name.charAt(0).toUpperCase() }}
                  </div>
                  <span class="font-semibold text-gray-900">{{ g.first_name }} {{ g.last_name }}</span>
                </div>
              </td>
              <td class="px-6 py-4">
                <div class="text-gray-900 font-medium">{{ g.phone_number || 'No Phone' }}</div>
                <div class="text-xs text-gray-500">{{ g.email || 'No Email' }}</div>
              </td>
              <td class="px-6 py-4 text-gray-600 font-mono text-xs">{{ g.cnic || '—' }}</td>
              <td class="px-6 py-4 text-right">
                <div class="flex items-center justify-end gap-3">
                  <router-link :to="`/school/guardians/${g.id}`" class="text-indigo-600 hover:text-indigo-900 font-medium text-sm">Profile</router-link>
                  <router-link :to="`/school/guardians/${g.id}/edit`" class="text-gray-500 hover:text-gray-900 font-medium text-sm">Edit</router-link>
                  <button @click="confirmDelete(g)" class="text-red-500 hover:text-red-700 font-medium text-sm">Delete</button>
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
      title="Delete Guardian"
      submitLabel="Delete"
      :loading="deleting"
      maxWidth="sm"
      @close="deleteTarget = null"
      @submit="handleDelete"
    >
      <template v-if="deleteTarget">
        <p class="text-sm text-gray-600">
          Are you sure you want to remove <strong>{{ deleteTarget.first_name }} {{ deleteTarget.last_name }}</strong>?<br>
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
import { guardianAPI, type Guardian } from '@/school/apis/guardianAPI'

const guardians = ref<Guardian[]>([])
const loading = ref(true)
const error = ref('')
const deleteTarget = ref<Guardian | null>(null)
const deleting = ref(false)

const fetchGuardians = async () => {
  loading.value = true
  try {
    const res = await guardianAPI.list()
    guardians.value = res.data.results || (res.data as any)
  } catch { error.value = 'Failed to load guardians.' }
  finally { loading.value = false }
}

const confirmDelete = (g: Guardian) => { deleteTarget.value = g }

const handleDelete = async () => {
  if (!deleteTarget.value) return
  deleting.value = true
  try {
    await guardianAPI.delete(deleteTarget.value.id)
    guardians.value = guardians.value.filter(x => x.id !== deleteTarget.value!.id)
    deleteTarget.value = null
  } catch { error.value = 'Failed to delete guardian.' }
  finally { deleting.value = false }
}

onMounted(fetchGuardians)
</script>
