from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    def __str__(self):
        return f'{self.username}'

class Profile(models.Model):
    USER_ROLES = [
        ('player', 'Player'),
        ('coach', 'Coach')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLES)

    bio = models.TextField(blank=True, null=True)