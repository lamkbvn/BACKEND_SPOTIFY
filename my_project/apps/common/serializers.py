from rest_framework import serializers
from .models import NguoiDung
from .models import DanhSachPhat

class NguoiDungSerializer(serializers.ModelSerializer):
    class Meta:
        model = NguoiDung
        fields = '__all__'  # Lấy tất cả các trường của model
        extra_kwargs = {'password': {'write_only': True}}  # Ẩn mật khẩu khi trả về response


class DanhSachPhatSerializer(serializers.ModelSerializer):
    class Meta:
        model = DanhSachPhat
        fields = '__all__'  # Lấy tất cả các trường của model