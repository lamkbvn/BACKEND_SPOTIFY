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

import datetime
from django.utils.timezone import now
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.http import JsonResponse


class TokenRefreshMiddleware:
    """
    Middleware để kiểm tra thời gian hết hạn của Access Token.
    Nếu Access Token còn dưới 1 phút, sẽ làm mới Access Token bằng Refresh Token.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Kiểm tra nếu cookies có access token và refresh token
        access_token_str = request.COOKIES.get("access_token")
        refresh_token_str = request.COOKIES.get("refresh_token")

        if access_token_str and refresh_token_str:
            try:
                # Kiểm tra Access Token
                access_token = AccessToken(access_token_str)
                # Lấy thời gian hết hạn của Access Token
                expiration_time = access_token.payload.get('exp')  # Thời gian hết hạn (Unix timestamp)
                remaining_time = expiration_time - int(now().timestamp())

                # Nếu Access Token còn dưới 1 phút
                if remaining_time < 60:
                    # Lấy Refresh Token và làm mới Access Token
                    refresh_token = RefreshToken(refresh_token_str)
                    access_token = refresh_token.access_token  # Tạo mới Access Token từ Refresh Token

                    # Cập nhật lại cookie với Access Token mới
                    response = self.get_response(request)

                    # Hủy cookie access_token cũ
                    response.delete_cookie('access_token')

                    response.set_cookie(
                        key="access_token",
                        value=str(access_token),
                        httponly=True,  # Bảo mật: Không thể truy cập từ JavaScript
                        secure=True,  # Bật nếu chạy trên HTTPS
                        samesite="Lax",  # Ngăn chặn CSRF
                        max_age=access_token.lifetime.total_seconds(),  # Token sống lâu hơn
                    )
                    return response
            except Exception as e:
                # Nếu có lỗi khi kiểm tra token, có thể là token không hợp lệ hoặc hết hạn
                print(f"Lỗi khi làm mới Access Token: {e}")

        # Nếu không làm mới token, tiếp tục xử lý bình thường
        return self.get_response(request)

from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

class AttachTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = request.COOKIES.get("access_token")
        if access_token:
            request.META["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"
