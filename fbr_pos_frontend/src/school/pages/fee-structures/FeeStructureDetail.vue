<template>
  <div class="p-8 space-y-6 max-w-4xl">
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center gap-3">
        <router-link to="/school/fee-structures" class="text-gray-400 hover:text-gray-700">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
        </router-link>
        <h1 class="text-2xl font-bold text-gray-900">Fee Structure Detail</h1>
      </div>
      <router-link v-if="structure" :to="`/school/fee-structures/${structure.id}/edit`" class="inline-flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 text-gray-700 text-sm font-semibold rounded-lg hover:bg-gray-50 transition-colors">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
        Edit Structure
      </router-link>
    </div>

    <div v-if="loading" class="flex items-center justify-center py-20"><div class="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div></div>
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 rounded-lg px-4 py-3 text-sm">{{ error }}</div>
    
    <template v-else-if="structure">
      <!-- Info Card -->
      <div class="bg-white border border-gray-200 rounded-xl shadow-sm p-6 mb-8">
        <div class="flex items-start justify-between">
          <div>
            <h2 class="text-xl font-bold text-gray-900">{{ structure.name }}</h2>
            <p class="text-sm text-gray-500 mt-1">{{ structure.description || 'No description' }}</p>
          </div>
          <span :class="structure.is_active ? 'bg-green-50 text-green-700 border-green-200' : 'bg-gray-100 text-gray-500 border-gray-200'" class="px-3 py-1 rounded-full text-xs font-bold border">
            {{ structure.is_active ? 'Active' : 'Inactive' }}
          </span>
        </div>
        <div class="grid grid-cols-2 gap-6 border-t border-gray-100 pt-5 mt-5">
          <div><p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Session</p><p class="text-sm font-medium text-gray-800">{{ structure.session_name || '—' }}</p></div>
          <div><p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Grade</p><p class="text-sm font-medium text-gray-800">{{ structure.grade_name || '—' }}</p></div>
        </div>
      </div>

      <!-- Items List -->
      <div>
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-bold text-gray-900">Fee Items</h3>
          <button @click="showAddItem = true" class="text-sm font-semibold text-indigo-600 hover:text-indigo-800 flex items-center gap-1">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg> Add Item
          </button>
        </div>

        <div v-if="items.length === 0" class="bg-gray-50 border border-gray-200 border-dashed rounded-xl p-10 text-center">
          <p class="text-gray-500 text-sm mb-3">No fee items added yet.</p>
          <button @click="showAddItem = true" class="text-indigo-600 text-sm font-semibold hover:underline">Add the first item</button>
        </div>

        <div v-else class="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
          <table class="w-full text-sm">
            <thead class="bg-gray-50 border-b border-gray-200">
              <tr>
                <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Fee Head</th>
                <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Amount</th>
                <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Frequency</th>
                <th class="text-right px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-for="item in items" :key="item.id" class="hover:bg-gray-50">
                <td class="px-6 py-4 font-medium text-gray-900">{{ item.fee_head_name }}</td>
                <td class="px-6 py-4 font-semibold text-gray-900">Rs {{ item.amount }}</td>
                <td class="px-6 py-4 capitalize text-gray-600">{{ item.frequency }}</td>
                <td class="px-6 py-4 text-right">
                  <button @click="confirmDeleteItem(item)" class="text-xs text-red-500 hover:text-red-700 font-semibold">Remove</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>

    <!-- Add Item Modal -->
    <div v-if="showAddItem" class="fixed inset-0 z-50 flex items-center justify-center bg-black/30 backdrop-blur-sm">
      <div class="bg-white rounded-xl shadow-xl p-6 w-full max-w-md mx-4">
        <h3 class="text-lg font-bold text-gray-900 mb-4">Add Fee Item</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Fee Head <span class="text-red-500">*</span></label>
            <select v-model="newItemForm.fee_head_id" class="w-full px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
              <option v-for="fh in feeHeads" :key="fh.id" :value="fh.id">{{ fh.name }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Amount <span class="text-red-500">*</span></label>
            <input v-model.number="newItemForm.amount" type="number" class="w-full px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Frequency</label>
            <select v-model="newItemForm.frequency" class="w-full px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
              <option value="once">Once</option>
              <option value="monthly">Monthly</option>
              <option value="quarterly">Quarterly</option>
              <option value="yearly">Yearly</option>
            </select>
          </div>
        </div>
        <div class="flex gap-3 justify-end mt-6">
          <button @click="showAddItem = false" class="px-4 py-2 text-sm font-medium text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50">Cancel</button>
          <button @click="handleAddItem" :disabled="savingItem" class="px-4 py-2 text-sm font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 disabled:opacity-50">
            {{ savingItem ? 'Saving...' : 'Add Item' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { feeStructureAPI, type FeeStructure } from '@/school/apis/feeStructureAPI'
import { feeStructureItemAPI, type FeeStructureItem } from '@/school/apis/feeStructureItemAPI'
import { feeHeadAPI, type FeeHead } from '@/school/apis/feeHeadAPI'

const route = useRoute()
const structureId = route.params.id as string

const structure = ref<FeeStructure | null>(null)
const items = ref<FeeStructureItem[]>([])
const feeHeads = ref<FeeHead[]>([])

const loading = ref(true)
const error = ref('')

const showAddItem = ref(false)
const savingItem = ref(false)
const newItemForm = ref({ fee_head_id: '', amount: 0, frequency: 'once' as any })

const deleteTarget = ref<FeeStructureItem | null>(null)

onMounted(async () => {
  try {
    const [stRes, itRes, fhRes] = await Promise.all([
      feeStructureAPI.retrieve(structureId),
      feeStructureItemAPI.list({ fee_structure_id: structureId }),
      feeHeadAPI.list()
    ])
    structure.value = stRes.data
    items.value = itRes.data.results || (itRes.data as any)
    feeHeads.value = fhRes.data.results || (fhRes.data as any)
  } catch {
    error.value = 'Failed to load details.'
  } finally {
    loading.value = false
  }
})

const handleAddItem = async () => {
  if (!newItemForm.value.fee_head_id || !newItemForm.value.amount) return
  savingItem.value = true
  try {
    const payload = {
      fee_structure_id: structureId,
      ...newItemForm.value
    }
    const res = await feeStructureItemAPI.create(payload)
    items.value.push(res.data)
    showAddItem.value = false
    newItemForm.value = { fee_head_id: '', amount: 0, frequency: 'once' }
  } catch (err: any) {
    alert('Failed to add item')
  } finally {
    savingItem.value = false
  }
}

const confirmDeleteItem = (item: FeeStructureItem) => {
  if(confirm(`Remove ${item.fee_head_name}?`)) {
    feeStructureItemAPI.delete(item.id).then(() => {
      items.value = items.value.filter(x => x.id !== item.id)
    }).catch(() => alert('Failed to remove'))
  }
}
</script>
