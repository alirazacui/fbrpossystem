<template>
  <div class="p-6 w-full mx-auto font-sans">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">Categories</h1>
      <p class="text-gray-500 text-sm">
        Drag a row onto another to make it a child. Drag onto the top-level drop zone to promote a category to root.
      </p>
    </div>

    <div class="bg-white rounded-lg shadow border border-gray-200">
      
      <!-- Top Level Drop Zone -->
      <div 
        class="bg-blue-50 border-b border-gray-200 px-6 py-3 text-center text-sm font-medium text-blue-700 transition-colors duration-200"
        :class="{ 'bg-blue-200 ring-2 ring-inset ring-blue-500': dragOverRoot }"
        @dragover.prevent="dragOverRoot = true"
        @dragleave.prevent="dragOverRoot = false"
        @drop="handleDropOnRoot"
      >
        — Drop here to make top level —
      </div>

      <!-- Add Category Bar -->
      <div class="p-4 border-b border-gray-200 bg-gray-50 flex flex-wrap gap-4 items-center">
        <div class="flex-1 min-w-[200px]">
          <label class="sr-only">Name</label>
          <input
            v-model="newCategoryName"
            type="text"
            class="block w-full border-gray-300 rounded-md shadow-sm focus:ring-teal-500 focus:border-teal-500 sm:text-sm px-4 py-2"
            placeholder="Name"
            @keyup.enter="handleAdd"
          />
        </div>
        <div class="flex-1 min-w-[200px]">
          <label class="sr-only">Parent</label>
          <select
            v-model="newCategoryParent"
            class="block w-full border-gray-300 rounded-md shadow-sm focus:ring-teal-500 focus:border-teal-500 sm:text-sm px-4 py-2"
          >
            <option :value="null">— Top level —</option>
            <option v-for="cat in flatCategories" :key="cat.id" :value="cat.id">
              {{ getIndent(cat.level) }} {{ cat.name }}
            </option>
          </select>
        </div>
        <button
          @click="handleAdd"
          :disabled="!newCategoryName.trim() || saving"
          class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-teal-600 hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500 disabled:opacity-50"
        >
          {{ saving ? 'Adding...' : 'Add' }}
        </button>
      </div>

      <!-- Table Header -->
      <div class="bg-gray-100 border-b border-gray-200 px-6 py-3 grid grid-cols-12 gap-4 font-bold text-xs text-gray-500 uppercase tracking-wider">
        <div class="col-span-8">Name</div>
        <div class="col-span-4">Parent</div>
      </div>

      <!-- Tree List -->
      <div class="divide-y divide-gray-200 min-h-[100px]">
        <div v-if="loading" class="p-6 text-center text-gray-500 animate-pulse">Loading categories...</div>
        <div v-else-if="treeData.length === 0" class="p-8 text-center text-gray-500">
          No categories yet. Add the first one above.
        </div>
        
        <template v-else>
          <!-- Recursive render for tree -->
          <div v-for="node in treeData" :key="node.id">
            <CategoryRow 
              :node="node" 
              :level="0" 
              @drag-start="handleDragStart"
              @drop-on="handleDropOnNode"
            />
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { categoriesAPI, type Category } from '@/apis/pos/categories/categoriesAPI'
import CategoryRow from './CategoryRow.vue'

interface TreeNode extends Category {
  children: TreeNode[]
  level: number
}

const categories = ref<Category[]>([])
const loading = ref(true)
const saving = ref(false)
const newCategoryName = ref('')
const newCategoryParent = ref<number | null>(null)

// Drag and drop state
const draggedCategoryId = ref<number | null>(null)
const dragOverRoot = ref(false)

const loadCategories = async () => {
  loading.value = true
  try {
    categories.value = await categoriesAPI.fetchCategories()
  } catch (error) {
    console.error('Failed to load categories', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadCategories()
})

const handleAdd = async () => {
  if (!newCategoryName.value.trim() || saving.value) return
  saving.value = true
  try {
    await categoriesAPI.createCategory({
      name: newCategoryName.value.trim(),
      parent: newCategoryParent.value
    })
    newCategoryName.value = ''
    newCategoryParent.value = null
    await loadCategories()
  } catch (error) {
    console.error('Failed to add category', error)
    alert('Failed to add category.')
  } finally {
    saving.value = false
  }
}

// Tree Building
const treeData = computed(() => {
  const map = new Map<number, TreeNode>()
  const roots: TreeNode[] = []

  // Initialize nodes
  categories.value.forEach(cat => {
    map.set(cat.id, { ...cat, children: [], level: 0 })
  })

  // Build relationships
  categories.value.forEach(cat => {
    const node = map.get(cat.id)!
    if (cat.parent) {
      const parentNode = map.get(cat.parent)
      if (parentNode) {
        parentNode.children.push(node)
      } else {
        roots.push(node) // parent missing, treat as root
      }
    } else {
      roots.push(node)
    }
  })

  // Calculate levels (recursive)
  const setLevels = (nodes: TreeNode[], level: number) => {
    nodes.forEach(node => {
      node.level = level
      if (node.children.length > 0) {
        setLevels(node.children, level + 1)
      }
    })
  }
  setLevels(roots, 0)

  return roots
})

// Flatten tree for the parent select dropdown
const flatCategories = computed(() => {
  const result: TreeNode[] = []
  const flatten = (nodes: TreeNode[]) => {
    nodes.forEach(node => {
      result.push(node)
      if (node.children.length > 0) {
        flatten(node.children)
      }
    })
  }
  flatten(treeData.value)
  return result
})

const getIndent = (level: number) => {
  return '— '.repeat(level)
}

// Drag and Drop Logic
const handleDragStart = (id: number) => {
  draggedCategoryId.value = id
}

const handleDropOnRoot = async () => {
  dragOverRoot.value = false
  if (!draggedCategoryId.value) return
  
  const targetId = draggedCategoryId.value
  draggedCategoryId.value = null

  // Check if it's already a root
  const cat = categories.value.find(c => c.id === targetId)
  if (cat && cat.parent === null) return

  try {
    await categoriesAPI.updateCategory(targetId, { parent: null })
    await loadCategories()
  } catch (error) {
    console.error('Failed to move category', error)
  }
}

const handleDropOnNode = async (parentId: number) => {
  if (!draggedCategoryId.value) return
  
  const targetId = draggedCategoryId.value
  draggedCategoryId.value = null

  // Prevent moving to self or if already parent
  if (targetId === parentId) return
  const cat = categories.value.find(c => c.id === targetId)
  if (cat && cat.parent === parentId) return

  // Basic cycle prevention: cannot move a parent into its own child (will rely on backend validation or simple front end block)
  // To keep it simple, we just call the API. If cycle, backend should ideally reject, or we could write a simple check here.
  const isDescendant = (parentSearchId: number, childId: number): boolean => {
    const child = categories.value.find(c => c.id === childId)
    if (!child || !child.parent) return false
    if (child.parent === parentSearchId) return true
    return isDescendant(parentSearchId, child.parent)
  }

  if (isDescendant(targetId, parentId)) {
    alert("Cannot move a category into its own subcategory.")
    return
  }

  try {
    await categoriesAPI.updateCategory(targetId, { parent: parentId })
    await loadCategories()
  } catch (error) {
    console.error('Failed to move category', error)
  }
}
</script>
