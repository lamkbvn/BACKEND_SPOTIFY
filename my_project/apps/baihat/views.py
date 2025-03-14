from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from ..common.models import BaiHat
from ..common.serializers import BaiHatSerializer, AlbumSerializer

# Tạo bài hát mới
@api_view(['POST'])
@permission_classes([AllowAny])
def them_baihat(request):
    serializer = BaiHatSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Bài hát đã được thêm thành công!", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Lấy tất cả bài hát
@api_view(['GET'])
@permission_classes([AllowAny])
def get_baihat(request):
    bai_hats = BaiHat.objects.all()
    serializer = BaiHatSerializer(bai_hats, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Lấy bài hát theo ID
@api_view(['GET'])
@permission_classes([AllowAny])
def get_baihat_by_id(request, id):
    try:
        bai_hat = BaiHat.objects.get(pk=id)
        serializer = BaiHatSerializer(bai_hat)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except BaiHat.DoesNotExist:
        return Response({"error": "Không tìm thấy bài hát!"}, status=status.HTTP_404_NOT_FOUND)


#Lấy lời bài hát theo id bài hát
@api_view(['GET'])
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
def delete_baihat(request, id):
    try:
        bai_hat = BaiHat.objects.get(pk=id)
        bai_hat.delete()
        return Response({"message": "Bài hát đã được xóa!"}, status=status.HTTP_200_OK)
    except BaiHat.DoesNotExist:
        return Response({"error": "Không tìm thấy bài hát!"}, status=status.HTTP_404_NOT_FOUND)


# Lấy bài hát theo tên bài hát và tên nghệ sĩ
@api_view(['GET'])
@permission_classes([AllowAny])
def search_baihat(request):
    ten_bai_hat = request.GET.get('ten_bai_hat', None)
    ten_nghe_si = request.GET.get('ten_nghe_si', None)

    # Lọc bài hát theo tên bài hát và tên nghệ sĩ nếu có
    bai_hats = BaiHat.objects.all()
    if ten_bai_hat:
        bai_hats = bai_hats.filter(ten_bai_hat__icontains=ten_bai_hat)  # Tìm kiếm không phân biệt chữ hoa/thường
    if ten_nghe_si:
        bai_hats = bai_hats.filter(nghe_si__ten_nghe_si__icontains=ten_nghe_si)  # Tìm kiếm không phân biệt chữ hoa/thường

    # Nếu không tìm thấy bài hát, trả về thông báo
    if not bai_hats:
        return Response({"error": "Không tìm thấy bài hát nào!"}, status=status.HTTP_404_NOT_FOUND)

    # Nếu tìm thấy bài hát, trả về danh sách bài hát
    serializer = BaiHatSerializer(bai_hats, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def search_album(request):
    ten_bai_hat = request.GET.get('ten_bai_hat', None)
    ten_nghe_si = request.GET.get('ten_nghe_si', None)

    # Lọc bài hát theo tên bài hát và tên nghệ sĩ nếu có
    bai_hats = BaiHat.objects.all()

    if ten_bai_hat:
        bai_hats = bai_hats.filter(ten_bai_hat__icontains=ten_bai_hat)  # Tìm kiếm không phân biệt chữ hoa/thường

    if ten_nghe_si:
        bai_hats = bai_hats.filter(nghe_si__ten_nghe_si__icontains=ten_nghe_si)  # Tìm kiếm không phân biệt chữ hoa/thường

    # Nếu không tìm thấy bài hát, trả về thông báo
    if not bai_hats:
        return Response({"error": "Không tìm thấy bài hát nào!"}, status=status.HTTP_404_NOT_FOUND)

    # Lấy danh sách các album của bài hát tìm được
    albums = [bai_hat.album for bai_hat in bai_hats if bai_hat.album is not None]

    if not albums:
        return Response({"error": "Không tìm thấy album nào!"}, status=status.HTTP_404_NOT_FOUND)

    # Trả về dữ liệu album
    album_serializer = AlbumSerializer(albums, many=True)
    return Response(album_serializer.data, status=status.HTTP_200_OK)
