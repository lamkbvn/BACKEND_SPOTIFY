from django.db import models

# Create your models here.
class DanhSachPhat(models.Model):
    ten = models.CharField(max_length=255)
    image = models.URLField(blank=True, null=True)  # Lưu URL ảnh từ Cloudinary
