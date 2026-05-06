from .models import PageVisit
from django.utils.deprecation import MiddlewareMixin
import re

class AnalyticsMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Skip tracking for static files, admin, and API calls
        if (request.path.startswith('/static/') or
            request.path.startswith('/admin/') or
            request.path.startswith('/media/') or
            'favicon' in request.path or
            request.path.endswith('.ico') or
            request.path.endswith('.png') or
            request.path.endswith('.jpg') or
            request.path.endswith('.jpeg') or
            request.path.endswith('.gif') or
            request.path.endswith('.css') or
            request.path.endswith('.js')):
            return None

        # Track the page visit
        try:
            PageVisit.objects.create(
                path=request.path,
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                ip_address=self.get_client_ip(request),
                referrer=request.META.get('HTTP_REFERER', ''),
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key or '',
            )
        except Exception as e:
            # Silently fail if tracking fails
            pass

        return None

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip