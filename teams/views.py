from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def manage_team(request):
    return render(request, "teams/create_team.html")