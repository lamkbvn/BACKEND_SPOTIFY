import time

from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes

from .models import BlacklistedAccessToken
from ..common.models import NguoiDung  # Import từ common
from ..common.serializers import NguoiDungSerializer  # Import từ common

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from twilio.rest import Client
from django.conf import settings

@api_view(['POST'])
@permission_classes([AllowAny])
def them_nguoi_dung(request):
    email = request.data.get('email', None)
    so_dien_thoai = request.data.get('so_dien_thoai', None)
    mat_khau = request.data.get('password', None)

    if so_dien_thoai and NguoiDung.objects.filter(so_dien_thoai=so_dien_thoai).exists():
        return Response({"error": "Số điện thoại đã được sử dụng!"}, status=status.HTTP_400_BAD_REQUEST)

    # Mã hóa mật khẩu trước khi lưu
    if mat_khau:
        request.data['password'] = make_password(mat_khau)

    serializer = NguoiDungSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Người dùng đã được thêm thành công!", "data": serializer.data},
                        status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
# @permission_classes([IsAuthenticated])  # Chỉ người dùng đã đăng nhập mới có thể cập nhật
def cap_nhat_nguoi_dung(request):
    nguoi_dung = request.user  # Lấy người dùng từ token

    email_moi = request.data.get('email', nguoi_dung.email)
    so_dien_thoai_moi = request.data.get('so_dien_thoai', nguoi_dung.so_dien_thoai)
    mat_khau_moi = request.data.get('password', None)

    if NguoiDung.objects.filter(email=email_moi).exclude(pk=nguoi_dung.nguoi_dung_id).exists():
        return Response({"error": "Email đã được sử dụng bởi người dùng khác!"}, status=status.HTTP_400_BAD_REQUEST)

    if so_dien_thoai_moi and NguoiDung.objects.filter(so_dien_thoai=so_dien_thoai_moi).exclude(
            pk=nguoi_dung.nguoi_dung_id).exists():
        return Response({"error": "Số điện thoại đã được sử dụng bởi người dùng khác!"}, status=status.HTTP_400_BAD_REQUEST)

    # Nếu có mật khẩu mới, mã hóa trước khi cập nhật
    data_update = request.data.copy()
    if mat_khau_moi:
        data_update['password'] = make_password(mat_khau_moi)

    serializer = NguoiDungSerializer(nguoi_dung, data=data_update, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Cập nhật thông tin thành công!", "data": serializer.data}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API đăng nhập bằng email và mật khẩu
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Vui lòng nhập email và mật khẩu'}, status=400)

    email = email.strip().lower()  # Chuẩn hóa email
    print(email)

    try:
        nguoidung = NguoiDung.objects.get(email=email)
    except NguoiDung.DoesNotExist:
        return Response({'error': 'Không tìm thấy tài khoản với email này'}, status=404)

    if not check_password(password, nguoidung.password):
        return Response({'error': 'Sai mật khẩu'}, status=400)

    # Tạo JWT token
    refresh = RefreshToken.for_user(nguoidung)
    access_token = str(refresh.access_token)

    # Thiết lập cookie HttpOnly cho refresh token
    response = Response({
        'message': 'Đăng nhập thành công',
        'refresh': str(refresh),
        'access': access_token,
        'nguoi_dung_id': nguoidung.nguoi_dung_id,
        'ten_hien_thi': nguoidung.ten_hien_thi,
        'email': nguoidung.email
    }, status=201)

    response.set_cookie(
        key="refresh_token",
        value=str(refresh),
        httponly=True,
        secure=True,
        samesite="Lax",
        max_age=7 * 24 * 60 * 60
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="Lax",
        max_age=7 * 24 * 60 * 60
    )

    return response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Vui lòng cung cấp refresh token'}, status=400)

        try:
            # Thử đưa Refresh Token vào blacklist
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response({'error': 'Refresh Token không hợp lệ hoặc đã hết hạn'}, status=400)

        # Lấy access token từ header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return Response({'error': 'Không có Access Token'}, status=400)

        access_token_str = auth_header.split(" ")[1]

        try:
            # Thử kiểm tra Access Token
            access_token = AccessToken(access_token_str)
            BlacklistedAccessToken.objects.create(token_access=access_token_str)
        except ValidationError:
            return Response({'error': 'Access Token không hợp lệ'}, status=400)

        return Response({'message': 'Đăng xuất thành công'}, status=200)

    except Exception as e:
        return Response({'error': f'Lỗi hệ thống: {str(e)}'}, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    """
    API này nhận refresh token và trả về access token mới.
    """
    refresh = request.COOKIES.get('refresh_token')

    if not refresh:
        return Response({"error": "Vui lòng cung cấp refresh token"}, status=400)

    try:
        # Lấy access token từ header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return Response({'error': 'Không có Access Token'}, status=400)

        access_token_str = auth_header.split(" ")[1]

        try:
            # Thử kiểm tra Access Token
            access_token = AccessToken(access_token_str)
            BlacklistedAccessToken.objects.create(token_access=access_token_str)
        except ValidationError:
            return Response({'error': 'Access Token không hợp lệ'}, status=400)
        # Lấy access token mới từ refresh token
        refresh_token = RefreshToken(refresh)
        access_token = str(refresh_token.access_token)
        return Response({"access": access_token}, status=200)
    except Exception as e:
        return Response({"error": "Refresh token không hợp lệ hoặc đã hết hạn"}, status=400)

def get_access_token(request):
    """
    Nhận refresh token từ cookie hoặc request body,
    kiểm tra tính hợp lệ và trả về access token mới.
    """
    refreshtoken = request.COOKIES.get('refresh_token') or request.data.get('refresh')

    if not refreshtoken:
        return Response({"error": "Vui lòng cung cấp refresh token"}, status=400)

    try:
        # Kiểm tra token hợp lệ và tạo access token mới
        refresh = RefreshToken(refreshtoken)
        access_token = str(refresh.access_token)
        return Response({"access_token": access_token}, status=200)
    except (TokenError, InvalidToken):
        return Response({"error": "Refresh token không hợp lệ hoặc đã hết hạn"}, status=400)

from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse

@api_view(['POST'])
@permission_classes([AllowAny])
def request_password_reset(request):
    email = request.data.get('email')
    try:
        user = NguoiDung.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = request.build_absolute_uri(reverse('password-reset-confirm', kwargs={'uidb64': uid, 'token': token}))

        # Gửi email chứa link reset password
        send_mail(
            'Reset Your Password',
            f'Click the link to reset your password: {reset_url}',
            'lamkbvn@gmail.com',
            [email],
            fail_silently=False,
        )

        return Response({'message': 'Password reset link sent'}, status=status.HTTP_200_OK)
    except NguoiDung.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = NguoiDung.objects.get(nguoi_dung_id=uid)

        if default_token_generator.check_token(user, token):
            new_password = request.data.get('password')
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
    except (NguoiDung.DoesNotExist, ValueError):
        return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])  # Dùng IsAdminUser thay cho AllowAny để chỉ admin mới có thể xem danh sách
def danh_sach_nguoi_dung(request):
    loai = request.query_params.get('loai', None)  # Lọc theo loại người dùng (premium hoặc thường)

    if loai == "premium":
        nguoi_dung = NguoiDung.objects.filter(la_premium=True)
    elif loai == "thuong":
        nguoi_dung = NguoiDung.objects.filter(la_premium=False)
    else:
        nguoi_dung = NguoiDung.objects.all()

    serializer = NguoiDungSerializer(nguoi_dung, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])  # Dùng IsAdminUser thay cho AllowAny để chỉ admin mới có thể chi tiết người dùng
def chi_tiet_nguoi_dung(request, nguoi_dung_id):
    nguoi_dung = get_object_or_404(NguoiDung, pk=nguoi_dung_id)
    serializer = NguoiDungSerializer(nguoi_dung)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([AllowAny])  # Dùng IsAdminUser thay cho AllowAny để chỉ admin mới có thể chi tiết người dùng
def khoa_tai_khoan(request, nguoi_dung_id):
    nguoi_dung = get_object_or_404(NguoiDung, pk=nguoi_dung_id)

    nguoi_dung.is_active = False  # Vô hiệu hóa tài khoản
    nguoi_dung.save()

    return Response({"message": f"Tài khoản {nguoi_dung.email} đã bị khóa"}, status=status.HTTP_200_OK)

from django.shortcuts import get_object_or_404

def update_premium_status(user_id, is_premium):
    """
    Cập nhật trạng thái premium của người dùng.
    
    :param user_id: ID của người dùng cần cập nhật.
    :param is_premium: Giá trị True (đăng ký Premium) hoặc False (hủy Premium).
    :return: Trả về người dùng sau khi cập nhật hoặc None nếu không tìm thấy.
    """
    user = get_object_or_404(NguoiDung, nguoi_dung_id=user_id)
    user.la_premium = is_premium
    user.save()
    return user