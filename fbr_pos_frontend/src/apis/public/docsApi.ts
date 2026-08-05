import axiosInstance from '@/apis/axiosInstance'

export interface HelpCategory {
  id: string
  name: string
  source_slug: string
  description: string | null
  display_order: number
  is_active: boolean
}

export interface HelpArticle {
  id: string
  source_id: string
  title: string
  slug: string
  content: string | null
  seo_title: string | null
  seo_description: string | null
  reading_time: string | null
  featured: boolean
  is_published: boolean
  published_at: string | null
  category: HelpCategory | null
  created_at: string
  updated_at: string
}

export const docsApi = {
  /** Fetch all active categories */
  getCategories(): Promise<HelpCategory[]> {
    return axiosInstance.get('/docs/categories/').then((r) => r.data)
  },

  /** Fetch published articles, optionally filtered by category slug */
  getArticles(categorySlug?: string): Promise<HelpArticle[]> {
    const params = categorySlug ? { category: categorySlug } : {}
    return axiosInstance.get('/docs/articles/', { params }).then((r) => r.data)
  },

  /** Fetch a single article by slug */
  getArticle(slug: string): Promise<HelpArticle> {
    return axiosInstance.get(`/docs/articles/${slug}/`).then((r) => r.data)
  },
}
