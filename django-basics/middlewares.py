from django.conf import settings
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class IpCheckMiddleware(MiddlewareMixin):
    """
    Just for example: we can refuse any unauthorized requests using
    `ALLOWED_IP` setting.
    """

    def process_request(self, request):
        ip = request.META['REMOTE_ADDR']
        if ip not in settings.ALLOWED_IP:
            if not request.user.is_authenticated:
                return HttpResponse("Not allowed {}".format(ip), status=403)
        return None
