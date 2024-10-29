from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Team

# Create your views here.
@login_required
def manage_team(request):
    if request.user.profile.role != "coach":
        return redirect('index')
    
    team = Team.objects.filter(coach=request.user).first()

    if team:
        return render(request, "teams/manage.html")
    else:
        return render(request, "teams/create_team.html")

@login_required
def create_team(request):
    if request.user.profile.role != "coach":
        messages.error(request, "Only coaches can create teams.")
        return redirect('index')
    
    if Team.objects.filter(coach=request.user).exists():
        messages.error(request, "You already have a team.")
        return redirect('manage_team')
    
    if request.method == "POST":
        team_name = request.POST.get("name")
        if team_name:
            Team.objects.create(name=team_name, coach=request.user)
            messages.success(request, f"Team '{team_name}' created successfully.")
            return redirect('manage_team')
        else:
            messages.error(request, "Please enter a team name.")
    return render(request, "teams/create_team.html")

@login_required
def team_list(request):
    teams = Team.objects.all()
    return render(request, "teams/team_list.html", {"teams" : teams})