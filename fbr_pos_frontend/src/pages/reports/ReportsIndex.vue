<template>
  <div class="h-full flex flex-col px-8 py-8 bg-gray-50 overflow-y-auto">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-900">Reports</h1>
      <p class="text-sm text-gray-500 mt-1">19 reports available.</p>
    </div>

    <!-- Groups -->
    <div class="space-y-10">
      <div v-for="group in reportGroups" :key="group.name">
        <h2 class="text-lg font-bold text-gray-800 mb-4 border-b border-gray-200 pb-2">{{ group.name }}</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          <RouterLink
            v-for="report in group.reports"
            :key="report.id"
            :to="`/reports/${report.id}`"
            class="bg-white rounded-lg border border-gray-200 p-5 shadow-sm hover:shadow-md hover:border-teal-500 transition-all cursor-pointer flex flex-col h-full"
          >
            <div class="flex items-start justify-between mb-2">
              <h3 class="text-base font-semibold text-gray-900">{{ report.name }}</h3>
              <svg class="w-5 h-5 text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </div>
            <p class="text-sm text-gray-500 flex-1">{{ report.description }}</p>
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const reportGroups = [
  {
    name: 'Sales',
    reports: [
      { id: 'daily-sales', name: 'Daily sales', description: 'Gross / tax / net per day per branch' },
      { id: 'hourly-heatmap', name: 'Hourly heatmap', description: 'Sales density by hour and weekday' },
      { id: 'item-wise', name: 'Item-wise sales', description: 'Quantity, revenue, COGS per product' },
      { id: 'category-wise', name: 'Category-wise', description: 'Sales rolled up by category' },
      { id: 'top-movers', name: 'Top movers', description: 'Best-selling products by revenue' },
      { id: 'slow-movers', name: 'Slow movers', description: 'In-stock items with low velocity' },
      { id: 'cashier-performance', name: 'Cashier performance', description: 'Invoices, gross, avg ticket per cashier' },
      { id: 'branch-comparison', name: 'Branch comparison', description: 'Side-by-side branch metrics' },
    ]
  },
  {
    name: 'Inventory & Operations',
    reports: [
      { id: 'stock', name: 'Stock report', description: 'Current quantity per branch with reorder flags' },
      { id: 'stock-aging', name: 'Stock aging', description: 'On-hand inventory bucketed by age' },
      { id: 'payment-methods', name: 'Payment methods', description: 'Totals by payment method' },
      { id: 'returns-analysis', name: 'Returns analysis', description: 'Return rate, reasons, FBR routes' },
      { id: 'profit-loss', name: 'Profit & loss', description: 'Revenue, COGS, gross margin per period' },
    ]
  },
  {
    name: 'Compliance & Customers',
    reports: [
      { id: 'tax', name: 'Tax report (FBR)', description: 'Tax collected per rate band' },
      { id: 'fbr-submissions', name: 'FBR submissions', description: 'Every PRAL roundtrip with status' },
      { id: 'audit-log', name: 'Audit log', description: 'Append-only history of changes' },
      { id: 'customer-top', name: 'Customer top-N', description: 'Biggest spenders' },
      { id: 'customer-dormant', name: 'Dormant customers', description: 'Customers who haven\'t returned' },
      { id: 'supplier-purchases', name: 'Supplier purchases', description: 'Spend by supplier (purchases module pending)' },
    ]
  }
]
</script>
