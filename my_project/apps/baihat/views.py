from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..common.models import BaiHat
from ..common.serializers import BaiHatSerializer

# Tạo bài hát mới
@api_view(['POST'])
def them_baihat(request):
    serializer = BaiHatSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Bài hát đã được thêm thành công!", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Lấy tất cả bài hát
@api_view(['GET'])
def get_baihat(request):
    bai_hats = BaiHat.objects.all()
    serializer = BaiHatSerializer(bai_hats, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Lấy bài hát theo ID
@api_view(['GET'])
def get_baihat_by_id(request, id):
    try:
        bai_hat = BaiHat.objects.get(pk=id)
        serializer = BaiHatSerializer(bai_hat)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except BaiHat.DoesNotExist:
        return Response({"error": "Không tìm thấy bài hát!"}, status=status.HTTP_404_NOT_FOUND)


#Lấy lời bài hát theo id bài hát
@api_view(['GET'])
def get_loi_bai_hat(request, id):
    try:
        # Tìm bài hát theo ID
        bai_hat = BaiHat.objects.get(pk=id)
        # Trả về lời bài hát
        return Response({"loi_bai_hat": bai_hat.loi_bai_hat}, status=status.HTTP_200_OK)
    except BaiHat.DoesNotExist:
        return Response({"error": "Không tìm thấy bài hát!"}, status=status.HTTP_404_NOT_FOUND)


# Cập nhật bài hát
@api_view(['PUT'])
def update_baihat(request, id):
    try:
        bai_hat = BaiHat.objects.get(pk=id)
    except BaiHat.DoesNotExist:
        return Response({"error": "Không tìm thấy bài hát!"}, status=status.HTTP_404_NOT_FOUND)

    serializer = BaiHatSerializer(bai_hat, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Bài hát đã được cập nhật!", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Xóa bài hát
@api_view(['DELETE'])
def delete_baihat(request, id):
    try:
        bai_hat = BaiHat.objects.get(pk=id)
        bai_hat.delete()
        return Response({"message": "Bài hát đã được xóa!"}, status=status.HTTP_200_OK)
    except BaiHat.DoesNotExist:
        return Response({"error": "Không tìm thấy bài hát!"}, status=status.HTTP_404_NOT_FOUND)
