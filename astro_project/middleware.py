import re
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [
            re.compile(r'^/$'),  # Home page
            re.compile(r'^/admin/'),
            re.compile(r'^/static/'),
            re.compile(r'^/media/'),
            re.compile(r'^/i18n/'), # Language switching
            re.compile(r'^/accounts/login/'),
            re.compile(r'^/accounts/register/'),
            re.compile(r'^/accounts/verify-phone-auth/'), # Phone auth verification
            re.compile(r'^/astrologers/'),
            re.compile(r'^/astromall/'),
            re.compile(r'^/blog/'),
            re.compile(r'^/kundali/'),
            re.compile(r'^/horoscope/'),
        ]

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')
        
        if request.user.is_authenticated:
            return None

        path = request.path_info
        
        # Check if the path is in the exempt list
        for url_pattern in self.exempt_urls:
            if url_pattern.match(path):
                return None

        # Redirect to login page for all other URLs
        login_url = reverse('accounts:login')
        return redirect(f'{login_url}?next={request.path}')
