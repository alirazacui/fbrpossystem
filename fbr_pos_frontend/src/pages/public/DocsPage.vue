<template>
  <div class="min-h-screen bg-white flex flex-col font-body-md overflow-hidden">
    <!-- Top Navigation -->
    <header class="w-full top-0 sticky z-50 bg-white/90 backdrop-blur-sm border-b border-outline-variant/60 h-16 flex items-center px-4 md:px-8 shrink-0 shadow-sm">
      <router-link to="/" class="flex items-center gap-2 font-display-lg text-xl font-bold text-primary mr-8">
        <span class="relative flex h-2.5 w-2.5">
          <span class="animate-ping-slow absolute inline-flex h-full w-full rounded-full bg-primary opacity-60"></span>
          <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-primary"></span>
        </span>
        MYFBRPOS
      </router-link>
      <span class="text-on-surface-variant font-medium text-sm hidden sm:inline-block pl-4 border-l border-outline-variant/60">
        Documentation Center
      </span>
      <div class="ml-auto">
        <button class="md:hidden p-2 text-on-surface-variant rounded-lg hover:bg-surface-container-low transition-colors" @click="mobileSidebarOpen = !mobileSidebarOpen">
          <span class="material-symbols-outlined">menu</span>
        </button>
      </div>
    </header>

    <div class="flex flex-1 overflow-hidden">
      <!-- Mobile Overlay -->
      <div 
        v-if="mobileSidebarOpen" 
        class="fixed inset-0 bg-black/40 backdrop-blur-[2px] z-40 md:hidden"
        @click="mobileSidebarOpen = false"
      ></div>

      <!-- Sidebar Tree -->
      <aside 
        class="absolute md:static inset-y-0 left-0 z-40 w-72 bg-white md:bg-surface-container-low/40 border-r border-outline-variant/50 transform transition-transform duration-300 md:transform-none overflow-y-auto flex flex-col h-[calc(100vh-4rem)]"
        :class="mobileSidebarOpen ? 'translate-x-0' : '-translate-x-full'"
      >
        <div class="p-4 shrink-0">
          <div class="relative">
            <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant text-[18px]">search</span>
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="Search articles..."
              class="w-full pl-9 pr-4 py-2.5 bg-white border border-outline-variant/60 rounded-full text-sm shadow-sm focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all"
            />
          </div>
        </div>

        <div class="flex-1 overflow-y-auto px-3 pb-6">
          <div v-if="loading" class="space-y-6 px-1 pt-2">
            <div v-for="i in 3" :key="i" class="space-y-3">
              <div class="h-3 bg-surface-container-highest rounded-full w-1/2 animate-pulse"></div>
              <div class="pl-3 space-y-2">
                <div class="h-8 bg-surface-container-highest rounded-lg w-full animate-pulse"></div>
                <div class="h-8 bg-surface-container-highest rounded-lg w-5/6 animate-pulse"></div>
              </div>
            </div>
          </div>

          <div v-else-if="filteredTree.length === 0" class="text-center text-on-surface-variant text-sm mt-10">
            No articles found.
          </div>

          <div v-else class="space-y-5">
            <div v-for="catNode in filteredTree" :key="catNode.category.id" class="space-y-1">
              <h3 class="font-semibold text-primary/80 text-xs tracking-wider uppercase px-3 pt-2 pb-1">
                {{ catNode.category.name }}
              </h3>
              <ul class="space-y-0.5">
                <li v-for="article in catNode.articles" :key="article.id">
                  <router-link 
                    :to="{ name: 'DocsPage', params: { slug: article.slug } }"
                    class="block px-3 py-2 rounded-lg text-sm transition-colors"
                    :class="route.params.slug === article.slug 
                      ? 'bg-primary text-white font-medium shadow-sm' 
                      : 'text-on-surface-variant hover:bg-primary/8 hover:text-primary'"
                    @click="mobileSidebarOpen = false"
                  >
                    {{ article.title }}
                  </router-link>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </aside>

      <!-- Main Content -->
      <main class="flex-1 overflow-y-auto bg-white h-[calc(100vh-4rem)] relative scroll-smooth" id="docs-main-scroll">
        <!-- Error State -->
        <div v-if="error" class="max-w-3xl p-8 lg:p-12 text-center mt-20">
          <span class="material-symbols-outlined text-6xl text-error mb-4">error_outline</span>
          <h2 class="text-2xl font-bold text-on-surface mb-2">Article not found</h2>
          <p class="text-on-surface-variant mb-6">The article you are looking for does not exist or has been removed.</p>
          <router-link to="/docs" class="text-primary hover:underline font-medium">Clear Selection</router-link>
        </div>

        <!-- Article Content -->
        <div v-else-if="currentArticle" class="max-w-4xl p-6 md:p-10 lg:p-16">
          <div class="mb-10">
            <div class="flex items-center gap-2 text-sm text-primary mb-4 font-medium">
              <span class="bg-primary/10 px-2.5 py-1 rounded-full">{{ currentArticle.category?.name || 'Uncategorized' }}</span>
              <span v-if="currentArticle.reading_time" class="text-on-surface-variant">• {{ currentArticle.reading_time }} read</span>
            </div>
            <h1 class="text-3xl md:text-4xl font-extrabold text-on-surface leading-tight mb-4">
              {{ currentArticle.title }}
            </h1>
            <p v-if="currentArticle.seo_description" class="text-lg text-on-surface-variant">
              {{ currentArticle.seo_description }}
            </p>
          </div>

          <div class="prose prose-teal max-w-none" v-html="currentArticle.content || '<p>No content provided.</p>'"></div>

          <div class="mt-16 pt-6 border-t border-outline-variant/50 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div class="text-sm text-on-surface-variant">
              Last updated: {{ formatDate(currentArticle.updated_at) }}
            </div>
            <div class="flex items-center gap-3">
              <span class="text-sm font-medium text-on-surface">Was this helpful?</span>
              <button class="flex items-center gap-1 px-3 py-1.5 rounded-full hover:bg-primary/8 hover:text-primary transition-colors text-sm text-on-surface-variant">
                <span class="material-symbols-outlined text-sm">thumb_up</span> Yes
              </button>
              <button class="flex items-center gap-1 px-3 py-1.5 rounded-full hover:bg-error/8 hover:text-error transition-colors text-sm text-on-surface-variant">
                <span class="material-symbols-outlined text-sm">thumb_down</span> No
              </button>
            </div>
          </div>
        </div>

        <!-- Welcome State (No slug) — kept simple, no duplicate article cards -->
        <div v-else class="max-w-xl p-8 lg:p-12 mt-24">
          <div class="w-20 h-20 bg-primary/10 rounded-full flex items-center justify-center mb-6 text-primary">
            <span class="material-symbols-outlined text-4xl" style="font-variation-settings: 'FILL' 1;">menu_book</span>
          </div>
          <h2 class="text-2xl md:text-3xl font-extrabold text-on-surface mb-3">FBR POS Documentation</h2>
          <p class="text-on-surface-variant">
            Select an article from the sidebar on the left to start reading.
          </p>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { docsApi, type HelpCategory, type HelpArticle } from '@/apis/public/docsApi'

const route = useRoute()
const mobileSidebarOpen = ref(false)

const allCategories = ref<HelpCategory[]>([])
const allArticles = ref<HelpArticle[]>([])
const loading = ref(true)

const searchQuery = ref('')

const currentArticle = ref<HelpArticle | null>(null)
const error = ref(false)

interface CategoryNode {
  category: HelpCategory
  articles: HelpArticle[]
}

const docsTree = computed<CategoryNode[]>(() => {
  const tree: CategoryNode[] = []

  const categoryMap = new Map<string, CategoryNode>()
  allCategories.value.forEach(cat => {
    const node = { category: cat, articles: [] }
    categoryMap.set(cat.source_slug, node)
    tree.push(node)
  })

  const uncategorizedNode: CategoryNode = {
    category: { id: 'uncategorized', name: 'Uncategorized', source_slug: 'uncategorized', description: '', display_order: 999, is_active: true },
    articles: []
  }

  allArticles.value.forEach(art => {
    if (art.category && categoryMap.has(art.category.source_slug)) {
      categoryMap.get(art.category.source_slug)!.articles.push(art)
    } else {
      uncategorizedNode.articles.push(art)
    }
  })

  if (uncategorizedNode.articles.length > 0) {
    tree.push(uncategorizedNode)
  }

  return tree
    .filter(node => node.articles.length > 0)
    .sort((a, b) => a.category.display_order - b.category.display_order)
})

const filteredTree = computed<CategoryNode[]>(() => {
  if (!searchQuery.value.trim()) return docsTree.value

  const q = searchQuery.value.toLowerCase()
  const result: CategoryNode[] = []

  docsTree.value.forEach(node => {
    if (node.category.name.toLowerCase().includes(q)) {
      result.push(node)
      return
    }

    const matchedArticles = node.articles.filter(a =>
      a.title.toLowerCase().includes(q) ||
      (a.content && a.content.toLowerCase().includes(q))
    )

    if (matchedArticles.length > 0) {
      result.push({
        category: node.category,
        articles: matchedArticles
      })
    }
  })

  return result
})

async function fetchInitialData() {
  loading.value = true
  try {
    const [cats, arts] = await Promise.all([
      docsApi.getCategories(),
      docsApi.getArticles()
    ])
    allCategories.value = cats
    allArticles.value = arts
  } catch (e) {
    console.error('Failed to fetch docs', e)
  } finally {
    loading.value = false
  }
}

async function loadArticleContent() {
  const slug = route.params.slug as string
  if (!slug) {
    currentArticle.value = null
    error.value = false
    return
  }

  try {
    currentArticle.value = await docsApi.getArticle(slug)
    error.value = false
    document.getElementById('docs-main-scroll')?.scrollTo(0, 0)
  } catch (e) {
    currentArticle.value = null
    error.value = true
  }
}

function formatDate(dateStr: string): string {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

onMounted(async () => {
  await fetchInitialData()
  loadArticleContent()
})

watch(() => route.params.slug, () => {
  loadArticleContent()
})
</script>

<style scoped>
.prose {
  color: var(--on-surface);
  line-height: 1.75;
}
:deep(.prose h1),
:deep(.prose h2),
:deep(.prose h3),
:deep(.prose h4) {
  color: var(--on-surface);
  font-weight: 700;
  margin-top: 2em;
  margin-bottom: 1em;
  line-height: 1.3333333;
}
:deep(.prose h2) {
  font-size: 1.5em;
  padding-bottom: 0.3em;
  border-bottom: 1px solid var(--outline-variant);
}
:deep(.prose h3) {
  font-size: 1.25em;
}
:deep(.prose p) {
  margin-top: 1.25em;
  margin-bottom: 1.25em;
}
:deep(.prose a) {
  color: var(--primary);
  text-decoration: underline;
  font-weight: 500;
}
:deep(.prose a:hover) {
  color: var(--primary-container);
}
:deep(.prose strong) {
  font-weight: 600;
  color: var(--on-surface);
}
:deep(.prose ul),
:deep(.prose ol) {
  margin-top: 1.25em;
  margin-bottom: 1.25em;
  padding-left: 1.625em;
}
:deep(.prose li) {
  margin-top: 0.5em;
  margin-bottom: 0.5em;
}
:deep(.prose ul > li) {
  list-style-type: disc;
}
:deep(.prose ol > li) {
  list-style-type: decimal;
}
:deep(.prose blockquote) {
  font-weight: 500;
  font-style: italic;
  color: var(--on-surface-variant);
  border-left-width: 0.25rem;
  border-left-color: var(--primary);
  quotes: "\201C""\201D""\2018""\2019";
  margin-top: 1.6em;
  margin-bottom: 1.6em;
  padding: 1rem;
  background: var(--primary-container);
  border-radius: 0 0.5rem 0.5rem 0;
}
:deep(.prose code) {
  color: var(--on-surface);
  background-color: var(--surface-container-highest);
  font-weight: 500;
  font-size: 0.875em;
  padding: 0.2em 0.4em;
  border-radius: 0.25rem;
}
:deep(.prose pre) {
  color: #e2e8f0;
  background-color: #1e293b;
  overflow-x: auto;
  font-size: 0.875em;
  line-height: 1.7142857;
  margin-top: 1.7142857em;
  margin-bottom: 1.7142857em;
  border-radius: 0.5rem;
  padding: 1.1428571em 1.4285714em;
}
:deep(.prose pre code) {
  background-color: transparent;
  border-width: 0;
  border-radius: 0;
  padding: 0;
  font-weight: inherit;
  color: inherit;
  font-size: inherit;
  font-family: inherit;
  line-height: inherit;
}
:deep(.prose table) {
  width: 100%;
  table-layout: auto;
  text-align: left;
  margin-top: 2em;
  margin-bottom: 2em;
  font-size: 0.875em;
  line-height: 1.7142857;
  border-collapse: collapse;
}
:deep(.prose thead) {
  color: var(--on-surface);
  font-weight: 600;
  border-bottom-width: 1px;
  border-bottom-color: var(--outline-variant);
  background-color: var(--surface-container-low);
}
:deep(.prose thead th) {
  vertical-align: bottom;
  padding: 0.75rem 1rem;
}
:deep(.prose tbody tr) {
  border-bottom-width: 1px;
  border-bottom-color: var(--outline-variant);
}
:deep(.prose tbody tr:last-child) {
  border-bottom-width: 0;
}
:deep(.prose tbody td) {
  vertical-align: baseline;
  padding: 0.75rem 1rem;
}
:deep(.prose img) {
  margin-top: 2em;
  margin-bottom: 2em;
  border-radius: 0.5rem;
  border: 1px solid var(--outline-variant);
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}
</style>