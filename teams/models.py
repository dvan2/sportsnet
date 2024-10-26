from django.db import models
from django.conf import settings


# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    coach = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="team")

    def __str__(self):
        return self.name

class Membership(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="members")
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player.username} - {self.team.name}"

