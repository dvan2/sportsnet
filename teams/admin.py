from django.contrib import admin

# Register your models here.
from .models import Team, Membership
admin.site.register(Team)
admin.site.register(Membership)