from rest_framework.authentication import TokenAuthentication

class CustomTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get("auth_token")  # Fetch token from cookies
        if token:
            return self.authenticate_credentials(token)
        return None
