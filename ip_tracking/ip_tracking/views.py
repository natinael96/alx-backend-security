from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.views import View


def get_rate_limit_key(request):
    """
    Custom key function for rate limiting.
    Returns 'user' key for authenticated users, 'ip' key for anonymous users.
    """
    if request.user.is_authenticated:
        return f"user:{request.user.id}"
    return f"ip:{request.META.get('REMOTE_ADDR', 'unknown')}"


def get_rate_limit_rate(request):
    """
    Custom rate function for rate limiting.
    Returns '10/m' for authenticated users, '5/m' for anonymous users.
    """
    if request.user.is_authenticated:
        return '10/m'
    return '5/m'


@ratelimit(key=get_rate_limit_key, rate=get_rate_limit_rate, method='POST', block=True)
@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    Login view with rate limiting:
    - 5 requests/minute for anonymous users (by IP)
    - 10 requests/minute for authenticated users (by user)
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'ip_tracking/login.html', {})


class LoginView(View):
    """
    Class-based login view with rate limiting.
    """
    @method_decorator(ratelimit(key=get_rate_limit_key, rate=get_rate_limit_rate, method='POST', block=True))
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'ip_tracking/login.html', {})
    
    def get(self, request):
        return render(request, 'ip_tracking/login.html', {})

