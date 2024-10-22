from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    def __str__(self):
        return f'{self.username}'


class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100, blank=True)
    experience = models.IntegerField(default=0)
    bio = models.TextField(blank=True, null=True)

class CoachProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    years_experience = models.IntegerField(default=0)