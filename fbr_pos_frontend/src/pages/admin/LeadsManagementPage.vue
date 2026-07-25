<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Leads Management</h1>
      <div class="flex gap-4">
        <button @click="markAllRead" class="px-4 py-2 bg-primary text-white rounded-lg hover:opacity-90">
          Mark All Read
        </button>
        <button @click="loadStats" class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300">
          Refresh Stats
        </button>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <div class="bg-white p-4 rounded-lg shadow border">
        <div class="text-sm text-gray-500">Total Leads</div>
        <div class="text-2xl font-bold">{{ stats.total_leads }}</div>
      </div>
      <div class="bg-white p-4 rounded-lg shadow border">
        <div class="text-sm text-gray-500">New Leads</div>
        <div class="text-2xl font-bold text-blue-600">{{ stats.new_leads }}</div>
      </div>
      <div class="bg-white p-4 rounded-lg shadow border">
        <div class="text-sm text-gray-500">Demo Requests</div>
        <div class="text-2xl font-bold text-purple-600">{{ stats.demo_requests }}</div>
      </div>
      <div class="bg-white p-4 rounded-lg shadow border">
        <div class="text-sm text-gray-500">Automation Requests</div>
        <div class="text-2xl font-bold text-green-600">{{ stats.automation_requests }}</div>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white p-4 rounded-lg shadow mb-6">
      <div class="flex flex-wrap gap-4">
        <div>
          <label class="block text-sm font-medium mb-1">Lead Type</label>
          <select v-model="filters.lead_type" class="px-3 py-2 border rounded-lg">
            <option value="">All Types</option>
            <option value="demo_request">Demo Request</option>
            <option value="business_automation">Business Automation</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">Status</label>
          <select v-model="filters.status" class="px-3 py-2 border rounded-lg">
            <option value="">All Status</option>
            <option value="new">New</option>
            <option value="contacted">Contacted</option>
            <option value="in_progress">In Progress</option>
            <option value="converted">Converted</option>
            <option value="closed">Closed</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">Search</label>
          <input v-model="filters.search" type="text" placeholder="Business name, email..." class="px-3 py-2 border rounded-lg">
        </div>
        <div class="flex items-end">
          <button @click="applyFilters" class="px-4 py-2 bg-primary text-white rounded-lg hover:opacity-90">
            Apply Filters
          </button>
        </div>
      </div>
    </div>

    <!-- Leads Table -->
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">Business</th>
            <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">Type</th>
            <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">Contact</th>
            <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">Email</th>
            <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">Phone</th>
            <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">Status</th>
            <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">Created</th>
            <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y">
          <tr v-for="lead in leads" :key="lead.id" class="hover:bg-gray-50">
            <td class="px-4 py-3 font-medium">{{ lead.business_name }}</td>
            <td class="px-4 py-3">
              <span class="px-2 py-1 rounded-full text-xs font-medium"
                :class="lead.lead_type === 'demo_request' ? 'bg-purple-100 text-purple-800' : 'bg-green-100 text-green-800'">
                {{ lead.lead_type === 'demo_request' ? 'Demo' : 'Automation' }}
              </span>
            </td>
            <td class="px-4 py-3">{{ lead.contact_name || '-' }}</td>
            <td class="px-4 py-3">{{ lead.email }}</td>
            <td class="px-4 py-3">{{ lead.phone }}</td>
            <td class="px-4 py-3">
              <select v-model="lead.status" @change="updateLeadStatus(lead)" class="px-2 py-1 border rounded text-sm">
                <option value="new">New</option>
                <option value="contacted">Contacted</option>
                <option value="in_progress">In Progress</option>
                <option value="converted">Converted</option>
                <option value="closed">Closed</option>
              </select>
            </td>
            <td class="px-4 py-3 text-sm text-gray-500">{{ formatDate(lead.created_at) }}</td>
            <td class="px-4 py-3">
              <button @click="viewLead(lead)" class="text-blue-600 hover:text-blue-800 mr-2">View</button>
              <button @click="deleteLead(lead.id)" class="text-red-600 hover:text-red-800">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="loading" class="p-4 text-center text-gray-500">
        Loading...
      </div>
      <div v-if="!loading && leads.length === 0" class="p-4 text-center text-gray-500">
        No leads found
      </div>
    </div>

    <!-- Lead Detail Modal -->
    <div v-if="selectedLead" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" @click.self="selectedLead = null">
      <div class="bg-white rounded-2xl p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="flex justify-between items-center mb-6">
          <h3 class="font-headline-lg text-headline-lg">Lead Details</h3>
          <button @click="selectedLead = null" class="text-on-surface-variant hover:text-on-surface">
            <span class="material-symbols-outlined">close</span>
          </button>
        </div>
        <div class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-500">Business Name</label>
              <div class="font-medium">{{ selectedLead.business_name }}</div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-500">Lead Type</label>
              <div class="font-medium">{{ selectedLead.lead_type === 'demo_request' ? 'Demo Request' : 'Business Automation' }}</div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-500">Contact Name</label>
              <div class="font-medium">{{ selectedLead.contact_name || '-' }}</div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-500">Email</label>
              <div class="font-medium">{{ selectedLead.email }}</div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-500">Phone</label>
              <div class="font-medium">{{ selectedLead.phone }}</div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-500">CNIC</label>
              <div class="font-medium">{{ selectedLead.cnic || '-' }}</div>
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-500">Address</label>
            <div class="font-medium">{{ selectedLead.address || '-' }}</div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-500">Message</label>
            <div class="font-medium">{{ selectedLead.message || '-' }}</div>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-500">Status</label>
              <div class="font-medium">{{ selectedLead.status }}</div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-500">Created At</label>
              <div class="font-medium">{{ formatDate(selectedLead.created_at) }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { publicAPI, type Lead } from '@/apis/public/publicAPI'

const leads = ref<Lead[]>([])
const selectedLead = ref<Lead | null>(null)
const loading = ref(false)
const stats = ref({
  total_leads: 0,
  new_leads: 0,
  demo_requests: 0,
  automation_requests: 0
})

const filters = ref({
  lead_type: '',
  status: '',
  search: ''
})

const loadLeads = async () => {
  loading.value = true
  try {
    const params: any = {}
    if (filters.value.lead_type) params.lead_type = filters.value.lead_type
    if (filters.value.status) params.status = filters.value.status
    if (filters.value.search) params.search = filters.value.search
    
    const response = await publicAPI.getLeads(params)
    leads.value = response.data.results
  } catch (error) {
    console.error('Failed to load leads:', error)
  } finally {
    loading.value = false
  }
}

const loadStats = async () => {
  try {
    const response = await publicAPI.getLeadStats()
    stats.value = response.data
  } catch (error) {
    console.error('Failed to load stats:', error)
  }
}

const applyFilters = () => {
  loadLeads()
}

const updateLeadStatus = async (lead: Lead) => {
  try {
    await publicAPI.updateLead(lead.id, { status: lead.status })
  } catch (error) {
    console.error('Failed to update lead status:', error)
    alert('Failed to update status')
  }
}

const viewLead = (lead: Lead) => {
  selectedLead.value = lead
}

const deleteLead = async (id: string) => {
  if (!confirm('Are you sure you want to delete this lead?')) return
  
  try {
    await publicAPI.deleteLead(id)
    leads.value = leads.value.filter(l => l.id !== id)
    await loadStats()
  } catch (error) {
    console.error('Failed to delete lead:', error)
    alert('Failed to delete lead')
  }
}

const markAllRead = async () => {
  try {
    await publicAPI.markAllRead()
    alert('All notifications marked as read')
  } catch (error) {
    console.error('Failed to mark all as read:', error)
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  loadLeads()
  loadStats()
})
</script>
