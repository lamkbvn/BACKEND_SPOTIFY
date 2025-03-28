from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from ..common.models import DanhSachPhat
from ..common.serializers import DanhSachPhatSerializer

# Tạo danh sách phạt (đã có)
@api_view(['POST'])
@permission_classes([AllowAny])
def them_danhsachphat(request):
    serializer = DanhSachPhatSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Danh sách phạt đã được thêm thành công!", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Lấy danh sách phạt theo nguoi_dung_id_id
@api_view(['GET'])
@permission_classes([AllowAny])
def get_danhsachphat_by_user(request, nguoi_dung_id):
    danh_sach = DanhSachPhat.objects.filter(nguoi_dung_id_id=nguoi_dung_id)
    if danh_sach.exists():
        serializer = DanhSachPhatSerializer(danh_sach, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"error": "Không tìm thấy danh sách phạt cho người dùng này!"}, status=status.HTTP_404_NOT_FOUND)


# Lấy danh sách phạt (GET all)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_danhsachphat(request):
    danh_sach = DanhSachPhat.objects.all()
    serializer = DanhSachPhatSerializer(danh_sach, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Lấy chi tiết danh sách phạt (GET by ID)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_danhsachphat_by_id(request, id):
    try:
        danh_sach = DanhSachPhat.objects.get(pk=id)
        serializer = DanhSachPhatSerializer(danh_sach)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except DanhSachPhat.DoesNotExist:
        return Response({"error": "Không tìm thấy danh sách phạt!"}, status=status.HTTP_404_NOT_FOUND)

# Cập nhật danh sách phạt (PUT)
@api_view(['PUT'])
def update_danhsachphat(request, id):
    try:
        danh_sach = DanhSachPhat.objects.get(pk=id)
    except DanhSachPhat.DoesNotExist:
        return Response({"error": "Không tìm thấy danh sách phạt!"}, status=status.HTTP_404_NOT_FOUND)

    serializer = DanhSachPhatSerializer(danh_sach, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Danh sách phạt đã được cập nhật!", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Xóa danh sách phạt (DELETE)
@api_view(['DELETE'])
def delete_danhsachphat(request, id):
    try:
        danh_sach = DanhSachPhat.objects.get(pk=id)
        danh_sach.delete()
        return Response({"message": "Danh sách phạt đã được xóa!"}, status=status.HTTP_200_OK)
    except DanhSachPhat.DoesNotExist:
        return Response({"error": "Không tìm thấy danh sách phạt!"}, status=status.HTTP_404_NOT_FOUND)
