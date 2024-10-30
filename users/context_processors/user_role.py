from users.models import Profile

def user_role(request):
    if request.user.is_authenticated:
        role = request.user.profile.role
    else:
        role ="guest"
    return {"user_role": role}