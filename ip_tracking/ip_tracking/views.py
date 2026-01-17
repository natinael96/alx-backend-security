from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.views import View


@ratelimit(key='ip', rate='5/m', method='POST', block=True)
@ratelimit(key='user', rate='10/m', method='POST', block=True)
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
    @method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True))
    @method_decorator(ratelimit(key='user', rate='10/m', method='POST', block=True))
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

