from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from ..common.models import Album, NgheSi, NguoiDung
from ..common.serializers import AlbumSerializer
from django.core.paginator import Paginator
from django.utils.timezone import now
from django.contrib.auth import get_user_model
User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def create_album(request):
    user_id = request.data.get("nguoi_dung_id")
    ten_nghe_si = request.data.get("ten_nghe_si")

    if not user_id or not ten_nghe_si:
        return Response({"error": "Thiếu thông tin người dùng hoặc tên nghệ sĩ!"}, status=400)

    # Lấy user
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({"error": "Không tìm thấy người dùng!"}, status=404)

    # Kiểm tra tên nghệ sĩ đã tồn tại chưa
    if NgheSi.objects.filter(ten_nghe_si=ten_nghe_si).exists():
        return Response({"error": f"Tên nghệ sĩ '{ten_nghe_si}' đã tồn tại. Vui lòng chọn tên khác."}, status=400)

    # Nếu chưa tồn tại → tạo mới
    try:
        nghe_si = NgheSi.objects.create(
            nguoi_dung=user,
            ten_nghe_si=ten_nghe_si,
            tieu_su="",
            anh_dai_dien=getattr(user, 'avatar_url', ''),
            ngay_sinh=getattr(user, 'ngay_sinh', None),
            quoc_gia=getattr(user, 'quoc_gia', ''),
            is_active=True,
            created_at=now(),
            updated_at=now()
        )
    except Exception as e:
        return Response({"error": f"Không thể tạo nghệ sĩ: {str(e)}"}, status=400)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def get_albums_by_user(request, user_id):
    try:
        # Lấy tất cả nghệ sĩ thuộc người dùng đó
        nghe_si_list = NgheSi.objects.filter(nguoi_dung_id=user_id)

        # Lấy tất cả album có nghe_si thuộc danh sách đó
        albums = Album.objects.filter(nghe_si__in=nghe_si_list)

        serializer = AlbumSerializer(albums, many=True)
        return Response({"user_id": user_id, "albums": serializer.data}, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)

    # Gắn nghệ sĩ vào dữ liệu tạo album
    data = request.data.copy()
    data['nghe_si'] = nghe_si.nghe_si_id
    data['ngay_phat_hanh'] = now().date()
    
    # ✅ Kiểm tra tên album trùng
    ten_album = data.get("ten_album")
    if Album.objects.filter(ten_album=ten_album).exists():
        return Response({"error": f"Tên album '{ten_album}' đã tồn tại. Vui lòng chọn tên khác."}, status=400)

    serializer = AlbumSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Album đã được tạo thành công!", "data": serializer.data}, status=201)
    return Response(serializer.errors, status=400)

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