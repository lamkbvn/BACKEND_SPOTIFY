from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from ..common.models import NguoiDung  # Import từ common
from ..common.serializers import NguoiDungSerializer  # Import từ common

@api_view(['POST'])
def them_nguoi_dung(request):
    serializer = NguoiDungSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Người dùng đã được thêm thành công!", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
