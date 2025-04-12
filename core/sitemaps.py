from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .blog import get_blog_posts
from .models import PageView

class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ['home', 'blog_list', 'calculators', 'impressum', 'datenschutz']

    def location(self, item):
        return reverse(f'core:{item}')

class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return get_blog_posts()

    def location(self, obj):
        return reverse('core:blog_detail', args=[obj['slug']])

    def lastmod(self, obj):
        return obj['date']

class CalculatorSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return ['risk_profiler']  # Add more calculators as they are created

    def location(self, item):
        return reverse(f'core:{item}') 