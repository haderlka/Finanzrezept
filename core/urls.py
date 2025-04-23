from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('impressum/', views.impressum, name='impressum'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_post, name='blog_post'),
    path('rechner/', views.calculators, name='calculators'),
    path('rechner/zinseszins/', views.compound_interest_calculator, name='compound_interest_calculator'),
    path('rechner/risikoprofil/', views.risk_profiler, name='risk_profiler'),
    path('statistiken/', views.statistics, name='statistics'),
    path('datenschutz/', views.datenschutz, name='datenschutz'),
    path('about/', views.about, name='about'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('suche/', views.search, name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static('/blog/images/', document_root='content/blog/images') 