from rest_framework import serializers
from .models import NguoiDung

class NguoiDungSerializer(serializers.ModelSerializer):
    class Meta:
        model = NguoiDung
        fields = '__all__'  # Lấy tất cả các trường của model
        extra_kwargs = {'mat_khau': {'write_only': True}}  # Ẩn mật khẩu khi trả về response
