from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..common.models import BaiHat, BaiHatTrongDanhSach, DanhSachPhat
from ..common.serializers import BaiHatSerializer, BaiHatTrongDanhSachSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
# API thêm bài hát mới
@api_view(['POST'])
@permission_classes([AllowAny])
def them_bai_hat(request):
    serializer = BaiHatSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Bài hát đã được thêm thành công!", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def lay_danh_sach_bai_hat(request, danh_sach_phat_id):
    # Kiểm tra xem danh sách phát có tồn tại không
    if not DanhSachPhat.objects.filter(danh_sach_phat_id=danh_sach_phat_id).exists():
        return Response({"error": "Danh sách phát không tồn tại!"}, status=status.HTTP_404_NOT_FOUND)

    # Lấy danh sách bài hát thuộc danh sách phát
    bai_hat_trong_ds = BaiHatTrongDanhSach.objects.filter(danh_sach_phat_id=danh_sach_phat_id)
    
    # Serialize dữ liệu
    serializer = BaiHatTrongDanhSachSerializer(bai_hat_trong_ds, many=True)

    return Response({"danh_sach_bai_hat": serializer.data}, status=status.HTTP_200_OK)


# API thêm bài hát vào danh sách phát
@api_view(['POST'])
@permission_classes([AllowAny])
def them_bai_hat_vao_danhsach(request):
    bai_hat_id = request.data.get('bai_hat_id')
    danh_sach_phat_id = request.data.get('danh_sach_phat_id')

    # Kiểm tra xem ID bài hát có tồn tại không
    if not BaiHat.objects.filter(bai_hat_id=bai_hat_id).exists():
        return Response({"error": "Bài hát không tồn tại!"}, status=status.HTTP_404_NOT_FOUND)

    # Kiểm tra xem ID danh sách phát có tồn tại không
    if not DanhSachPhat.objects.filter(danh_sach_phat_id=danh_sach_phat_id).exists():
        return Response({"error": "Danh sách phát không tồn tại!"}, status=status.HTTP_404_NOT_FOUND)

    # Kiểm tra xem bài hát đã có trong danh sách chưa
    if BaiHatTrongDanhSach.objects.filter(bai_hat_id=bai_hat_id, danh_sach_phat_id=danh_sach_phat_id).exists():
        return Response({"error": "Bài hát đã có trong danh sách phát!"}, status=status.HTTP_400_BAD_REQUEST)

    # Thêm bài hát vào danh sách phát
    bai_hat_trong_ds = BaiHatTrongDanhSach.objects.create(
        bai_hat_id=bai_hat_id,
        danh_sach_phat_id=danh_sach_phat_id
    )
    

    return Response(
        {
            "message": "Bài hát đã được thêm vào danh sách phát!",
            "data": {
                "bai_hat_trong_danh_sach_id": bai_hat_trong_ds.bai_hat_trong_danh_sach_id,
                "bai_hat_id": bai_hat_trong_ds.bai_hat_id,
                "danh_sach_phat_id": bai_hat_trong_ds.danh_sach_phat_id,
                "ngay_them": bai_hat_trong_ds.ngay_them
            }
        },
        status=status.HTTP_201_CREATED
    )


@api_view(['DELETE'])
@permission_classes([AllowAny])

def xoa_bai_hat_khoi_danhsach(request):
    bai_hat_id = request.data.get('bai_hat_id')
    danh_sach_phat_id = request.data.get('danh_sach_phat_id')

    try:
        bai_hat_trong_ds = BaiHatTrongDanhSach.objects.get(
            bai_hat_id=bai_hat_id, danh_sach_phat_id=danh_sach_phat_id
        )
    except BaiHatTrongDanhSach.DoesNotExist:
        return Response({"error": "Bài hát không có trong danh sách phát!"}, status=status.HTTP_404_NOT_FOUND)

    bai_hat_trong_ds.delete()
    return Response({"message": "Bài hát đã được xóa khỏi danh sách phát!"}, status=status.HTTP_200_OK)
