import uuid
from django.db import models


class HelpCategory(models.Model):
    """
    Locally stored category — synced from CMS via push.
    source_slug: CMS Category ka slug — upsert key for update_or_create.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source_slug = models.SlugField(max_length=255, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('display_order', 'name')
        verbose_name = 'Help Category'
        verbose_name_plural = 'Help Categories'

    def __str__(self):
        return self.name


class HelpArticle(models.Model):
    """
    Locally stored article — synced from CMS via push.
    source_id: CMS Article UUID — the primary upsert key.
    When the same article is re-published (after an edit),
    update_or_create(source_id=...) updates the existing record
    instead of creating a duplicate.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # CMS article.id — never changes for the same article
    source_id = models.UUIDField(unique=True, db_index=True)
    category = models.ForeignKey(
        HelpCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles',
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField(blank=True, null=True)
    seo_title = models.CharField(max_length=255, blank=True, null=True)
    seo_description = models.CharField(max_length=512, blank=True, null=True)
    reading_time = models.CharField(max_length=20, blank=True, null=True)
    featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-published_at', '-created_at')
        verbose_name = 'Help Article'
        verbose_name_plural = 'Help Articles'

    def __str__(self):
        return self.title
