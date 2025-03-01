from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import UserSerializer

@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User updated successfully", "data": serializer.data , "status" : status.HTTP_201_CREATED})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH'])
def update_user(request, id):
    user = get_object_or_404(User, id=id)  # Tìm user theo ID

    serializer = UserSerializer(user, data=request.data, partial=True)  # Cho phép cập nhật một phần nếu dùng PATCH
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User updated successfully", "data": serializer.data , "status" : status.HTTP_201_CREATED})

    return Response(serializer.errors, status=400)