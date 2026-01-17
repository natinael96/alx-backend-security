from django.utils import timezone
from .models import RequestLog


class IPLoggingMiddleware:
    """
    Middleware to log IP address, timestamp, and path of every incoming request.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the IP address from the request
        # Try to get the real IP address (considering proxies)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0].strip()
        else:
            ip_address = request.META.get('REMOTE_ADDR', '0.0.0.0')

        # Get the path
        path = request.path

        # Log the request
        RequestLog.objects.create(
            ip_address=ip_address,
            timestamp=timezone.now(),
            path=path
        )

        # Process the request
        response = self.get_response(request)

        return response

