<template>
  <div class="min-h-screen bg-gray-50/50 pb-12">
    <!-- Header/Navigation Bar -->
    <div class="bg-white border-b border-gray-200 sticky top-0 z-10 px-6 py-4 shadow-sm">
      <div class="w-full flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <div class="flex items-center gap-3">
            <h1 class="text-2xl font-bold text-gray-900">Customers</h1>
            <span class="px-2.5 py-0.5 text-xs font-semibold bg-indigo-50 text-indigo-700 rounded-full border border-indigo-100">
              {{ pagination.count || 0 }} Total
            </span>
          </div>
          <p class="text-sm text-gray-500 mt-1">Manage customer profiles, credit limits, and FBR tax registrations.</p>
        </div>

        <div class="flex items-center gap-3" v-if="viewMode === 'list'">
          <!-- Search Bar -->
          <div class="relative w-full md:w-80">
            <span class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </span>
            <input
              type="text"
              v-model="searchQuery"
              @input="handleSearch"
              placeholder="Search by name, phone, CNIC, NTN..."
              class="w-full pl-10 pr-4 py-2 bg-gray-50 border border-gray-300 rounded-lg text-sm text-gray-950 focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors"
            />
          </div>

          <!-- Import CSV Button -->
          <button
            @click="openImportModal"
            class="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 transition-all"
          >
            <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
            </svg>
            Import CSV
          </button>

          <!-- New Customer Button -->
          <button
            @click="switchToCreate"
            class="flex items-center gap-2 px-4 py-2 bg-indigo-600 rounded-lg text-sm font-medium text-white hover:bg-indigo-700 shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-all"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            New customer
          </button>
        </div>

        <div class="flex items-center gap-2" v-else>
          <button
            @click="switchToList"
            class="flex items-center gap-1.5 px-3 py-1.5 border border-gray-300 rounded-lg bg-white text-xs font-medium text-gray-700 hover:bg-gray-50 hover:border-gray-400 transition-all"
          >
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back to list
          </button>
        </div>
      </div>
    </div>

    <!-- Alert / Toast Banner -->
    <div class="w-full px-6 mt-4" v-if="alert">
      <div :class="[
        'p-4 rounded-lg flex items-start gap-3 border shadow-sm transition-all duration-300',
        alert.type === 'success' ? 'bg-emerald-50 border-emerald-200 text-emerald-800' : 'bg-rose-50 border-rose-200 text-rose-800'
      ]">
        <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path v-if="alert.type === 'success'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <div class="flex-1">
          <p class="text-sm font-semibold">{{ alert.title }}</p>
          <p class="text-xs opacity-90 mt-0.5">{{ alert.message }}</p>
        </div>
        <button @click="alert = null" class="opacity-65 hover:opacity-100 transition-opacity">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Main Workspace Container -->
    <div class="w-full px-6 mt-6">
      
      <!-- 1. CUSTOMERS LIST VIEW -->
      <div v-if="viewMode === 'list'">
        <!-- Loading State -->
        <div v-if="loading" class="flex flex-col items-center justify-center py-20 bg-white border border-gray-200 rounded-xl shadow-sm">
          <div class="animate-spin rounded-full h-10 w-10 border-4 border-indigo-500 border-t-transparent"></div>
          <p class="text-sm text-gray-500 mt-4 font-medium">Fetching customer database...</p>
        </div>

        <!-- Empty State -->
        <div v-else-if="customers.length === 0" class="flex flex-col items-center justify-center text-center py-20 px-4 bg-white border border-gray-200 rounded-xl shadow-sm">
          <div class="h-16 w-16 bg-gray-50 rounded-full flex items-center justify-center border border-gray-100 shadow-inner">
            <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
          <h3 class="text-lg font-bold text-gray-900 mt-5">No customers yet</h3>
          <p class="text-sm text-gray-500 mt-2 max-w-sm">Add one to start tracking credit, store credit, and generating compliant invoices.</p>
          <div class="flex items-center gap-3 mt-6">
            <button
              @click="switchToCreate"
              class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-sm font-semibold shadow transition-all focus:ring-2 focus:ring-indigo-500/20"
            >
              + New Customer
            </button>
            <button
              @click="openImportModal"
              class="px-4 py-2 border border-gray-300 hover:bg-gray-50 text-gray-700 rounded-lg text-sm font-semibold transition-all"
            >
              Import CSV
            </button>
          </div>
        </div>

        <!-- Customers Table Grid -->
        <div v-else class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200 table-fixed">
              <thead class="bg-gray-50/70 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
                <tr>
                  <th scope="col" class="px-6 py-4 w-1/4">Customer</th>
                  <th scope="col" class="px-6 py-4 w-1/5">Contact</th>
                  <th scope="col" class="px-6 py-4 w-1/6">Registration</th>
                  <th scope="col" class="px-6 py-4 w-1/6">CNIC / NTN</th>
                  <th scope="col" class="px-6 py-4 w-1/8 text-right">Credit Limit</th>
                  <th scope="col" class="px-6 py-4 w-1/12 text-center">Status</th>
                  <th scope="col" class="px-6 py-4 w-1/8 text-right pr-6">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100 text-sm text-gray-600 bg-white">
                <tr
                  v-for="customer in customers"
                  :key="customer.id"
                  :class="['hover:bg-gray-50/60 transition-colors', customer.is_walk_in ? 'bg-indigo-50/20' : '']"
                >
                  <td class="px-6 py-4">
                    <div class="flex items-center gap-3">
                      <div :class="[
                        'w-9 h-9 rounded-full flex items-center justify-center font-bold text-xs shadow-inner',
                        customer.is_walk_in ? 'bg-indigo-100 text-indigo-700 border border-indigo-200' : 'bg-gray-100 text-gray-700'
                      ]">
                        {{ customer.name.charAt(0).toUpperCase() }}
                      </div>
                      <div class="truncate">
                        <div class="font-semibold text-gray-900 flex items-center gap-1.5">
                          {{ customer.name }}
                          <span
                            v-if="customer.is_walk_in"
                            class="px-1.5 py-0.5 text-[10px] font-bold bg-indigo-100 text-indigo-800 rounded border border-indigo-200 uppercase tracking-wider"
                          >
                            Walk-In
                          </span>
                        </div>
                        <div class="text-xs text-gray-400 truncate mt-0.5">{{ customer.email || 'No email registered' }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="font-medium text-gray-800">{{ customer.phone || '—' }}</div>
                    <div class="text-xs text-gray-400 mt-0.5">{{ customer.province || 'No province set' }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="[
                      'inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold border',
                      customer.registration_type === 'Registered'
                        ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                        : 'bg-amber-50 text-amber-700 border-amber-200'
                    ]">
                      {{ customer.registration_type }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap font-mono text-xs text-gray-700">
                    {{ customer.ntn_cnic || '—' }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-right font-semibold text-gray-900">
                    Rs {{ Number(customer.credit_limit || 0).toLocaleString() }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-center">
                    <span :class="[
                      'inline-block w-2.5 h-2.5 rounded-full ring-4 ring-offset-0',
                      customer.is_active ? 'bg-emerald-500 ring-emerald-500/20' : 'bg-gray-300 ring-gray-200'
                    ]" :title="customer.is_active ? 'Active' : 'Inactive'"></span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-right pr-6">
                    <div class="flex items-center justify-end gap-3">
                      <!-- Edit Button -->
                      <button
                        @click="switchToEdit(customer)"
                        class="text-indigo-600 hover:text-indigo-900 font-semibold text-xs"
                      >
                        Edit
                      </button>

                      <div class="w-px h-3 bg-gray-200" v-if="!customer.is_walk_in"></div>

                      <!-- Toggle Status Button -->
                      <button
                        v-if="!customer.is_walk_in"
                        @click="toggleCustomerStatus(customer)"
                        :class="[
                          'font-semibold text-xs transition-colors',
                          customer.is_active ? 'text-rose-600 hover:text-rose-900' : 'text-emerald-600 hover:text-emerald-900'
                        ]"
                      >
                        {{ customer.is_active ? 'Deactivate' : 'Activate' }}
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Pagination Bar -->
          <div class="bg-gray-50 border-t border-gray-100 px-6 py-4 flex items-center justify-between">
            <span class="text-xs text-gray-500">
              Showing <span class="font-semibold text-gray-800">{{ customers.length }}</span> of
              <span class="font-semibold text-gray-800">{{ pagination.count }}</span> customers
            </span>
            
            <div class="flex items-center gap-2">
              <button
                @click="changePage(pagination.previous)"
                :disabled="!pagination.previous"
                class="px-3 py-1.5 bg-white border border-gray-300 rounded-lg text-xs font-semibold text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                Previous
              </button>
              <button
                @click="changePage(pagination.next)"
                :disabled="!pagination.next"
                class="px-3 py-1.5 bg-white border border-gray-300 rounded-lg text-xs font-semibold text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                Next
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 2. CREATE / EDIT CUSTOMER FORM VIEW -->
      <div v-else-if="viewMode === 'create' || viewMode === 'edit'">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
          
          <!-- LEFT COLUMN: Profile Fields Form -->
          <div class="lg:col-span-2 space-y-6">
            <div class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
              <div class="border-b border-gray-100 bg-gray-50/50 px-6 py-4">
                <h3 class="text-base font-bold text-gray-900">Profile</h3>
                <p class="text-xs text-gray-500 mt-0.5">Primary information, identity credentials, and credit setup.</p>
              </div>

              <form @submit.prevent="saveCustomer" class="p-6 space-y-5">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <!-- Name Field -->
                  <div class="md:col-span-2">
                    <label class="block text-xs font-bold text-gray-700 uppercase tracking-wide">Name <span class="text-rose-500">*</span></label>
                    <input
                      type="text"
                      required
                      v-model="form.name"
                      placeholder="e.g. John Doe / Alpha Traders"
                      class="mt-1.5 w-full px-3.5 py-2 border border-gray-300 rounded-lg text-sm text-gray-950 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-colors"
                    />
                  </div>

                  <!-- Phone Field -->
                  <div>
                    <label class="block text-xs font-bold text-gray-700 uppercase tracking-wide">Phone</label>
                    <input
                      type="tel"
                      v-model="form.phone"
                      placeholder="e.g. 03001234567"
                      class="mt-1.5 w-full px-3.5 py-2 border border-gray-300 rounded-lg text-sm text-gray-950 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-colors"
                    />
                  </div>

                  <!-- Email Field -->
                  <div>
                    <label class="block text-xs font-bold text-gray-700 uppercase tracking-wide">Email</label>
                    <input
                      type="email"
                      v-model="form.email"
                      placeholder="e.g. john@example.com"
                      class="mt-1.5 w-full px-3.5 py-2 border border-gray-300 rounded-lg text-sm text-gray-950 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-colors"
                    />
                  </div>

                  <!-- Registration Dropdown -->
                  <div>
                    <label class="block text-xs font-bold text-gray-700 uppercase tracking-wide">Registration</label>
                    <select
                      v-model="form.registration_type"
                      class="mt-1.5 w-full px-3.5 py-2 border border-gray-300 rounded-lg bg-white text-sm text-gray-950 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-colors"
                    >
                      <option value="Unregistered">Unregistered</option>
                      <option value="Registered">Registered (NTN holder)</option>
                    </select>
                  </div>

                  <!-- Province Dropdown -->
                  <div>
                    <label class="block text-xs font-bold text-gray-700 uppercase tracking-wide">Province</label>
                    <select
                      v-model="form.province"
                      class="mt-1.5 w-full px-3.5 py-2 border border-gray-300 rounded-lg bg-white text-sm text-gray-950 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-colors"
                    >
                      <option value="">No Province Set</option>
                      <option value="Punjab">Punjab</option>
                      <option value="Sindh">Sindh</option>
                      <option value="Khyber Pakhtunkhwa">Khyber Pakhtunkhwa (KPK)</option>
                      <option value="Balochistan">Balochistan</option>
                      <option value="Islamabad">Islamabad Capital Territory</option>
                      <option value="Azad Jammu & Kashmir">Azad Jammu & Kashmir</option>
                      <option value="Gilgit-Baltistan">Gilgit-Baltistan</option>
                    </select>
                  </div>

                  <!-- CNIC Field (Conditional or always visible) -->
                  <div>
                    <label class="block text-xs font-bold text-gray-700 uppercase tracking-wide flex items-center justify-between">
                      <span>CNIC</span>
                      <span class="text-[10px] text-gray-400 font-normal lowercase">(13 digits, digits only)</span>
                    </label>
                    <input
                      type="text"
                      v-model="form.cnic"
                      placeholder="e.g. 3520112345671"
                      class="mt-1.5 w-full px-3.5 py-2 border border-gray-300 rounded-lg text-sm text-gray-950 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-colors"
                    />
                  </div>

                  <!-- NTN Field (Conditional or always visible) -->
                  <div>
                    <label class="block text-xs font-bold text-gray-700 uppercase tracking-wide flex items-center justify-between">
                      <span>NTN</span>
                      <span class="text-[10px] text-gray-400 font-normal lowercase">(7 or 9 digits, digits only)</span>
                    </label>
                    <input
                      type="text"
                      v-model="form.ntn"
                      placeholder="e.g. 1234567"
                      class="mt-1.5 w-full px-3.5 py-2 border border-gray-300 rounded-lg text-sm text-gray-950 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-colors"
                    />
                  </div>

                  <!-- Credit Limit Field -->
                  <div>
                    <label class="block text-xs font-bold text-gray-700 uppercase tracking-wide">Credit Limit (Rs)</label>
                    <input
                      type="number"
                      min="0"
                      step="0.01"
                      v-model="form.credit_limit"
                      class="mt-1.5 w-full px-3.5 py-2 border border-gray-300 rounded-lg text-sm text-gray-950 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-colors"
                    />
                  </div>

                  <!-- Vendor Code Field -->
                  <div>
                    <label class="block text-xs font-bold text-gray-700 uppercase tracking-wide flex items-center justify-between">
                      <span>Vendor Code</span>
                      <span class="text-[10px] text-gray-400 font-normal lowercase">(Optional code)</span>
                    </label>
                    <input
                      type="text"
                      v-model="form.vendor_code"
                      placeholder="e.g. V-001"
                      class="mt-1.5 w-full px-3.5 py-2 border border-gray-300 rounded-lg text-sm text-gray-950 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-colors"
                    />
                  </div>

                  <!-- Address Field -->
                  <div class="md:col-span-2">
                    <label class="block text-xs font-bold text-gray-700 uppercase tracking-wide">Address</label>
                    <textarea
                      v-model="form.address"
                      rows="3"
                      placeholder="Enter customer billing/shipping address..."
                      class="mt-1.5 w-full px-3.5 py-2 border border-gray-300 rounded-lg text-sm text-gray-950 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-colors resize-none"
                    ></textarea>
                  </div>

                  <!-- Notes Field -->
                  <div class="md:col-span-2">
                    <label class="block text-xs font-bold text-gray-700 uppercase tracking-wide">Notes</label>
                    <textarea
                      v-model="form.notes"
                      rows="2.5"
                      placeholder="Private notes (payment behavior, special agreements...)"
                      class="mt-1.5 w-full px-3.5 py-2 border border-gray-300 rounded-lg text-sm text-gray-950 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-colors resize-none"
                    ></textarea>
                  </div>
                </div>

                <!-- Form Controls -->
                <div class="flex items-center justify-end gap-3 border-t border-gray-100 pt-5 mt-5">
                  <button
                    type="button"
                    @click="switchToList"
                    class="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    :disabled="formSubmitting"
                    class="flex items-center gap-2 px-5 py-2 bg-indigo-600 rounded-lg text-sm font-medium text-white hover:bg-indigo-700 shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                  >
                    <span v-if="formSubmitting" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                    {{ viewMode === 'create' ? 'Create Customer' : 'Save Changes' }}
                  </button>
                </div>
              </form>
            </div>
          </div>

          <!-- RIGHT COLUMN: Ledger Info Panel -->
          <div class="lg:col-span-1">
            <div class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
              <div class="border-b border-gray-100 bg-gray-50/50 px-6 py-4">
                <h3 class="text-base font-bold text-gray-900">Ledger</h3>
              </div>

              <!-- Unsaved Customer State -->
              <div v-if="viewMode === 'create'" class="p-8 text-center flex flex-col items-center justify-center min-h-[300px]">
                <div class="w-12 h-12 rounded-full bg-gray-50 border border-gray-200 flex items-center justify-center text-gray-400 mb-4">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
                <p class="text-sm font-semibold text-gray-900">Save first to see ledger</p>
                <p class="text-xs text-gray-400 mt-1 max-w-[200px]">Ledger histories, credit balances, and billing statements are generated on profile save.</p>
              </div>

              <!-- Existing Customer State (Show beautiful, structured ledger info) -->
              <div v-else class="p-6 space-y-6">
                <!-- Balance & Limits -->
                <div class="space-y-4">
                  <div class="p-4 bg-indigo-50/30 border border-indigo-100 rounded-lg flex items-center justify-between">
                    <div>
                      <p class="text-xs font-bold text-indigo-900 uppercase tracking-wide">Outstanding Balance</p>
                      <p class="text-2xl font-black text-indigo-950 mt-1">Rs 0.00</p>
                    </div>
                    <div class="w-10 h-10 rounded-full bg-indigo-50 border border-indigo-100 flex items-center justify-center text-indigo-600">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
                      </svg>
                    </div>
                  </div>

                  <div class="grid grid-cols-2 gap-3">
                    <div class="p-3 border border-gray-100 rounded-lg bg-gray-50/30">
                      <p class="text-[10px] font-bold text-gray-400 uppercase tracking-wide">Credit Limit</p>
                      <p class="text-sm font-bold text-gray-850 mt-1">Rs {{ Number(form.credit_limit || 0).toLocaleString() }}</p>
                    </div>
                    <div class="p-3 border border-gray-100 rounded-lg bg-gray-50/30">
                      <p class="text-[10px] font-bold text-gray-400 uppercase tracking-wide">Available Credit</p>
                      <p class="text-sm font-bold text-emerald-600 mt-1">Rs {{ Number(form.credit_limit || 0).toLocaleString() }}</p>
                    </div>
                  </div>
                </div>

                <!-- Ledger Activity -->
                <div>
                  <h4 class="text-xs font-bold text-gray-400 uppercase tracking-wider">Recent Activity</h4>
                  
                  <div class="mt-4 flex flex-col items-center justify-center py-8 border border-dashed border-gray-200 rounded-lg text-center bg-gray-50/30">
                    <svg class="w-8 h-8 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                    </svg>
                    <p class="text-xs font-semibold text-gray-800 mt-3">Ledger is clean</p>
                    <p class="text-[10px] text-gray-400 mt-0.5 max-w-[170px]">No historical credit sales, returns, or adjustments found.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 3. CUSTOMER IMPORT CSV MODAL -->
    <div v-if="importModalOpen" class="fixed inset-0 bg-gray-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-xl shadow-xl max-w-2xl w-full overflow-hidden border border-gray-150 animate-in fade-in zoom-in-95 duration-200">
        
        <!-- Modal Header -->
        <div class="border-b border-gray-150 px-6 py-4 bg-gray-50 flex items-center justify-between">
          <div>
            <h3 class="text-base font-bold text-gray-900">Import Customers from CSV</h3>
            <p class="text-xs text-gray-500 mt-0.5">Bulk upload customer list from a comma-separated text file.</p>
          </div>
          <button @click="closeImportModal" class="text-gray-400 hover:text-gray-600 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div class="p-6 space-y-5">
          <!-- Step 1: Upload Dropzone -->
          <div v-if="!importParsedData.length" class="space-y-4">
            <div
              @dragover.prevent="dragOver = true"
              @dragleave.prevent="dragOver = false"
              @drop.prevent="handleFileDrop"
              :class="[
                'border-2 border-dashed rounded-lg p-10 flex flex-col items-center text-center transition-all cursor-pointer',
                dragOver ? 'border-indigo-500 bg-indigo-50/20' : 'border-gray-300 hover:border-gray-450 hover:bg-gray-50/30'
              ]"
              @click="triggerFileInput"
            >
              <input
                type="file"
                ref="fileInput"
                accept=".csv"
                class="hidden"
                @change="handleFileSelect"
              />
              <div class="w-12 h-12 bg-indigo-50 rounded-full flex items-center justify-center text-indigo-600 mb-4 border border-indigo-100">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 13h6m-3-3v6m-9 1V4a2 2 0 012-2h6l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
                </svg>
              </div>
              <p class="text-sm font-bold text-gray-900">Drag and drop your CSV file here</p>
              <p class="text-xs text-gray-400 mt-1.5">or click to browse local files (max size 2MB)</p>
            </div>

            <!-- CSV Formatting Guide -->
            <div class="p-4 bg-gray-50 border border-gray-150 rounded-lg">
              <h4 class="text-xs font-bold text-gray-700 uppercase tracking-wide">Required format / columns:</h4>
              <p class="text-xs text-gray-500 mt-1 leading-relaxed">Your CSV file must include a header row. Columns should be ordered as follows (or contain these column headers):</p>
              
              <div class="mt-3 font-mono text-[11px] bg-white border border-gray-250 p-2 rounded text-gray-700 overflow-x-auto select-all shadow-inner">
                Name,Phone,Email,CNIC,NTN,RegistrationType,Province,CreditLimit,Address,Notes
              </div>
              <p class="text-[10px] text-gray-400 mt-1.5 leading-relaxed">
                * <strong class="text-gray-600">Name</strong> is required.<br />
                * <strong class="text-gray-600">RegistrationType</strong> must be 'Registered' or 'Unregistered'.<br />
                * <strong class="text-gray-600">Province</strong> must match 'Punjab', 'Sindh', 'Khyber Pakhtunkhwa', 'Balochistan', 'Islamabad', 'Azad Jammu & Kashmir' or 'Gilgit-Baltistan'.
              </p>
            </div>
          </div>

          <!-- Step 2: Preview & Import Confirmation -->
          <div v-else class="space-y-4">
            <div class="flex items-center justify-between">
              <span class="text-xs text-gray-500">
                Parsed <span class="font-bold text-gray-800">{{ importParsedData.length }}</span> customers from file.
              </span>
              <button
                @click="resetImport"
                class="text-xs font-bold text-rose-600 hover:text-rose-800 transition-colors"
              >
                Clear file
              </button>
            </div>

            <!-- Parsed Preview Table -->
            <div class="border border-gray-200 rounded-lg max-h-60 overflow-y-auto shadow-inner bg-gray-50/20">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50 sticky top-0 z-10 text-left text-[10px] font-bold text-gray-500 uppercase">
                  <tr>
                    <th scope="col" class="px-4 py-2.5">Name</th>
                    <th scope="col" class="px-4 py-2.5">Phone</th>
                    <th scope="col" class="px-4 py-2.5">Reg Type</th>
                    <th scope="col" class="px-4 py-2.5">CNIC/NTN</th>
                    <th scope="col" class="px-4 py-2.5 text-right">Credit Limit</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100 text-xs bg-white text-gray-600">
                  <tr v-for="(row, idx) in importParsedData" :key="idx">
                    <td class="px-4 py-2 font-medium text-gray-900">{{ row.name }}</td>
                    <td class="px-4 py-2">{{ row.phone || '—' }}</td>
                    <td class="px-4 py-2">{{ row.registration_type }}</td>
                    <td class="px-4 py-2 font-mono text-[10px]">{{ row.ntn || row.cnic || '—' }}</td>
                    <td class="px-4 py-2 text-right">Rs {{ Number(row.credit_limit || 0).toLocaleString() }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Import Progress Bar -->
            <div v-if="importingInProgress" class="space-y-2">
              <div class="flex items-center justify-between text-xs font-semibold">
                <span class="text-indigo-600">Importing list...</span>
                <span class="text-gray-600">{{ importProgress }} / {{ importParsedData.length }}</span>
              </div>
              <div class="w-full h-2.5 bg-gray-100 rounded-full overflow-hidden border border-gray-200 shadow-inner">
                <div
                  class="h-full bg-indigo-600 rounded-full transition-all duration-300 shadow-inner"
                  :style="{ width: `${(importProgress / importParsedData.length) * 100}%` }"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Modal Footer -->
        <div class="border-t border-gray-150 px-6 py-4 bg-gray-50 flex items-center justify-end gap-3">
          <button
            @click="closeImportModal"
            :disabled="importingInProgress"
            class="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none transition-colors"
          >
            Cancel
          </button>
          <button
            v-if="importParsedData.length"
            @click="executeImport"
            :disabled="importingInProgress"
            class="flex items-center gap-2 px-5 py-2 bg-indigo-600 rounded-lg text-sm font-medium text-white hover:bg-indigo-700 shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 transition-all font-semibold"
          >
            <span v-if="importingInProgress" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
            Confirm Import
          </button>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { customersAPI, type Customer, type CustomerCreatePayload } from '@/apis/pos/customers/customersAPI'

// Views State
type ViewMode = 'list' | 'create' | 'edit'
const viewMode = ref<ViewMode>('list')
const customers = ref<Customer[]>([])
const loading = ref(false)
const searchQuery = ref('')
let searchTimeout: any = null

// Alert/Toast banner state
interface Alert {
  type: 'success' | 'error'
  title: string
  message: string
}
const alert = ref<Alert | null>(null)

// Pagination Metadata
const pagination = reactive({
  count: 0,
  next: null as string | null,
  previous: null as string | null,
  currentPage: 1
})

// Customer Form State
const selectedCustomer = ref<Customer | null>(null)
const formSubmitting = ref(false)
const form = reactive<CustomerCreatePayload>({
  name: '',
  phone: '',
  email: '',
  cnic: '',
  ntn: '',
  registration_type: 'Unregistered',
  province: '',
  vendor_code: '0',
  credit_limit: 0,
  address: '',
  notes: '',
  is_active: true
})

// CSV Import Modal State
const importModalOpen = ref(false)
const dragOver = ref(false)
const importParsedData = ref<CustomerCreatePayload[]>([])
const importingInProgress = ref(false)
const importProgress = ref(0)
const fileInput = ref<HTMLInputElement | null>(null)

// ── LIFECYCLE ─────────────────────────────────────────────────────────────
onMounted(() => {
  fetchCustomers()
})

// ── CUSTOMER LISTING & SEARCH ─────────────────────────────────────────────
const fetchCustomers = async (urlOrParams?: string | Record<string, any>) => {
  loading.value = true
  try {
    let res
    if (typeof urlOrParams === 'string') {
      // Direct axios call via full url path
      const url = new URL(urlOrParams)
      const params = Object.fromEntries(url.searchParams.entries())
      res = await customersAPI.list(params)
    } else {
      res = await customersAPI.list(urlOrParams || { page: pagination.currentPage })
    }
    
    customers.value = res.data.results
    pagination.count = res.data.count
    pagination.next = res.data.next
    pagination.previous = res.data.previous
  } catch (err: any) {
    showToast('error', 'Retrieval Error', err.response?.data?.detail || 'Failed to fetch customer database.')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    if (searchQuery.value.trim() === '') {
      fetchCustomers({ page: 1 })
    } else {
      loading.value = true
      customersAPI.search(searchQuery.value)
        .then((res) => {
          customers.value = res.data
          pagination.count = res.data.length
          pagination.next = null
          pagination.previous = null
        })
        .catch((err) => {
          showToast('error', 'Search Error', err.response?.data?.detail || 'Search operation failed.')
        })
        .finally(() => {
          loading.value = false
        })
    }
  }, 400)
}

const changePage = (url: string | null) => {
  if (url) {
    fetchCustomers(url)
  }
}

const toggleCustomerStatus = async (customer: Customer) => {
  try {
    if (customer.is_active) {
      await customersAPI.deactivate(customer.id)
      customer.is_active = false
      showToast('success', 'Profile Deactivated', `Customer '${customer.name}' has been deactivated.`)
    } else {
      await customersAPI.activate(customer.id)
      customer.is_active = true
      showToast('success', 'Profile Activated', `Customer '${customer.name}' is now active.`)
    }
  } catch (err: any) {
    showToast('error', 'Status Update Error', err.response?.data?.detail || 'Could not update status.')
  }
}

// ── VIEW SWITCHING ────────────────────────────────────────────────────────
const switchToList = () => {
  viewMode.value = 'list'
  selectedCustomer.value = null
  resetForm()
  fetchCustomers()
}

const switchToCreate = () => {
  resetForm()
  selectedCustomer.value = null
  viewMode.value = 'create'
}

const switchToEdit = (customer: Customer) => {
  selectedCustomer.value = customer
  form.name = customer.name
  form.phone = customer.phone || ''
  form.email = customer.email || ''
  form.cnic = customer.cnic || ''
  form.ntn = customer.ntn || ''
  form.registration_type = customer.registration_type
  form.province = customer.province || ''
  form.vendor_code = customer.vendor_code || '0'
  form.credit_limit = customer.credit_limit
  form.address = customer.address || ''
  form.notes = customer.notes || ''
  form.is_active = customer.is_active
  
  viewMode.value = 'edit'
}

const resetForm = () => {
  form.name = ''
  form.phone = ''
  form.email = ''
  form.cnic = ''
  form.ntn = ''
  form.registration_type = 'Unregistered'
  form.province = ''
  form.vendor_code = '0'
  form.credit_limit = 0
  form.address = ''
  form.notes = ''
  form.is_active = true
}

// ── CUSTOMER CRUD ACTIONS ─────────────────────────────────────────────────
const saveCustomer = async () => {
  formSubmitting.value = true
  
  // Format Payload - Remove dashes from CNIC/NTN for compliance
  const payload: CustomerCreatePayload = {
    ...form,
    cnic: form.cnic?.replace(/-/g, '').trim() || undefined,
    ntn: form.ntn?.replace(/-/g, '').trim() || undefined,
    phone: form.phone?.trim() || undefined,
    email: form.email?.trim() || undefined,
    address: form.address?.trim() || undefined,
    notes: form.notes?.trim() || undefined,
    province: form.province || undefined,
    vendor_code: form.vendor_code?.trim() || undefined,
    credit_limit: Number(form.credit_limit) || 0
  }

  try {
    if (viewMode.value === 'create') {
      await customersAPI.create(payload)
      showToast('success', 'Customer Created', `Profile for '${payload.name}' saved successfully.`)
    } else if (viewMode.value === 'edit' && selectedCustomer.value) {
      await customersAPI.update(selectedCustomer.value.id, payload)
      showToast('success', 'Customer Updated', `Profile modifications for '${payload.name}' saved.`)
    }
    switchToList()
  } catch (err: any) {
    const errorData = err.response?.data
    let errorMsg = 'Failed to submit form.'
    
    // Parse nested serializer error objects
    if (errorData) {
      if (typeof errorData === 'object') {
        errorMsg = Object.entries(errorData)
          .map(([field, errs]) => `${field}: ${Array.isArray(errs) ? errs.join(', ') : errs}`)
          .join(' | ')
      } else {
        errorMsg = errorData.detail || errorMsg
      }
    }
    showToast('error', 'Form Submission Failed', errorMsg)
  } finally {
    formSubmitting.value = false
  }
}

// ── BULK CSV UPLOAD LOGIC ──────────────────────────────────────────────────
const openImportModal = () => {
  importParsedData.value = []
  importingInProgress.value = false
  importProgress.value = 0
  importModalOpen.value = true
}

const closeImportModal = () => {
  if (importingInProgress.value) return
  importModalOpen.value = false
  importParsedData.value = []
}

const resetImport = () => {
  importParsedData.value = []
}

const handleFileSelect = (e: Event) => {
  const target = e.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) parseCSVFile(file)
}

const handleFileDrop = (e: DragEvent) => {
  dragOver.value = false
  const file = e.dataTransfer?.files?.[0]
  if (file) parseCSVFile(file)
}

const parseCSVFile = (file: File) => {
  if (file.type !== 'text/csv' && !file.name.endsWith('.csv')) {
    showToast('error', 'Invalid File Type', 'Please upload a valid .csv file.')
    return
  }

  const reader = new FileReader()
  reader.onload = (e) => {
    const text = e.target?.result as string
    if (!text) return

    try {
      const rows = text.split('\n').map(row => row.split(','))
      if (rows.length < 2) {
        showToast('error', 'Empty File', 'The uploaded file has no data rows.')
        return
      }

      // Check header matches fields
      const headers = rows[0].map(h => h.trim().toLowerCase())
      const nameIndex = headers.indexOf('name')
      const phoneIndex = headers.indexOf('phone')
      const emailIndex = headers.indexOf('email')
      const cnicIndex = headers.indexOf('cnic')
      const ntnIndex = headers.indexOf('ntn')
      const regTypeIndex = headers.indexOf('registrationtype')
      const provinceIndex = headers.indexOf('province')
      const limitIndex = headers.indexOf('creditlimit')
      const addressIndex = headers.indexOf('address')
      const notesIndex = headers.indexOf('notes')

      if (nameIndex === -1) {
        showToast('error', 'Invalid Format', "CSV header is missing the 'Name' column.")
        return
      }

      const parsed: CustomerCreatePayload[] = []
      for (let i = 1; i < rows.length; i++) {
        const columns = rows[i].map(col => col.trim().replace(/^["']|["']$/g, '')) // strip quotes
        
        // Skip empty lines
        if (columns.length === 0 || (columns.length === 1 && !columns[0])) continue

        const name = columns[nameIndex]
        if (!name) continue // Skip rows with no name

        const regType = regTypeIndex !== -1 ? columns[regTypeIndex] : 'Unregistered'
        const registration_type = (regType === 'Registered' || regType === 'Unregistered') ? regType : 'Unregistered'

        parsed.push({
          name,
          phone: phoneIndex !== -1 ? columns[phoneIndex] : '',
          email: emailIndex !== -1 ? columns[emailIndex] : '',
          cnic: cnicIndex !== -1 ? columns[cnicIndex] : '',
          ntn: ntnIndex !== -1 ? columns[ntnIndex] : '',
          registration_type,
          province: provinceIndex !== -1 ? columns[provinceIndex] : '',
          credit_limit: limitIndex !== -1 ? (Number(columns[limitIndex]) || 0) : 0,
          address: addressIndex !== -1 ? columns[addressIndex] : '',
          notes: notesIndex !== -1 ? columns[notesIndex] : '',
          is_active: true
        })
      }

      importParsedData.value = parsed
      if (parsed.length === 0) {
        showToast('error', 'Parse Error', 'No valid rows found in CSV.')
      }
    } catch (err) {
      showToast('error', 'Parse Failure', 'Failed to parse CSV file content.')
    }
  }
  reader.readAsText(file)
}

const executeImport = async () => {
  importingInProgress.value = true
  importProgress.value = 0
  
  let successCount = 0
  let failCount = 0

  for (const customer of importParsedData.value) {
    try {
      // Normalize values
      const payload = {
        ...customer,
        cnic: customer.cnic?.replace(/-/g, '') || undefined,
        ntn: customer.ntn?.replace(/-/g, '') || undefined,
        phone: customer.phone || undefined,
        email: customer.email || undefined,
        province: customer.province || undefined
      }
      await customersAPI.create(payload)
      successCount++
    } catch (err) {
      failCount++
    }
    importProgress.value++
  }

  showToast(
    failCount === 0 ? 'success' : 'error',
    'Import Completed',
    `Successfully imported ${successCount} customers. Failed rows: ${failCount}`
  )
  
  importingInProgress.value = false
  importModalOpen.value = false
  importParsedData.value = []
  fetchCustomers({ page: 1 })
}

const triggerFileInput = () => {
  fileInput.value?.click()
}

// ── HELPER NOTIFICATIONS ──────────────────────────────────────────────────
const showToast = (type: 'success' | 'error', title: string, message: string) => {
  alert.value = { type, title, message }
  // Auto-dismiss after 6 seconds
  setTimeout(() => {
    if (alert.value && alert.value.title === title) {
      alert.value = null
    }
  }, 6000)
}
</script>
