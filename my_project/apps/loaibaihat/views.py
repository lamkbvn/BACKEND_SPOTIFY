from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..common.models import LoaiBaiHat
from ..common.serializers import LoaiBaiHatSerializer

# Thêm loại bài hát
@api_view(['POST'])
def them_loaibaihat(request):
    serializer = LoaiBaiHatSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Loại bài hát đã được thêm thành công!", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Lấy danh sách tất cả loại bài hát
@api_view(['GET'])
def get_loaibaihat(request):
    danh_sach = LoaiBaiHat.objects.all()
    serializer = LoaiBaiHatSerializer(danh_sach, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Lấy chi tiết loại bài hát theo ID
@api_view(['GET'])
def get_loaibaihat_by_id(request, id):
    try:
        loai_bai_hat = LoaiBaiHat.objects.get(pk=id)
        serializer = LoaiBaiHatSerializer(loai_bai_hat)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except LoaiBaiHat.DoesNotExist:
        return Response({"error": "Không tìm thấy loại bài hát!"}, status=status.HTTP_404_NOT_FOUND)

# Cập nhật loại bài hát
@api_view(['PUT'])
def update_loaibaihat(request, id):
    try:
        loai_bai_hat = LoaiBaiHat.objects.get(pk=id)
    except LoaiBaiHat.DoesNotExist:
        return Response({"error": "Không tìm thấy loại bài hát!"}, status=status.HTTP_404_NOT_FOUND)

    serializer = LoaiBaiHatSerializer(loai_bai_hat, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Loại bài hát đã được cập nhật!", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Xóa loại bài hát
@api_view(['DELETE'])
def delete_loaibaihat(request, id):
    try:
        loai_bai_hat = LoaiBaiHat.objects.get(pk=id)
        loai_bai_hat.delete()
        return Response({"message": "Loại bài hát đã được xóa!"}, status=status.HTTP_200_OK)
    except LoaiBaiHat.DoesNotExist:
        return Response({"error": "Không tìm thấy loại bài hát!"}, status=status.HTTP_404_NOT_FOUND)
