from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100, blank=True)
    experience = models.IntegerField(default=0)
    bio = models.TextField(blank=True, null=True)