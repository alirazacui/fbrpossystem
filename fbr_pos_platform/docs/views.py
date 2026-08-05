import logging

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import HelpCategory, HelpArticle
from .serializers import (
    ReceiveArticleSerializer,
    HelpArticleSerializer,
    HelpCategorySerializer,
)

logger = logging.getLogger(__name__)


def _verify_api_key(request):
    """
    Shared API-key guard for all incoming CMS push endpoints.
    Key is compared against DOCS_RECEIVER_API_KEY in settings.
    """
    incoming_key = request.headers.get('X-API-KEY', '').strip()
    expected_key = getattr(settings, 'DOCS_RECEIVER_API_KEY', '').strip()
    return bool(expected_key) and incoming_key == expected_key


# ─────────────────────────────────────────────────────────────────────────────
# Internal Push Endpoints  (called by CMS Celery tasks)
# ─────────────────────────────────────────────────────────────────────────────

class ReceiveArticleView(APIView):
    """
    POST /api/docs/receive-article/
    Called by CMS whenever an article is published.

    Flow:
      1. Verify X-API-KEY header
      2. Validate payload via ReceiveArticleSerializer
      3. Upsert HelpCategory (source_slug as key)
      4. Upsert HelpArticle  (source_id  as key) → no duplicates on re-publish
    """
    permission_classes = [AllowAny]  # Auth handled manually via API key

    def post(self, request, *args, **kwargs):
        if not _verify_api_key(request):
            logger.warning("[docs] ReceiveArticle: invalid or missing X-API-KEY")
            return Response(
                {'detail': 'Forbidden — invalid API key.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ReceiveArticleSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"[docs] ReceiveArticle validation error: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        # ── 1. Resolve / create category ──────────────────────────────────
        category = None
        cat_name = data.get('category_name')
        cat_slug = data.get('category_slug')
        if cat_name and cat_slug:
            category, cat_created = HelpCategory.objects.update_or_create(
                source_slug=cat_slug,
                defaults={'name': cat_name, 'is_active': True},
            )
            logger.info(
                f"[docs] Category {'created' if cat_created else 'updated'}: "
                f"'{category.name}' (slug={cat_slug})"
            )

        # ── 2. Upsert article (source_id = unique key from CMS) ───────────
        article, created = HelpArticle.objects.update_or_create(
            source_id=data['source_id'],
            defaults={
                'title':           data['title'],
                'slug':            data['slug'],
                'content':         data.get('content', ''),
                'category':        category,
                'seo_title':       data.get('seo_title', ''),
                'seo_description': data.get('seo_description', ''),
                'reading_time':    data.get('reading_time', ''),
                'featured':        data.get('featured', False),
                'is_published':    True,
                'published_at':    data.get('published_at'),
            },
        )

        action_label = 'created' if created else 'updated'
        logger.info(
            f"[docs] Article {action_label}: '{article.title}' "
            f"(source_id={article.source_id})"
        )
        return Response(
            {
                'detail': f'Article {action_label} successfully.',
                'id': str(article.id),
                'action': action_label,
            },
            status=status.HTTP_200_OK,
        )


class RemoveArticleView(APIView):
    """
    POST /api/docs/remove-article/
    Called by CMS when an article is unpublished or deleted.
    Performs a soft-delete: sets is_published=False.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if not _verify_api_key(request):
            logger.warning("[docs] RemoveArticle: invalid or missing X-API-KEY")
            return Response(
                {'detail': 'Forbidden — invalid API key.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        source_id = request.data.get('source_id')
        if not source_id:
            return Response(
                {'detail': 'source_id is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        updated_count = HelpArticle.objects.filter(source_id=source_id).update(
            is_published=False
        )
        if updated_count:
            logger.info(f"[docs] Article unpublished: source_id={source_id}")
            return Response({'detail': 'Article unpublished successfully.'})

        logger.warning(f"[docs] RemoveArticle: no article found for source_id={source_id}")
        return Response(
            {'detail': 'Article not found.'},
            status=status.HTTP_404_NOT_FOUND,
        )


# ─────────────────────────────────────────────────────────────────────────────
# Public Read Endpoints  (called by Vue frontend)
# ─────────────────────────────────────────────────────────────────────────────

class HelpCategoryListView(APIView):
    """
    GET /api/docs/categories/
    Returns all active categories for the sidebar.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        categories = HelpCategory.objects.filter(is_active=True)
        serializer = HelpCategorySerializer(categories, many=True)
        return Response(serializer.data)


class HelpArticleListView(APIView):
    """
    GET /api/docs/articles/
    GET /api/docs/articles/?category=<source_slug>
    Returns published articles, optionally filtered by category slug.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = HelpArticle.objects.filter(
            is_published=True
        ).select_related('category')

        cat_slug = request.query_params.get('category')
        if cat_slug:
            queryset = queryset.filter(category__source_slug=cat_slug)

        serializer = HelpArticleSerializer(queryset, many=True)
        return Response(serializer.data)


class HelpArticleDetailView(APIView):
    """
    GET /api/docs/articles/<slug>/
    Returns a single published article by slug.
    """
    permission_classes = [AllowAny]

    def get(self, request, slug):
        try:
            article = HelpArticle.objects.select_related('category').get(
                slug=slug, is_published=True
            )
        except HelpArticle.DoesNotExist:
            return Response(
                {'detail': 'Article not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(HelpArticleSerializer(article).data)
