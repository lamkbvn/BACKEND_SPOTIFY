from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.core.paginator import Paginator
from ..common.models import ThanhToan
from ..common.serializers import ThanhToanSerializer

from ..nguoidung.views import update_premium_status

# 🟢 Tạo thanh toán mới
@api_view(['POST'])
@permission_classes([AllowAny])
def them_thanh_toan(request):
    serializer = ThanhToanSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        update_premium_status(request.data['nguoi_dung'], True)  # Cập nhật trạng thái premium cho người dùng
        return Response({"message": "Thanh toán đã được thêm thành công!", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 🔵 Lấy danh sách thanh toán (có phân trang & tìm kiếm)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_thanh_toan(request):
    # Lấy tham số từ request
    page = int(request.GET.get('page', 0))
    size = int(request.GET.get('size', 10))
    search_query = request.GET.get('search', '').strip()  # Lấy từ khóa tìm kiếm

    # Lọc danh sách thanh toán nếu có từ khóa tìm kiếm (lọc theo phương thức thanh toán)
    if search_query:
        thanh_toan_list = ThanhToan.objects.filter(phuong_thuc__icontains=search_query)
    else:
        thanh_toan_list = ThanhToan.objects.all()

    # Áp dụng phân trang
    paginator = Paginator(thanh_toan_list, size)
    total_pages = paginator.num_pages

    try:
        thanh_toan_page = paginator.page(page + 1)  # Django page index bắt đầu từ 1
    except:
        return Response({"message": "Page out of range"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ThanhToanSerializer(thanh_toan_page, many=True)

    return Response({
        "page": page,
        "size": size,
        "total_pages": total_pages,
        "total_items": paginator.count,
        "data": serializer.data
    }, status=status.HTTP_200_OK)

# 🟠 Lấy thanh toán theo ID
@api_view(['GET'])
@permission_classes([AllowAny])
def get_thanh_toan_by_id(request, id):
    try:
        thanh_toan = ThanhToan.objects.get(pk=id)
        serializer = ThanhToanSerializer(thanh_toan)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ThanhToan.DoesNotExist:
        return Response({"error": "Không tìm thấy thanh toán!"}, status=status.HTTP_404_NOT_FOUND)

# 🔵 Cập nhật thanh toán
@api_view(['PUT'])
@permission_classes([AllowAny])
def update_thanh_toan(request, id):
    try:
        thanh_toan = ThanhToan.objects.get(pk=id)
    except ThanhToan.DoesNotExist:
        return Response({"error": "Không tìm thấy thanh toán!"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ThanhToanSerializer(thanh_toan, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Thông tin thanh toán đã được cập nhật!", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ❌ Xóa thanh toán
@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_thanh_toan(request, id):
    try:
        thanh_toan = ThanhToan.objects.get(pk=id)
        thanh_toan.delete()
        return Response({"message": "Thanh toán đã được xóa!"}, status=status.HTTP_200_OK)
    except ThanhToan.DoesNotExist:
        return Response({"error": "Không tìm thấy thanh toán!"}, status=status.HTTP_404_NOT_FOUND)

# 🔒 Khóa thanh toán (giả sử có cột `is_active`)
@api_view(['PATCH'])
@permission_classes([AllowAny])
def lock_thanh_toan(request, id):
    try:
        thanh_toan = ThanhToan.objects.get(pk=id)
        thanh_toan.is_active = False
        thanh_toan.save()
        return Response({"message": "Thanh toán đã bị khóa!"}, status=status.HTTP_200_OK)
    except ThanhToan.DoesNotExist:
        return Response({"error": "Không tìm thấy thanh toán!"}, status=status.HTTP_404_NOT_FOUND)

# 🔓 Mở khóa thanh toán
@api_view(['PATCH'])
@permission_classes([AllowAny])
def unlock_thanh_toan(request, id):
    try:
        thanh_toan = ThanhToan.objects.get(pk=id)
        thanh_toan.is_active = True
        thanh_toan.save()
        return Response({"message": "Thanh toán đã được mở khóa!"}, status=status.HTTP_200_OK)
    except ThanhToan.DoesNotExist:
        return Response({"error": "Không tìm thấy thanh toán!"}, status=status.HTTP_404_NOT_FOUND)