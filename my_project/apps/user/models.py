from django.db import models

# Create your models here.
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # Lưu ý: Nên mã hóa mật khẩu trước khi lưu
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
