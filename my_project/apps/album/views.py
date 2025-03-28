from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from ..common.models import Album, NgheSi
from ..common.serializers import AlbumSerializer
from django.core.paginator import Paginator

# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def them_album(request):
    serializer = AlbumSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Album đã được thêm thành công!", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_albums(request):
    albums = Album.objects.all()
    serializer = AlbumSerializer(albums, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_album_phan_trang(request):
    # Lấy tham số từ request
    page = int(request.GET.get('page', 0))
    size = int(request.GET.get('size', 10))
    search_query = request.GET.get('search', '').strip()  # Lấy từ khóa tìm kiếm

    # Lọc danh sách nghệ sĩ nếu có từ khóa tìm kiếm
    if search_query:
        album_list = Album.objects.filter(ten_album__icontains=search_query)
    else:
        album_list = Album.objects.all()

    # Áp dụng phân trang
    paginator = Paginator(album_list, size)
    total_pages = paginator.num_pages

    try:
        album_page = paginator.page(page + 1)  # Django page index bắt đầu từ 1
    except:
        return Response({"message": "Page out of range"}, status=status.HTTP_404_NOT_FOUND)

    serializer = AlbumSerializer(album_page, many=True)

    return Response({
        "page": page,
        "size": size,
        "total_pages": total_pages,
        "total_items": paginator.count,
        "data": serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_album_by_id(request, album_id):
    try:
        album = Album.objects.get(pk=album_id)
        serializer = AlbumSerializer(album)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Album.DoesNotExist:
        return Response({"error": "Không tìm thấy album!"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([AllowAny])
def update_album(request, album_id):
    try:
        album = Album.objects.get(pk=album_id)
    except Album.DoesNotExist:
        return Response({"error": "Không tìm thấy album!"}, status=status.HTTP_404_NOT_FOUND)

    serializer = AlbumSerializer(album, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Album đã được cập nhật!", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_album(request, album_id):
    try:
        album = Album.objects.get(pk=album_id)
        album.delete()
        return Response({"message": "Album đã được xóa!"}, status=status.HTTP_200_OK)
    except Album.DoesNotExist:
        return Response({"error": "Không tìm thấy album!"}, status=status.HTTP_404_NOT_FOUND)