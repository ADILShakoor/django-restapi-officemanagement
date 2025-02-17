from django.utils.deprecation import MiddlewareMixin
from rest_framework.authtoken.models import Token

class TokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """ Attach token from cookies to headers so DRF can authenticate """
        if 'auth_token' in request.COOKIES:
            request.META['HTTP_AUTHORIZATION'] = f'Token {request.COOKIES["auth_token"]}'
        # if request.user.is_authenticated:
        #     token, _ = Token.objects.get_or_create(user=request.user)  # Fetch token
        #     request.META['HTTP_AUTHORIZATION'] = f"Token {token.key}"  # Attach token
