from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..common.models import LoiBaiHatDongBo
from ..common.serializers import LoiBaiHatDongBoSerializer

# Thêm lời bài hát đồng bộ (POST)
@api_view(['POST'])
def them_loibaihatdongbo(request):
    serializer = LoiBaiHatDongBoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Lời bài hát đồng bộ đã được thêm thành công!", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Lấy danh sách lời bài hát đồng bộ (GET all)
@api_view(['GET'])
def get_loibaihatdongbo(request):
    loi_bai_hat = LoiBaiHatDongBo.objects.all()
    serializer = LoiBaiHatDongBoSerializer(loi_bai_hat, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Lấy chi tiết lời bài hát đồng bộ (GET by ID)
@api_view(['GET'])
def get_loibaihatdongbo_by_id(request, id):
    try:
        loi_bai_hat = LoiBaiHatDongBo.objects.get(pk=id)
        serializer = LoiBaiHatDongBoSerializer(loi_bai_hat)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except LoiBaiHatDongBo.DoesNotExist:
        return Response({"error": "Không tìm thấy lời bài hát đồng bộ!"}, status=status.HTTP_404_NOT_FOUND)

# Cập nhật lời bài hát đồng bộ (PUT)
@api_view(['PUT'])
def update_loibaihatdongbo(request, id):
    try:
        loi_bai_hat = LoiBaiHatDongBo.objects.get(pk=id)
    except LoiBaiHatDongBo.DoesNotExist:
        return Response({"error": "Không tìm thấy lời bài hát đồng bộ!"}, status=status.HTTP_404_NOT_FOUND)

    serializer = LoiBaiHatDongBoSerializer(loi_bai_hat, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Lời bài hát đồng bộ đã được cập nhật!", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Xóa lời bài hát đồng bộ (DELETE)
@api_view(['DELETE'])
def delete_loibaihatdongbo(request, id):
    try:
        loi_bai_hat = LoiBaiHatDongBo.objects.get(pk=id)
        loi_bai_hat.delete()
        return Response({"message": "Lời bài hát đồng bộ đã được xóa!"}, status=status.HTTP_200_OK)
    except LoiBaiHatDongBo.DoesNotExist:
        return Response({"error": "Không tìm thấy lời bài hát đồng bộ!"}, status=status.HTTP_404_NOT_FOUND)
