from django.http.request import split_domain_port

from django.conf import settings
from django.contrib.redirects.models import Redirect
from django.http import HttpResponseGone, HttpResponsePermanentRedirect
from django.utils.deprecation import MiddlewareMixin


class RedirectFallbackMiddleware(MiddlewareMixin):
    # Defined as class-level attributes to be subclassing-friendly.
    response_gone_class = HttpResponseGone
    response_redirect_class = HttpResponsePermanentRedirect

    def process_response(self, request, response):
        # No need to check for a redirect for non-404 responses.
        if response.status_code != 404:
            return response

        domain, _ = split_domain_port(request.get_host())

        paths = [request.get_full_path()]
        if settings.APPEND_SLASH and not request.path.endswith('/'):
            paths.append(
                request.get_full_path(force_append_slash=True)
            )

        r = Redirect.objects.filter(
            domain__in=[domain, ''],
            old_path__in=paths
        ).order_by('-domain', 'old_path').first()

        if r is not None:
            if r.new_path == '':
                return self.response_gone_class()

            return self.response_redirect_class(r.new_path)

        return response
