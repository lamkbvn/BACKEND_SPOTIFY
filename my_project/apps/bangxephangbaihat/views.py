from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from ..common.models import LichSuNghe, BangXepHangBaiHat
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
# Create your views here.
@api_view(['GET'])
@permission_classes([AllowAny])
def top_songs(request):
    top_songs = LichSuNghe.objects.filter(
        thoi_gian_nghe__gte='2025-03-01'
    ).values('bai_hat').annotate(luot_nghe=Count('bai_hat')).order_by('-luot_nghe')[:10]
    return Response(top_songs)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_loai_bang_xep_hang_as_playlist(request):
    loai_list = (
        BangXepHangBaiHat.objects
        .values_list('loai_bang_xep_hang', flat=True)
        .distinct()
    )

    result = []
    IMAGE_MAP = {
        "nghe_nhieu": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ2fFQpuNkGCv-I3c-icubdLm1dsMmkjyp5yA&s",
        "yeu_thich": "https://avatar-ex-swe.nixcdn.com/playlist/2015/08/10/3/6/8/f/1439149758808_500.jpg",
        "tai_xuong": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTiQH2-4jsgFqtbV25sZzgpR3gNfi3ssyDOmA&s",
    }
    TEN_LOAI_MAP = {
        "nghe_nhieu": "nghe nhiều",
        "yeu_thich": "yêu thích",
        "tai_xuong": "tải xuống",
    }
    for idx, loai in enumerate(loai_list):
        anh = IMAGE_MAP.get(loai, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ2fFQpuNkGCv-I3c-icubdLm1dsMmkjyp5yA&s")  # Nếu không có thì lấy ảnh default
        ten = TEN_LOAI_MAP.get(loai, "BXH")
        playlist_item = {
            "danh_sach_phat_id": None,   # ID bài hát hoặc playlist_id
            "album_id": None,
            "bxh_id": loai,               # Vì đây không phải là bài hát cụ thể nên để None
            "order": idx + 1,             # Thứ tự, index tăng dần
            "ten_danh_sach": f"TOP bài hát - {ten}",
            "anh_danh_sach": anh,
            "followers": None,            # Nếu cần sau này có thể thêm
            "description": None,
        }
        result.append(playlist_item)

    return Response(result)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_danh_sach_bai_hat_theo_bxh_name(request, ten_baxh):
    # Giả sử model tên là BaiHatTrongDanhSach
    bai_hat_list = BangXepHangBaiHat.objects.filter(loai_bang_xep_hang=ten_baxh)

    danh_sach_bai_hat = []

    for bai_hat in bai_hat_list:
        item = {
            "bai_hat_trong_danh_sach_id": None,
            "ngay_them": None,
            "danh_sach_phat": None,  # Nếu có
            "bai_hat": bai_hat.bai_hat_id,  # ID bài hát
        }
        danh_sach_bai_hat.append(item)

    return Response({"danh_sach_bai_hat": danh_sach_bai_hat})

@api_view(['GET'])
@permission_classes([AllowAny])
def get_bang_xep_hang_theo_loai(request, ten_bxh):
    try:
        # Ví dụ bảng xếp hạng có model là BangXepHang
        bxh = BangXepHangBaiHat.objects.filter(loai_bang_xep_hang=ten_bxh).first()

        IMAGE_MAP = {
                "nghe_nhieu": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ2fFQpuNkGCv-I3c-icubdLm1dsMmkjyp5yA&s",
                "yeu_thich": "https://avatar-ex-swe.nixcdn.com/playlist/2015/08/10/3/6/8/f/1439149758808_500.jpg",
                "tai_xuong": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTiQH2-4jsgFqtbV25sZzgpR3gNfi3ssyDOmA&s",
            }
        TEN_LOAI_MAP = {
        "nghe_nhieu": "nghe nhiều",
        "yeu_thich": "yêu thích",
        "tai_xuong": "tải xuống",
        }
        image = IMAGE_MAP.get(ten_bxh, "BXH")
        ten = TEN_LOAI_MAP.get(ten_bxh, "BXH")
        playlist_data = {
            "anh_danh_sach": image,  # Nếu ảnh là ImageField
            "danh_sach_phat_id": None,  # ID bảng xếp hạng
            "la_cong_khai": True,
            "mo_ta": f"Album {bxh.loai_bang_xep_hang}",
            "ngay_tao": None,
            "nguoi_dung_id": None,  # Nếu có nghệ sĩ
            "so_nguoi_theo_doi": 0,
            "so_thu_tu": 1,
            "ten_danh_sach": ten,
            "tong_thoi_luong": 0,
        }

        return Response({"playlistData": playlist_data}, status=200)

    except Exception as e:
        print("Lỗi xảy ra:", str(e))
        return Response({"error": str(e)}, status=500)