from django.db import models

class Message(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField()
    avatar_url = models.URLField(blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.email}): {self.content}"
