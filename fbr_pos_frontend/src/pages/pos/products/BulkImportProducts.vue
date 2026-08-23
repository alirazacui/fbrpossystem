<template>
  <div class="h-full flex flex-col bg-gray-50">
    <!-- Header -->
    <div class="px-8 py-5 border-b border-gray-200 bg-white sticky top-0 z-10 flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Bulk Import Products</h1>
        <p class="text-sm text-gray-500 mt-0.5">Upload an Excel (.xlsx) or CSV file to import multiple products at once.</p>
      </div>
      <div class="flex gap-3">
        <button @click="downloadTemplate" class="px-4 py-2 border border-teal-600 text-teal-600 bg-white rounded-md text-sm font-semibold hover:bg-teal-50 transition-colors flex items-center gap-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
          Download Template
        </button>
        <button @click="$router.back()" class="px-4 py-2 border border-gray-300 text-gray-700 bg-white rounded-md text-sm font-semibold hover:bg-gray-50 transition-colors">
          Cancel
        </button>
      </div>
    </div>

    <div class="flex-1 overflow-auto px-8 py-6 space-y-6">

      <!-- STEP 1: Upload File -->
      <section v-if="step === 'upload'" class="bg-white rounded-lg border border-gray-200 shadow-sm p-8">
        <h2 class="text-lg font-bold text-gray-800 mb-1">Step 1: Upload Your File</h2>
        <p class="text-sm text-gray-500 mb-6">Supported formats: <strong>.xlsx</strong> (Excel) and <strong>.csv</strong>. Maximum 500 products, 5 MB.</p>

        <!-- Drop zone -->
        <div
          class="border-2 border-dashed rounded-xl p-12 text-center transition-colors cursor-pointer"
          :class="isDragging ? 'border-teal-400 bg-teal-50' : 'border-gray-300 hover:border-teal-400 hover:bg-gray-50'"
          @dragover.prevent="isDragging = true"
          @dragleave.prevent="isDragging = false"
          @drop.prevent="handleDrop"
          @click="triggerFileInput"
        >
          <input ref="fileInputRef" type="file" accept=".xlsx,.csv" class="hidden" @change="handleFileSelect" />
          <div class="flex flex-col items-center gap-3">
            <div class="w-14 h-14 rounded-full bg-teal-50 flex items-center justify-center">
              <svg class="w-7 h-7 text-teal-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
              </svg>
            </div>
            <div>
              <p class="text-base font-semibold text-gray-700">Drag & drop your file here</p>
              <p class="text-sm text-gray-500">or <span class="text-teal-600 font-semibold">click to browse</span></p>
            </div>
            <p v-if="selectedFile" class="mt-2 text-sm font-medium text-teal-700 bg-teal-50 px-3 py-1.5 rounded-lg border border-teal-200">
              📄 {{ selectedFile.name }} ({{ formatFileSize(selectedFile.size) }})
            </p>
          </div>
        </div>

        <!-- Column guide -->
        <div class="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
          <p class="text-sm font-semibold text-blue-800 mb-2">📋 Required & Optional Columns</p>
          <div class="grid grid-cols-2 md:grid-cols-3 gap-2 text-xs">
            <div v-for="col in columnGuide" :key="col.name" class="flex items-center gap-1.5">
              <span :class="col.required ? 'bg-red-100 text-red-700' : 'bg-gray-100 text-gray-600'" class="px-1.5 py-0.5 rounded text-xs font-mono">{{ col.required ? '★' : '○' }}</span>
              <span class="text-gray-700">{{ col.name }}</span>
            </div>
          </div>
          <p class="text-xs text-blue-600 mt-2">★ = Required &nbsp;&nbsp; ○ = Optional (has default value)</p>
        </div>

        <div class="mt-6 flex justify-end">
          <button
            @click="parseFile"
            :disabled="!selectedFile || parsing"
            class="px-6 py-2.5 bg-teal-600 text-white rounded-md text-sm font-semibold hover:bg-teal-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
          >
            <svg v-if="parsing" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
            {{ parsing ? 'Analyzing file...' : 'Analyze & Preview →' }}
          </button>
        </div>
      </section>

      <!-- STEP 2: Preview & Confirm -->
      <section v-if="step === 'preview'" class="space-y-4">
        <!-- Summary cards -->
        <div class="grid grid-cols-3 gap-4">
          <div class="bg-white rounded-lg border border-gray-200 shadow-sm p-5 text-center">
            <p class="text-3xl font-bold text-gray-900">{{ parseResult.total_rows }}</p>
            <p class="text-sm text-gray-500 mt-1">Total Rows</p>
          </div>
          <div class="bg-white rounded-lg border border-green-200 shadow-sm p-5 text-center">
            <p class="text-3xl font-bold text-green-600">{{ parseResult.valid_rows }}</p>
            <p class="text-sm text-gray-500 mt-1">✅ Ready to Import</p>
          </div>
          <div class="bg-white rounded-lg border shadow-sm p-5 text-center" :class="parseResult.invalid_rows > 0 ? 'border-red-200' : 'border-gray-200'">
            <p class="text-3xl font-bold" :class="parseResult.invalid_rows > 0 ? 'text-red-600' : 'text-gray-400'">{{ parseResult.invalid_rows }}</p>
            <p class="text-sm text-gray-500 mt-1">{{ parseResult.invalid_rows > 0 ? '❌ Has Errors' : '🎉 No Errors' }}</p>
          </div>
        </div>

        <!-- Filter tabs -->
        <div class="bg-white rounded-lg border border-gray-200 shadow-sm">
          <div class="flex border-b border-gray-200">
            <button
              v-for="tab in ['all', 'valid', 'invalid']" :key="tab"
              @click="filterTab = tab"
              :class="filterTab === tab ? 'border-b-2 border-teal-600 text-teal-600' : 'text-gray-500 hover:text-gray-700'"
              class="px-5 py-3 text-sm font-medium capitalize transition-colors"
            >
              {{ tab === 'all' ? `All (${parseResult.total_rows})` : tab === 'valid' ? `Ready (${parseResult.valid_rows})` : `Errors (${parseResult.invalid_rows})` }}
            </button>
          </div>

          <!-- Preview table -->
          <div class="overflow-x-auto">
            <table class="min-w-full text-sm">
              <thead>
                <tr class="bg-gray-50 text-left">
                  <th class="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider w-12">#</th>
                  <th class="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Status</th>
                  <th class="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Name</th>
                  <th class="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Sale Price</th>
                  <th class="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Tax</th>
                  <th class="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">HS Code</th>
                  <th class="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Category</th>
                  <th class="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Stock</th>
                  <th class="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Errors</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr
                  v-for="row in filteredRows" :key="row.row_number"
                  :class="row.status === 'invalid' ? 'bg-red-50' : 'hover:bg-gray-50'"
                >
                  <td class="px-4 py-3 text-gray-400 text-xs">{{ row.row_number }}</td>
                  <td class="px-4 py-3">
                    <span :class="row.status === 'valid' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'" class="px-2 py-0.5 rounded-full text-xs font-semibold">
                      {{ row.status === 'valid' ? '✅ Ready' : '❌ Error' }}
                    </span>
                  </td>
                  <td class="px-4 py-3 font-medium text-gray-900">{{ row.data.name || '—' }}</td>
                  <td class="px-4 py-3 text-gray-700">{{ row.data.selling_price || '—' }}</td>
                  <td class="px-4 py-3 text-gray-700">{{ row.data.tax_rate_percent || '—' }}</td>
                  <td class="px-4 py-3 font-mono text-xs text-gray-600">{{ row.data.hs_code || '—' }}</td>
                  <td class="px-4 py-3 text-gray-600">{{ row.data.category_name || '—' }}</td>
                  <td class="px-4 py-3 text-gray-600">{{ row.data.current_stock || '0' }}</td>
                  <td class="px-4 py-3 text-xs text-red-600 max-w-xs">
                    <ul v-if="row.errors.length" class="list-disc list-inside space-y-0.5">
                      <li v-for="err in row.errors" :key="err">{{ err }}</li>
                    </ul>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Action bar -->
        <div class="bg-white rounded-lg border border-gray-200 shadow-sm p-4 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <button @click="step = 'upload'; parseResult = null; selectedFile = null" class="px-4 py-2 border border-gray-300 text-gray-700 bg-white rounded-md text-sm font-semibold hover:bg-gray-50 transition-colors">
              ← Upload Different File
            </button>
            <label v-if="parseResult.invalid_rows > 0" class="flex items-center gap-2 text-sm text-gray-600 cursor-pointer">
              <input type="checkbox" v-model="skipErrors" class="rounded text-teal-600" />
              Skip rows with errors (import only {{ parseResult.valid_rows }} valid rows)
            </label>
          </div>
          <button
            @click="startImport"
            :disabled="parseResult.valid_rows === 0 || (!skipErrors && parseResult.invalid_rows > 0)"
            class="px-6 py-2.5 bg-teal-600 text-white rounded-md text-sm font-semibold hover:bg-teal-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Start Import ({{ skipErrors || parseResult.invalid_rows === 0 ? parseResult.valid_rows : parseResult.total_rows }} products) →
          </button>
        </div>
      </section>

      <!-- STEP 3: Live Import Progress -->
      <section v-if="step === 'importing'" class="bg-white rounded-lg border border-gray-200 shadow-sm p-6 space-y-5">
        <div class="flex items-center justify-between">
          <h2 class="text-lg font-bold text-gray-800">Importing Products...</h2>
          <span class="text-sm text-gray-500">{{ importProgress.done }} / {{ importProgress.total }}</span>
        </div>

        <!-- Progress bar -->
        <div class="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
          <div
            class="h-3 rounded-full transition-all duration-300"
            :class="importProgress.failed > 0 ? 'bg-amber-500' : 'bg-teal-500'"
            :style="{ width: `${Math.round((importProgress.done / importProgress.total) * 100)}%` }"
          />
        </div>

        <!-- Live log -->
        <div ref="logContainer" class="bg-gray-900 rounded-lg p-4 h-72 overflow-y-auto font-mono text-xs space-y-1">
          <div
            v-for="(entry, idx) in importLog" :key="idx"
            :class="{
              'text-green-400': entry.type === 'success',
              'text-red-400':   entry.type === 'error',
              'text-yellow-400': entry.type === 'info',
              'text-gray-400':  entry.type === 'done',
            }"
          >
            {{ entry.message }}
          </div>
        </div>

        <!-- Mini summary while running -->
        <div class="flex gap-6 text-sm">
          <span class="text-green-600 font-semibold">✅ {{ importProgress.success }} Succeeded</span>
          <span class="text-red-600 font-semibold">❌ {{ importProgress.failed }} Failed</span>
          <span class="text-gray-400">⏳ {{ importProgress.total - importProgress.done }} Remaining</span>
        </div>
      </section>

      <!-- STEP 4: Done -->
      <section v-if="step === 'done'" class="bg-white rounded-lg border border-gray-200 shadow-sm p-8 text-center space-y-4">
        <div class="w-16 h-16 rounded-full mx-auto flex items-center justify-center" :class="importProgress.failed === 0 ? 'bg-green-100' : 'bg-amber-100'">
          <span class="text-3xl">{{ importProgress.failed === 0 ? '🎉' : '⚠️' }}</span>
        </div>
        <h2 class="text-xl font-bold text-gray-900">Import Complete</h2>
        <div class="flex justify-center gap-8 text-sm">
          <div class="text-center">
            <p class="text-2xl font-bold text-green-600">{{ importProgress.success }}</p>
            <p class="text-gray-500">Products Added</p>
          </div>
          <div class="text-center">
            <p class="text-2xl font-bold text-red-600">{{ importProgress.failed }}</p>
            <p class="text-gray-500">Failed</p>
          </div>
        </div>
        <p v-if="importProgress.failed === 0" class="text-gray-500">All products were imported successfully!</p>
        <p v-else class="text-amber-600 text-sm">{{ importProgress.failed }} product(s) could not be imported. Review the log above for details.</p>
        <div class="flex justify-center gap-3 pt-2">
          <button @click="goToProducts" class="px-6 py-2.5 bg-teal-600 text-white rounded-md text-sm font-semibold hover:bg-teal-700 transition-colors">
            View Products →
          </button>
          <button @click="resetAll" class="px-4 py-2.5 border border-gray-300 text-gray-700 rounded-md text-sm font-semibold hover:bg-gray-50 transition-colors">
            Import More
          </button>
        </div>
      </section>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import axiosInstance from '@/apis/axiosInstance'
import { categoriesAPI } from '@/apis/pos/categories/categoriesAPI'

const router = useRouter()

// ── State ────────────────────────────────────────────────────────────────────
const step = ref<'upload' | 'preview' | 'importing' | 'done'>('upload')
const isDragging = ref(false)
const selectedFile = ref<File | null>(null)
const parsing = ref(false)
const parseResult = ref<any>(null)
const filterTab = ref<'all' | 'valid' | 'invalid'>('all')
const skipErrors = ref(false)
const fileInputRef = ref<HTMLInputElement | null>(null)
const logContainer = ref<HTMLElement | null>(null)

const importProgress = ref({ total: 0, done: 0, success: 0, failed: 0 })
const importLog = ref<{ type: string; message: string }[]>([])

// ── Column guide for UI hint ──────────────────────────────────────────────────
const columnGuide = [
  { name: 'Name',                required: true  },
  { name: 'Selling Price',       required: true  },
  { name: 'Tax Rate',            required: false },
  { name: 'HS Code / PCT Code',  required: false },
  { name: 'Sale Type',           required: false },
  { name: 'SRO Schedule',        required: false },
  { name: 'SRO Serial No',       required: false },
  { name: 'Retail Price (FBR)',  required: false },
  { name: 'Cost Price',          required: false },
  { name: 'Barcode',             required: false },
  { name: 'SKU',                 required: false },
  { name: 'Category',            required: false },
  { name: 'Initial Stock',       required: false },
  { name: 'Unit of Measure',     required: false },
  { name: 'Reorder Level',       required: false },
  { name: 'Description',         required: false },
]

// ── Filtered rows for preview table ──────────────────────────────────────────
const filteredRows = computed(() => {
  if (!parseResult.value) return []
  if (filterTab.value === 'valid') return parseResult.value.rows.filter((r: any) => r.status === 'valid')
  if (filterTab.value === 'invalid') return parseResult.value.rows.filter((r: any) => r.status === 'invalid')
  return parseResult.value.rows
})

// ── File handling ─────────────────────────────────────────────────────────────
const triggerFileInput = () => fileInputRef.value?.click()

const handleFileSelect = (e: Event) => {
  const input = e.target as HTMLInputElement
  if (input.files?.[0]) selectedFile.value = input.files[0]
}

const handleDrop = (e: DragEvent) => {
  isDragging.value = false
  const file = e.dataTransfer?.files[0]
  if (file) selectedFile.value = file
}

const formatFileSize = (bytes: number) => {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`
}

// ── Parse file (call Django endpoint) ────────────────────────────────────────
const parseFile = async () => {
  if (!selectedFile.value) return
  parsing.value = true
  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    const res = await axiosInstance.post('/products/parse-bulk/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    parseResult.value = res.data
    filterTab.value = parseResult.value.invalid_rows > 0 ? 'invalid' : 'all'
    step.value = 'preview'
  } catch (err: any) {
    const msg = err?.response?.data?.detail || 'Failed to parse file. Please check the format and try again.'
    alert(`❌ ${msg}`)
  } finally {
    parsing.value = false
  }
}

// ── Start import loop ─────────────────────────────────────────────────────────
const startImport = async () => {
  const rowsToImport = skipErrors.value
    ? parseResult.value.rows.filter((r: any) => r.status === 'valid')
    : parseResult.value.rows

  importProgress.value = { total: rowsToImport.length, done: 0, success: 0, failed: 0 }
  importLog.value = []
  step.value = 'importing'

  // Pre-load categories so we can resolve category_name → ID
  let categoryMap: Record<string, number> = {}
  try {
    const cats = await categoriesAPI.fetchCategories()
    cats.forEach((c: any) => { categoryMap[c.name.toLowerCase()] = c.id })
  } catch (_) {
    addLog('info', '⚠ Could not load categories — category field will be skipped.')
  }

  addLog('info', `🚀 Starting import of ${rowsToImport.length} products...`)

  for (const row of rowsToImport) {
    const data = row.data
    const rowLabel = `Row ${row.row_number} — "${data.name || 'Unnamed'}"`

    try {
      const payload = buildPayload(data, categoryMap)
      await axiosInstance.post('/products/', payload)
      importProgress.value.success++
      addLog('success', `✅ ${rowLabel} — Added successfully`)
    } catch (err: any) {
      importProgress.value.failed++
      const errMsg = extractError(err)
      addLog('error', `❌ ${rowLabel} — ${errMsg}`)
    }

    importProgress.value.done++
    await scrollLog()
  }

  const { success, failed } = importProgress.value
  addLog('done', ``)
  addLog('done', `═══════════════════════════════`)
  addLog('done', `Import complete: ${success} succeeded, ${failed} failed.`)
  step.value = 'done'
}

// ── Build API payload from parsed row ────────────────────────────────────────
const buildPayload = (data: Record<string, string>, categoryMap: Record<string, number>) => {
  const payload: Record<string, any> = {
    name:             (data.name || '').trim(),
    selling_price:    parseFloat(data.selling_price) || 0,
    cost_price:       data.cost_price ? parseFloat(data.cost_price) : 0,
    tax_rate_percent: data.tax_rate_percent || '18%',
    fbr_sale_type:    data.fbr_sale_type || 'Goods at standard rate (default)',
    unit_of_measure:  data.unit_of_measure || 'Numbers, pieces, units',
    current_stock:    parseFloat(data.current_stock) || 0,
    is_active:        true,
  }

  if (data.hs_code)                payload.hs_code                = data.hs_code
  if (data.barcode)                payload.barcode                = data.barcode
  if (data.sku)                    payload.sku                    = data.sku
  if (data.description)            payload.description            = data.description
  if (data.fbr_sro_schedule_no)    payload.fbr_sro_schedule_no    = data.fbr_sro_schedule_no
  if (data.fbr_sro_item_serial_no) payload.fbr_sro_item_serial_no = data.fbr_sro_item_serial_no
  if (data.fbr_fixed_retail_price && parseFloat(data.fbr_fixed_retail_price) > 0)
    payload.fbr_fixed_retail_price = parseFloat(data.fbr_fixed_retail_price)
  if (data.low_stock_threshold && parseFloat(data.low_stock_threshold) > 0)
    payload.low_stock_threshold = parseFloat(data.low_stock_threshold)
  if (data.track_inventory) {
    const tv = data.track_inventory.toLowerCase()
    payload.track_inventory = ['true', 'yes', '1'].includes(tv)
  }

  if (data.category_name) {
    const catId = categoryMap[data.category_name.toLowerCase()]
    if (catId) payload.category = catId
  }

  return payload
}

const extractError = (err: any): string => {
  const d = err?.response?.data
  if (!d) return 'Network error'
  if (typeof d === 'string') return d
  if (d.detail) return d.detail
  // DRF field errors
  const fieldErrors = Object.entries(d)
    .map(([field, msgs]) => `${field}: ${Array.isArray(msgs) ? msgs[0] : msgs}`)
    .join('; ')
  return fieldErrors || 'Unknown error'
}

// ── Log helpers ───────────────────────────────────────────────────────────────
const addLog = (type: string, message: string) => {
  importLog.value.push({ type, message })
}

const scrollLog = async () => {
  await nextTick()
  if (logContainer.value) {
    logContainer.value.scrollTop = logContainer.value.scrollHeight
  }
}

// ── Download template ─────────────────────────────────────────────────────────
const downloadTemplate = () => {
  const rows: string[][] = [
    ['Name','Selling Price','Cost Price','Tax Rate','HS Code / PCT Code','Sale Type','SRO Schedule','SRO Serial No','Retail Price (FBR)','Barcode','SKU','Category','Initial Stock','Reorder Level','Unit of Measure','Description'],
    ['Pepsi 1.5L','150','100','18%','2202.1000','Goods at standard rate (default)','','','','12345','PEP-1.5L','Beverages','50','10','Numbers, pieces, units',''],
    ['Consulting Service','5000','3000','5%','','Services','','','','','SERV-001','Services','0','','Service','Professional consulting'],
    ['Branded Shirt','2500','1800','18%','6205.2000','3rd Schedule Goods','','','3000','','SHIRT-L','Clothing','100','20','Piece',''],
    [],
    ['--- VALID SALE TYPE VALUES (copy-paste exactly) ---'],
    ['Goods at standard rate (default)'],['3rd Schedule Goods'],['Goods at Reduced Rate'],
    ['Goods at zero-rate'],['Exempt Goods'],['Services'],['Electric Vehicle'],['Mobile Phones'],
    ['CNG Sales'],['Petroleum Products'],['Cement /Concrete Block'],['Cotton Ginners'],
    ['Electricity Supply to Retailers'],['Gas to CNG stations'],['Goods (FED in ST Mode)'],
    ['Non-Adjustable Supplies'],['Potassium Chlorate'],['Processing/ Conversion of Goods'],
    ['Services (FED in ST Mode)'],['Ship breaking'],['Steel Melting and re-rolling'],
    ['Telecommunication services'],['Toll Manufacturing'],
    [],
    ['--- VALID TAX RATE VALUES ---'],
    ['18%'],['17%'],['16%'],['15%'],['8%'],['5%'],['0%'],['Exempt'],
    [],
    ['--- COMMON UNIT OF MEASURE VALUES ---'],
    ['Numbers, pieces, units'],['KG'],['Gram'],['Litre'],['Metre'],['Box'],['Carton'],
    ['Bag'],['Bottle'],['Dozen'],['Pair'],['Set'],['Pack'],['Piece'],['Service'],['Ton'],
  ]
  const csvContent = rows.map(r =>
    r.map(c => `"${String(c).replace(/"/g, '""')}"`).join(',')
  ).join('\n')
  const blob = new Blob(['\uFEFF' + csvContent], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'product_import_template.csv'
  a.click()
  URL.revokeObjectURL(url)
}

const goToProducts = () => router.push('/pos/products')
const resetAll = () => {
  step.value = 'upload'
  selectedFile.value = null
  parseResult.value = null
  importLog.value = []
  importProgress.value = { total: 0, done: 0, success: 0, failed: 0 }
  filterTab.value = 'all'
  skipErrors.value = false
}
</script>
