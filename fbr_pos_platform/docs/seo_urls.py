"""
Root-level (not under /api/) SEO routes.
In config/urls.py include via: path("", include("docs.seo_urls"))
"""

from django.urls import path, re_path

from .seo_views import doc_detail, doc_index, robots_txt, sitemap_xml

urlpatterns = [
    # /docs and /docs/
    re_path(r"^docs/?$", doc_index, name="seo-docs-index"),
    # /docs/<slug> and /docs/<slug>/
    re_path(r"^docs/(?P<slug>[-\w]+)/?$", doc_detail, name="seo-docs-detail"),
    path("sitemap.xml", sitemap_xml, name="seo-sitemap"),
    path("robots.txt", robots_txt, name="seo-robots"),
]
