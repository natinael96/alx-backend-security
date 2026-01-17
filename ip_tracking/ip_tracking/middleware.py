from django.http import HttpResponseForbidden
from django.utils import timezone
from django.core.cache import cache
from .models import RequestLog, BlockedIP


class IPLoggingMiddleware:
    """
    Middleware to log IP address, timestamp, path, and geolocation data of every incoming request.
    Also blocks requests from IPs in the BlockedIP model.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def _get_ip_address(self, request):
        """Extract IP address from request, handling proxies."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0].strip()
        else:
            ip_address = request.META.get('REMOTE_ADDR', '0.0.0.0')
        return ip_address

    def _get_geolocation(self, ip_address):
        """
        Get geolocation data for an IP address with 24-hour caching.
        Returns tuple (country, city) or (None, None) if unavailable.
        Uses django-ipgeolocation package.
        """
        # Check cache first (24 hours = 86400 seconds)
        cache_key = f'ip_geolocation_{ip_address}'
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return cached_data.get('country', None), cached_data.get('city', None)

        # If not in cache, fetch from API
        country = None
        city = None
        
        try:
            # Try to use django-ipgeolocation or ipgeolocation package
            from django.conf import settings
            
            # Try ipgeolocation package (common package)
            try:
                from ipgeolocation import IPGeolocationAPI
                api_key = getattr(settings, 'IPGEOLOCATION_API_KEY', None)
                if api_key:
                    api = IPGeolocationAPI(api_key)
                    result = api.get_geolocation(ip_address=ip_address)
                    
                    if result and result.get('status') == 200:
                        country = result.get('country_name', '')
                        city = result.get('city', '')
            except ImportError:
                # Try alternative: ipapi or other geolocation services
                try:
                    import requests
                    # Using ipapi.co as a free alternative (no API key required for basic usage)
                    response = requests.get(f'https://ipapi.co/{ip_address}/json/', timeout=2)
                    if response.status_code == 200:
                        data = response.json()
                        country = data.get('country_name', '')
                        city = data.get('city', '')
                except Exception:
                    pass
        except Exception:
            # If geolocation fails, return None values
            pass

        # Cache results for 24 hours (86400 seconds)
        cache.set(cache_key, {'country': country, 'city': city}, 86400)
        return country, city

    def __call__(self, request):
        # Get the IP address from the request
        ip_address = self._get_ip_address(request)

        # Check if IP is blocked
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden("Access Denied: Your IP address has been blocked.")

        # Get the path
        path = request.path

        # Get geolocation data
        country, city = self._get_geolocation(ip_address)

        # Log the request
        RequestLog.objects.create(
            ip_address=ip_address,
            timestamp=timezone.now(),
            path=path,
            country=country,
            city=city
        )

        # Process the request
        response = self.get_response(request)

        return response

