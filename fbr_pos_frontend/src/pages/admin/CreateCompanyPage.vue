<template>
  <div class="space-y-6 pb-12">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Add New Business</h1>
        <p class="text-gray-600 mt-1">Fill in all details to onboard a new tenant</p>
      </div>
      <button
        @click="goBack"
        class="px-4 py-2 text-gray-600 hover:text-gray-900 flex items-center space-x-2"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <!-- Form -->
    <form @submit.prevent="submitForm" class="space-y-6">
      <!-- Section 1: Basic Information -->
      <div class="bg-white rounded-lg shadow p-8">
        <h2 class="text-xl font-bold text-gray-900 mb-6 pb-4 border-b border-gray-200">Basic Information</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Business Name -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Business Name *</label>
            <input
              v-model="form.business_name"
              type="text"
              placeholder="ABC Trading Company"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
              required
            />
            <p v-if="errors.business_name" class="text-red-600 text-sm mt-1">{{ errors.business_name }}</p>
          </div>

          <!-- NTN -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">NTN / CNIC *</label>
            <input
              v-model="form.ntn"
              type="text"
              placeholder="1234567 or 13-digit CNIC"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
              required
            />
            <p v-if="errors.ntn" class="text-red-600 text-sm mt-1">{{ errors.ntn }}</p>
          </div>

          <!-- STRN -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">STRN (Optional)</label>
            <input
              v-model="form.strn"
              type="text"
              placeholder="1234567890123"
              maxlength="17"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
            />
          </div>

          <!-- Owner CNIC -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Owner CNIC (Format: 00000-0000000-0) *</label>
            <input
              v-model="form.owner_cnic"
              type="text"
              placeholder="12345-0000000-0"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
              required
            />
            <p v-if="errors.owner_cnic" class="text-red-600 text-sm mt-1">{{ errors.owner_cnic }}</p>
          </div>
        </div>
      </div>

      <!-- Section 2: FBR & Regulatory Information -->
      <div class="bg-white rounded-lg shadow p-8">
        <h2 class="text-xl font-bold text-gray-900 mb-6 pb-4 border-b border-gray-200">FBR & Regulatory</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Business Mode -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Business Mode *</label>
            <select
              v-model="form.business_mode"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
              required
            >
              <option value="">Select Mode</option>
              <option value="pos_only">POS Only</option>
              <option value="di_only">Digital Invoicing Only</option>
              <option value="both">POS + Digital Invoicing</option>
            </select>
          </div>

          <!-- FBR Sector -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">FBR Sector *</label>
            <select
              v-model="form.fbr_sector"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
              required
            >
              <option value="">Select Sector</option>
              <option value="wholesale_retails">Wholesale / Retails</option>
              <option value="cement_concrete">Cement or Concrete Blocks</option>
              <option value="mobile">Mobile</option>
              <option value="pharmaceuticals">Pharmaceuticals</option>
              <option value="cng_stations">CNG Stations</option>
              <option value="automobile">Automobile</option>
              <option value="services">Services</option>
              <option value="gas_distribution">Gas Distribution</option>
              <option value="electricity">Electricity Distribution</option>
              <option value="petroleum">Petroleum</option>
              <option value="telecom">Telecom</option>
              <option value="textile">Textile</option>
              <option value="fmcg">FMCG</option>
              <option value="steel">Steel</option>
              <option value="potassium_chlorate">Potassium Chlorate</option>
              <option value="all_other">All Other Sectors</option>
            </select>
            <p v-if="errors.fbr_sector" class="text-red-600 text-sm mt-1">{{ errors.fbr_sector }}</p>
          </div>
        </div>

        <!-- FBR Business Nature -->
        <div class="mt-6">
          <label class="block text-sm font-medium text-gray-700 mb-3">FBR Business Nature (Select at least 1) *</label>
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            <label v-for="nature in businessNatures" :key="nature.value" class="flex items-center space-x-3 cursor-pointer">
              <input
                type="checkbox"
                :value="nature.value"
                v-model="form.fbr_business_nature"
                class="w-4 h-4 text-teal-600 rounded accent-teal-600"
              />
              <span class="text-sm text-gray-700">{{ nature.label }}</span>
            </label>
          </div>
          <p v-if="errors.fbr_business_nature" class="text-red-600 text-sm mt-2">{{ errors.fbr_business_nature }}</p>
        </div>
      </div>

      <!-- Section 3: Business Classification -->
      <div class="bg-white rounded-lg shadow p-8">
        <h2 class="text-xl font-bold text-gray-900 mb-6 pb-4 border-b border-gray-200">Business Classification</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Vertical -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Business Vertical *</label>
            <select
              v-model="form.vertical"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
              required
            >
              <option value="">Select Vertical</option>
              <option value="grocery">Grocery Store</option>
              <option value="general_store">General Store</option>
              <option value="restaurant">Restaurant / F&B</option>
              <option value="pharmacy">Pharmacy</option>
              <option value="electronics">Electronics</option>
              <option value="clothing">Clothing / Apparel</option>
              <option value="wholesale">Wholesale</option>
              <option value="other">Other</option>
            </select>
          </div>

          <!-- Subscription Plan -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Subscription Plan</label>
            <select
              v-model="form.subscription_plan"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
            >
              <option value="">No Plan</option>
              <option v-for="plan in subscriptionPlans" :key="plan.id" :value="plan.code">
                {{ plan.name }} ({{ plan.price_per_month === 0 ? 'Free' : `Rs ${plan.price_per_month}/mo` }})
              </option>
            </select>
          </div>
        </div>
      </div>

      <!-- Section 4: Contact & Branding -->
      <div class="bg-white rounded-lg shadow p-8">
        <h2 class="text-xl font-bold text-gray-900 mb-6 pb-4 border-b border-gray-200">Contact & Branding</h2>
        
        <div class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Business Logo</label>
            <input
              type="file"
              accept="image/*"
              @change="onLogoChange"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
            />
            <p class="text-xs text-gray-500 mt-1">Optional. Recommended size: square image (PNG/JPG).</p>
            <div v-if="logoPreview" class="mt-3">
              <img :src="logoPreview" alt="Logo preview" class="h-20 w-20 rounded-lg border border-gray-200 object-cover" />
            </div>
          </div>

          <!-- Address -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Business Address *</label>
            <textarea
              v-model="form.address"
              placeholder="Street address, city, province, postal code"
              rows="3"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
              required
            ></textarea>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Phone -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Phone</label>
              <input
                v-model="form.phone"
                type="tel"
                placeholder="+92 300 1234567"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
              />
            </div>

            <!-- Email -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
              <input
                v-model="form.email"
                type="email"
                placeholder="info@business.com"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
              />
            </div>

            <!-- Website -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Website URL</label>
              <input
                v-model="form.website_url"
                type="url"
                placeholder="https://example.com"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Section 5: Feature Modules -->
      <div class="bg-white rounded-lg shadow p-8">
        <h2 class="text-xl font-bold text-gray-900 mb-6 pb-4 border-b border-gray-200">Feature Modules</h2>
        
        <!-- Forced Modules (Read-only) -->
        <div class="mb-8">
          <h3 class="text-sm font-semibold text-gray-900 mb-4">Forced Modules (Always Enabled)</h3>
          <div class="space-y-3">
            <div class="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
              <input type="checkbox" checked disabled class="w-4 h-4 text-teal-600 rounded" />
              <div>
                <p class="font-medium text-gray-900">Invoices</p>
                <p class="text-sm text-gray-600">Core invoicing system (locked)</p>
              </div>
            </div>
            <div class="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
              <input type="checkbox" checked disabled class="w-4 h-4 text-teal-600 rounded" />
              <div>
                <p class="font-medium text-gray-900">FBR Digital Invoicing</p>
                <p class="text-sm text-gray-600">FBR submission & tokens (locked)</p>
              </div>
            </div>
            <div class="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
              <input type="checkbox" checked disabled class="w-4 h-4 text-teal-600 rounded" />
              <div>
                <p class="font-medium text-gray-900">Customer Database</p>
                <p class="text-sm text-gray-600">Customer management (locked)</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Optional Modules -->
        <div>
          <h3 class="text-sm font-semibold text-gray-900 mb-4">Optional Modules</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <label class="flex items-center space-x-3 cursor-pointer p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition">
              <input
                type="checkbox"
                v-model="form.module_multi_branch"
                class="w-4 h-4 text-teal-600 rounded accent-teal-600"
              />
              <div>
                <p class="font-medium text-gray-900">Multi-Branch</p>
                <p class="text-sm text-gray-600">Multiple locations</p>
              </div>
            </label>

            <label class="flex items-center space-x-3 cursor-pointer p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition">
              <input
                type="checkbox"
                v-model="form.module_terminals_cash_sessions"
                class="w-4 h-4 text-teal-600 rounded accent-teal-600"
              />
              <div>
                <p class="font-medium text-gray-900">Terminals & Cash Sessions</p>
                <p class="text-sm text-gray-600">POS terminal management</p>
              </div>
            </label>

            <label class="flex items-center space-x-3 cursor-pointer p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition">
              <input
                type="checkbox"
                v-model="form.module_user_management"
                class="w-4 h-4 text-teal-600 rounded accent-teal-600"
              />
              <div>
                <p class="font-medium text-gray-900">User Management</p>
                <p class="text-sm text-gray-600">Owner can create staff users</p>
              </div>
            </label>

            <label class="flex items-center space-x-3 cursor-pointer p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition">
              <input
                type="checkbox"
                v-model="form.module_inventory"
                class="w-4 h-4 text-teal-600 rounded accent-teal-600"
              />
              <div>
                <p class="font-medium text-gray-900">Inventory Tracking</p>
                <p class="text-sm text-gray-600">Stock management</p>
              </div>
            </label>

            <label class="flex items-center space-x-3 cursor-pointer p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition">
              <input
                type="checkbox"
                v-model="form.module_warehousing"
                class="w-4 h-4 text-teal-600 rounded accent-teal-600"
              />
              <div>
                <p class="font-medium text-gray-900">Warehousing</p>
                <p class="text-sm text-gray-600">Warehouse management</p>
              </div>
            </label>

            <label class="flex items-center space-x-3 cursor-pointer p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition">
              <input
                type="checkbox"
                v-model="form.module_returns"
                class="w-4 h-4 text-teal-600 rounded accent-teal-600"
              />
              <div>
                <p class="font-medium text-gray-900">Returns</p>
                <p class="text-sm text-gray-600">Customer returns workflow</p>
              </div>
            </label>

            <label class="flex items-center space-x-3 cursor-pointer p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition">
              <input
                type="checkbox"
                v-model="form.module_debit_credit_notes"
                class="w-4 h-4 text-teal-600 rounded accent-teal-600"
              />
              <div>
                <p class="font-medium text-gray-900">Debit / Credit Notes</p>
                <p class="text-sm text-gray-600">Follow-up notes</p>
              </div>
            </label>

            <label class="flex items-center space-x-3 cursor-pointer p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition">
              <input
                type="checkbox"
                v-model="form.module_fbr_amendments"
                class="w-4 h-4 text-teal-600 rounded accent-teal-600"
              />
              <div>
                <p class="font-medium text-gray-900">Manual FBR Amendments</p>
                <p class="text-sm text-gray-600">Amendment workflow</p>
              </div>
            </label>

            <label class="flex items-center space-x-3 cursor-pointer p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition">
              <input
                type="checkbox"
                v-model="form.module_cheque_bank_transfer"
                class="w-4 h-4 text-teal-600 rounded accent-teal-600"
              />
              <div>
                <p class="font-medium text-gray-900">Cheques & Bank Transfers</p>
                <p class="text-sm text-gray-600">Non-cash payments</p>
              </div>
            </label>

            <label class="flex items-center space-x-3 cursor-pointer p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition">
              <input
                type="checkbox"
                v-model="form.module_customer_display"
                class="w-4 h-4 text-teal-600 rounded accent-teal-600"
              />
              <div>
                <p class="font-medium text-gray-900">Customer Display</p>
                <p class="text-sm text-gray-600">Customer-facing monitor</p>
              </div>
            </label>

            <label class="flex items-center space-x-3 cursor-pointer p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition">
              <input
                type="checkbox"
                v-model="form.module_hardware_integration"
                class="w-4 h-4 text-teal-600 rounded accent-teal-600"
              />
              <div>
                <p class="font-medium text-gray-900">Hardware Integration</p>
                <p class="text-sm text-gray-600">Printer, scanner, cash drawer</p>
              </div>
            </label>

            <label class="flex items-center space-x-3 cursor-pointer p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition">
              <input
                type="checkbox"
                v-model="form.module_restaurant_fnb"
                class="w-4 h-4 text-teal-600 rounded accent-teal-600"
              />
              <div>
                <p class="font-medium text-gray-900">Restaurant / F&B</p>
                <p class="text-sm text-gray-600">All restaurant features</p>
              </div>
            </label>

            <label class="flex items-center space-x-3 cursor-pointer p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition">
              <input
                type="checkbox"
                v-model="form.module_advanced_reports"
                class="w-4 h-4 text-teal-600 rounded accent-teal-600"
              />
              <div>
                <p class="font-medium text-gray-900">Advanced Reports</p>
                <p class="text-sm text-gray-600">Detailed analytics</p>
              </div>
            </label>

            <label class="flex items-center space-x-3 cursor-pointer p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition">
              <input
                type="checkbox"
                v-model="form.module_audit_logs"
                class="w-4 h-4 text-teal-600 rounded accent-teal-600"
              />
              <div>
                <p class="font-medium text-gray-900">Audit Logs</p>
                <p class="text-sm text-gray-600">Audit trail viewer</p>
              </div>
            </label>
          </div>
        </div>
      </div>

      <!-- Section 6: FBR Sandbox Scenarios -->
      <div class="bg-white rounded-lg shadow p-8">
        <h2 class="text-xl font-bold text-gray-900 mb-6 pb-4 border-b border-gray-200">FBR Sandbox Scenarios</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <label v-for="(label, key) in sandboxScenarios" :key="key" class="flex items-start space-x-3 cursor-pointer p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition">
            <input
              type="checkbox"
              v-model="form[key]"
              class="w-4 h-4 mt-0.5 text-teal-600 rounded accent-teal-600"
            />
            <span class="text-sm text-gray-700 leading-tight">{{ label }}</span>
          </label>
        </div>
      </div>

      <!-- Sticky Action Bar -->
      <div class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 p-6 shadow-lg">
        <div class="max-w-7xl mx-auto flex items-center justify-between">
          <button
            type="button"
            @click="goBack"
            class="px-6 py-2 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50 transition font-medium"
          >
            Cancel
          </button>

          <div class="flex items-center space-x-4">
            <span v-if="error" class="text-red-600 text-sm font-medium">{{ error }}</span>
            <button
              v-if="!loading"
              type="submit"
              class="px-8 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition font-medium"
            >
              Create Business
            </button>
            <button
              v-else
              disabled
              class="px-8 py-2 bg-teal-400 text-white rounded-lg cursor-not-allowed font-medium flex items-center space-x-2"
            >
              <div class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              <span>Creating...</span>
            </button>
          </div>
        </div>
      </div>
    </form>

    <!-- Bottom Padding for sticky bar -->
    <div class="h-20"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import companyAPI from '@/apis/admin/companyAPI'
import { subscriptionsAPI } from '@/apis/admin/subscriptionsAPI'

const router = useRouter()
const subscriptionPlans = ref<any[]>([])

const form = ref<any>({
  business_name: '',
  ntn: '',
  strn: '',
  owner_cnic: '',
  business_mode: 'pos_only',
  fbr_business_nature: [],
  fbr_sector: '',
  vertical: 'general_store',
  address: '',
  phone: '',
  email: '',
  website_url: '',
  subscription_plan: 'trial',
  module_multi_branch: false,
  module_terminals_cash_sessions: false,
  module_user_management: false,
  module_inventory: false,
  module_warehousing: false,
  module_returns: false,
  module_debit_credit_notes: false,
  module_fbr_amendments: false,
  module_cheque_bank_transfer: false,
  module_customer_display: false,
  module_hardware_integration: false,
  module_restaurant_fnb: false,
  module_advanced_reports: false,
  module_audit_logs: false,
  fbr_scenario_sn001: false,
  fbr_scenario_sn002: false,
  fbr_scenario_sn003: false,
  fbr_scenario_sn004: false,
  fbr_scenario_sn005: false,
  fbr_scenario_sn006: false,
  fbr_scenario_sn007: false,
  fbr_scenario_sn008: false,
  fbr_scenario_sn009: false,
  fbr_scenario_sn010: false,
  fbr_scenario_sn011: false,
  fbr_scenario_sn012: false,
  fbr_scenario_sn013: false,
  fbr_scenario_sn014: false,
  fbr_scenario_sn015: false,
  fbr_scenario_sn016: false,
  fbr_scenario_sn017: false,
  fbr_scenario_sn018: false,
  fbr_scenario_sn019: false,
  fbr_scenario_sn020: false,
  fbr_scenario_sn021: false,
  fbr_scenario_sn022: false,
  fbr_scenario_sn023: false,
  fbr_scenario_sn024: false,
  fbr_scenario_sn025: false,
  fbr_scenario_sn026: false,
  fbr_scenario_sn027: false,
  fbr_scenario_sn028: false,
})

const sandboxScenarios: Record<string, string> = {
  fbr_scenario_sn001: "SN001 · Standard Rate — Registered Buyer",
  fbr_scenario_sn002: "SN002 · Standard Rate — Unregistered Buyer",
  fbr_scenario_sn003: "SN003 · Steel Melted",
  fbr_scenario_sn004: "SN004 · Steel Scrap by Ship Breaker",
  fbr_scenario_sn005: "SN005 · Reduced Rate — Registered Buyer",
  fbr_scenario_sn006: "SN006 · Exempted Goods",
  fbr_scenario_sn007: "SN007 · Zero Rated Goods",
  fbr_scenario_sn008: "SN008 · Third Schedule Goods",
  fbr_scenario_sn009: "SN009 · Purchase from Cotton Grower",
  fbr_scenario_sn010: "SN010 · Telecom Services by Mobile Operators",
  fbr_scenario_sn011: "SN011 · Steel via Toll Manufacturing",
  fbr_scenario_sn012: "SN012 · Petroleum Products",
  fbr_scenario_sn013: "SN013 · Electricity to Retailers",
  fbr_scenario_sn014: "SN014 · Gas to CNG Stations",
  fbr_scenario_sn015: "SN015 · Mobile Phones",
  fbr_scenario_sn016: "SN016 · Processing / Conversion of Goods",
  fbr_scenario_sn017: "SN017 · Goods (FED in ST Mode)",
  fbr_scenario_sn018: "SN018 · Services (FED in ST Mode)",
  fbr_scenario_sn019: "SN019 · Services (ICT Ordinance)",
  fbr_scenario_sn020: "SN020 · Electric Vehicles",
  fbr_scenario_sn021: "SN021 · Cement / Concrete Block",
  fbr_scenario_sn022: "SN022 · Potassium Chloride",
  fbr_scenario_sn023: "SN023 · SNNG Sale",
  fbr_scenario_sn024: "SN024 · Goods per SC004",
  fbr_scenario_sn025: "SN025 · Goods per SRO2971",
  fbr_scenario_sn026: "SN026 · Standard Rate — End Consumer (Retailer)",
  fbr_scenario_sn027: "SN027 · Third Schedule — End Consumer (Retailer)",
  fbr_scenario_sn028: "SN028 · Reduced Rate — End Consumer (Retailer)",
};

const loading = ref(false)
const error = ref('')
const errors = ref<Record<string, string>>({})
const logoFile = ref<File | null>(null)
const logoPreview = ref('')

const businessNatures = [
  { value: 'manufacturer', label: 'Manufacturer' },
  { value: 'importer', label: 'Importer' },
  { value: 'exporter', label: 'Exporter' },
  { value: 'distributor', label: 'Distributor' },
  { value: 'wholesaler', label: 'Wholesaler' },
  { value: 'retailer', label: 'Retailer' },
  { value: 'service_provider', label: 'Service Provider' },
  { value: 'other', label: 'Other' },
]

onMounted(async () => {
  try {
    subscriptionPlans.value = await subscriptionsAPI.getPlans()
    // Select first plan by default if available
    if (subscriptionPlans.value.length > 0) {
      form.value.subscription_plan = subscriptionPlans.value[0].code
    }
  } catch (error) {
    console.error('Failed to fetch subscription plans')
  }
})

const submitForm = async () => {
  loading.value = true
  error.value = ''
  errors.value = {}

  try {
    const payload = new FormData()
    Object.entries(form.value).forEach(([key, value]) => {
      if (Array.isArray(value)) {
        value.forEach((item) => payload.append(key, String(item)))
        return
      }
      if (typeof value === 'boolean') {
        payload.append(key, value ? 'true' : 'false')
        return
      }
      if (value !== null && value !== undefined) {
        payload.append(key, String(value))
      }
    })

    if (logoFile.value) {
      payload.append('logo', logoFile.value)
    }

    await companyAPI.createCompany(payload)
    // Success - redirect to tenants list
    router.push('/admin/tenants')
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to create company'
    
    // Parse field errors
    if (err.response?.data && typeof err.response.data === 'object') {
      Object.entries(err.response.data).forEach(([key, value]: [string, any]) => {
        if (Array.isArray(value)) {
          errors.value[key] = value.join(', ')
        } else if (typeof value === 'string') {
          errors.value[key] = value
        }
      })
    }

    console.error('Company creation error:', err)
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.push('/admin/tenants')
}

const onLogoChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0] || null
  logoFile.value = file
  logoPreview.value = file ? URL.createObjectURL(file) : ''
}
</script>
