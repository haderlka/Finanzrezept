from django.shortcuts import render, get_object_or_404
from django.http import Http404
from core.blog import get_blog_posts, get_post_by_slug, get_all_tags
from calculators.compound_interest.calculator import calculate_compound_interest
from calculators.risk_profiler.calculator import calculate_risk_profile

# Create your views here.

def home(request):
    return render(request, 'core/home.html')

def impressum(request):
    return render(request, 'core/impressum.html', {
        'title': 'Impressum - Finanzrezept'
    })

def blog_list(request):
    tags = request.GET.getlist('tag')  # Get all tags from the query parameters
    posts = get_blog_posts(tags=tags)  # Pass the list of tags to get_blog_posts
    all_tags = get_all_tags()
    return render(request, 'core/blog_list.html', {
        'posts': posts,
        'tags': all_tags,
        'selected_tags': tags  # Pass the selected tags to the template
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

def search(request):
    query = request.GET.get('q', '')
    blog_results = []
    calculator_results = []

    if query:
        # Search in blog posts
        all_posts = get_blog_posts()
        for post in all_posts:
            if (query.lower() in post.title.lower() or 
                query.lower() in post.description.lower() or 
                query.lower() in post.content.lower()):
                blog_results.append(post)

        # Search in calculators
        available_calculators = [
            {
                'title': 'Zinseszinsrechner',
                'description': 'Berechnen Sie, wie sich Ihr Vermögen durch Zinseszins entwickelt.',
                'url': '/rechner/zinseszins/'
            }
        ]
        
        # Only add calculators that match the search query
        for calculator in available_calculators:
            if (query.lower() in calculator['title'].lower() or 
                query.lower() in calculator['description'].lower()):
                calculator_results.append(calculator)

    return render(request, 'core/search.html', {
        'query': query,
        'blog_results': blog_results,
        'calculator_results': calculator_results
    })

def risk_profiler(request):
    if request.method == 'POST':
        result = calculate_risk_profile(request.POST)
        return render(request, 'core/calculator_risk_profiler_result.html', result)
    return render(request, 'core/calculator_risk_profiler.html')
