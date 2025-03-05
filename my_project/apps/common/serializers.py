from rest_framework import serializers
from .models import NguoiDung
from .models import DanhSachPhat
from .models import LoiBaiHatDongBo
from .models import LoaiBaiHat
from ..common.models import BaiHat, BaiHatTrongDanhSach

class NguoiDungSerializer(serializers.ModelSerializer):
    class Meta:
        model = NguoiDung
        fields = '__all__'  # Lấy tất cả các trường của model
        extra_kwargs = {'mat_khau': {'write_only': True}}  # Ẩn mật khẩu khi trả về response


class DanhSachPhatSerializer(serializers.ModelSerializer):
    class Meta:
        model = DanhSachPhat
        fields = '__all__'  # Lấy tất cả các trường của model
        
        from rest_framework import serializers

class BaiHatSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaiHat
        fields = '__all__'

class BaiHatTrongDanhSachSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaiHatTrongDanhSach
        fields = '__all__'

class LoiBaiHatDongBoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoiBaiHatDongBo
        fields = '__all__'

class LoaiBaiHatSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoaiBaiHat
        fields = '__all__'
