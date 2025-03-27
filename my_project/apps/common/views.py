import http

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import NgheSi, Album, BaiHat
from .serializers import NgheSiSerializer, AlbumSerializer, BaiHatSerializer


# Create your views here.

@api_view(['GET'])
def search(request):
    """
    API tìm kiếm bài hát, nghệ sĩ và album theo từ khóa
    """
    query = request.GET.get('q', '')  # Lấy từ khóa từ query string

    if not query:
        return Response({"message": "Hãy nhập từ bất kì để bắt đầu tìm kiếm"}, status=400)

    # Tìm kiếm nghệ sĩ theo tên
    nghe_si = NgheSi.objects.filter(ten_nghe_si__icontains=query)
    nghe_si_serializer = NgheSiSerializer(nghe_si, many=True)

    # Tìm kiếm album theo tên
    albums = Album.objects.filter(ten_album__icontains=query)
    album_serializer = AlbumSerializer(albums, many=True)

    # Tìm kiếm bài hát theo tên
    bai_hat = BaiHat.objects.filter(ten_bai_hat__icontains=query)
    bai_hat_serializer = BaiHatSerializer(bai_hat, many=True)

    return Response({
        "message" : "kết quả tìm kiếm",
        "nghe_si": nghe_si_serializer.data,
        "albums": album_serializer.data,
        "bai_hat": bai_hat_serializer.data
    } , status= status.HTTP_200_OK)