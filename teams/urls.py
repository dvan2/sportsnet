from django.urls import path
from . import views

urlpatterns = [
    path('manage/', views.manage_team, name="manage_team"),
]