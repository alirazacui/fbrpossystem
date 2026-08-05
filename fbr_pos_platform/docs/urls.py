from django.urls import path
from .views import (
    ReceiveArticleView,
    RemoveArticleView,
    HelpCategoryListView,
    HelpArticleListView,
    HelpArticleDetailView,
)

urlpatterns = [
    # ── Internal: CMS push endpoints ──────────────────────────────────────
    path('docs/receive-article/', ReceiveArticleView.as_view(),  name='docs-receive-article'),
    path('docs/remove-article/',  RemoveArticleView.as_view(),   name='docs-remove-article'),

    # ── Public: Vue frontend read endpoints ───────────────────────────────
    path('docs/categories/',             HelpCategoryListView.as_view(),  name='docs-categories'),
    path('docs/articles/',               HelpArticleListView.as_view(),   name='docs-articles'),
    path('docs/articles/<slug:slug>/',   HelpArticleDetailView.as_view(), name='docs-article-detail'),
]
