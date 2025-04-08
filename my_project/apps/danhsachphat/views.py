from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from ..common.models import DanhSachPhat
from ..common.serializers import DanhSachPhatSerializer
from django.core.files.uploadedfile import InMemoryUploadedFile
import cloudinary.uploader


@api_view(['POST'])
@permission_classes([AllowAny])
def them_danhsachphat(request):
    data = request.data.copy()  # Sao chép dữ liệu từ request

    # Kiểm tra xem có ảnh không
    if 'anh_danh_sach' in request.FILES:
        anh_danh_sach = request.FILES['anh_danh_sach']

        # Upload ảnh lên Cloudinary
        result = cloudinary.uploader.upload(anh_danh_sach)
        image_url = result.get("secure_url")

        # Lưu URL ảnh vào dữ liệu request
        data['anh_danh_sach'] = image_url

    # Đảm bảo tên key chính xác với model
    if "nguoi_dung_id_id" in data:
        data["nguoi_dung_id"] = data.pop("nguoi_dung_id_id")

    serializer = DanhSachPhatSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Danh sách phát đã được thêm thành công!",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Lấy danh sách phát theo nguoi_dung_id_id
@api_view(['GET'])
@permission_classes([AllowAny])
def get_danhsachphat_by_user(request, nguoi_dung_id):
    danh_sach = DanhSachPhat.objects.filter(nguoi_dung_id_id=nguoi_dung_id)
    if danh_sach.exists():
        serializer = DanhSachPhatSerializer(danh_sach, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"error": "Không tìm thấy danh sách phát cho người dùng này!"}, status=status.HTTP_404_NOT_FOUND)


# Lấy danh sách phát (GET all)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_danhsachphat(request):
    danh_sach = DanhSachPhat.objects.all()
    serializer = DanhSachPhatSerializer(danh_sach, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Lấy chi tiết danh sách phát (GET by ID)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_danhsachphat_by_id(request, id):
    try:
        danh_sach = DanhSachPhat.objects.get(pk=id)
        serializer = DanhSachPhatSerializer(danh_sach)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except DanhSachPhat.DoesNotExist:
        return Response({"error": "Không tìm thấy danh sách phát!"}, status=status.HTTP_404_NOT_FOUND)

# Cập nhật danh sách phát (PUT)
@api_view(['PUT'])
def update_danhsachphat(request, id):
    try:
        danh_sach = DanhSachPhat.objects.get(pk=id)
    except DanhSachPhat.DoesNotExist:
        return Response({"error": "Không tìm thấy danh sách phát!"}, status=status.HTTP_404_NOT_FOUND)

    serializer = DanhSachPhatSerializer(danh_sach, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Danh sách phát đã được cập nhật!", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Xóa danh sách phát (DELETE)
@api_view(['DELETE'])
def delete_danhsachphat(request, id):
    try:
        danh_sach = DanhSachPhat.objects.get(pk=id)
        danh_sach.delete()
        return Response({"message": "Danh sách phát đã được xóa!"}, status=status.HTTP_200_OK)
    except DanhSachPhat.DoesNotExist:
        return Response({"error": "Không tìm thấy danh sách phát!"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def get_so_luong_dsp(request):
    try:
        so_luong = DanhSachPhat.objects.count()
        return Response({"so_luong_dsp": so_luong}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)