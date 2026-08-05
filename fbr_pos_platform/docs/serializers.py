from rest_framework import serializers
from .models import HelpCategory, HelpArticle


class HelpCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpCategory
        fields = [
            'id', 'name', 'source_slug', 'description',
            'display_order', 'is_active',
        ]


class HelpArticleSerializer(serializers.ModelSerializer):
    category = HelpCategorySerializer(read_only=True)

    class Meta:
        model = HelpArticle
        fields = [
            'id', 'source_id', 'title', 'slug', 'content',
            'seo_title', 'seo_description', 'reading_time',
            'featured', 'is_published', 'published_at',
            'category', 'created_at', 'updated_at',
        ]


class ReceiveArticleSerializer(serializers.Serializer):
    """
    Validates the incoming push payload from the CMS.
    Not a ModelSerializer — save is handled manually via update_or_create.
    """
    source_id       = serializers.UUIDField()
    title           = serializers.CharField(max_length=255)
    slug            = serializers.SlugField(max_length=255)
    content         = serializers.CharField(allow_blank=True, required=False, default='')
    category_name   = serializers.CharField(max_length=255, allow_null=True, required=False)
    category_slug   = serializers.SlugField(max_length=255, allow_null=True, required=False)
    seo_title       = serializers.CharField(max_length=255, allow_blank=True, required=False, default='')
    seo_description = serializers.CharField(max_length=512, allow_blank=True, required=False, default='')
    reading_time    = serializers.CharField(max_length=20, allow_blank=True, required=False, default='')
    featured        = serializers.BooleanField(default=False)
    published_at    = serializers.DateTimeField(allow_null=True, required=False)
