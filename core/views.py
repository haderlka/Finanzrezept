from django.shortcuts import render, get_object_or_404
from django.http import Http404
from . import blog

# Create your views here.

def home(request):
    return render(request, 'core/home.html', {
        'title': 'Finanzquant - Ihr persönlicher Finanzmanager'
    })

def impressum(request):
    return render(request, 'core/impressum.html', {
        'title': 'Impressum - Finanzquant'
    })

def blog_list(request):
    posts = blog.get_blog_posts()
    return render(request, 'core/blog_list.html', {
        'title': 'Blog - Finanzquant',
        'posts': posts
    })

def blog_post(request, slug):
    post = blog.get_post_by_slug(slug)
    if post is None:
        raise Http404("Blog post not found")
    return render(request, 'core/blog_post.html', {
        'title': f'{post.title} - Finanzquant Blog',
        'post': post
    })
