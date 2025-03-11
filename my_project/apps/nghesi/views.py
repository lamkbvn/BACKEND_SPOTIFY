from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..common.models import NgheSi
from ..common.serializers import NgheSiSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

# Tạo nghệ sĩ mới
@api_view(['POST'])
@permission_classes([AllowAny])
def them_nghesi(request):
    serializer = NgheSiSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Nghệ sĩ đã được thêm thành công!", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Lấy danh sách tất cả nghệ sĩ
@api_view(['GET'])
@permission_classes([AllowAny])
def get_nghesi(request):
    nghesi_list = NgheSi.objects.all()
    serializer = NgheSiSerializer(nghesi_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

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