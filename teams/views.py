from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Team, Membership

# Create your views here.
@login_required
def manage_team(request):
    if request.user.profile.role != "coach":
        return redirect('index')
    
    team = Team.objects.filter(coach=request.user).first()

    if team:
        players = team.members.filter(status=Membership.APPROVED)
        return render(request, "teams/manage.html", {"team": team, "players": players})
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
    # Only display teams player is not in
    joined_teams = Team.objects.filter(members__player=request.user)
    teams = Team.objects.exclude(Q(coach=request.user) | Q(id__in=joined_teams))
    return render(request, "teams/team_list.html", {"teams" : teams})

@login_required
def current_team(request):
    membership = get_object_or_404(Membership, player=request.user, status=Membership.APPROVED)
    team= membership.team

    return render(request, "teams/current_team.html", {"team": team})

@login_required
def join_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    membership, created = Membership.objects.get_or_create(team=team, player=request.user, defaults={"status": Membership.PENDING})

    if not created:
        messages.info(request, "You have already request to join this team")
    else:
        messages.success(request, "Join request sent")
    
    return redirect('team_list')

@login_required
def manage_requests(request):
    coach_team = request.user.team
    pending_requests = coach_team.members.filter(status=Membership.PENDING)
    return render(request, "teams/manage_requests.html", {"pending_requests": pending_requests})

@login_required
def approve_request(request, membership_id):
    # ensure it's the team's coach
    membership = get_object_or_404(Membership, id=membership_id, team__coach=request.user)
    membership.status = Membership.APPROVED
    membership.save()
    messages.success(request, "Approved Request")
    return redirect('pending_requests')

@login_required
def reject_request(request, membership_id):
    membership = get_object_or_404(Membership, id=membership_id, team__coach=request.user)
    membership.status = Membership.APPROVED
    membership.save()
    messages.success(request, "Rejected Request")
    return redirect('pending_requests')