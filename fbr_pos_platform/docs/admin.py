from django.contrib import admin
from .models import HelpCategory, HelpArticle


@admin.register(HelpCategory)
class HelpCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'source_slug', 'is_active', 'display_order', 'updated_at')
    search_fields = ('name', 'source_slug')
    list_filter = ('is_active',)
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(HelpArticle)
class HelpArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_published', 'featured', 'published_at', 'updated_at')
    search_fields = ('title', 'slug', 'source_id')
    list_filter = ('is_published', 'featured', 'category')
    readonly_fields = ('id', 'source_id', 'created_at', 'updated_at')
    ordering = ('-published_at',)
