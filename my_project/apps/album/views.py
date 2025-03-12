from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from ..common.models import Album, NgheSi
from ..common.serializers import AlbumSerializer

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