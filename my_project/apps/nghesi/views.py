from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..common.models import NgheSi
from ..common.serializers import NgheSiSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.core.paginator import Paginator
# Tạo nghệ sĩ mới
@api_view(['POST'])
@permission_classes([AllowAny])
def them_nghesi(request):
    serializer = NgheSiSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Nghệ sĩ đã được thêm thành công!", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_nghesi(request):
    # Lấy tham số từ request
    page = int(request.GET.get('page', 0))
    size = int(request.GET.get('size', 10))
    search_query = request.GET.get('search', '').strip()  # Lấy từ khóa tìm kiếm

    # Lọc danh sách nghệ sĩ nếu có từ khóa tìm kiếm
    if search_query:
        nghesi_list = NgheSi.objects.filter(ten_nghe_si__icontains=search_query)
    else:
        nghesi_list = NgheSi.objects.all()

    # Áp dụng phân trang
    paginator = Paginator(nghesi_list, size)
    total_pages = paginator.num_pages

    try:
        nghesi_page = paginator.page(page + 1)  # Django page index bắt đầu từ 1
    except:
        return Response({"message": "Page out of range"}, status=status.HTTP_404_NOT_FOUND)

    serializer = NgheSiSerializer(nghesi_page, many=True)

    return Response({
        "page": page,
        "size": size,
        "total_pages": total_pages,
        "total_items": paginator.count,
        "data": serializer.data
    }, status=status.HTTP_200_OK)

# Lấy nghệ sĩ theo ID
@api_view(['GET'])
@permission_classes([AllowAny])
def get_nghesi_by_id(request, id):
    try:
        nghesi = NgheSi.objects.get(pk=id)
        serializer = NgheSiSerializer(nghesi)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except NgheSi.DoesNotExist:
        return Response({"error": "Không tìm thấy nghệ sĩ!"}, status=status.HTTP_404_NOT_FOUND)

# Cập nhật thông tin nghệ sĩ
@api_view(['PUT'])
@permission_classes([AllowAny])
def update_nghesi(request, id):
    try:
        nghesi = NgheSi.objects.get(pk=id)
    except NgheSi.DoesNotExist:
        return Response({"error": "Không tìm thấy nghệ sĩ!"}, status=status.HTTP_404_NOT_FOUND)

    serializer = NgheSiSerializer(nghesi, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Thông tin nghệ sĩ đã được cập nhật!", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Xóa nghệ sĩ
@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_nghesi(request, id):
    try:
        nghesi = NgheSi.objects.get(pk=id)
        nghesi.delete()
        return Response({"message": "Nghệ sĩ đã được xóa!"}, status=status.HTTP_200_OK)
    except NgheSi.DoesNotExist:
        return Response({"error": "Không tìm thấy nghệ sĩ!"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['PATCH'])  # Sử dụng PATCH vì chỉ cập nhật một trường
@permission_classes([AllowAny])
def lock_nghesi(request, id):
    try:
        nghesi = NgheSi.objects.get(pk=id)
        nghesi.is_active = False
        nghesi.save()
        return Response({"message": "Nghệ sĩ đã bị khóa!"}, status=status.HTTP_200_OK)
    except NgheSi.DoesNotExist:
        return Response({"error": "Không tìm thấy nghệ sĩ!"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['PATCH'])  # Sử dụng PATCH vì chỉ cập nhật một trường
@permission_classes([AllowAny])
def unlock_nghesi(request, id):
    try:
        nghesi = NgheSi.objects.get(pk=id)
        nghesi.is_active = True
        nghesi.save()
        return Response({"message": "Nghệ sĩ đã mở khóa!"}, status=status.HTTP_200_OK)
    except NgheSi.DoesNotExist:
        return Response({"error": "Không tìm thấy nghệ sĩ!"}, status=status.HTTP_404_NOT_FOUND)