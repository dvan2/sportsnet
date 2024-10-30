from django.urls import path
from . import views

urlpatterns = [
    path('manage/', views.manage_team, name="manage_team"),
    path('create/', views.create_team, name="create_team"),
    path('team_list/', views.team_list, name="team_list"),
    path('join_team/<int:team_id>/', views.join_team, name="join_team"),
    path('pending_requests', views.manage_requests, name="pending_requests"),
    path("approve_request/<int:membership_id>/", views.approve_request, name="approve_request"),
    path("reject_request/<int:membership_id>/", views.reject_request, name="reject_request"),
    path("current_team/", views.current_team, name="current_team")
]