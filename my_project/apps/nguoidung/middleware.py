from rest_framework_simplejwt.tokens import AccessToken
from django.http import JsonResponse
from .models import BlacklistedAccessToken


class JWTBlacklistMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            if BlacklistedAccessToken.objects.filter(token_access=token).exists():
                return JsonResponse({'error': 'Token đã hết hạn'}, status=401)
        return self.get_response(request)

from django.utils.timezone import now
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.conf import settings
from django.contrib.auth.models import AnonymousUser

class TokenRefreshMiddleware:
    """
    Middleware để tự động làm mới Access Token.
    - Nếu Access Token còn dưới 1 phút -> làm mới Access Token từ Refresh Token.
    - Nếu Refresh Token hết hạn -> Không tạo mới token, yêu cầu người dùng đăng nhập lại.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        access_token_str = request.COOKIES.get("access_token")
        refresh_token_str = request.COOKIES.get("refresh_token")
        response = self.get_response(request)  # Mặc định lấy response

        if not access_token_str or not refresh_token_str:
            return response  # Không có token -> bỏ qua middleware

        try:
            # Kiểm tra Access Token có hợp lệ không
            access_token = AccessToken(access_token_str)
            expiration_time = access_token["exp"]  # Unix timestamp
            remaining_time = expiration_time - int(now().timestamp())

            if remaining_time < 60:  # Nếu còn dưới 1 phút, làm mới Access Token
                refresh_token = RefreshToken(refresh_token_str)
                new_access_token = refresh_token.access_token

                response.set_cookie(
                    key="access_token",
                    value=str(new_access_token),
                    httponly=True,
                    secure=True,
                    samesite="None",
                    max_age=new_access_token.lifetime.total_seconds(),
                )

        except Exception:
            # Access Token không hợp lệ, kiểm tra Refresh Token
            try:
                refresh_token = RefreshToken(refresh_token_str)
                new_access_token = refresh_token.access_token

                response.set_cookie(
                    key="access_token",
                    value=str(new_access_token),
                    httponly=True,
                    secure=True,
                    samesite="None",
                    max_age=new_access_token.lifetime.total_seconds(),
                )

            except Exception:
                # Refresh Token hết hạn -> Không tự động tạo lại, yêu cầu đăng nhập lại
                response.delete_cookie("access_token")
                response.delete_cookie("refresh_token")

        return response


from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

class AttachTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Lấy token từ Cookie
        access_token = request.COOKIES.get("access_token")
        if access_token :
            request.META["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"