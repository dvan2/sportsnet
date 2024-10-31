from django.db import models
from django.conf import settings

# Create your models here.
class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    date = models.DateTimeField(auto_now_add=True)
    # likes = models.PositiveIntegerField(default=0)
    # comments_count = models.PositiveIntegerField


