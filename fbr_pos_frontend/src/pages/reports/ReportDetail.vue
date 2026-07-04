<template>
  <ReportLayout
    :title="reportTitle"
    :row-count="results.length"
    :loading="loading"
    hint="limit, additional_filters"
    @run="handleRun"
    @export="handleExport"
  >
    <!-- Placeholder Table -->
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr v-if="results.length > 0">
          <th v-for="(value, key) in results[0]" :key="key" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            {{ key }}
          </th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        <tr v-for="(row, index) in results" :key="index" class="hover:bg-gray-50">
          <td v-for="(value, key) in row" :key="key" class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
            {{ value }}
          </td>
        </tr>
      </tbody>
    </table>
  </ReportLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import ReportLayout from '@/components/reports/ReportLayout.vue'
import axiosInstance from '@/apis/axiosInstance'

const route = useRoute()
const reportId = route.params.id as string

const reportTitle = computed(() => {
  return reportId.replace(/-/g, ' ')
})

const results = ref<any[]>([])
const loading = ref(false)

const handleRun = async (filters: any) => {
  loading.value = true
  try {
    const params = new URLSearchParams()
    if (filters.from) params.append('from', filters.from)
    if (filters.to) params.append('to', filters.to)
    
    // Some reports may not have backend endpoints yet, handle gracefully
    const response = await axiosInstance.get(`/reports/${reportId}/?${params.toString()}`)
    results.value = response.data
  } catch (error: any) {
    if (error.response?.status === 404) {
      // Endpoint not implemented yet
      alert(`Backend integration for ${reportTitle.value} is coming soon!`)
      results.value = []
    } else {
      console.error('Report failed:', error)
      alert('Failed to load report data')
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  handleRun({})
})

const handleExport = (type: string) => {
  if (results.value.length === 0) {
    alert('No data to export.')
    return
  }

  if (type === 'csv' || type === 'excel') {
    const headers = Object.keys(results.value[0])
    const csvContent = [
      headers.join(','),
      ...results.value.map(row => 
        headers.map(header => {
          let cell = row[header] === null || row[header] === undefined ? '' : row[header].toString()
          cell = cell.replace(/"/g, '""')
          if (cell.search(/("|,|\n)/g) >= 0) cell = `"${cell}"`
          return cell
        }).join(',')
      )
    ].join('\n')

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
    const url = URL.createObjectURL(blob)
    const downloadLink = document.createElement('a')
    downloadLink.href = url
    downloadLink.setAttribute('download', `${reportTitle.value.replace(/ /g, '_')}_export.csv`)
    document.body.appendChild(downloadLink)
    downloadLink.click()
    document.body.removeChild(downloadLink)
  } else if (type === 'pdf') {
    window.print()
  } else {
    alert(`Export to ${type} coming soon!`)
  }
}
</script>
