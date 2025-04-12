from django.utils import timezone
from .models import PageView, CalculatorUsage

class StatisticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user has accepted cookies
        cookie_consent = request.COOKIES.get('cookie_consent')
        
        # Only track if user has accepted cookies or hasn't made a choice yet
        if cookie_consent != 'rejected':
            # Don't track admin pages
            if not request.path.startswith('/admin/'):
                PageView.objects.create(
                    url=request.path,
                    ip_address=request.META.get('REMOTE_ADDR'),
                    user_agent=request.META.get('HTTP_USER_AGENT'),
                    referrer=request.META.get('HTTP_REFERER'),
                    session_id=request.session.session_key,
                    timestamp=timezone.now()
                )

        response = self.get_response(request)
        return response

class CalculatorTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user has accepted cookies
        cookie_consent = request.COOKIES.get('cookie_consent')
        
        # Only track if user has accepted cookies or hasn't made a choice yet
        if cookie_consent != 'rejected' and request.method == 'POST' and '/rechner/' in request.path:
            calculator_name = request.path.split('/rechner/')[1].split('/')[0]
            CalculatorUsage.objects.create(
                calculator_name=calculator_name,
                ip_address=request.META.get('REMOTE_ADDR'),
                session_id=request.session.session_key,
                input_data=dict(request.POST),
                timestamp=timezone.now()
            )

        response = self.get_response(request)
        return response 