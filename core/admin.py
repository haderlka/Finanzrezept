from django.contrib import admin
from django.urls import path
from django.utils.html import format_html
from .models import PageView, CalculatorUsage
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ('url', 'timestamp', 'ip_address')
    list_filter = ('timestamp',)
    search_fields = ('url', 'ip_address')
    readonly_fields = ('url', 'timestamp', 'ip_address', 'user_agent', 'referrer', 'session_id')

@admin.register(CalculatorUsage)
class CalculatorUsageAdmin(admin.ModelAdmin):
    list_display = ('calculator_name', 'timestamp', 'ip_address')
    list_filter = ('calculator_name', 'timestamp')
    search_fields = ('calculator_name', 'ip_address')
    readonly_fields = ('calculator_name', 'timestamp', 'ip_address', 'session_id', 'input_data')

    def get_list_display_links(self, request, list_display):
        return None

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

# Custom admin site to add statistics view
class CustomAdminSite(admin.AdminSite):
    index_template = 'admin/custom_index.html'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('statistics/', self.admin_view(self.statistics_view), name='statistics'),
        ]
        return custom_urls + urls

    def statistics_view(self, request):
        if not request.user.is_staff:
            return self.login_required(request)
            
        # Get time ranges
        today = timezone.now().date()
        last_week = today - timedelta(days=7)
        last_month = today - timedelta(days=30)

        # Page view statistics
        total_views = PageView.objects.count()
        today_views = PageView.objects.filter(timestamp__date=today).count()
        weekly_views = PageView.objects.filter(timestamp__date__gte=last_week).count()
        monthly_views = PageView.objects.filter(timestamp__date__gte=last_month).count()

        # Popular pages
        popular_pages = PageView.objects.values('url').annotate(
            count=Count('id')
        ).order_by('-count')[:10]

        # Calculator usage statistics
        calculator_stats = CalculatorUsage.objects.values('calculator_name').annotate(
            count=Count('id')
        ).order_by('-count')

        context = {
            'total_views': total_views,
            'today_views': today_views,
            'weekly_views': weekly_views,
            'monthly_views': monthly_views,
            'popular_pages': popular_pages,
            'calculator_stats': calculator_stats,
            'title': 'Website Statistics',
            'site_header': 'Finanzrezept Administration',
            'site_title': 'Finanzrezept Admin',
            'has_permission': request.user.is_staff,
            'available_apps': self.get_app_list(request),
            'is_popup': False,
            'is_nav_sidebar_enabled': True,
        }
        return render(request, 'admin/statistics.html', context)

# Create and configure the custom admin site
admin_site = CustomAdminSite(name='admin')
admin_site.register(PageView, PageViewAdmin)
admin_site.register(CalculatorUsage, CalculatorUsageAdmin)

# Replace the default admin site
admin.site = admin_site
