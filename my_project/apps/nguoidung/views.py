import time
from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
@csrf_exempt
def them_nguoi_dung(request):

    email = request.data.get('email', None)
    so_dien_thoai = request.data.get('so_dien_thoai', None)
    mat_khau = request.data.get('password', None)


    required_fields = ['email', 'password', 'ten_hien_thi', 'gioi_tinh', 'ngay_sinh']
    errors = {}

    # Kiểm tra các trường có bị thiếu không
    for field in required_fields:
        if not request.data.get(field):
            errors[field] = "Không được để trống"

    # Kiểm tra định dạng ngày sinh
    ngay_sinh = request.data.get('ngay_sinh', None)
    if ngay_sinh:
        try:
            datetime.strptime(ngay_sinh, '%Y-%m-%d')  # Kiểm tra xem có đúng định dạng không
        except ValueError:
            errors['ngay_sinh'] = "Ngày sinh không đúng định dạng YYYY-MM-DD"

    # Kiểm tra email đã tồn tại chưa
    if NguoiDung.objects.filter(email=email).exists():
        errors['email'] = "Email đã được sử dụng"


    if so_dien_thoai and NguoiDung.objects.filter(so_dien_thoai=so_dien_thoai).exists():
        errors['so_dien_thoai'] = "Số điện thoại đã được sử dụng!"

    # Nếu có lỗi, trả về lỗi chi tiết
    if errors:
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
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
# @csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    email = email.strip().lower()  # Chuẩn hóa email
    print(email)
    try:
        nguoidung = NguoiDung.objects.get(email=email)
    except NguoiDung.DoesNotExist:
        return Response({'email': 'Không tìm thấy tài khoản với email này'}, status=404)

    if not check_password(password, nguoidung.password):  # Đảm bảo bạn lưu mật khẩu đã mã hóa trong DB
        return Response({'password': 'Sai mật khẩu'}, status=400)
    # Tạo JWT token
    refresh = RefreshToken.for_user(nguoidung)
    access_token = str(refresh.access_token)

    # Thiết lập cookie HttpOnly cho refresh token
    response = JsonResponse(data ={
            'message' : 'Dang nhap thanh cong',
            # 'refresh' : str(refresh),
            'access': access_token,  # Access token sẽ được frontend sử dụng
            # 'nguoi_dung_id': nguoidung.nguoi_dung_id,
            'ten_hien_thi': nguoidung.ten_hien_thi,
            # 'email': nguoidung.email,
    } , status = 201)

    response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,  # Bảo mật: Không thể truy cập từ JavaScript
            secure=True,  # Bật nếu chạy trên HTTPS
            samesite="None",  # Ngăn chặn CSRF , đặt thành none nếu khác domain
            max_age=  int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()),  # Token sống 7 ngày
    )

    response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,  # Bảo mật: Không thể truy cập từ JavaScript
            secure=True, # Bật nếu chạy trên HTTPS
            samesite="None",  # Ngăn chặn CSRF , đặt thành None nếu khác domain
            max_age= int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()),  # Token sống 7 ngày
    )

    return response

@api_view(['GET'])
def get_access_token(request):
    access_token = request.COOKIES.get("access_token")

    if not access_token:  # Kiểm tra nếu access_token là None hoặc chuỗi rỗng
        return Response({"message": "Bạn chưa đăng nhập"}, status=status.HTTP_401_UNAUTHORIZED)

    return Response({"access_token": access_token}, status=status.HTTP_200_OK)

from django.utils.timezone import now
from datetime import timedelta

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.COOKIES.get('refresh_token')
        access_token = request.COOKIES.get('access_token')

        if not refresh_token:
            return Response({'error': 'Vui lòng cung cấp refresh token'}, status=400)

        try:
            # Thêm Refresh Token vào blacklist
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response({'error': 'Refresh Token không hợp lệ hoặc đã hết hạn'}, status=400)

        if not access_token:
            return Response({'error': 'Không có Access Token'}, status=400)

        try:
            # Thêm Access Token vào danh sách bị vô hiệu hóa
            access_token_obj = AccessToken(access_token)
            BlacklistedAccessToken.objects.create(token_access=access_token)
        except ValidationError:
            return Response({'error': 'Access Token không hợp lệ'}, status=400)

        # Xóa cả refresh token và access token khỏi cookie
        response = Response({'message': 'Đăng xuất thành công'}, status=200)
        expire_time = now() - timedelta(seconds=1)  # Đặt thời gian hết hạn về quá khứ

        response.set_cookie(
            key='refresh_token',
            value='',
            httponly=True,
            expires=expire_time
        )
        response.set_cookie(
            key='access_token',
            value='',
            httponly=True,
            expires=expire_time
        )

        return response

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
        reset_url = reset_url = f'http://localhost:5173/reset-password/{uid}/{token}'

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
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


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
@permission_classes([IsAuthenticated])  # Chỉ cho phép người đã đăng nhập
def thong_tin_nguoi_dung(request):
    # Lấy id từ query param (nếu có)
    nguoi_dung_id = request.query_params.get("id")

    if nguoi_dung_id:
        # Nếu có id trong query param, tìm người dùng với id đó
        try:
            user = NguoiDung.objects.get(nguoi_dung_id=nguoi_dung_id)
        except NguoiDung.DoesNotExist:
            return Response({"error": "Không tìm thấy người dùng với id này!"}, status=status.HTTP_404_NOT_FOUND)
    else:
        # Nếu không có id, sử dụng thông tin của người dùng đã đăng nhập (request.user)
        user = request.user

    return Response({
        "id": user.nguoi_dung_id,
        "email": user.email,
        "ten_hien_thi": user.ten_hien_thi,
        "gioi_tinh": user.gioi_tinh,
        "ngay_sinh": user.ngay_sinh,
        "avatar_url": user.avatar_url
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAdminUser])  # Dùng IsAdminUser thay cho AllowAny để chỉ admin mới có thể xem danh sách
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