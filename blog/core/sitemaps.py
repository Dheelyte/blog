from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Article, Category

class ArticleSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Article.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.updated_at

class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        # Only categories that actually have published articles —
        # never advertise empty pages to crawlers/AdSense.
        return (
            Category.objects
            .filter(articles__published=True)
            .distinct()
        )

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['home', 'about', 'contact', 'privacy', 'terms', 'cookies']

    def location(self, item):
        return reverse(f'blog:{item}')
