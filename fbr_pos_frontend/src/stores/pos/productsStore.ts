import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { productsAPI, type Product } from '@/apis/pos/products/productsAPI'

export const useProductsStore = defineStore('products', () => {
  // State
  const products = ref<Product[]>([])
  const selectedProduct = ref<Product | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const pagination = ref({ count: 0, page: 1, pageSize: 20 })

  // Computed
  const hasProducts = computed(() => products.value.length > 0)

  // Methods
  const fetchProducts = async (page = 1) => {
    loading.value = true
    error.value = null

    try {
      const response = await productsAPI.list({
        page,
        page_size: pagination.value.pageSize,
      })

      products.value = response.data.results
      pagination.value.count = response.data.count
      pagination.value.page = page
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch products'
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchProductById = async (id: number) => {
    loading.value = true
    error.value = null

    try {
      const response = await productsAPI.retrieve(id)
      selectedProduct.value = response.data
      return response.data
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch product'
      throw err
    } finally {
      loading.value = false
    }
  }

  const searchProducts = async (query: string) => {
    loading.value = true
    error.value = null

    try {
      const response = await productsAPI.search(query)
      products.value = response.data
      return response.data
    } catch (err: any) {
      error.value = err.message || 'Search failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  const createProduct = async (payload: any) => {
    loading.value = true
    error.value = null

    try {
      const response = await productsAPI.create(payload)
      products.value.unshift(response.data)
      return response.data
    } catch (err: any) {
      error.value = err.message || 'Failed to create product'
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateProduct = async (id: number, payload: any) => {
    loading.value = true
    error.value = null

    try {
      const response = await productsAPI.update(id, payload)
      const index = products.value.findIndex((p) => p.id === id)
      if (index !== -1) {
        products.value[index] = response.data
      }
      if (selectedProduct.value?.id === id) {
        selectedProduct.value = response.data
      }
      return response.data
    } catch (err: any) {
      error.value = err.message || 'Failed to update product'
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteProduct = async (id: number) => {
    loading.value = true
    error.value = null

    try {
      await productsAPI.delete(id)
      products.value = products.value.filter((p) => p.id !== id)
      if (selectedProduct.value?.id === id) {
        selectedProduct.value = null
      }
    } catch (err: any) {
      error.value = err.message || 'Failed to delete product'
      throw err
    } finally {
      loading.value = false
    }
  }

  const reset = () => {
    products.value = []
    selectedProduct.value = null
    loading.value = false
    error.value = null
    pagination.value = { count: 0, page: 1, pageSize: 20 }
  }

  return {
    // State
    products,
    selectedProduct,
    loading,
    error,
    pagination,

    // Computed
    hasProducts,

    // Methods
    fetchProducts,
    fetchProductById,
    searchProducts,
    createProduct,
    updateProduct,
    deleteProduct,
    reset,
  }
})
