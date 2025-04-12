from django.shortcuts import render, get_object_or_404
from django.http import Http404
from core.blog import get_blog_posts, get_post_by_slug, get_all_tags
from calculators.compound_interest.calculator import calculate_compound_interest

# Create your views here.

def home(request):
    return render(request, 'core/home.html')

def impressum(request):
    return render(request, 'core/impressum.html', {
        'title': 'Impressum - Finanzquant'
    })

def blog_list(request):
    tag = request.GET.get('tag')
    posts = get_blog_posts(tag=tag)
    tags = get_all_tags()
    return render(request, 'core/blog_list.html', {
        'posts': posts,
        'tags': tags,
        'current_tag': tag
    })

def blog_post(request, slug):
    post = get_post_by_slug(slug)
    if not post:
        return render(request, 'core/404.html', status=404)
    return render(request, 'core/blog_post.html', {'post': post})

def calculators(request):
    return render(request, 'core/calculators.html')

def compound_interest_calculator(request):
    result = None
    initial_amount = None
    monthly_contribution = None
    annual_interest_rate = None
    years = None
    
    if request.method == 'POST':
        try:
            initial_amount = float(request.POST.get('initial_amount', 1000))
            monthly_contribution = float(request.POST.get('monthly_contribution', 100))
            annual_interest_rate = float(request.POST.get('annual_interest_rate', 5))
            years = int(request.POST.get('years', 10))
            
            result = calculate_compound_interest(
                initial_amount=initial_amount,
                monthly_contribution=monthly_contribution,
                annual_interest_rate=annual_interest_rate,
                years=years
            )
        except (ValueError, TypeError):
            # Handle invalid input
            pass
    
    return render(request, 'core/calculators_compound_interest.html', {
        'result': result,
        'initial_amount': initial_amount,
        'monthly_contribution': monthly_contribution,
        'annual_interest_rate': annual_interest_rate,
        'years': years
    })
