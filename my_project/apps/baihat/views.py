from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import api_view, permission_classes
from ..common.models import BaiHat, NgheSi
from ..common.serializers import BaiHatSerializer, AlbumSerializer

from django.core.files.storage import FileSystemStorage
from urllib.parse import unquote
import os
import librosa 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.http import JsonResponse
import numpy as np
from django.utils.timezone import now

from shazamio import Shazam
import tempfile
import asyncio
import requests

#thêm bài hát với  'trang_thai_duyet': 'pending'
@api_view(['POST'])
@permission_classes([AllowAny])
def upload_song(request):
    nghe_si_id = request.data.get('nghe_si') or request.data.get('nghe_si_id')
    if not nghe_si_id:
        return Response({"error": "Thiếu thông tin nghệ sĩ!"}, status=status.HTTP_400_BAD_REQUEST)

    data = {
        'ten_bai_hat': request.data.get('ten_bai_hat'),
        'the_loai': request.data.get('the_loai'),
        'loi_bai_hat': request.data.get('loi_bai_hat', ''),
        'thoi_luong': request.data.get('thoi_luong'),
        'ngay_phat_hanh': request.data.get('ngay_phat_hanh'),
        'album': request.data.get('album', None),
        'nghe_si': int(nghe_si_id),
        'trang_thai_duyet': 'pending'
    }

    if 'file_bai_hat' not in request.FILES:
        return Response({"error": "Vui lòng cung cấp file bài hát!"}, status=status.HTTP_400_BAD_REQUEST)

    data['file_bai_hat'] = request.FILES['file_bai_hat']

    serializer = BaiHatSerializer(data=data)
    if serializer.is_valid():
        song = serializer.save()
        if song.album:
            song.album.update_trang_thai_duyet()
        return Response({
            "message": "Bài hát đã được tải lên và đang chờ duyệt!",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# lấy bài hát theo album
@api_view(['GET'])
@permission_classes([AllowAny])
def get_bai_hat_theo_album(request, album_id):
    try:
        bai_hats = BaiHat.objects.filter(album__album_id=album_id)
        serializer = BaiHatSerializer(bai_hats, many=True)
        return Response({"danh_sach_bai_hat": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([AllowAny]) #thay đổi thành IsAdminUser để tăng tín bảo mật
def review_song(request, id):
    try:
        song = BaiHat.objects.get(pk=id)
    except BaiHat.DoesNotExist:
        return Response({"error": "Không tìm thấy bài hát!"}, status=status.HTTP_404_NOT_FOUND)

    trang_thai_duyet = request.data.get('trang_thai_duyet')
    if trang_thai_duyet not in ['approved', 'rejected']:
        return Response({"error": "Trạng thái duyệt không hợp lệ!"}, status=status.HTTP_400_BAD_REQUEST)

    song.trang_thai_duyet = trang_thai_duyet
    song.save()

    # Update the album's status if the song is part of an album
    if song.album:
        song.album.update_trang_thai_duyet()

    return Response({"message": f"Bài hát đã được {trang_thai_duyet}!"}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_baihat_for_album(request):
    bai_hats = BaiHat.objects.all()
    if not request.user.is_staff:  # If not admin, only show approved songs
        bai_hats = bai_hats.filter(trang_thai_duyet='approved')
    serializer = BaiHatSerializer(bai_hats, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def sync_lyrics(request):
    # Nhận đường link file mp3 và lời bài hát từ request
    audio_url = request.data.get('audio_url')
    lyrics = request.data.get('lyrics')

    if not audio_url:
        return Response({"error": "No audio URL provided"}, status=400)
    if not lyrics:
        return Response({"error": "No lyrics provided"}, status=400)

    try:
        # Tải file mp3 từ đường link về file tạm
        response = requests.get(audio_url, stream=True)
        if response.status_code != 200:
            return Response({"error": "Unable to download audio file"}, status=400)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            for chunk in response.iter_content(chunk_size=8192):
                tmp_file.write(chunk)
            tmp_file_path = tmp_file.name

        # Dùng librosa để load file
        y, sr = librosa.load(tmp_file_path, sr=None)

        # Tính toán tempo và beat
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)

        # Phân tích onset (bắt đầu có âm thanh)
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        onset_times = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr, units='time')

        first_sound_time = onset_times[0] if len(onset_times) > 0 else 0
        adjusted_beat_times = beat_times - first_sound_time
        adjusted_beat_times = adjusted_beat_times[adjusted_beat_times >= 0]  # Lọc bỏ âm âm

        # Xử lý lyrics
        lyrics_lines = [line.strip() for line in lyrics.split('\n') if line.strip()]
        num_lines = len(lyrics_lines)

        if num_lines == 0:
            return Response({"error": "Lyrics is empty or invalid"}, status=400)

        total_time = adjusted_beat_times[-1] if len(adjusted_beat_times) > 0 else len(y)/sr
        time_per_line = total_time / num_lines

        timestamps = []
        for i, line in enumerate(lyrics_lines):
            timestamp = round(i * time_per_line, 2)
            timestamps.append({"line": line, "timestamp": timestamp})

        return Response({
            "tempo": tempo,
            "timestamps": timestamps
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)

    finally:
        # Dọn dẹp file tạm
        if 'tmp_file_path' in locals() and os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)       
            

def find_lyric_start_time(audio_file_path):
    # Tải file âm thanh với Librosa
    y, sr = librosa.load(audio_file_path, sr=None)
    
    # Tính toán mức năng lượng (energy) của tín hiệu
    energy = librosa.feature.rms(y=y)[0]  # RMS energy
    
    # Tính spectral flux (sự thay đổi phổ)
    spectral_flux = librosa.onset.onset_strength(y=y, sr=sr)

    # Tính ngưỡng năng lượng (có thể điều chỉnh)
    energy_threshold = 0.02  # Ngưỡng năng lượng cho phần giọng hát
    flux_threshold = 0.2    # Ngưỡng spectral flux để phát hiện thay đổi

    # Tìm điểm mà năng lượng vượt qua ngưỡng và có sự thay đổi phổ
    start_frame_energy = np.argmax(energy > energy_threshold)
    start_frame_flux = np.argmax(spectral_flux > flux_threshold)

    # Chọn điểm bắt đầu là khi cả năng lượng và spectral flux vượt qua ngưỡng
    start_beat_frame = max(start_frame_energy, start_frame_flux)
    
    # Chuyển chỉ số frame thành thời gian (giây)
    start_time = librosa.frames_to_time(start_beat_frame, sr=sr)
    
    return start_time

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

async def find_song_shazam(audio_file):
    """Nhận diện bài hát bằng Shazam."""
    shazam = Shazam()
    try:
        # Lưu audio_file vào tệp tạm thời
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            for chunk in audio_file.chunks():
                tmp_file.write(chunk)
            temp_file_path = tmp_file.name  # Lấy đường dẫn file tạm thời

        out = await shazam.recognize_song(temp_file_path)

        # Xóa file tạm thời sau khi nhận diện xong
        os.remove(temp_file_path)

        return out
    except Exception as e:
        print(f"Shazam error for {audio_file}: {e}")
        return {"error": str(e)}

@api_view(['POST'])
def upload_audio(request):
    if 'audio' not in request.FILES:
        return Response({'error': 'No audio file provided.'}, status=status.HTTP_400_BAD_REQUEST)

    audio_file = request.FILES['audio']

    # Nhận diện bài hát bằng Shazam (chạy bất đồng bộ)
    shazam_info = asyncio.run(find_song_shazam(audio_file))

    return Response({
        'message': 'Audio file uploaded and processed successfully!',
        'shazam_info': shazam_info
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_bai_hat_theo_album(request):
    try:
        album_id = request.GET.get('albumid')
        # Lấy tất cả bài hát thuộc album_id
        bai_hat_list = BaiHat.objects.filter(album_id=album_id)

        # Tạo danh sách theo format yêu cầu
        danh_sach_bai_hat = []
        for index, bai_hat in enumerate(bai_hat_list, start=1):
            danh_sach_bai_hat.append({
                "bai_hat_trong_danh_sach_id": bai_hat.bai_hat_id,       # Fake id tự tăng
                "ngay_them": now(),                        # Fake ngày thêm
                "danh_sach_phat": album_id,                # Lấy luôn album id làm "danh_sach_phat"
                "bai_hat": bai_hat.bai_hat_id              # id bài hát
            })

        return Response({
            "danh_sach_bai_hat": danh_sach_bai_hat
        })

    except:
        return Response({"error": "Album not found."}, status=404)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_so_luong_bai_hat(request):
    try:
        so_luong = BaiHat.objects.count()
        return Response({"so_luong_bai_hat": so_luong}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
from django.db.models.functions import ExtractMonth
from django.db.models import Count
from datetime import datetime
def thong_ke_bai_hat_theo_thang(nam):
    ket_qua = (
        BaiHat.objects
        .filter(ngay_phat_hanh__year=nam)
        .annotate(thang=ExtractMonth('ngay_phat_hanh'))
        .values('thang')
        .annotate(so_luong=Count('bai_hat_id'))
        .order_by('thang')
    )
    
    # Tạo list 12 tháng đầy đủ (nếu tháng nào không có thì giá trị là 0)
    du_lieu_thong_ke = []
    for i in range(1, 13):
        bai_hat_thang = next((item for item in ket_qua if item['thang'] == i), None)
        du_lieu_thong_ke.append({
            "thang": i,
            "so_luong": bai_hat_thang['so_luong'] if bai_hat_thang else 0
        })

    return du_lieu_thong_ke

from django.http import JsonResponse
@api_view(['GET'])
@permission_classes([AllowAny])
def thong_ke_bai_hat_view(request):
    nam = request.GET.get('nam', datetime.now().year)  # Mặc định là năm hiện tại
    du_lieu = thong_ke_bai_hat_theo_thang(int(nam))
    return JsonResponse(du_lieu, safe=False)


from django.core.paginator import Paginator
@api_view(['GET'])
@permission_classes([AllowAny])
def get_bai_hat_pagination(request):
    # Lấy tham số từ request
    page = int(request.GET.get('page', 0))
    size = int(request.GET.get('size', 10))
    search_query = request.GET.get('search', '').strip()  # Lấy từ khóa tìm kiếm

    # Lọc danh sách bài hát nếu có từ khóa tìm kiếm
    if search_query:
        nghesi_list = BaiHat.objects.filter(ten_bai_hat__icontains=search_query)
    else:
        nghesi_list = BaiHat.objects.all()

    # Áp dụng phân trang
    paginator = Paginator(nghesi_list, size)
    total_pages = paginator.num_pages

    try:
        nghesi_page = paginator.page(page + 1)  # Django page index bắt đầu từ 1
    except:
        return Response({"message": "Page out of range"}, status=status.HTTP_404_NOT_FOUND)

    serializer = BaiHatSerializer(nghesi_page, many=True)

    return Response({
        "page": page,
        "size": size,
        "total_pages": total_pages,
        "total_items": paginator.count,
        "data": serializer.data
    }, status=status.HTTP_200_OK)
