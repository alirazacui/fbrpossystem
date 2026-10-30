"""
Server-rendered (SEO friendly) pages for the docs/help section.

Why: Vue SPA can return a mostly empty shell to crawlers. These views render
full HTML with unique title/meta/canonical/schema per page.

Optional settings.py values (all have defaults):
    DOCS_SITE_URL = "https://myfbrpos.com"  # canonical domain, no trailing slash
    DOCS_BRAND = "myfbrpos"
    DOCS_CTA_URL = "/"                      # where CTA button points
    DOCS_CTA_TEXT = "Free demo lein"
"""

import html
import json
import re
from xml.sax.saxutils import escape

from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.utils.html import strip_tags
from django.views.decorators.http import require_GET

from .models import HelpArticle, HelpCategory

_IMG_SRC = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.I)
_WS = re.compile(r"\s+")
_H1_OPEN = re.compile(r"<h1(?=[\\s>])", re.I)
_H1_CLOSE = re.compile(r"</h1>", re.I)
_IMG_NO_LAZY = re.compile(r"<img(?![^>]*\\sloading=)", re.I)


def _site():
    return getattr(settings, "DOCS_SITE_URL", "https://myfbrpos.com").rstrip("/")


def _brand():
    return getattr(settings, "DOCS_BRAND", "myfbrpos")


def _plain(raw_html, limit):
    text = _WS.sub(" ", html.unescape(strip_tags(raw_html or ""))).strip()
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(",.;:- ") + "..."


def _meta_title(article):
    title = (article.seo_title or article.title or "").strip()
    brand = _brand()
    if brand.lower() not in title.lower() and len(title) + len(brand) + 3 <= 60:
        title = f"{title} | {brand}"
    return title


def _prepare_body(raw_html):
    # The page already has one <h1>; demote h1s inside article body.
    body = raw_html or ""
    body = _H1_OPEN.sub("<h2", body)
    body = _H1_CLOSE.sub("</h2>", body)
    return _IMG_NO_LAZY.sub('<img loading="lazy"', body)


def _ld_json(data):
    # "</" must not appear inside an inline <script>.
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")


def _cta():
    return {
        "cta_url": getattr(settings, "DOCS_CTA_URL", "/"),
        "cta_text": getattr(settings, "DOCS_CTA_TEXT", "Free demo lein"),
        "brand": _brand(),
        "site_url": _site(),
    }


@require_GET
def doc_detail(request, slug):
    try:
        article = HelpArticle.objects.select_related("category").get(
            slug=slug, is_published=True
        )
    except HelpArticle.DoesNotExist:
        raise Http404("Article not found")

    site = _site()
    url = f"{site}/docs/{article.slug}"
    description = (article.seo_description or "").strip() or _plain(article.content, 155)
    m = _IMG_SRC.search(article.content or "")
    og_image = m.group(1) if m else ""

    related = []
    if article.category_id:
        related = list(
            HelpArticle.objects.filter(
                category_id=article.category_id, is_published=True
            )
            .exclude(pk=article.pk)
            .only("title", "slug")[:5]
        )

    crumbs = [("Home", f"{site}/"), ("Docs", f"{site}/docs")]
    if article.category:
        crumbs.append((article.category.name, f"{site}/docs"))
    crumbs.append((article.title, url))

    org = {"@type": "Organization", "name": _brand(), "url": site}
    article_ld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": article.title[:110],
        "description": description,
        "mainEntityOfPage": url,
        "datePublished": (article.published_at or article.created_at).isoformat(),
        "dateModified": article.updated_at.isoformat(),
        "author": org,
        "publisher": org,
    }
    if og_image:
        article_ld["image"] = [og_image]

    breadcrumb_ld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": n, "item": u}
            for i, (n, u) in enumerate(crumbs, start=1)
        ],
    }

    ctx = {
        "article": article,
        "body": _prepare_body(article.content),
        "meta_title": _meta_title(article),
        "meta_description": description,
        "canonical": url,
        "og_image": og_image,
        "related": related,
        "ld_json": [_ld_json(article_ld), _ld_json(breadcrumb_ld)],
        **_cta(),
    }
    return render(request, "docs/seo_detail.html", ctx)


@require_GET
def doc_index(request):
    categories = list(HelpCategory.objects.filter(is_active=True))
    active_ids = {c.id for c in categories}
    by_cat, uncategorized = {}, []

    for article in HelpArticle.objects.filter(is_published=True).only(
        "title", "slug", "seo_description", "reading_time", "category_id"
    ):
        if article.category_id in active_ids:
            by_cat.setdefault(article.category_id, []).append(article)
        else:
            uncategorized.append(article)

    sections = [(c, by_cat[c.id]) for c in categories if c.id in by_cat]
    if uncategorized:
        sections.append((None, uncategorized))

    ctx = {
        "sections": sections,
        "canonical": f"{_site()}/docs",
        "meta_title": getattr(
            settings, "DOCS_INDEX_TITLE", f"FBR Guides and Help Center | {_brand()}"
        ),
        "meta_description": getattr(
            settings,
            "DOCS_INDEX_DESCRIPTION",
            "FBR digital invoicing, NTN/STRN registration, HS code aur POS integration "
            "ki asaan guides Pakistani businesses ke liye.",
        ),
        **_cta(),
    }
    return render(request, "docs/seo_index.html", ctx)


@require_GET
def sitemap_xml(request):
    site = _site()
    articles = list(
        HelpArticle.objects.filter(is_published=True).only("slug", "updated_at")
    )
    latest = max((article.updated_at for article in articles), default=None)

    entries = [(f"{site}/", None, "1.0"), (f"{site}/docs", latest, "0.8")]
    entries += [(f"{site}/docs/{article.slug}", article.updated_at, "0.7") for article in articles]

    out = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc, mod, priority in entries:
        out.append("<url>")
        out.append(f"<loc>{escape(loc)}</loc>")
        if mod:
            out.append(f"<lastmod>{mod.strftime('%Y-%m-%d')}</lastmod>")
        out.append(f"<priority>{priority}</priority>")
        out.append("</url>")
    out.append("</urlset>")

    return HttpResponse("\n".join(out), content_type="application/xml")


@require_GET
def robots_txt(request):
    body = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /api/\n"
        "Disallow: /admin/\n\n"
        f"Sitemap: {_site()}/sitemap.xml\n"
    )
    return HttpResponse(body, content_type="text/plain")
