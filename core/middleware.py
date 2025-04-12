from django.utils import timezone
from .models import PageView, CalculatorUsage

class StatisticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Track page view
        if not request.path.startswith('/admin/'):  # Don't track admin pages
            PageView.objects.create(
                url=request.path,
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT'),
                referrer=request.META.get('HTTP_REFERER'),
                session_id=request.session.session_key
            )

        response = self.get_response(request)
        return response

class CalculatorTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Track calculator usage
        if request.method == 'POST' and '/rechner/' in request.path:
            calculator_name = request.path.split('/')[-2]  # Get the calculator name from URL
            CalculatorUsage.objects.create(
                calculator_name=calculator_name,
                ip_address=request.META.get('REMOTE_ADDR'),
                session_id=request.session.session_key,
                input_data=request.POST.dict()  # Store all POST data
            )

        response = self.get_response(request)
        return response 