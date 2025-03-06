from django.db import models

# Create your models here.
from django.db import models

class BlacklistedAccessToken(models.Model):
    token_access = models.CharField(max_length=255 , unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
