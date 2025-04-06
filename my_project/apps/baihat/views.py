from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from ..common.models import BaiHat
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

@api_view(['POST'])
def sync_lyrics(request):
    # Nhận file mp3 từ request
    audio_file = request.FILES.get('audio')
    lyrics = request.data.get('lyrics')  # Nhận lời bài hát từ request
    
    if not audio_file:
        return JsonResponse({"error": "No audio file provided"}, status=400)
    if not lyrics:
        return JsonResponse({"error": "No lyrics provided"}, status=400)
    
    # Lưu file mp3 tạm thời
    fs = FileSystemStorage()
    audio_path = fs.save(audio_file.name, audio_file)
    
    # Lấy đường dẫn thực tế của tệp âm thanh
    audio_file_path = os.path.join(settings.MEDIA_ROOT, audio_path)
    
    # Giải mã URL encoding trong tên tệp
    audio_file_path = unquote(audio_file_path)
    
    try:
        # Tải file âm thanh với Librosa
        y, sr = librosa.load(audio_file_path, sr=None)

        # Tính toán tempo và beat
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)

        # Bỏ qua beat dạo (giả sử bài hát bắt đầu ở 30s)
        start_time = 30.0  # Thời gian bắt đầu bài hát tính từ 30s (có thể điều chỉnh nếu cần)
        beat_times = [time for time in beat_times if time >= start_time]

        # Chia lời bài hát thành các câu
        lyrics_lines = lyrics.split('\n')
        
        # Tính toán timestamp cho mỗi câu
        num_beats = len(beat_times)
        num_lines = len(lyrics_lines)
        time_per_line = (beat_times[-1] - start_time) / num_lines  # Thời gian trung bình cho mỗi câu

        timestamps = []
        for i, line in enumerate(lyrics_lines):
            timestamp = start_time + (i * time_per_line)
            timestamps.append({"line": line, "timestamp": timestamp})

        return JsonResponse({"tempo": tempo, "timestamps": timestamps})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    finally:
        # Kiểm tra tồn tại của file trước khi xóa
        if os.path.exists(audio_file_path):
            os.remove(audio_file_path)
        else:
            print(f"File not found: {audio_file_path}")
            
            

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

# Ví dụ gọi hàm với đường dẫn file MP3
audio_file_path = r'D:\Downloads\aaxxx.mp3'
start_time = find_lyric_start_time(audio_file_path)
print(f"Thời điểm bắt đầu lời bài hát: {start_time} giây")

      
@api_view(['POST'])
def sync_lyrics(request):
    # Nhận file mp3 từ request
    audio_file = request.FILES.get('audio')
    lyrics = request.data.get('lyrics')  # Nhận lời bài hát từ request
    
    if not audio_file:
        return Response({"error": "No audio file provided"}, status=400)
    if not lyrics:
        return Response({"error": "No lyrics provided"}, status=400)
    
    # Lưu file mp3 tạm thời
    fs = FileSystemStorage()
    audio_path = fs.save(audio_file.name, audio_file)
    
    # Lấy đường dẫn thực tế của tệp âm thanh
    audio_file_path = os.path.join(settings.MEDIA_ROOT, audio_path)
    
    # Giải mã URL encoding trong tên tệp
    audio_file_path = unquote(audio_file_path)
    
    try:
        # Tải file âm thanh với Librosa
        y, sr = librosa.load(audio_file_path, sr=None)

        # Tính toán tempo và beat
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)

        # Tìm thời gian có âm thanh đầu tiên (khi có tiếng hát bắt đầu)
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        onset_times = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr, units='time')

        if len(onset_times) > 0:
            first_sound_time = onset_times[0]
        else:
            first_sound_time = 0  # Nếu không có phát hiện âm thanh, giả sử bắt đầu từ 0

        # Điều chỉnh beat_times để bắt đầu từ khi tiếng hát xuất hiện
        adjusted_beat_times = beat_times - first_sound_time

        # Chia lời bài hát thành các câu
        lyrics_lines = lyrics.split('\n')
        
        # Tính toán timestamp cho mỗi câu
        num_beats = len(adjusted_beat_times)
        num_lines = len(lyrics_lines)
        time_per_line = adjusted_beat_times[-1] / num_lines  # Thời gian trung bình cho mỗi câu

        timestamps = []
        for i, line in enumerate(lyrics_lines):
            timestamp = i * time_per_line
            timestamps.append({"line": line, "timestamp": timestamp})

        return Response({"tempo": tempo, "timestamps": timestamps})
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
    finally:
        # Kiểm tra tồn tại của file trước khi xóa
        if os.path.exists(audio_file_path):
            os.remove(audio_file_path)
        else:
            print(f"File not found: {audio_file_path}")
            
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
